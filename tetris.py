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
    def __init__(self, shapes: list[Shape], pos: Position) -> None:
        self.shapes = shapes
        self.active_shape_ind = 0
        self.start_pos = pos
        self.pos = pos

    def reset(self) -> None:
        self.active_shape_ind = 0
        self.pos = self.start_pos

    def get_active_shape(self) -> Shape:
        return self.shapes[self.active_shape_ind]

class GridNode(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2

def get_empty_row() -> list[GridNode]:
    return [GridNode.WALL] + [GridNode.EMPTY for _ in range(Tetris.GRID_WIDTH - 2)] + [GridNode.WALL]

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

    UP = Position(-1, 0)
    DOWN = Position(1, 0)
    LEFT = Position(0, -1)
    RIGHT = Position(0, 1)

    def __init__(self) -> None:
        self.pieces: list[Piece] = []
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
        ], Position(0, Tetris.GRID_WIDTH // 2)))
        self._active_piece: Piece = random.choice(self.pieces)
        self._grid = [get_empty_row() for _ in range(Tetris.GRID_HEIGHT-1)]
        self._grid.append([GridNode.WALL for _ in range(Tetris.GRID_WIDTH)])
        self._score = 0

    def update(self) -> None:
        if self.active_piece_can_move(Tetris.DOWN):
            self.move_active_piece_down()
        else:
            self.make_active_piece_blocks()

    def get_active_piece_grid_positions(self) -> list[Position]:
        positions = []

        for r, row in enumerate(self._active_piece.get_active_shape()):
            for c, val in enumerate(row):
                if val:
                    positions.append(Position(self._active_piece.pos.r + r, self._active_piece.pos.c + c))

        return positions

    def active_piece_is_colliding(self) -> bool:
        return any(self._grid[r][c] != GridNode.EMPTY for r, c in self.get_active_piece_grid_positions())

    def make_active_piece_blocks(self) -> None:
        for r, c in self.get_active_piece_grid_positions():
            self._grid[r][c] = GridNode.BLOCK

        self._active_piece.reset()
        self._active_piece = random.choice(self.pieces)
        self.check_for_full_rows()

    def row_is_full(self, r: int) -> bool:
        return all(node == GridNode.BLOCK for node in self._grid[r][1:-1])

    def check_for_full_rows(self) -> None:
        full_row_count = 0

        for r in range(Tetris.GRID_HEIGHT-2, -1, -1):
            while self.row_is_full(r):
                full_row_count += 1
                self.clear_row(r)

        self.increase_score(full_row_count)

    def clear_row(self, r: int) -> None:
        for r in range(r, 0, -1):
            self._grid[r] = self._grid[r-1]
        self._grid[0] = get_empty_row()

    def increase_score(self, rows_cleared: int) -> None:
        match rows_cleared:
            case 1:
                self._score += 100
            case 2:
                self._score += 300
            case 3:
                self._score += 500
            case 4:
                self._score += 800

    def rotate_active_piece(self) -> None:
        start_shape_ind = self._active_piece.active_shape_ind
        self._active_piece.active_shape_ind = (start_shape_ind + 1) % len(self._active_piece.shapes)

        if self.active_piece_is_colliding():
            self._active_piece.active_shape_ind = start_shape_ind

    def active_piece_can_move(self, offset: Position) -> bool:
        return all(
            self._grid[r + offset.r][c + offset.c] == GridNode.EMPTY
            for r, c in self.get_active_piece_grid_positions()
        )

    def move_active_piece(self, offset: Position) -> None:
        self._active_piece.pos = Position(self._active_piece.pos.r + offset.r, self._active_piece.pos.c + offset.c)

    def move_active_piece_up(self) -> None:
        if self.active_piece_can_move(Tetris.UP):
            self.move_active_piece(Tetris.UP)

    def move_active_piece_down(self) -> None:
        if self.active_piece_can_move(Tetris.DOWN):
            self.move_active_piece(Tetris.DOWN)

    def move_active_piece_left(self) -> None:
        if self.active_piece_can_move(Tetris.LEFT):
            self.move_active_piece(Tetris.LEFT)

    def move_active_piece_right(self) -> None:
        if self.active_piece_can_move(Tetris.RIGHT):
            self.move_active_piece(Tetris.RIGHT)

    def move_active_piece_to_bottom(self) -> None:
        while self.active_piece_can_move(Tetris.DOWN):
            self.move_active_piece_down()
        self.update()

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

        for r, c in self.get_active_piece_grid_positions():
            draw_rect = pygame.Rect(
                c * node_size,
                r * node_size,
                node_size,
                node_size
            )

            pygame.draw.rect(surf, colours.BLUE, draw_rect)
