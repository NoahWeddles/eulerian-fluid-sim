from random import random
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

#1
def density_to_rgb(d):
    d = np.clip(d, 0.0, 1.0)
    h6 = (1.0 - d) * 0.66 * 6.0
    r = np.clip(np.abs(h6 - 3.0) - 1.0, 0.0, 1.0)
    g = np.clip(2.0 - np.abs(h6 - 2.0), 0.0, 1.0)
    b = np.clip(2.0 - np.abs(h6 - 4.0), 0.0, 1.0)
    return (np.stack([r, g, b], axis=-1) * 255).astype(np.uint8)
#2
def density_to_white(d):
    d = np.clip(d, 0.0, 1.0)
    return (np.stack([d, d, d], axis=-1) * 255).astype(np.uint8)
#3
def pressure_to_rgb(p):
    p = np.clip(p, -1.0, 1.0)
    r = np.clip(p, 0.0, 1.0)
    g = np.clip(1.0 - np.abs(p), 0.0, 1.0)
    b = np.clip(-p, 0.0, 1.0)
    return (np.stack([r, g, b], axis=-1) * 255).astype(np.uint8)
#4
def velocity_to_rgb(u, v):
    mag = np.sqrt(u**2 + v**2)
    angle = np.arctan2(v, u) / (2 * np.pi) + 0.5
    r = np.clip(np.abs(angle - 0.5) * 2, 0.0, 1.0)
    g = np.clip(1.0 - np.abs(angle - 0.25) * 4, 0.0, 1.0)
    b = np.clip(1.0 - np.abs(angle - 0.75) * 4, 0.0, 1.0)
    return (np.stack([r, g, b], axis=-1) * (mag[..., None] / np.max(mag)) * 255).astype(np.uint8)



def main():
    pygame.init()

    view_mode = 1

    gravity = False

    grid_cols = 80
    grid_rows = 80
    cell_size = 1000 // grid_cols

    screen = pygame.display.set_mode((grid_cols*cell_size, grid_rows * cell_size))
    pygame.display.set_caption("Eulerian Fluid Simulation")
    clock = pygame.time.Clock()

    dt = 1/30

    #with border cells
    shape = (grid_cols + 2 , grid_rows + 2)
    u = np.zeros(shape, dtype=np.float32)
    v = np.zeros(shape, dtype=np.float32)
    pressure = np.zeros(shape, dtype=np.float32)
    density = np.zeros(shape, dtype=np.float32)
    solid = np.zeros(shape, dtype=np.bool)

    x_idx, y_idx = np.meshgrid(
        np.arange(shape[0], dtype=np.float32),
        np.arange(shape[1], dtype=np.float32),
        indexing="ij",
    )

    source_width = 10
    source_height = 5

    source_offset_x = 10
    source_offset_y = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    view_mode = 1
                elif event.key == pygame.K_2:
                    view_mode = 2
                elif event.key == pygame.K_3:
                    view_mode = 3
                elif event.key == pygame.K_4:
                    view_mode = 4

                elif event.key == pygame.K_RIGHT:
                    source_offset_x += 10
                elif event.key == pygame.K_LEFT:
                    source_offset_x -= 10
                elif event.key == pygame.K_UP:
                    source_offset_y -= 10
                elif event.key == pygame.K_DOWN:
                    source_offset_y += 10

                elif event.key == pygame.K_g:
                    gravity = not gravity

        #add forces
        #gravity
        if gravity:
            v[1:-1, 1:-1] += 200 * dt    
        #source


        mid_point_x = grid_cols//2 + source_offset_x

        left_x = mid_point_x-(source_width//2)
        right_x = mid_point_x+(source_width//2)

        top_point_y = grid_rows - source_height + source_offset_y
        bottom_point_y = grid_rows+1 + source_offset_y

        density[left_x:right_x, top_point_y:bottom_point_y] = 1
        v[left_x:right_x, top_point_y:bottom_point_y] += -50

        # v[30:50, 1:10] += 50
        # density[30:50, 1:10] = 1
        #mouse
        mouse_dx, mouse_dy = pygame.mouse.get_rel()

        if pygame.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // cell_size
            grid_y = mouse_y // cell_size
            radius = 4
            for i in range(-radius, radius + 1):
                for j in range(-radius, radius + 1):
                    if i**2 + j**2 <= radius**2:
                        x = grid_x + i + 1
                        y = grid_y + j + 1
                        if 1 <= x < shape[0] - 1 and 1 <= y < shape[1] - 1:
                            # density[x, y] = 0.5
                            u[x, y] += mouse_dx * 10
                            v[x, y] += mouse_dy * 10
        #density decay
        density *= 0.999

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

        #enforce boundary conditions
        u[0, :] = 0
        u[-1, :] = 0
        u[:, 0] = 0
        u[:, -1] = 0
        v[0, :] = 0
        v[-1, :] = 0
        v[:, 0] = 0
        v[:, -1] = 0
        

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

        if view_mode == 1:
            rgb = density_to_rgb(density[1:-1, 1:-1])
        elif view_mode == 2:
            rgb = density_to_white(density[1:-1, 1:-1])
        elif view_mode == 3:
            rgb = pressure_to_rgb(pressure[1:-1, 1:-1])
        elif view_mode == 4:
            rgb = velocity_to_rgb(u[1:-1, 1:-1], v[1:-1, 1:-1])
        else:
            rgb = density_to_rgb(density[1:-1, 1:-1])

        small = pygame.surfarray.make_surface(rgb)
        screen.blit(pygame.transform.scale(small, screen.get_size()), (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


