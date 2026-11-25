import pygame


def main():
    pygame.init()

    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Simple Grid")
    clock = pygame.time.Clock()

    grid_cols = 20
    grid_rows = 20
    cell_size = 400 // grid_cols

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 40))

        for row in range(grid_rows):
            for col in range(grid_cols):
                rect = pygame.Rect(
                    col * cell_size, row * cell_size, cell_size, cell_size
                )
                pygame.draw.rect(screen, (80, 80, 100), rect, 1)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
