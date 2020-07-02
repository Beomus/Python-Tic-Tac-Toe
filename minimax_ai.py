board = [[None] * 3, [None] * 3, [None] * 3]

human = "O"
ai = "X"

scores = {"X": 10, "O": -10, "Draw": 0}

cur_player = human

def draw_board():
    print("==================")
    for i in range(3):
        print(board[i])
    print("==================")

def minimax(board, depth, alpha, beta, isMax):
    global scores, human, ai

    result = check_winner()
    if result is not None:
        return scores[result] 

    if isMax:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                # if position is available
                if board[i][j] is None:
                    # check move
                    board[i][j] = ai
                    # compute score
                    cur_eval = minimax(board, depth+1, alpha, beta, False)
                    # reset position
                    board[i][j] = None
                    # evaluation
                    max_eval = max(max_eval, cur_eval)
                    alpha = max(alpha, cur_eval)
                    if beta <= alpha:
                       break

        return max_eval

    else:
        min_eval = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = human
                    cur_eval = minimax(board, depth+1, alpha, beta, True)
                    board[i][j] = None
                    min_eval = min(min_eval, cur_eval)
                    beta = min(beta, cur_eval)
                    if beta <= alpha:
                       break
        return min_eval

def best_move():
    global ai, human, cur_player
    best_score = float("-inf")
    move = {'row': 0, 'col': 0}
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = ai
                score = minimax(board, 0, float("-inf"), float("inf"), False)
                board[i][j] = None
                if score > best_score:
                    best_score = score
                    move['row'] = i
                    move['col'] = j
    
    print(f"Choice: {move} | Score: {best_score}")
    # print(f"Score: {best_score}")
    board[move['row']][move['col']] = ai
    cur_player = human

def check_winner():
    global board
    winner = None
    for row in range(3):
            if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
                winner = board[row][0]
                # return winner

    for col in range(3):
            if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
                winner = board[0][col]
                # return winner

    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = board[0][0]
        # return winner

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        winner = board[0][2]
        # return winner

    open_spots = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                open_spots += 1

    if winner is None and open_spots == 0:
        return "Draw"
    else:
        return winner

    
def main():
    global ai, human, cur_player, board
    run = True
    cur_player = human

    while run:
        draw_board()

        if cur_player == human:
            pos = list(map(int, input("Input your position: ").split()))
            if board[pos[0]][pos[1]] is None:
                board[pos[0]][pos[1]] = human
                cur_player = ai
            elif board[pos[0]][pos[1]] is not None:
                print(f"Invalid move at {pos}")
            
        elif cur_player == ai:
            best_move()
            # cur_player = human

        winner = check_winner()

        if winner is not None:
            draw_board()
            run = False
            if winner == "Draw":
                print("It's a draw!")
            else: 
                print(f"Winner is {winner}")


if __name__ == "__main__":
    main()