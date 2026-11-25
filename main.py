import pygame
import math
from typing import *

def main():
    pygame.init()

    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Simple Grid")
    clock = pygame.time.Clock()

    grid_cols = 80
    grid_rows = 80
    cell_size = 400 // grid_cols

    cell_colors: list[list[tuple]] = [[(255,255,255)for _ in range(grid_cols)] for _ in range(grid_rows)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(event.pos)
                    i = math.floor(event.pos[0]/cell_size)
                    j = math.floor(event.pos[1]/cell_size)
                    print("i: " + str(i) + ", j: " + str(j))
                    cell_colors[j][i] = (255,0,0)

        screen.fill((30, 30, 40))

        for i in range(grid_rows):
            for j in range(grid_cols):
                rect = pygame.Rect(
                    j * cell_size, i * cell_size, cell_size, cell_size
                )
                pygame.draw.rect(screen, cell_colors[i][j], rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
