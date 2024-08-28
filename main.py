import pygame
import tetris

def main():
    pygame.init()
    surf = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Tetris')
    frame_counter = pygame.time.Clock()
    frame_counter.tick(60)
    update_time = 250
    update_event = pygame.event.custom_type()
    pygame.time.set_timer(update_event, update_time)
    game = tetris.Tetris()
