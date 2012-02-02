from tc import TerminalController as TermCtrl
from time import sleep
from sys import stdout

term = TermCtrl()


msg = "This  could and should be much, much longer than it is.    "
l = 30
diff = l - len(msg)
if diff > 0:
    msg += " " * diff

stdout.write(term.BLINK + term.BOLD + term.GREEN + term.DIM)
while 1:
    stdout.write(term.CLEAR_BOL)
    stdout.write(term.BOL)
    stdout.write(msg[:l])
    stdout.flush()
    sleep(0.1)
    msg = msg[-1] + msg[:-1]
