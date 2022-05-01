from tc import TerminalController as TermCtrl
import tty
import sys


tty.setcbreak(sys.stdin.fileno()) # cbreak mode, no buffer
term = TermCtrl()

acts = ("h", "l", "j", "k")
feild = "Use the l and h @rrow keys to move"
#i = 16

sys.stdout.write(term.CYAN + feild + term.LEFT * 18)
sys.stdout.flush()

while 1:
    char = sys.stdin.read(1)
    o = ""
    if char in acts:
        if char == "h":
            o += term.LEFT + "@." + term.LEFT
        elif char == "k":
            o += "." + term.LEFT + term.UP + "@"
        elif char == "j":
            o += "." + term.DOWN + "@"
        else:
            o += ".@"
    else:
        o += "@"
    sys.stdout.write(o + term.LEFT)
    sys.stdout.flush()
