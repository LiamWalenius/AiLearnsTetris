from dataclasses import dataclass
from enum import Enum
import pygame
import colours

@dataclass
class Position:
    r: int
    c: int

@dataclass(frozen=True)
class Shape:
    _data: list[list[bool]]

    def get(self, r: int, c: int) -> bool:
        return self._data[r][c]

class Piece:
    def __init__(self, shapes: list[Shape]) -> None:
        self.shapes = shapes
        self.active_shape_ind = 0
        self.pos = Position(0, 0)

    def rotate(self) -> None:
        self.active_shape_ind = (self.active_shape_ind + 1) % len(self.shapes)

    def move_down(self) -> None:
        self.pos.r -= 1

    def move_left(self) -> None:
        self.pos.c -= 1

    def move_right(self) -> None:
        self.pos.c += 1

    def get_active_shape(self) -> Shape:
        return self.shapes[self.active_shape_ind]

class GridNode(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2

class Tetris:
    node_colours = {
        GridNode.EMPTY: colours.BLACK,
        GridNode.WALL: colours.WHITE,
        GridNode.BLOCK: colours.RED,
    }

    def __init__(self) -> None:
        self.pieces = list[Piece]()
        self.active_piece = self.pieces[0]
        self.grid = list[list[GridNode]]()

    def update(self) -> None:
        self.active_piece.move_down()

    def rotate_active_piece(self) -> None:
        self.active_piece.rotate()

    def draw(self, surf: pygame.surface.Surface) -> None:
        width, height = surf.get_size()
        node_size = min(width // len(self.grid[0]), height // len(self.grid))

        for r, row in enumerate(self.grid):
            for c, node in enumerate(row):
                draw_rect = pygame.Rect(
                    c * node_size,
                    r * node_size,
                    node_size,
                    node_size
                )

                pygame.draw.rect(surf, Tetris.node_colours[node], draw_rect)
