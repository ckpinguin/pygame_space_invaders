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
        self.background_image = pygame.image.load(
            'assets/background/background.png')
        self.background_image = pygame.transform.scale(
            self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def main(self):
        world = World(self.screen)
        while True:
            self.screen.blit(self.background_image, (0, 0))
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
