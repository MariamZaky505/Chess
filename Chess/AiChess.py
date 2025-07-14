import random

PIECE_SCORE = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

KNIGHT_SCORES = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.6, 0.6, 0.6, 0.5, 0.2],
                 [0.2, 0.5, 0.6, 0.7, 0.7, 0.6, 0.5, 0.2],
                 [0.2, 0.5, 0.6, 0.7, 0.7, 0.6, 0.5, 0.2],
                 [0.2, 0.5, 0.6, 0.6, 0.6, 0.6, 0.5, 0.2],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

BISHOP_SCORES = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

ROOK_SCORES = [[0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
               [0.5, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.5],
               [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
               [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
               [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
               [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
               [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
               [0.2, 0.2, 0.2, 0.5, 0.5, 0.2, 0.2, 0.2]]

QUEEN_SCORES = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

PAWN_SCORES = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.2, 0.2, 0.3, 0.4, 0.4, 0.3, 0.2, 0.2],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.2, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.2],
               [0.2, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.2],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

PIECE_POSITION_SCORES = {
    "wp": PAWN_SCORES,
    "bp": PAWN_SCORES[::-1],
    "wN": KNIGHT_SCORES,
    "bN": KNIGHT_SCORES[::-1],
    "wB": BISHOP_SCORES,
    "bB": BISHOP_SCORES[::-1],
    "wR": ROOK_SCORES,
    "bR": ROOK_SCORES[::-1],
    "wQ": QUEEN_SCORES,
    "bQ": QUEEN_SCORES[::-1]
}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 0
nextMove = None

def findRandomMove(validMoves):
    return random.choice(validMoves)

def findBestMove(gs, validMoves, returnQueue):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveMinimaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    returnQueue.put(nextMove)

def findMoveMinimaxAlphaBeta(gs, validMoves, depth, alpha, beta, maximizingPlayer):
    global nextMove
    if depth == 0:
        return scoreBoard(gs)
    if maximizingPlayer:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinimaxAlphaBeta(gs, nextMoves, depth - 1, alpha, beta, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinimaxAlphaBeta(gs, nextMoves, depth - 1, alpha, beta, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
            beta = min(beta, score)
            if alpha >= beta:
                break
        return minScore

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            piece = gs.board[row][col]
            if piece != "--":
                piecePositionScore = PIECE_POSITION_SCORES.get(piece, [[0]*8 for _ in range(8)])[row][col]
                if piece[0] == 'w':
                    score += PIECE_SCORE[piece[1]] + piecePositionScore
                elif piece[0] == 'b':
                    score -= PIECE_SCORE[piece[1]] + piecePositionScore

    return score
