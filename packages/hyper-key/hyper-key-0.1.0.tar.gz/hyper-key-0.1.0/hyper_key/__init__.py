__version__ = '0.1.0'

from readchar import readkey

up = "\x1b[A"
down = "\x1b[B"
right = "\x1b[C"
left = "\x1b[D"

def get(): return readkey()