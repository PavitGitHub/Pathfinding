"""
Greedy Best-First Search (GBFS)
Optimality:
Completeness:
Time Complexity:
Space Complexity:
"""

import pygame
from queue import PriorityQueue
from constants import *
from grid import make_grid, draw, get_clicked_pos, reconstruct_path


def heuristic(p1, p2):
    """Manhattan distance heuristic."""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def gbfs(draw_fn, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    visited = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]

        if current == end:
            reconstruct_path(came_from, end, draw_fn)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                h = heuristic(neighbor.get_pos(), end.get_pos())
                count += 1
                open_set.put((h, count, neighbor))
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
                    gbfs(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Greedy Best-First Search Pathfinding")
    main(WIN, WIDTH)