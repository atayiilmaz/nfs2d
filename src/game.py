import pygame
import time
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MAIN_FONT, PATH, GRASS_IMG, TRACK_IMG, TRACK_BORDER_IMG, FINISH_IMG, RED_CAR_IMG, GREEN_CAR_IMG, PURPLE_CAR_IMG
from src.utils import scale_image, blit_rotate_center, blit_text_center
from src.car import PlayerCar, ComputerCar
from src.game_info import GameInfo

class RacingGame:
    def __init__(self):
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racing Game!")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(MAIN_FONT, 44)
        self.collision_sound = pygame.mixer.Sound("assets/sounds/car_crash.wav")
        self.car_move_sound = pygame.mixer.Sound("assets/sounds/car_move.wav")
        self.tire_sound = pygame.mixer.Sound("assets/sounds/tires_squal_loop.wav")
        self.car_move_sound.set_volume(0.1)
        self.collision_sound.set_volume(0.2)
        self.tire_sound.set_volume(0.2)
        self.game_mode = None
        self.load_assets()
        self.setup()

    def load_assets(self):
        self.grass = scale_image(pygame.image.load(GRASS_IMG), 2.5)
        self.track = scale_image(pygame.image.load(TRACK_IMG), 0.9)
        self.track_border = scale_image(pygame.image.load(TRACK_BORDER_IMG), 0.9)
        self.track_border_mask = pygame.mask.from_surface(self.track_border)
        self.finish = pygame.image.load(FINISH_IMG)
        self.finish_mask = pygame.mask.from_surface(self.finish)
        self.finish_position = (130, 250)
        self.red_car = scale_image(pygame.image.load(RED_CAR_IMG), 0.4)
        self.green_car = scale_image(pygame.image.load(GREEN_CAR_IMG), 0.4)
        self.purple_car = scale_image(pygame.image.load(PURPLE_CAR_IMG), 0.4)

    def setup(self):
        self.images = [(self.grass, (0, 0)), (self.track, (0, 0)),
                       (self.finish, self.finish_position), (self.track_border, (0, 0))]
        self.all_sprites = pygame.sprite.Group()

        if self.game_mode == "single":
            self.player_car = PlayerCar(self.red_car, 4, 4, (190, 200), self.car_move_sound)
            self.computer_car = ComputerCar(self.green_car, 2, 4, PATH, self.car_move_sound)
            self.all_sprites.add(self.player_car, self.computer_car)
        elif self.game_mode == "two":
            self.player_car = PlayerCar(self.red_car, 4, 4, (190, 200), self.car_move_sound)
            self.player2_car = PlayerCar(self.purple_car, 2, 4, (160, 200), self.car_move_sound)
            self.all_sprites.add(self.player_car, self.player2_car)

        self.game_info = GameInfo()
        self.track_border_group = pygame.sprite.Group()
        self.finish_group = pygame.sprite.Group()

        self.track_border_sprite = pygame.sprite.Sprite()
        self.track_border_sprite.image = self.track_border
        self.track_border_sprite.rect = self.track_border_sprite.image.get_rect()
        self.track_border_sprite.mask = self.track_border_mask
        self.track_border_group.add(self.track_border_sprite)

        self.finish_sprite = pygame.sprite.Sprite()
        self.finish_sprite.image = self.finish
        self.finish_sprite.rect = self.finish_sprite.image.get_rect(topleft=self.finish_position)
        self.finish_sprite.mask = self.finish_mask
        self.finish_group.add(self.finish_sprite)

    def draw_mode_selection(self):
        self.win.fill((0, 0, 0))
        single_player_text = self.font.render("Single Player (Press 1)", True, (255, 255, 255))
        two_player_text = self.font.render("Two Player (Press 2)", True, (255, 255, 255))
        self.win.blit(single_player_text, (SCREEN_WIDTH // 2 - single_player_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.win.blit(two_player_text, (SCREEN_WIDTH // 2 - two_player_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        pygame.display.update()

    def draw(self):
        for img, pos in self.images:
            self.win.blit(img, pos)

        level_text = self.font.render(f"Level {self.game_info.level}", 1, (255, 255, 255))
        self.win.blit(level_text, (10, SCREEN_HEIGHT - level_text.get_height() - 70))

        time_text = self.font.render(f"Time: {self.game_info.get_level_time()}s", 1, (255, 255, 255))
        self.win.blit(time_text, (10, SCREEN_HEIGHT - time_text.get_height() - 40))

        self.all_sprites.draw(self.win)
        pygame.display.update()

    def move_player(self):
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a]:
            self.player_car.rotate(left=True)
        if keys[pygame.K_d]:
            self.player_car.rotate(right=True)
        if keys[pygame.K_w]:
            moved = True
            self.player_car.move_forward()
        if keys[pygame.K_s]:
            pygame.mixer.Channel(1).play(self.tire_sound, 0, 500)
            moved = True
            self.player_car.move_backward()

        if self.game_mode == "two":
            if keys[pygame.K_LEFT]:
                self.player2_car.rotate(left=True)
            if keys[pygame.K_RIGHT]:
                self.player2_car.rotate(right=True)
            if keys[pygame.K_UP]:
                moved = True
                self.player2_car.move_forward()
            if keys[pygame.K_DOWN]:
                pygame.mixer.Channel(1).play(self.tire_sound, 0, 500)
                moved = True
                self.player2_car.move_backward()

        if not moved:
            self.player_car.reduce_speed()
            self.player2_car.reduce_speed()

    def handle_collision(self):
        if self.game_mode == "single":
            if pygame.sprite.spritecollide(self.computer_car, self.track_border_group, False, pygame.sprite.collide_mask):
                # pygame.mixer.Channel(3).play(self.collision_sound)
                self.computer_car.bounce()
            if pygame.sprite.spritecollide(self.computer_car, [self.player_car], False, pygame.sprite.collide_mask):
                self.computer_car.bounce()
            if pygame.sprite.spritecollide(self.player_car, [self.computer_car], False, pygame.sprite.collide_mask):
                self.player_car.bounce()
            if pygame.sprite.spritecollide(self.computer_car, self.finish_group, False, pygame.sprite.collide_mask):
                blit_text_center(self.win, self.font, "You lost!")
                pygame.display.update()
                pygame.time.wait(2000)
                self.game_info.reset()
                self.player_car.reset((190, 200))
                self.computer_car.reset((160, 200))
            if pygame.sprite.spritecollide(self.player_car, self.finish_group, False, pygame.sprite.collide_mask):
                if self.finish_mask.overlap(pygame.mask.from_surface(self.player_car.image), (int(self.player_car.rect.x - self.finish_position[0]), int(self.player_car.rect.y - self.finish_position[1]))) is not None:
                    self.game_info.next_level()
                    self.player_car.reset((190, 200))
                    self.computer_car.next_level(self.game_info.level)

        if self.game_mode == "two":
            if pygame.sprite.spritecollide(self.player2_car, self.track_border_group, False, pygame.sprite.collide_mask):
                pygame.mixer.Channel(3).play(self.collision_sound)
                self.player2_car.bounce()
            if pygame.sprite.spritecollide(self.player2_car, [self.player_car], False, pygame.sprite.collide_mask):
                self.player2_car.bounce()
            if pygame.sprite.spritecollide(self.player_car, [self.player2_car], False, pygame.sprite.collide_mask):
                self.player_car.bounce()
            if pygame.sprite.spritecollide(self.player2_car, self.finish_group, False, pygame.sprite.collide_mask):
                blit_text_center(self.win, self.font, "Player 2 won!")
                pygame.display.update()
                pygame.time.wait(2000)
                self.game_info.reset()
                self.player_car.reset((190, 200))
                self.player2_car.reset((160, 200))
            if pygame.sprite.spritecollide(self.player_car, self.finish_group, False, pygame.sprite.collide_mask):
                blit_text_center(self.win, self.font, "Player 1 won!")
                pygame.display.update()
                pygame.time.wait(2000)
                self.game_info.reset()
                self.player_car.reset((190, 200))
                self.player2_car.reset((160, 200))

        if pygame.sprite.spritecollide(self.player_car, self.track_border_group, False, pygame.sprite.collide_mask):
            pygame.mixer.Channel(3).play(self.collision_sound)
            self.player_car.bounce()

    def run(self):
        run = True
        gameState = False
        while run:
            self.clock.tick(FPS)
            self.draw()

            if not gameState:
                self.draw_mode_selection()
                gameState = True

            while not self.game_info.started:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.game_mode = "single"
                            self.setup()
                        elif event.key == pygame.K_2:
                            self.game_mode = "two"
                            self.setup()   
                        self.game_info.start_level()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.move_player()
            if self.game_mode == "single":
                self.computer_car.move()
            if self.game_mode == "two":
                self.player2_car.move()
            self.handle_collision()

            if self.game_info.game_finished():
                blit_text_center(self.win, self.font, "You won the game!")
                gameState = False
                self.game_info.reset()