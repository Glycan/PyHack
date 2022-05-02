from tc import TerminalController as TermCtrl
from random import randint, choice
import itertools
import time
import urllib
import tty
import select
import sys

tty.setcbreak(sys.stdin.fileno())  # cbreak mode, no buffer
term = TermCtrl()

# def highlight(char):
#     if char.lower() == "l":
#         return term.RED + char + term.NORMAL
#     if char.lower() == "p":
#         return term.GREEN + char + term.NORMAL
#     return char


# for i in range(20):
#     placed = (randint(0, cols - 1), randint(0, rows - 1))
#     board = set_cursor(board, placed, highlight(choice("lp")))


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return "P<%s, %s>" % (self.x, self.y)


class Matrix:
    def __init__(self, rows, cols, fill=" "):
        fill_iter = itertools.cycle(fill)
        self.matrix = [[next(fill_iter) for j in range(cols)] for i in range(rows)]
        self.rows = rows
        self.cols = cols

    def set(self, point, value):
        self.matrix[point.y % self.cols][point.x % self.rows] = value

    def index(self, point):
        return self.matrix[point.y][point.x]

    def blit(self, cursor, blurb=""):
        sys.stdout.write(
            term.CLEAR_SCREEN
            + "\n".join("".join(row) for row in self.matrix)
            + blurb
            + term.UP * (blurb.count("\n") + self.rows - (cursor.y % self.rows) - 1)
            + term.BOL
            + term.RIGHT * (cursor.x % self.cols)
        )
        sys.stdout.flush()

    def apply(self, fn):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = fn(self.matrix[i][j])

cardinal = {
    "h": Point(-1, 0),
    "l": Point(1, 0),
    "j": Point(0, +1),
    "k": Point(0, -1),
}

moves = {
    **cardinal,
    "y": Point(-1, -1),
    "u": Point(1, -1),
    "b": Point(-1, 1),
    "n": Point(1, 1),
}


diamond = list(cardinal.values())


moves_wasd = {
    "w": moves["k"],
    "a": moves["h"],
    "s": moves["j"],
    "d": moves["l"],
}
moves.update(moves_wasd)

# center = Point(5, 5)

log = open("log", "w")

transitions = {
    term.BOLD + term.BLUE + "#" + term.NORMAL: term.BOLD + "#" + term.NORMAL,
    term.BOLD + "#" + term.NORMAL: "#",
    "#": "o",
    "o": ".",
    ".": ".",
}


def iterate(board, center, speed):
    if sys.stdin in select.select([sys.stdin], [], [], 0.4)[0]:
        char = sys.stdin.read(1)
        speed += moves[char]  # .get(char, Point(0, 0))
        log.write("new speed: %s\n" % speed)
    board.apply(lambda c: transitions.get(c, c))
    board.set(center, term.BOLD + term.BLUE + "#" + term.NORMAL)
    # for direction in diamond:
    #     log.write(repr(center + direction) + "\n")
    #     board.set(center + direction, term.BOLD + "#" + term.NORMAL)
    log.write(str(len([c for row in board.matrix for c in row if c == "#"])) + "\n")
    board.blit(center, blurb="speed: %s" % speed)
    new_center = center + speed
    log.write("new center: %s\n" % new_center)
    if 0 >= new_center.y or new_center.y >= board.cols:
        log.write("flip y")
        speed = Point(speed.x, -speed.y)
    if 0 >= new_center.x or new_center.x >= board.rows:
        log.write("flip x")
        speed = Point(-speed.x, speed.y)
    return board, center + speed, speed


state = Point(5, 5)
speed = Point(0, 1)
board = Matrix(30, 30, ".")
while 1:
    board, state, speed = iterate(board, state, speed)
