import pygame
from config import Config


class Paddle:
    def __init__(self, x: int, y: int, side_left: bool, config: Config, width: int = None, height: int = None,
                 velocity: float = None, multiplier: float = None, color: tuple[int, int, int] = None):
        self.config = config
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.side_left = side_left
        self.width = width if width is not None else (self.config.LEFT_PADDLE_WIDTH if self.side_left else self.config.RIGHT_PADDLE_WIDTH)
        self.height = height if height is not None else (self.config.LEFT_PADDLE_HEIGHT if self.side_left else self.config.RIGHT_PADDLE_HEIGHT)
        self.velocity = self.original_velocity = velocity if velocity is not None else (self.config.LEFT_PADDLE_VELOCITY if self.side_left else self.config.RIGHT_PADDLE_VELOCITY)
        self.multiplier = multiplier if multiplier is not None else (self.config.LEFT_PADDLE_MULTIPLIER if self.side_left else self.config.RIGHT_PADDLE_MULTIPLIER)
        self.color = color if color is not None else (self.config.LEFT_PADDLE_COLOR if self.side_left else self.config.RIGHT_PADDLE_COLOR)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def update_velocity(self):
        self.velocity *= self.multiplier

    def move(self, up=True):
        if up:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    def merge_velocity(self, *, set_vel: int = None, increase_vel: int = None, decrease_vel: int = None) -> int:
        if set_vel is not None:
            self.velocity = set_vel
        if increase_vel is not None:
            self.velocity += increase_vel
        if decrease_vel is not None:
            self.velocity -= decrease_vel
        return self.velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity = self.original_velocity
