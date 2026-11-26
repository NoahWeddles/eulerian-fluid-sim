from random import random

import colorsys
import pygame
import math
from typing import *
import numpy as np

def advect(field, x0, y0, x1, y1, sx, sy):
    c1 = field[x0, y0]
    c2 = field[x1, y0]
    c3 = field[x0, y1]
    c4 = field[x1, y1]

    return (1 - sx) * (1 - sy) * c1 + sx * (1 - sy) * c2 + (1 - sx) * sy * c3 + sx * sy * c4

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

    x_idx, y_idx = np.meshgrid(
        np.arange(shape[0], dtype=np.float32),
        np.arange(shape[1], dtype=np.float32),
        indexing="ij",
    )
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #add forces
        #source
        density[30:50, 75:80] = 1
        v[30:50, 70:80] += -50
        #mouse
        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // cell_size
            grid_y = mouse_y // cell_size
            radius = 3
            for i in range(-radius, radius + 1):
                for j in range(-radius, radius + 1):
                    if i**2 + j**2 <= radius**2:
                        x = grid_x + i + 1
                        y = grid_y + j + 1
                        if 0 <= x < shape[0] and 0 <= y < shape[1]:
                            density[x, y] = 0.5
                            mouse_dx, mouse_dy = pygame.mouse.get_rel()
                            u[x, y] += mouse_dx * 200
                            v[x, y] += mouse_dy * 200
        #density decay
        density *= 0.99

        #advect
        x_source = x_idx - u * dt
        y_source = y_idx - v * dt
        
        x_source = np.clip(x_source, 0, grid_cols + 1.999)
        y_source = np.clip(y_source, 0, grid_rows + 1.999)

        x0 = np.floor(x_source)
        y0 = np.floor(y_source)

        sx = x_source - x0
        sy = y_source - y0

        x0 = x0.astype(np.int32)
        y0 = y0.astype(np.int32)

        x1 = np.clip(x0 + 1, 0, grid_cols + 1)
        y1 = np.clip(y0 + 1, 0, grid_rows + 1)

        density[1:-1, 1:-1] = advect(density, x0, y0, x1, y1, sx, sy)[1:-1, 1:-1]
        u[1:-1, 1:-1] = advect(u, x0, y0, x1, y1, sx, sy)[1:-1, 1:-1]
        v[1:-1, 1:-1] = advect(v, x0, y0, x1, y1, sx, sy)[1:-1, 1:-1]

        #projection
        divergence = (u[2:, 1:-1] - u[:-2, 1:-1] + v[1:-1, 2:] - v[1:-1, :-2]) * 0.5

        #jacobi iteration
        for _ in range(50):
            pressure[1:-1, 1:-1] = (pressure[2:, 1:-1] + pressure[:-2, 1:-1] + pressure[1:-1, 2:] + pressure[1:-1, :-2] - divergence) * 0.25
            #enforce boundary conditions
            pressure[0, :] = pressure[1, :]
            pressure[-1, :] = pressure[-2, :]
            pressure[:, 0] = pressure[:, 1]
            pressure[:, -1] = pressure[:, -2]
        #subtract pressure gradient
        u[1:-1, 1:-1] -= (pressure[2:, 1:-1] - pressure[:-2, 1:-1]) * 0.5
        v[1:-1, 1:-1] -= (pressure[1:-1, 2:] - pressure[1:-1, :-2]) * 0.5



        screen.fill((30, 30, 40))

        for j in range(grid_rows):
            for i in range(grid_cols):
                rect = pygame.Rect(
                    j * cell_size, i * cell_size, cell_size, cell_size
                )
                #density is 0-1
                d = density[j+1][i+1]

                h = (1 - d) * 0.66  # 0.66 is blue, 0 is red
                r, g, b = colorsys.hsv_to_rgb(h, 1, 1)

                pygame.draw.rect(screen, (round(r * 255), round(g * 255), round(b * 255)), rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


