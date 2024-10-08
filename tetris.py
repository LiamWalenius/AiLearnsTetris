from typing import NamedTuple, Iterator
from enum import Enum
import pygame
import pygame.freetype
import colours
import random

class Position(NamedTuple):
    r: int
    c: int

class Shape:
    def __init__(self, data: list[str]) -> None:
        self._data = [[c == '1' for c in line] for line in data]

    def __iter__(self) -> Iterator[list[bool]]:
        return iter(self._data)

class Piece:
    def __init__(self, shapes: list[Shape], colour: pygame.Color, pos: Position) -> None:
        self.shapes = shapes
        self.active_shape_ind = 0
        self.colour = colour
        self.start_pos = pos
        self.pos = pos

    def reset(self) -> None:
        self.active_shape_ind = 0
        self.pos = self.start_pos

    def get_active_shape(self) -> Shape:
        return self.shapes[self.active_shape_ind]

def load_pieces_from_file(path: str) -> list[Piece]:
    pieces = []

    with open(path, 'r') as in_file:
        for line in in_file:
            sections = line.strip().split(',')
            colour = colours.get_colour_from_str(sections[0])
            shapes = [Shape(s.split()) for s in sections[1:]]
            pieces.append(Piece(shapes, colour, Position(0, 4)))

    return pieces

class GridNode(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2

def get_empty_row(width: int) -> list[GridNode]:
    return [GridNode.WALL] + [GridNode.EMPTY for _ in range(width - 2)] + [GridNode.WALL]

class Tetris:
    # 10 empty spaces + 2 for the walls
    GRID_WIDTH = 10 + 2
    # 20 empty spaces + 1 for the floor
    GRID_HEIGHT = 20 + 1

    UP = Position(-1, 0)
    DOWN = Position(1, 0)
    LEFT = Position(0, -1)
    RIGHT = Position(0, 1)

    def __init__(self) -> None:
        self._pieces = load_pieces_from_file('pieces.txt')
        random.shuffle(self._pieces)
        self._active_piece_ind = 0
        self._active_piece = self._pieces[self._active_piece_ind]
        self._grid = [get_empty_row(Tetris.GRID_WIDTH) for _ in range(Tetris.GRID_HEIGHT-1)]
        self._grid.append([GridNode.WALL for _ in range(Tetris.GRID_WIDTH)])
        self._grid_colours: list[list[pygame.Color]] = [[colours.WHITE for _ in range(Tetris.GRID_WIDTH)] for _ in range(Tetris.GRID_HEIGHT)]
        self._score = 0
        self._has_lost = False

    def update(self) -> None:
        if not self._has_lost:
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
            self._grid_colours[r][c] = self._active_piece.colour

        self.increment_active_piece()
        self.check_for_full_rows()

    def increment_active_piece(self) -> None:
        self._active_piece.reset()
        self._active_piece_ind += 1
        if self._active_piece_ind == len(self._pieces):
            self._active_piece_ind = 0
            random.shuffle(self._pieces)
        self._active_piece = self._pieces[self._active_piece_ind]

        if self.active_piece_is_colliding():
            self.lose()

    def lose(self) -> None:
        self._has_lost = True

    def row_is_full(self, r: int) -> bool:
        return all(node == GridNode.BLOCK for node in self._grid[r][1:-1])

    def check_for_full_rows(self) -> None:
        full_row_count = 0

        for r in range(Tetris.GRID_HEIGHT-2, -1, -1):
            while self.row_is_full(r):
                full_row_count += 1
                self.clear_row(r)

        self.increase_score(full_row_count)

    def clear_row(self, row_ind: int) -> None:
        for r in range(row_ind, 0, -1):
            self._grid[r] = self._grid[r-1]
        self._grid[0] = get_empty_row(Tetris.GRID_WIDTH)

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
            if self.active_piece_can_move(Tetris.LEFT):
                self.move_active_piece_left()
            elif self.active_piece_can_move(Tetris.RIGHT):
                self.move_active_piece_right()
            else:
                self._active_piece.active_shape_ind = start_shape_ind

    def active_piece_can_move(self, offset: Position) -> bool:
        return all(self._grid[r + offset.r][c + offset.c] == GridNode.EMPTY for r, c in self.get_active_piece_grid_positions())

    def move_active_piece(self, offset: Position) -> None:
        if self._has_lost or not self.active_piece_can_move(offset):
            return

        self._active_piece.pos = Position(self._active_piece.pos.r + offset.r, self._active_piece.pos.c + offset.c)

    def move_active_piece_up(self) -> None:
        self.move_active_piece(Tetris.UP)

    def move_active_piece_down(self) -> None:
        self.move_active_piece(Tetris.DOWN)

    def move_active_piece_left(self) -> None:
        self.move_active_piece(Tetris.LEFT)

    def move_active_piece_right(self) -> None:
        self.move_active_piece(Tetris.RIGHT)

    def move_active_piece_to_bottom(self) -> None:
        while self.active_piece_can_move(Tetris.DOWN):
            self.move_active_piece_down()
        self.make_active_piece_blocks()

    def draw(self, surf: pygame.surface.Surface, font: pygame.freetype.Font) -> None:
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

                match node:
                    case GridNode.EMPTY:
                        colour = colours.BLACK
                    case GridNode.WALL:
                        colour = colours.WHITE
                    case _:  # GridNode.Block
                        colour = self._grid_colours[r][c]

                pygame.draw.rect(surf, colour, draw_rect)

        for r, c in self.get_active_piece_grid_positions():
            draw_rect = pygame.Rect(
                c * node_size,
                r * node_size,
                node_size,
                node_size
            )

            pygame.draw.rect(surf, self._active_piece.colour, draw_rect)

        font.render_to(surf, (500, 100), f'Score: {self._score}', fgcolor=colours.WHITE, size=30)

        if self._has_lost:
            font.render_to(surf, (500, 300), 'Game over!', fgcolor=colours.WHITE, size=30)
