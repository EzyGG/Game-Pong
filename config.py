import pygame
from dataclasses import dataclass


@dataclass
class Config:
    # NB: Multipliers shouldn't exceed 15 post comma digits.

    TITLE: str = "Pong"

    WIN_WIDTH: int = 700
    WIN_HEIGHT: int = 500
    BACKGROUND: tuple[int, int, int] = (0, 0, 0)
    FOREGROUND: tuple[int, int, int] = (255, 255, 255)
    SCORE_FONT: pygame.font.Font = pygame.font.SysFont("Arial", 50, bold=True)

    FPS: int = 500

    LEFT_PADDLE_WIDTH: int = 15
    LEFT_PADDLE_HEIGHT: int = 100
    LEFT_PADDLE_VELOCITY: float = 1.75
    LEFT_PADDLE_MULTIPLIER: float = 0.99993
    LEFT_PADDLE_COLOR: tuple[int, int, int] = (255, 0, 0)

    RIGHT_PADDLE_WIDTH: int = 15
    RIGHT_PADDLE_HEIGHT: int = 100
    RIGHT_PADDLE_VELOCITY: float = 1.75
    RIGHT_PADDLE_MULTIPLIER: float = 0.999995
    RIGHT_PADDLE_COLOR: tuple[int, int, int] = (0, 255, 0)

    BALL_RADIUS: int = 7
    BALL_VELOCITY: float = -1.0
    BALL_MULTIPLIER: float = 1.00003
    BALL_COLOR: tuple[int, int, int] = (255, 255, 255)

    SEPARATOR_AMOUNT: int = 15
    SEPARATOR_WIDTH: int = 5
    SEPARATOR_COLOR: tuple[int, int, int] = (0, 0, 255)

    WINNING_SCORE: int = 100
    WINNING_DELAY: int = 5000
    WINNING_LEFT_TEXT: str = "Red Player Won!"
    WINNING_RIGHT_TEXT: str = "Green Player Won!"

    PAUSE_LABEL: str = "Pause"
    PAUSE_RESUME: str = "Press Escape to Resume"
    PAUSE_EXIT: str = "Press C to Exit"
