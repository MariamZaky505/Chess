#handles user input and displays current game state, for rendering
import pygame as p
import ChessEngine
import AiChess
from multiprocessing import Process, Queue

# Board and screen dimensions
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8  # Dimensions of a chess board are 8x8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

# Define some preset themes
THEMES = {
    1: (p.Color(255, 255, 255), p.Color(45, 45, 45)),  # White and Black
    2: (p.Color(240, 240, 240), p.Color(247, 135, 154)),  # Light and Dark Gray
    3: (p.Color(240, 240, 240), p.Color(10, 15, 58)),  # Navy Blue
    4: (p.Color(255, 223, 186), p.Color(93, 3, 3)),  # Dark Red
    5: (p.Color(230, 230, 240), p.Color(58, 12, 87)),  # Amethyst Light
}

# Default theme (White and Black)
current_theme = 1
LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR = THEMES[current_theme]

"""
Initialize global dictionary of images. 
This will be called exactly once in the main function
"""
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

"""
The main driver for our code. 
It will handle user input and updating graphics
"""
def main():
    global LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR
    p.init()
    screen = p.display.set_mode([BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT])
    clock = p.time.Clock()
    moveLogFont = p.font.SysFont("Arial", 14, False, False)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    sqSelected = ()  # keep track of last user click, tuple: (row, col)
    playerClicks = []  # keep track of last two player clicks, two tuples: [(row, col), (row, col)]
    playerOne = True  # If true, human is playing white, otherwise AI is playing white
    playerTwo = False  # same as above, except playing black
    moveFinderProcess = None
    returnQueue = None
    AIThinking = False
    gameOver = False
    moveMade = False
    moveUndone = False
    animate = False
    running = True

    loadImages()

    print("Press 1 for Classic Black & White Theme")
    print("Press 2 for Rose Pink Theme")
    print("Press 3 for Navy Blue Theme")
    print("Press 4 for Dark Red Theme")
    print("Press 5 for Amethyst Light Theme ")

    # Game loop
    while running:
        try:
            isHumanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False

                elif e.type == p.MOUSEBUTTONDOWN:
                    if not gameOver:
                        location = p.mouse.get_pos()
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE

                        if sqSelected == (row, col) or col >= 8:  # user clicked the same square twice or the move log
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)

                        if len(playerClicks) == 2 and isHumanTurn:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]

                elif e.type == p.KEYDOWN:
                    if e.key == p.K_u:
                        gs.undoMove()
                        moveMade = True
                        animate = False
                        gameOver = False
                        if AIThinking:
                            moveFinderProcess.terminate()
                            AIThinking = False
                        moveUndone = True
                    if e.key == p.K_r:
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False
                        if AIThinking:
                            moveFinderProcess.terminate()
                            AIThinking = False
                        moveUndone = True

                    # Theme switch (1-5)
                    elif e.key == p.K_1:
                        LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR = THEMES[1]
                    elif e.key == p.K_2:
                        LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR = THEMES[2]
                    elif e.key == p.K_3:
                        LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR = THEMES[3]
                    elif e.key == p.K_4:
                        LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR = THEMES[4]
                    elif e.key == p.K_5:
                        LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR = THEMES[5]

            if not gameOver and not isHumanTurn and not moveUndone:
                if not AIThinking:
                    AIThinking = True
                    returnQueue = Queue()  # used to pass data between threads
                    moveFinderProcess = Process(target=AiChess.findBestMove, args=(gs, validMoves, returnQueue))
                    moveFinderProcess.start()

                if not moveFinderProcess.is_alive():
                    AIMove = returnQueue.get()
                    if AIMove is None:
                        AIMove = AiChess.findRandomMove(validMoves)

                    gs.makeMove(AIMove)
                    moveMade = True
                    animate = True
                    AIThinking = False

            if moveMade:
                if animate:
                    animateMove(gs.moveLog[-1], screen, gs.board, clock)
                validMoves = gs.getValidMoves()
                moveMade = False
                animate = False
                moveUndone = False

            drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

            if gs.checkmate or gs.stalemate:
                gameOver = True
                if gs.stalemate:
                    text = "Stalemate"
                else:
                    text = "Black wins by checkmate" if gs.whiteToMove else "White wins by checkmate"
                drawEndGameText(screen, text)

            clock.tick(MAX_FPS)
            p.display.flip()

        except Exception as e:
            print(f"An error occurred: {e}")
            running = False
            p.quit()


"""
Responsible for all the graphics within a current game state
"""
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)


"""
Draws the squares on the board with customizable colors
"""
def drawBoard(screen):
    global LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = LIGHT_SQUARE_COLOR if (r + c) % 2 == 0 else DARK_SQUARE_COLOR
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Highlight square selection
"""
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

            # highlight valid moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


"""
Draws the pieces on top of the board using the current GameState.board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]

            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Draws the move log on the right side of the window
"""
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i // 2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog):  # append opponent move
            moveString += str(moveLog[i + 1]) + "  "
        moveTexts.append(moveString)

    movesPerRow = 2
    padding = 5
    lineSpacing = 2
    textY = padding

    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]

        textObject = font.render(text, True, p.Color('White'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing


"""
Animating a move including playing the sound
"""
def animateMove(move, screen, board, clock):
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 7
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare

    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)

        # Erase the piece moved from its ending square
        color = LIGHT_SQUARE_COLOR if (move.endRow + move.endCol) % 2 == 0 else DARK_SQUARE_COLOR
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)

        # Draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


"""
Draws the end game text (checkmate, stalemate, etc.)
"""
def drawEndGameText(screen, text):
    font = p.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, True, p.Color('White'))
    textLocation = p.Rect(BOARD_WIDTH // 2 - textObject.get_width() // 2, BOARD_HEIGHT // 2 - textObject.get_height() // 2)
    screen.blit(textObject, textLocation)
    p.display.flip()




if __name__ == "__main__":
    main()
