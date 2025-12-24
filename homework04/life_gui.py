import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.paused = False

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                x = col * self.cell_size
                y = row * self.cell_size
                cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                if self.life.curr_generation[row][col] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")
                pygame.draw.rect(self.screen, color, cell_rect)

    def run(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.paused = not self.paused
            if not self.paused and self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.life.step()
            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == "__main__":
    from life import GameOfLife

    game = GameOfLife(size=(20, 30), randomize=True)
    gui = GUI(game)
    gui.run()
