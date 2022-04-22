import pygame
import random
from config import Config


class Ball:
    def __init__(self, x: int, y: int, config: Config, radius: int = None, velocity: float = None,
                 multiplier: float = None, color: tuple[int, int, int] = None):
        self.config = config
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius if radius is not None else self.config.BALL_RADIUS
        self.x_vel = self.original_x_vel = velocity if velocity is not None else self.config.BALL_VELOCITY
        self.y_vel = random.random() * random.choice((1, -1))
        self.multiplier = multiplier if multiplier is not None else self.config.BALL_MULTIPLIER
        self.color = color if color is not None else self.config.BALL_COLOR

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def update_velocity(self):
        self.x_vel *= self.multiplier
        self.y_vel *= self.multiplier

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel = self.original_x_vel
        self.y_vel = random.random() * random.choice((1, -1))
