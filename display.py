import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SPACE, FONT_SIZE, EVENT_FONT_SIZE

pygame.font.init()


class Display:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.score_font = pygame.font.SysFont("monospace", FONT_SIZE)
        self.level_font = pygame.font.SysFont("impact", FONT_SIZE)
        self.event_font = pygame.font.SysFont("impact", EVENT_FONT_SIZE)
        self.text_color = pygame.Color("blue")
        self.event_color = pygame.Color("red")

    def show_life(self, life: int):
        life_size = 30
        img_path = "assets/life/life.png"
        life_image = pygame.image.load(img_path)
        life_image = pygame.transform.scale(life_image, (life_size, life_size))
        life_x = SCREEN_WIDTH // 2
        if life != 0:
            for life in range(life):
                self.screen.blit(
                    life_image,
                    (life_x + life_size * life, SCREEN_HEIGHT + (SPACE // 2))
                )

    def show_score(self, score: int):
        score_x = SPACE // 2
        score = self.score_font.render(
            f'Score: {score}', True, self.text_color)
        self.screen.blit(score, (score_x, (SCREEN_HEIGHT + (SPACE // 2))))

    def show_level(self, level: int):
        level_x = SCREEN_WIDTH - SPACE * 2.5
        level = self.level_font.render(f'Level {level}', True, self.text_color)
        self.screen.blit(level, (level_x, (SCREEN_HEIGHT + (SPACE // 2))))

    def game_over_message(self):
        message = self.event_font.render(
            'GAME OVER!! (Restart with "r")', True, self.event_color)
        self.screen.blit(message, ((SCREEN_WIDTH // 3) - (EVENT_FONT_SIZE //
                         2), (SCREEN_HEIGHT // 2) - (EVENT_FONT_SIZE // 2)))
