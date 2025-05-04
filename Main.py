# Aivaras Praniauskas - Space Invaders

import pygame
import sys
from Player import Player
import Obstacle
from Alien import Alien
from Alien import Extra
from random import choice
from random import randint
from Laser import Laser
from SoundManager import SoundManager


class Game:
    
    def __init__(self):
        
        # Sound setup

        self.sound = SoundManager()
        
        # Player setup
        
        player_sprite = Player((screen_width / 2, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health and score setup
        self.lives = 3
        original_image = pygame.image.load('Pictures/Heart.png').convert_alpha()
        scaled_size = (20, 20)  # Set this to whatever size looks good
        self.live_surf = pygame.transform.scale(original_image, scaled_size)
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('Micro5-Regular.ttf', 40)
        self.bonus_awarded = False
        self.highscore = self.read_highscore()

        # obstacle setup
        
        self.shape = Obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start=screen_width / 15, y_start=480)

        # Alien setup

        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1

        # Extra setup
        
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

        # Time-based score penalty
        
        self.time_penalty_timer = pygame.time.get_ticks()
        self.game_over = False


    def read_highscore(self):
        try:
            with open("Highscore.txt", "r") as file:
                highscore = int(file.read().strip())
        except FileNotFoundError:
            highscore = 0
        return highscore


    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Obstacle.Block(self.block_size,(241, 79, 80), x, y)
                    self.blocks.add(block)


    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)


    def alien_setup(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: alien_sprite = Alien('Enemy_1', x, y)
                elif 1 <=row_index <= 2: alien_sprite = Alien('Enemy_2', x, y)
                else: alien_sprite = Alien('Enemy_3', x, y)
                self.aliens.add(alien_sprite)


    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)


    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance


    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.sound.laser_sound()


    def extra_alien_timer(self):
        if not self.aliens.sprites():
            return
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 800)


    def collision_checks(self):

        # Player lasers
        
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                
                # Obstacle collisions
                
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # Alien collisions
                
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.sound.explosion_sound()

                # Extra collision

                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()
                    self.sound.explosion_sound()

        # Alien lasers
        
        if self.alien_lasers:
            for laser in self.alien_lasers:
                
                # Obstacle collisions
                
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.sound.explosion_sound()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                        self.display_game_over()
                        return

        # Aliens
        
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.game_over = True
                    self.display_game_over()
                    return


    def display_lives(self):
        for live in range(self.lives -1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft = (10, 0))
        screen.blit(score_surf, score_rect)

        highscore_surf = self.font.render(f'Highscore: {self.highscore}', False, 'white')
        highscore_rect = highscore_surf.get_rect(topleft=(10, 40))
        screen.blit(highscore_surf, highscore_rect)


    def victory_message(self):
        if not self.aliens.sprites():
            if not self.bonus_awarded:
                if self.lives == 3:
                    self.score += 400
                elif self.lives == 2:
                    self.score += 200
                self.bonus_awarded = True

            self.game_over = True
            
            victory_surf = self.font.render('You won', False, 'White')
            victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_height / 2))
            screen.blit(victory_surf, victory_rect)

            score_text = f'Your score: {self.score}'
            score_surf = self.font.render(score_text, False, 'White')
            score_rect = score_surf.get_rect(center = (screen_width / 2, screen_height / 2 + 30))
            screen.blit(score_surf, score_rect)

            press_enter_surf = self.font.render('Press Enter to exit', False, 'White')
            press_enter_rect = press_enter_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 80))
            screen.blit(press_enter_surf, press_enter_rect)


    def display_game_over(self):

        pygame.time.set_timer(ALIENLASER, 0)
        game_over_surf = self.font.render('You Lost', False, 'White')
        game_over_rect = game_over_surf.get_rect(center=(screen_width / 2, screen_height / 2 - 30))
        screen.blit(game_over_surf, game_over_rect)

        score_text = f'Your score: {self.score}'
        score_surf = self.font.render(score_text, False, 'White')
        score_rect = score_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 30))
        screen.blit(score_surf, score_rect)

        press_enter_surf = self.font.render('Press Enter to exit', False, 'White')
        press_enter_rect = press_enter_surf.get_rect(center=(screen_width / 2, screen_height / 2 + 80))
        screen.blit(press_enter_surf, press_enter_rect)


    def run(self):
        if self.game_over:
            if self.score > self.highscore:
                self.highscore = self.score
                with open("Highscore.txt", "w") as file:
                    file.write(str(self.highscore))
                    
            if not self.aliens.sprites():
                self.victory_message()
            else:
                self.display_game_over()
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.time_penalty_timer >= 1000:
            if self.score >= 5:
                self.score -= 5
            else:
                self.score = 0
            self.time_penalty_timer = current_time
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        
        self.alien_lasers.update()
        self.extra_alien_timer()
        self.extra.update()
        self.collision_checks()
        self.display_lives()
        
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_score()
        self.victory_message()


class CRT:
    def __init__(self, screen_width, screen_height):
        self.tv = pygame.image.load('Pictures/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))


    def create_crt_lines(self):
        line_height = 3
        line_amount = int(self.tv.get_height() / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (self.tv.get_width(), y_pos), 1)


    def draw(self):
        self.tv.set_alpha(randint(20, 100))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load("Audio/Song.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

    screen_width = 600
    screen_height = 600

    screen = pygame.display.set_mode((screen_width, screen_height))

    game = Game()
    crt = CRT(screen_width, screen_height)

    clock = pygame.time.Clock()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game.game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    pygame.quit()
                    sys.exit()
            else:
                if event.type == ALIENLASER:
                    game.alien_shoot()
        screen.fill((30, 30, 30))
        game.run()
        crt.draw()

        pygame.display.flip()
        clock.tick(60)
