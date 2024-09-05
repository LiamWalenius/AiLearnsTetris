from pygame import Color

BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
YELLOW = Color(255, 255, 0)
ORANGE = Color(255, 102, 0)
PINK = Color(255, 182, 193)
PURPLE = Color(128, 0, 128)

def get_colour_from_str(colour_str: str) -> Color | None:
    match colour_str:
        case 'black':
            return BLACK
        case 'white':
            return WHITE
        case 'red':
            return RED
        case 'green':
            return GREEN
        case 'blue':
            return BLUE
        case 'yellow':
            return YELLOW
        case 'orange':
            return ORANGE
        case 'pink':
            return PINK
        case 'purple':
            return PURPLE
        case _:
            return None
