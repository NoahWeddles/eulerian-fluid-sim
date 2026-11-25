from random import random

import pygame
import math
from typing import *
import numpy as np

def main():
    pygame.init()

    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Simple Grid")
    clock = pygame.time.Clock()

    grid_cols = 80
    grid_rows = 80
    cell_size = 400 // grid_cols

    dt = 1/60

    #with border cells
    shape = (grid_cols + 2 , grid_rows + 2)
    u = np.zeros(shape, dtype=np.float32)
    v = np.zeros(shape, dtype=np.float32)
    pressure = np.zeros(shape, dtype=np.float32)
    density = np.zeros(shape, dtype=np.float32)

#change to center 3 cells only
    # density[1:-1, 1:-1] = np.random.rand(grid_cols, grid_rows)
    density[34:45, 34:45] = np.random.rand(11, 11)

    x_idx, y_idx = np.meshgrid(
        np.arange(shape[0], dtype=np.float32),
        np.arange(shape[1], dtype=np.float32),
        indexing="ij",
    )

    u[:] = 10
    v[:] = 10
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #add forces
        
        #advect
        x_source = x_idx - u * dt
        y_source = y_idx - v * dt
        
        x_source = np.clip(x_source, 0, 80.999)
        y_source = np.clip(y_source, 0, 80.999)

        x0 = np.floor(x_source)
        y0 = np.floor(y_source)

        sx = x_source - x0
        sy = y_source - y0

        x0 = x0.astype(np.int32)
        y0 = y0.astype(np.int32)

        x1 = np.clip(x0 + 1, 0, 81)
        y1 = np.clip(y0 + 1, 0, 81)

        c1 = density[x0, y0]
        c2 = density[x1, y0]
        c3 = density[x0, y1]
        c4 = density[x1, y1]

        density = (1 - sx) * (1 - sy) * c1 + sx * (1 - sy) * c2 + (1 - sx) * sy * c3 + sx * sy * c4

        screen.fill((30, 30, 40))

        for j in range(grid_rows):
            for i in range(grid_cols):
                rect = pygame.Rect(
                    j * cell_size, i * cell_size, cell_size, cell_size
                )
                #density is 0-1
                d = density[j+1][i+1]

                pygame.draw.rect(screen, (int(255 * d), int(255 * d), int(255 * d)), rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
