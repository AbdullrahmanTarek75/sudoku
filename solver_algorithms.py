from copy import deepcopy

def is_valid(board, row, col, num):
    # check row, col and 3x3 box
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = row//3 * 3, col//3 * 3
    for i in range(3):
        for j in range(3):
            if board[start_row+i][start_col+j] == num:
                return False
    return True

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def solve_backtracking(board):
    empty = find_empty(board)
    if not empty:
        return board
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_backtracking(board):
                return board
            board[row][col] = 0
    return False

def solve_backtracking_mrv(board):
    def find_mrv():
        min_options = 10
        best = None
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    options = [num for num in range(1, 10) if is_valid(board, i, j, num)]
                    if len(options) < min_options:
                        min_options = len(options)
                        best = (i, j, options)
        return best

    def backtrack():
        mrv = find_mrv()
        if not mrv:
            return True
        row, col, options = mrv
        for num in options:
            board[row][col] = num
            if backtrack():
                return True
            board[row][col] = 0
        return False

    if backtrack():
        return board
    return False

def a_star_sudoku_solver(board):
    from queue import PriorityQueue

    def heuristic(b):
        return sum(row.count(0) for row in b)

    frontier = PriorityQueue()
    frontier.put((heuristic(board), board))

    visited = set()

    while not frontier.empty():
        _, current = frontier.get()
        state_tuple = tuple(tuple(row) for row in current)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        empty = find_empty(current)
        if not empty:
            return current
        row, col = empty
        for num in range(1, 10):
            if is_valid(current, row, col, num):
                new_board = deepcopy(current)
                new_board[row][col] = num
                frontier.put((heuristic(new_board), new_board))
    return False
