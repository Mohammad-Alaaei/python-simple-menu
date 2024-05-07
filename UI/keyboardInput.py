class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

def getch(msg = ''):
    keys={
        b'H':'UP',
        b'M':'RIGHT',
        b'P':'DOWN',
        b'K':'LEFT',
        b';':'F1',
        b'<':'F2',
        b'=':'F3',
        b'>':'F4',
        b'?':'F5',
        b'@':'F6',
        b'A':'F7',
        b'B':'F8',
        b'C':'F9',
        b'D':'F10',
        b'\x85':'F11',
        b'\x86':'F12',
        '\x08':'BACKSPACE',
        '\x03':'CTRL+C',
        '\x18':'CTRL+X',
        '\x1a':'CTRL+Z',
        '\x06':'CTRL+F',
    }
    inkey = _Getch()
    
    if msg != '' : print(msg)
    
    base = inkey()
    if base in (b'\xe0',b'\x00'):
        sub = inkey()
        key = sub
    else:
        if type(base)!= bytes: base.encode('utf-8').strip()
        try:
            key = str(base.decode("utf-8"))
        except:
            key = str(base)
    
    return keys.get(key,key)
