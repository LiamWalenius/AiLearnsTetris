from dataclasses import dataclass
from enum import Enum
import pygame
import colours

@dataclass
class Position:
    r: int
    c: int

class Shape:
    def __init__(self, data: list[list[int]]):
        self._data = [[bool(i) for i in row] for row in data]

    def __iter__(self):
        return iter(self._data)

    def get(self, r: int, c: int) -> bool:
        return self._data[r][c]

class Piece:
    def __init__(self, shapes: list[Shape]) -> None:
        self.shapes = shapes
        self.active_shape_ind = 0
        self.pos = Position(0, 1)

    def rotate(self) -> None:
        self.active_shape_ind = (self.active_shape_ind + 1) % len(self.shapes)

    def move_up(self) -> None:
        self.pos.r -= 1

    def move_down(self) -> None:
        self.pos.r += 1

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
    NODE_COLOURS = {
        GridNode.EMPTY: colours.BLACK,
        GridNode.WALL: colours.WHITE,
        GridNode.BLOCK: colours.RED,
    }

    # 10 empty spaces + 2 for the walls
    GRID_WIDTH = 10 + 2
    # 20 empty spaces + 1 for the floor
    GRID_HEIGHT = 20 + 1

    def __init__(self) -> None:
        self.pieces = list[Piece]()
        self.pieces.append(Piece([
            Shape([
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]
            ]),
            Shape([
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ])
        ]))
        self.active_piece = self.pieces[0]
        self.grid = [[GridNode.EMPTY for _ in range(Tetris.GRID_WIDTH)] for _ in range(Tetris.GRID_HEIGHT)]
        for i in range(Tetris.GRID_HEIGHT):
            self.grid[i][0] = self.grid[i][-1] = GridNode.WALL
        self.grid[-1] = [GridNode.WALL for _ in range(Tetris.GRID_WIDTH)]

    def update(self) -> None:
        self.active_piece.move_down()

        for r, row in enumerate(self.active_piece.get_active_shape()):
            for c, val in enumerate(row):
                if not val:
                    continue

                grid_r = self.active_piece.pos.r + r
                grid_c = self.active_piece.pos.c + c

                if self.grid[grid_r][grid_c] != GridNode.EMPTY:
                    self.active_piece.move_up()
                    self.make_active_piece_blocks()
                    return

    def make_active_piece_blocks(self) -> None:
        pass

    def rotate_active_piece(self) -> None:
        self.active_piece.rotate()

    def draw(self, surf: pygame.surface.Surface) -> None:
        width, height = surf.get_size()
        node_size = min(width // Tetris.GRID_WIDTH, height // Tetris.GRID_HEIGHT)

        for r, row in enumerate(self.grid):
            for c, node in enumerate(row):
                draw_rect = pygame.Rect(
                    c * node_size,
                    r * node_size,
                    node_size,
                    node_size
                )

                pygame.draw.rect(surf, Tetris.NODE_COLOURS[node], draw_rect)

        for r, row in enumerate(self.active_piece.get_active_shape()):
            for c, node in enumerate(row):
                if not node:
                    continue

                draw_rect = pygame.Rect(
                    (self.active_piece.pos.c + c) * node_size,
                    (self.active_piece.pos.r + r) * node_size,
                    node_size,
                    node_size
                )

                pygame.draw.rect(surf, colours.RED, draw_rect)
