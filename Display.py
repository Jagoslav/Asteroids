
import pygame
"""
File Display.pl holds screen display information for a game to keep track on
"""
if __name__ == "__main__":
    exit()


pygame.init()
pygame.display.set_caption("Asteroids")
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME | pygame.FULLSCREEN)
width, height = screen.get_size()
center_x, center_y = width // 2, height // 2
value_modifier = min(width, height) // 400
clock = pygame.time.Clock()
pygame.event.get()
