import pygame
from ball import Ball
from config import Config
from ezyapi.mysql_connection import DatabaseConnexionError
from paddle import Paddle
from score import Scores
from error import Error

import ezyapi.game_manager as manager


class Pong:
    def __init__(self, config: Config):
        self.config = config
        self.window = pygame.display.set_mode((self.config.WIN_WIDTH, self.config.WIN_HEIGHT))
        pygame.display.set_caption(self.config.TITLE)
        try:
            pygame.display.set_icon(pygame.image.load("pong x32.png"))
        except:
            pass

        self.run = self.playing = True
        self.clock = pygame.time.Clock()

        self.left_paddle = Paddle(10, self.config.WIN_HEIGHT // 2 - self.config.LEFT_PADDLE_HEIGHT // 2, True, config)
        self.right_paddle = Paddle(self.config.WIN_WIDTH - 10 - self.config.RIGHT_PADDLE_WIDTH, self.config.WIN_HEIGHT // 2
                                   - self.config.RIGHT_PADDLE_HEIGHT // 2, False, config)
        self.ball = Ball(self.config.WIN_WIDTH // 2, self.config.WIN_HEIGHT // 2, self.config)

        self.left_score = 0
        self.right_score = 0

    def start_loop(self):
        escape_pressed = False

        while self.run:
            self.clock.tick(self.config.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break

            if not self.run:
                break

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                escape_pressed = True
            elif escape_pressed:
                escape_pressed = False
                self.playing = not self.playing

            if self.playing:
                self.draw()

                self.ball.update_velocity()
                self.left_paddle.update_velocity()
                self.right_paddle.update_velocity()

                self.handle_paddle_movement(keys)

                self.ball.move()
                self.handle_collision()

                if self.ball.x < 0:
                    self.right_score += 1
                    self.ball.reset()
                    self.left_paddle.reset()
                    self.right_paddle.reset()
                elif self.ball.x > self.config.WIN_WIDTH:
                    self.left_score += 1
                    self.ball.reset()
                    self.left_paddle.reset()
                    self.right_paddle.reset()

                won, win_text = False, None
                if self.left_score >= self.config.WINNING_SCORE:
                    won = True
                    win_text = self.config.WINNING_LEFT_TEXT
                elif self.right_score >= self.config.WINNING_SCORE:
                    won = True
                    win_text = self.config.WINNING_RIGHT_TEXT

                if won:
                    self.draw()
                    text = self.config.SCORE_FONT.render(win_text, 1, self.config.FOREGROUND)
                    self.window.blit(text, (self.config.WIN_WIDTH // 2 - text.get_width() // 2,
                                            self.config.WIN_HEIGHT // 2 - text.get_height() // 2))
                    pygame.display.update()
                    pygame.time.delay(5000)
                    self.ball.reset()
                    self.left_paddle.reset()
                    self.right_paddle.reset()
                    self.run = False

            else:
                txt_label = self.config.SCORE_FONT.render(self.config.PAUSE_LABEL, 1, self.config.FOREGROUND)
                self.window.blit(txt_label, (self.config.WIN_WIDTH // 2 - txt_label.get_width() // 2,
                                             self.config.WIN_HEIGHT // 4 - txt_label.get_height() // 2))
                txt_resume = self.config.SCORE_FONT.render(self.config.PAUSE_RESUME, 1, self.config.FOREGROUND)
                self.window.blit(txt_resume, (self.config.WIN_WIDTH // 2 - txt_resume.get_width() // 2,
                                              2 * self.config.WIN_HEIGHT // 4 - txt_resume.get_height() // 2))
                txt_exit = self.config.SCORE_FONT.render(self.config.PAUSE_EXIT, 1, self.config.FOREGROUND)
                self.window.blit(txt_exit, (self.config.WIN_WIDTH // 2 - txt_exit.get_width() // 2,
                                            3 * self.config.WIN_HEIGHT // 4 - txt_exit.get_height() // 2))
                pygame.display.update()

                if keys[pygame.K_c]:
                    self.run = False

        pygame.quit()
        scores = Scores(self.right_score, self.left_score)
        if manager.linked() and (self.right_score + self.left_score):
            try:
                manager.start_new_game()
                manager.commit_new_set(self.right_score >= self.left_score, scores.v_total_exp, scores.v_total_gp)
            except manager.AlreadyCommitted as e:
                Error("AlreadyCommitted", str(e) + "\nYou can close now :).")
            except DatabaseConnexionError as e:
                Error("DatabaseConnexionError", str(e) + "\nThe SQL Serveur is potentially down for maintenance...\nWait and Rety Later.\n\nIf you Continue, you will not be able to get rewards and update the ranking.")
            except Exception as e:
                Error(str(type(e))[8:-2], str(e))
        scores.start()

    def draw(self):
        self.window.fill(self.config.BACKGROUND)

        left_score_text = self.config.SCORE_FONT.render(f"{self.left_score}", 1, self.config.FOREGROUND)
        right_score_text = self.config.SCORE_FONT.render(f"{self.right_score}", 1, self.config.FOREGROUND)
        self.window.blit(left_score_text, (self.config.WIN_WIDTH // 4 - left_score_text.get_width() // 2, 20))
        self.window.blit(right_score_text, (self.config.WIN_WIDTH * (3/4) - right_score_text.get_width() // 2, 20))

        self.left_paddle.draw(self.window)
        self.right_paddle.draw(self.window)

        for i in range(self.config.SEPARATOR_AMOUNT * 2 + 1):
            if i % 2:
                continue
            pygame.draw.rect(self.window, self.config.SEPARATOR_COLOR, (
                self.config.WIN_WIDTH // 2 - self.config.SEPARATOR_WIDTH // 2,
                i * (self.config.WIN_HEIGHT - self.config.WIN_HEIGHT // (self.config.SEPARATOR_AMOUNT * 2))
                // (self.config.SEPARATOR_AMOUNT * 2),
                self.config.SEPARATOR_WIDTH,
                (self.config.WIN_HEIGHT - self.config.WIN_HEIGHT // (self.config.SEPARATOR_AMOUNT * 2))
                // (self.config.SEPARATOR_AMOUNT * 2)
            ))

        self.ball.draw(self.window)
        pygame.display.update()

    def handle_paddle_movement(self, keys):
        # if keys[pygame.K_s] and self.left_paddle.y - self.left_paddle.velocity >= 0:
        #     self.left_paddle.move(up=True)
        # if keys[pygame.K_w] and self.left_paddle.y + self.left_paddle.velocity + self.left_paddle.height <= self.config.WIN_HEIGHT:
        #     self.left_paddle.move(up=False)

        if self.ball.y > self.left_paddle.y + self.left_paddle.height / 2:
            self.left_paddle.move(up=False)
        elif self.ball.y < self.left_paddle.y + self.left_paddle.height / 2:
            self.left_paddle.move(up=True)

        if keys[pygame.K_UP] and self.right_paddle.y - self.right_paddle.velocity >= 0:
            self.right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and self.right_paddle.y + self.right_paddle.velocity + self.right_paddle.height <= self.config.WIN_HEIGHT:
            self.right_paddle.move(up=False)

    def handle_collision(self):
        if self.ball.y + self.ball.radius >= self.config.WIN_HEIGHT:
            self.ball.y_vel *= -1
        elif self.ball.y - self.ball.radius <= 0:
            self.ball.y_vel *= -1

        if self.ball.x_vel < 0:
            if self.left_paddle.y <= self.ball.y <= self.left_paddle.y + self.left_paddle.height:
                if self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width:
                    self.ball.x_vel *= -1

                    middle_y = self.left_paddle.y + self.left_paddle.height / 2
                    difference_in_y = middle_y - self.ball.y
                    reduction_factor = (self.left_paddle.height / 2) / self.ball.x_vel
                    y_vel = difference_in_y / reduction_factor
                    self.ball.y_vel = -1 * y_vel

        else:
            if self.right_paddle.y <= self.ball.y <= self.right_paddle.y + self.right_paddle.height:
                if self.ball.x + self.ball.radius >= self.right_paddle.x:
                    self.ball.x_vel *= -1

                    middle_y = self.right_paddle.y + self.right_paddle.height / 2
                    difference_in_y = middle_y - self.ball.y
                    reduction_factor = (self.right_paddle.height / 2) / self.ball.x_vel
                    y_vel = difference_in_y / reduction_factor
                    self.ball.y_vel = y_vel
