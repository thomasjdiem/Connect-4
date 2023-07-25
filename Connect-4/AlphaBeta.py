from copy import deepcopy

def AlphaBeta(MyGame, depth, alpha, beta, maximizing_player):

    MyGame.CheckWinner()
    if MyGame.winner != 0 or MyGame.num_moves == MyGame.nrows * MyGame.ncols:
        return (10000 + depth) * MyGame.winner * maximizing_player, None
    if depth == 0:
        return HeuristicScore(MyGame, maximizing_player), None

    if maximizing_player == MyGame.turn:
        max_eval = -1000000
        best_move = None
        for move in MyGame.possible_moves:
            NextGame = deepcopy(MyGame)
            NextGame.MakeMove(move)
            eval, _ = AlphaBeta(NextGame, depth - 1, alpha, beta, maximizing_player)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return max_eval, best_move
    else:
        min_eval = 1000000
        best_move = None
        for move in MyGame.possible_moves:
            NextGame = deepcopy(MyGame)
            NextGame.MakeMove(move)
            eval, _ = AlphaBeta(NextGame, depth - 1, alpha, beta, maximizing_player)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if alpha >= beta:
                break
        return min_eval, best_move


def HeuristicScore(MyGame, maximizing_player):
    score = 0

    # Evaluate rows
    for row in range(MyGame.nrows):
        for col in range(MyGame.ncols - 3):
            window = MyGame.board[row][col:col+4]
            score += EvaluateWindow(window, maximizing_player)

    # Evaluate columns
    for col in range(MyGame.ncols):
        for row in range(MyGame.nrows - 3):
            window = [MyGame.board[row+i][col] for i in range(4)]
            score += EvaluateWindow(window, maximizing_player)

    # Evaluate diagonals (tog right to bottom left)
    for row in range(MyGame.nrows - 3):
        for col in range(MyGame.ncols - 3):
            window = [MyGame.board[row+i][col+i] for i in range(4)]
            score += EvaluateWindow(window, maximizing_player)

    # Evaluate diagonals (top left to bottom right)
    for row in range(3, MyGame.nrows):
        for col in range(MyGame.ncols - 3):
            window = [MyGame.board[row-i][col+i] for i in range(4)]
            score += EvaluateWindow(window, maximizing_player)

    return score

def EvaluateWindow(window, maximizing_player):

    if window.count(maximizing_player) == 4:
        return 10000
    elif window.count(maximizing_player) == 3 and window.count(0) == 1:
        return 5
    elif window.count(maximizing_player) == 2 and window.count(0) == 2:
        return 2
    elif window.count(maximizing_player * -1) == 3 and window.count(0) == 1:
        return -5
    else:
        return 0