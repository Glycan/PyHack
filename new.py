from tc import TerminalController as TermCtrl
from random import randint, choice
from collections import defaultdict
import urllib
import tty
import sys

tty.setcbreak(sys.stdin.fileno())  # cbreak mode, no buffer
term = TermCtrl()

inventory = defaultdict(lambda: 0)

names = {"l": "Life", "p": "Points"}


def blit(board, cursor):
    inv = ", ".join(
        "%s: %s" % (names.get(k, k), 10 - v if k == "l" else v)
        for k, v in inventory.items()
        if v > 1 and k.isalpha()
    )
    sys.stdout.write(
        term.CLEAR_SCREEN
        + "\n".join("".join(row) for row in board)
        + (("\n" + inv + term.UP) if inv else "")
        + term.UP * (len(board) - cursor[1] - 1)
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


def get_cursor(board, cursor):
    return board[cursor[1]][cursor[0]]


rows = 10
cols = 20
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
# text = ""
# while len(text) < rows * cols:
#     text += urllib.urlopen("https://colbyolson.com/printers").read()
board = [
    [highlight(char) for char in text[i * cols : i * cols + cols]] for i in range(rows)
]

for i in range(40):
    placed = (randint(0, cols - 1), randint(0, rows - 1))
    board = set_cursor(board, placed, highlight(choice("lp")))

cursor = (5, 5)
board[5][5] = "@"
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
    new_char = get_cursor(board, cursor).lower()
    print(new_char)
    inventory[new_char] += 1
    # # move the letter to the next position in the path
    # set_cursor(board, moves[char](*cursor), new_char)
    set_cursor(board, cursor, "@")
    blit(board, cursor)
    state = "win" if inventory["p"] >= 10 else "lose" if inventory["l"] >= 10 else ""
    if state:
        sys.stdout.write("\n" * (len(board) - cursor[1]) + "\n\nyou %s" % state)
        sys.exit(0)
