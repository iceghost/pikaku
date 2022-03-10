from board import Board

def blind_search(board: Board):
    blind_search_help(board, 0, 0)

def blind_search_help(board: Board, x: int, y: int) -> bool:
    if y == len(board):
        return board.is_solved()
    for _ in range(0, board.at(x, y).MAX_ROTATION):
        board.rotate(x, y)
        next_x, next_y = next(x, y, len(board))
        if blind_search_help(board, next_x, next_y):
            return True
    return False


def next(x: int, y: int, size: int):
    if x == size - 1:
        return 0, y + 1
    return x + 1, y
