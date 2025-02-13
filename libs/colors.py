from enum import Enum

class Colors(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DEFAULT = 39

class Color:
    bgoffset = 10
    reset = 0
    fgcolor = bgcolor = None
    map = {}

    @staticmethod
    def setdefault(fgcolor : Colors, bgcolor : Colors = None):
        if fgcolor and fgcolor in Colors:
            Color.fgcolor = fgcolor

        if bgcolor and bgcolor in Colors:
            Color.bgcolor = bgcolor
    
    @staticmethod
    def mapfg(seq : list[str], fgcolors : list[Colors], repeat=False):
        index = 0
        for elem in seq:
            if fgcolors and index < len(fgcolors):
                Color.map[elem] = fgcolors[index]

            elif fgcolors and repeat:
                Color.map[elem] = fgcolors[len(fgcolors) - 1]
                
            elif Color.fgcolor:
                Color.map[elem] = Color.fgcolor

            index += 1


    @staticmethod
    def color(text, fgcolor : Colors = None, bgcolor : Colors = None):
        fgcolor = fgcolor or Color.map[text] if text in Color.map else Color.fgcolor
        bgcolor = bgcolor or Color.bgcolor

        result = text
        if fgcolor and fgcolor in Colors:
            result = f"\033[{fgcolor.value}m{text}\033[{Color.reset}m"

        if bgcolor and bgcolor in Colors:
            return f"\033[{bgcolor.value + Color.bgoffset}m{result}\033[{Color.reset}m"
        
        return result


    