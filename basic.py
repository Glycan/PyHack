from tc import TerminalController as TermCtrl
import sys

term = TermCtrl()

acts = ("h", "l")
feild = "Use the l and h @rrow keys to move"
#i = 16

sys.stdout.write(term.CYAN + feild + term.LEFT * 18)
sys.stdout.flush()

while 1:
    char = sys.stdin.read(1)
    o = term.LEFT
    if char in acts:
        if char == "h":
            o += term.LEFT + "@."
        else:
            o += ".@"
    else:
        o += "@"
    sys.stdout.write(o)
    sys.stdout.flush()
