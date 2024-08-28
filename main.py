import pygame
import tetris
import sys
import colours

def main():
    pygame.init()
    surf = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Tetris')
    frame_counter = pygame.time.Clock()
    frame_counter.tick(60)
    update_time = 500
    update_event = pygame.event.custom_type()
    pygame.time.set_timer(update_event, update_time)
    game = tetris.Tetris()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == update_event:
                game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    game.active_piece.move_left()
                elif event.key == pygame.K_d:
                    game.active_piece.move_right()
                elif event.key == pygame.K_r:
                    game.active_piece.rotate()

        surf.fill(colours.BLACK)
        game.draw(surf)
        pygame.display.update()


if __name__ == '__main__':
    main()
