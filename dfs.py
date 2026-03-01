"""
Depth-First Search (DFS)
Optimality:
Completeness:
Time Complexity:
Space Complexity:
"""

import pygame
from constants import *
from grid import make_grid, draw, get_clicked_pos, reconstruct_path


def dfs(draw_fn, grid, start, end):
    stack = [start]
    came_from = {}
    visited = {start}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        if current == end:
            reconstruct_path(came_from, end, draw_fn)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                neighbor.make_open()

        draw_fn()
        if current != start:
            current.make_closed()

    return False


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("DFS Pathfinding")
    main(WIN, WIDTH)