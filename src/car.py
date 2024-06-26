import pygame
import math
from src.utils import blit_rotate_center
import random

class AbstractCar(pygame.sprite.Sprite):
    def __init__(self, img, max_vel, rotation_vel, start_pos, engine_sound):
        super().__init__()
        self.image = img
        self.original_image = img
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = start_pos
        self.acceleration = 0.1
        self.engine_sound = engine_sound
        self.sound_playing = False
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)

    def collide_top(self, mask, x=0, y=0):
        offset = (int(self.rect.left - x), int(self.rect.top - y))
        poi = mask.overlap(self.mask, offset)
        if poi:
            # Check if the collision point is at the top of the mask
            return poi[1] == 0
        return False

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

    def move_forward(self):
        if not self.sound_playing:
            self.engine_sound.play(-1, fade_ms=1000)
            self.sound_playing = True
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        if not self.sound_playing:
            self.engine_sound.play(-1, fade_ms=1000)
            self.sound_playing = True
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
        self.rect.center = (self.x, self.y)

    def reset(self, start_pos):
        self.x, self.y = start_pos
        self.angle = 0
        self.vel = 0
        self.rect.center = (self.x, self.y)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.mask = pygame.mask.from_surface(self.image)

class PlayerCar(AbstractCar):
    def __init__(self, img, max_vel, rotation_vel, start_pos, engine_sound):
        super().__init__(img, max_vel, rotation_vel, start_pos, engine_sound)

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
        if self.vel == 0:
            self.engine_sound.stop()
            self.sound_playing = False

    def bounce(self):
        self.vel = -self.vel * 0.5
        self.move()

class ComputerCar(AbstractCar):
    def __init__(self, img, max_vel, rotation_vel, path, engine_sound):
        super().__init__(img, max_vel, rotation_vel, (160,200), engine_sound)
        self.original_path = path
        self.path = self.randomize_path(path)
        self.current_point = 0
        self.vel = max_vel

    def randomize_path(self, path):
        new_path = []
        for point in path:
            offset_x = random.uniform(-20, 20)
            offset_y = random.uniform(-20, 20)  
            new_path.append((point[0] + offset_x, point[1] + offset_y))
        return new_path
    
    def reset_path(self):
        self.path = self.randomize_path(self.original_path)

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update_path_point(self):
        target = self.path[self.current_point]
        if self.rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        super().move()

    def bounce(self):
        self.vel = -self.vel * 0.5
        self.move()

    def next_level(self, level):
        self.reset((160,200))
        self.reset_path()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0