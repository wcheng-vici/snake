import sys
import os
import termios
import tty
import select
import time as time_module
from collections import namedtuple

K_UP = 1
K_DOWN = 2
K_LEFT = 3
K_RIGHT = 4
K_SPACE = 5
K_ESCAPE = 6
KEYDOWN = 7
QUIT = 8

Event = namedtuple('Event', ['type', 'key'])
RectClass = namedtuple('Rect', ['x', 'y', 'width', 'height'])

class Display:
    def __init__(self):
        self.caption = ""
        self.screen = None
        
    def set_mode(self, size):
        self.screen = Screen(size[0], size[1])
        return self.screen
        
    def set_caption(self, caption):
        self.caption = caption
        
    def flip(self):
        if self.screen:
            self.screen.render()

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_width = width // 20
        self.cell_height = height // 20
        self.buffer = [[' ' for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        self.colors = [[None for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        
    def fill(self, color):
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                self.buffer[y][x] = ' '
                self.colors[y][x] = None
                
    def blit(self, surface, pos):
        pass
        
    def render(self):
        os.system('clear')
        print("╔" + "═" * self.cell_width + "╗")
        for y in range(self.cell_height):
            print("║", end="")
            for x in range(self.cell_width):
                print(self.buffer[y][x], end="")
            print("║")
        print("╚" + "═" * self.cell_width + "╝")
        sys.stdout.flush()

class Draw:
    @staticmethod
    def rect(screen, color, rect, width=0):
        if isinstance(rect, RectClass):
            x = rect.x // 20
            y = rect.y // 20
        else:
            x = rect[0] // 20
            y = rect[1] // 20
            
        if 0 <= y < screen.cell_height and 0 <= x < screen.cell_width:
            if color == (0, 255, 0) or color == (0, 150, 0):
                screen.buffer[y][x] = '█'
            elif color == (255, 0, 0):
                screen.buffer[y][x] = '●'
            elif color == (255, 255, 255):
                screen.buffer[y][x] = '○'
                
    @staticmethod
    def line(screen, color, start, end, width):
        pass

class Font:
    def __init__(self, name, size):
        self.size = size
        
    def render(self, text, antialias, color):
        return TextSurface(text)
        
    def get_rect(self, **kwargs):
        return RectClass(0, 0, 0, 0)

class TextSurface:
    def __init__(self, text):
        self.text = text
        
    def get_rect(self, **kwargs):
        return RectClass(0, 0, len(self.text), 1)

class Clock:
    def __init__(self):
        self.last_tick = time_module.time()
        
    def tick(self, fps):
        current = time_module.time()
        elapsed = current - self.last_tick
        delay = 1.0 / fps - elapsed
        if delay > 0:
            time_module.sleep(delay)
        self.last_tick = time_module.time()

class EventHandler:
    def __init__(self):
        self.old_settings = None
        try:
            if sys.stdin.isatty():
                self.old_settings = termios.tcgetattr(sys.stdin)
                tty.setcbreak(sys.stdin.fileno())
        except:
            pass
        
    def get(self):
        events = []
        try:
            if select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.read(1)
                if key == '\x1b':
                    if select.select([sys.stdin], [], [], 0)[0]:
                        key2 = sys.stdin.read(1)
                        if key2 == '[':
                            if select.select([sys.stdin], [], [], 0)[0]:
                                key3 = sys.stdin.read(1)
                                if key3 == 'A':
                                    events.append(Event(type=KEYDOWN, key=K_UP))
                                elif key3 == 'B':
                                    events.append(Event(type=KEYDOWN, key=K_DOWN))
                                elif key3 == 'C':
                                    events.append(Event(type=KEYDOWN, key=K_RIGHT))
                                elif key3 == 'D':
                                    events.append(Event(type=KEYDOWN, key=K_LEFT))
                        else:
                            events.append(Event(type=KEYDOWN, key=K_ESCAPE))
                    else:
                        events.append(Event(type=KEYDOWN, key=K_ESCAPE))
                elif key == ' ':
                    events.append(Event(type=KEYDOWN, key=K_SPACE))
                elif key == 'w' or key == 'W':
                    events.append(Event(type=KEYDOWN, key=K_UP))
                elif key == 's' or key == 'S':
                    events.append(Event(type=KEYDOWN, key=K_DOWN))
                elif key == 'a' or key == 'A':
                    events.append(Event(type=KEYDOWN, key=K_LEFT))
                elif key == 'd' or key == 'D':
                    events.append(Event(type=KEYDOWN, key=K_RIGHT))
                elif key == 'q' or key == '\x03':
                    events.append(Event(type=QUIT, key=None))
                    events.append(Event(type=KEYDOWN, key=K_ESCAPE))
        except:
            pass
        return events
        
    def cleanup(self):
        if self.old_settings:
            try:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            except:
                pass

display = Display()
draw = Draw()
font = type('font', (), {'Font': Font})()
event_handler = None
time = type('time', (), {'Clock': Clock})()

def init():
    global event_handler
    event_handler = EventHandler()

def quit():
    global event_handler
    if event_handler:
        event_handler.cleanup()
    os.system('clear')

class event:
    @staticmethod
    def get():
        if event_handler:
            return event_handler.get()
        return []

def Rect(x, y, width, height):
    return RectClass(x, y, width, height)