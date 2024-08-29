from typing import NamedTuple
from enum import Enum
import pygame
import colours
import random

class Position(NamedTuple):
    r: int
    c: int

class Shape:
    def __init__(self, data: list[list[int]]):
        self._data = [[bool(i) for i in row] for row in data]

    def __iter__(self):
        return iter(self._data)

class Piece:
    def __init__(self, shapes: list[Shape]) -> None:
        self.shapes = shapes
        self.active_shape_ind = 0
        self.pos = Position(0, 1)

    def reset(self) -> None:
        self.active_shape_ind = 0
        self.pos = Position(0, 1)

    def rotate(self) -> None:
        self.active_shape_ind = (self.active_shape_ind + 1) % len(self.shapes)

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
        self._active_piece: Piece = random.choice(self.pieces)
        self._grid = [[GridNode.EMPTY for _ in range(Tetris.GRID_WIDTH)] for _ in range(Tetris.GRID_HEIGHT)]
        for i in range(Tetris.GRID_HEIGHT):
            self._grid[i][0] = self._grid[i][-1] = GridNode.WALL
        self._grid[-1] = [GridNode.WALL for _ in range(Tetris.GRID_WIDTH)]

    def update(self) -> None:
        self.move_active_piece_down()

        if self.active_piece_is_colliding():
            self.move_active_piece_up()
            self.make_active_piece_blocks()

    def get_active_piece_positions(self) -> list[Position]:
        positions = []

        for r, row in enumerate(self._active_piece.get_active_shape()):
            for c, val in enumerate(row):
                if not val:
                    continue

                grid_r = self._active_piece.pos.r + r
                grid_c = self._active_piece.pos.c + c

                positions.append(Position(grid_r, grid_c))

        return positions

    def make_active_piece_blocks(self) -> None:
        for r, c in self.get_active_piece_positions():
            self._grid[r][c] = GridNode.BLOCK

        self._active_piece.reset()
        self._active_piece = random.choice(self.pieces)

    def rotate_active_piece(self) -> None:
        self._active_piece.rotate()

    def move_active_piece_up(self) -> None:
        self._active_piece.pos = Position(self._active_piece.pos.r - 1, self._active_piece.pos.c)

    def move_active_piece_down(self) -> None:
        self._active_piece.pos = Position(self._active_piece.pos.r + 1, self._active_piece.pos.c)

    def move_active_piece_left(self) -> None:
        self._active_piece.pos = Position(self._active_piece.pos.r, self._active_piece.pos.c - 1)

    def move_active_piece_right(self) -> None:
        self._active_piece.pos = Position(self._active_piece.pos.r, self._active_piece.pos.c + 1)

    def move_active_piece_to_bottom(self) -> None:
        while not self.active_piece_is_colliding():
            self.move_active_piece_down()
        self.move_active_piece_up()
        self.update()

    def active_piece_is_colliding(self) -> bool:
        return any(self._grid[r][c] != GridNode.EMPTY for r, c in self.get_active_piece_positions())

    def draw(self, surf: pygame.surface.Surface) -> None:
        width, height = surf.get_size()
        node_size = min(width // Tetris.GRID_WIDTH, height // Tetris.GRID_HEIGHT)

        for r, row in enumerate(self._grid):
            for c, node in enumerate(row):
                draw_rect = pygame.Rect(
                    c * node_size,
                    r * node_size,
                    node_size,
                    node_size
                )

                pygame.draw.rect(surf, Tetris.NODE_COLOURS[node], draw_rect)

        for r, c in self.get_active_piece_positions():
            draw_rect = pygame.Rect(
                c * node_size,
                r * node_size,
                node_size,
                node_size
            )

            pygame.draw.rect(surf, colours.BLUE, draw_rect)
