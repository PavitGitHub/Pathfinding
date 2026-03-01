"""
Dijkstra's Algorithm
Optimality:
Completeness:
Time Complexity:
Space Complexity:
"""

import pygame
from queue import PriorityQueue
from constants import *
from grid import make_grid, draw, get_clicked_pos, reconstruct_path


def dijkstra(draw_fn, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    dist = {spot: float("inf") for row in grid for spot in row}
    dist[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_dist, _, current = open_set.get()
        open_set_hash.discard(current)

        if current == end:
            reconstruct_path(came_from, end, draw_fn)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            new_dist = dist[current] + 1
            if new_dist < dist[neighbor]:
                came_from[neighbor] = current
                dist[neighbor] = new_dist
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((new_dist, count, neighbor))
                    open_set_hash.add(neighbor)
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
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Dijkstra's Pathfinding")
    main(WIN, WIDTH)