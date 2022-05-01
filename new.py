from tc import TerminalController as TermCtrl
from random import randint, choice
import tty
import sys

tty.setcbreak(sys.stdin.fileno())  # cbreak mode, no buffer
term = TermCtrl()

life = 10
points = 0


def blit(board, cursor):
    sys.stdout.write(
        term.CLEAR_SCREEN
        + "\n".join("".join(row) for row in board)
        + "\nLife: %s Points: %s" % (life, points)
        + term.UP * (len(board) - cursor[1])
        + term.BOL
        + term.RIGHT * (cursor[0])
    )
    sys.stdout.flush()


def highlight(char):
    if char.lower() == "l":
        return term.RED + char + term.NORMAL
    if char.lower() == "p":
        return term.GREEN + char + term.NORMAL
    return char


def set_cursor(board, cursor, char):
    board[cursor[1]][cursor[0]] = char
    return board

rows = 10
cols = 20
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
board = [
    [highlight(char) for char in text[i * cols : i * cols + cols]] for i in range(rows)
]

for i in range(20):
    placed = (randint(0, cols - 1), randint(0, rows - 1))
    board = set_cursor(board, placed, highlight(choice("lp")))

# board = [[text[i*j] for i in range(10)] for j in range(10)]
board[5][5] = "@"
cursor = (5, 5)
blit(board, cursor)


moves = {
    "h": (lambda x, y: (x - 1, y)),
    "l": (lambda x, y: (x + 1, y)),
    "j": (lambda x, y: (x, y + 1)),
    "k": (lambda x, y: (x, y - 1)),
    "y": lambda x, y: (x - 1, y - 1),
    "u": lambda x, y: (x + 1, y - 1),
    "b": lambda x, y: (x - 1, y + 1),
    "n": lambda x, y: (x + 1, y + 1),
}
moves_wasd = {
    "w": moves["k"],
    "a": moves["h"],
    "s": moves["j"],
    "d": moves["l"],
}
moves.update(moves_wasd)


while 1:
    char = sys.stdin.read(1)
    board = set_cursor(board, cursor, ".")
    if char in moves:
        new_x, new_y = moves[char](*cursor)
        if 0 <= new_x < cols and 0 <= new_y < rows:
            cursor = (new_x, new_y)
    new_char = board[cursor[1]][cursor[0]].lower()
    if "l" in new_char:
        life -= 1
    if "p" in new_char:
        points += 1
    set_cursor(board, cursor, "@")
    blit(board, cursor)
    if life == 0:
        print "\n" * (len(board) - cursor[1]) + "\n\nyou loose"
        sys.exit(0)
    if points >= 10:
        print "\n\nyou win"
        sys.exit(0)
