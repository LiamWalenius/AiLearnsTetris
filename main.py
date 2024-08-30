import pygame
import pygame.freetype
import tetris
import sys
import colours

def main():
    pygame.init()
    surf = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Tetris')
    frame_counter = pygame.time.Clock()
    frame_counter.tick(60)
    update_event = pygame.event.custom_type()
    pygame.time.set_timer(update_event, 500)
    game = tetris.Tetris()
    arial_font = pygame.freetype.SysFont('Arial', 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == update_event:
                game.update()
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        sys.exit()
                    case pygame.K_s:
                        game.move_active_piece_down()
                    case pygame.K_a:
                        game.move_active_piece_left()
                    case pygame.K_d:
                        game.move_active_piece_right()
                    case pygame.K_SPACE:
                        game.move_active_piece_to_bottom()
                    case pygame.K_r:
                        game.rotate_active_piece()

        surf.fill(colours.BLACK)
        game.draw(surf, arial_font)
        pygame.display.update()


if __name__ == '__main__':
    main()
