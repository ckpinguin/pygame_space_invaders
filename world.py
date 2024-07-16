from time import sleep
from display import Display
import pygame
from ship import Ship
from alien import Alien
from settings import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    CHARACTER_SIZE,
    ALIEN_ROWS,
    NAV_THICKNESS
)

pygame.mixer.init()


class World:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.player: pygame.sprite.GroupSingle[Ship] = pygame.sprite.GroupSingle()  # noqa
        self.aliens: pygame.sprite.Group[Alien] = pygame.sprite.Group()
        self.display = Display(self.screen)

        self.background_image = pygame.image.load(
            'assets/background/background.png')
        self.background_image = pygame.transform.scale(
            self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.game_over = False
        self.player_score = 0
        self.game_level = 1

        self._prepare_sounds()
        self._generate_world()

    def _prepare_sounds(self):
        self.shoot_sound = pygame.mixer.Sound('assets/sounds/laser.mp3')
        self.alien_hit_sound = pygame.mixer.Sound(
            'assets/sounds/explosion.mp3')
        self.victory_sound = pygame.mixer.Sound('assets/sounds/victory.mp3')
        self.game_over_sound = pygame.mixer.Sound(
            'assets/sounds/game_over.mp3')
        self.lose_life_sound = pygame.mixer.Sound('assets/sound/buzzer.mp3')

    def _generate_aliens(self):
        alien_cols = (SCREEN_WIDTH // CHARACTER_SIZE) // 2
        alien_rows = ALIEN_ROWS
        for y in range(alien_rows):
            for x in range(alien_cols):
                alien_x = CHARACTER_SIZE * x
                alien_y = CHARACTER_SIZE * y
                specific_pos = (alien_x, alien_y)
                self.aliens.add(Alien(specific_pos, CHARACTER_SIZE, y))

    def _generate_player(self):
        player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - CHARACTER_SIZE
        center_size = CHARACTER_SIZE // 2  # To really center the sprite :-)
        player_pos = (player_x - center_size, player_y)
        self.player.add(Ship(player_pos, CHARACTER_SIZE))

    def _generate_world(self):
        self._generate_player()
        self._generate_aliens()

    def add_additionals(self):
        nav = pygame.Rect(0, SCREEN_HEIGHT, SCREEN_WIDTH, NAV_THICKNESS)
        pygame.draw.rect(self.screen, pygame.Color("gray"), nav)
        self.display.show_life(self.player.sprite.life)
        self.display.show_score(self.player_score)
        self.display.show_level(self.game_level)

    def check_keypress(self):
        # This does not work for the shooting (SPACE), because
        # we only want to shoot once per game loop iteration, so
        # the soot is called in main.py
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not self.game_over:
            if self.player.sprite.rect.left > 0:
                self.player.sprite.move_left()

        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not self.game_over:
            if self.player.sprite.rect.left < SCREEN_WIDTH:
                self.player.sprite.move_right()

        if (keys[pygame.K_w] or keys[pygame.K_DOWN]) and not self.game_over:
            if self.player.sprite.rect.bottom < SCREEN_HEIGHT:
                self.player.sprite.move_down()

        # Restart button
        if keys[pygame.K_r]:
            self.game_over = False
            self.player_score = 0
            self.game_level = 1
            for alien in self.aliens.sprites():
                alien.kill()
            self._generate_world()

    def player_shoot(self):
        self.player.sprite._shoot()
        self.shoot_sound.play()

    def _detect_collisions(self):
        player_attack_collision = pygame.sprite.groupcollide(
            self.aliens, self.player.sprite.player_bullets, True, True
        )
        if player_attack_collision:
            self.player_score += 10
            self.alien_hit_sound.play()
        for alien in self.aliens.sprites():
            alien_attack_collision = pygame.sprite.groupcollide(
                alien.bullets, self.player, True, False
            )
            if alien_attack_collision:
                self.player.sprite.life -= 1
                self.lose_life_sound.play()
                break

        alien_to_player_collision = pygame.sprite.groupcollide(
            self.aliens, self.player, True, False
        )
        if alien_to_player_collision:
            self.player.sprite.life -= 1
            self.lose_life_sound.play()

        if self.player.sprite.life <= 0:
            self.game_over_sound.play()

    def _alien_movement(self):
        move_sideward = False
        move_forward = False

        for alien in self.aliens.sprites():
            if alien.to_direction == "right" \
                    and alien.rect.right < SCREEN_WIDTH \
                    or alien.to_direction == "left" and alien.rect.left > 0:
                move_sideward = True
                move_forward = False
            else:
                move_sideward = False
                move_forward = True
                alien.to_direction = \
                    "left" if alien.to_direction == "right" else "right"
                break

        for alien in self.aliens.sprites():
            if move_sideward and not move_forward:
                if alien.to_direction == "right":
                    alien.move_right()
                if alien.to_direction == "left":
                    alien.move_left()
            if not move_sideward and move_forward:
                alien.move_down()

    def _alien_shoot(self):
        for alien in self.aliens.sprites():
            # Shoot when in line with the player
            if (SCREEN_WIDTH - alien.rect.x) // CHARACTER_SIZE == \
                    (SCREEN_WIDTH - self.player.sprite.rect.x) // CHARACTER_SIZE:
                alien._shoot()
                break

    def _check_game_state(self):
        if self.player.sprite.life <= 0:
            self.game_over = True
            self.display.game_over_message()
        for alien in self.aliens.sprites():
            if alien.rect.top >= SCREEN_HEIGHT:
                self.game_over = True
                self.display.game_over_message()
                break

        if len(self.aliens) == 0 and self.player.sprite.life > 0:
            self.game_level += 1
            self.victory_sound.play()
            sleep(1)
            self._generate_aliens()
            for alien in self.aliens.sprites():
                # Raise speed according to current level
                alien.move_speed += self.game_level - 1

    def update(self):
        self.screen.blit(self.background_image, (0, 0))
        if not self.game_over:
            self._detect_collisions()
            self._alien_movement()
            self._alien_shoot()
            self.player.sprite.player_bullets.update()
            self.player.sprite.player_bullets.draw(self.screen)
            [alien.bullets.update() for alien in self.aliens.sprites()]
            [alien.bullets.draw(self.screen)
             for alien in self.aliens.sprites()]
            self.player.update()
        self.player.draw(self.screen)
        self.aliens.draw(self.screen)
        self.add_additionals()
        self._check_game_state()
