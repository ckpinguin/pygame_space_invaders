import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, NAV_THICKNESS
from world import World

pygame.init()
# the display surface:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + NAV_THICKNESS))
pygame.display.set_caption('Space Invaders Clone Attack')


class Main:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.FPS = pygame.time.Clock()

    def main(self):
        world = World(self.screen)
        while True:
            self.screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        world.player_shoot()
            world.check_keypress()
            world.update()
            pygame.display.update()
            self.FPS.tick(30)


if __name__ == "__main__":
    play = Main(screen)
    play.main()
