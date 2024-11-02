import pygame
import math
from queue import PriorityQueue
from tkinter import messagebox, Tk


WIDTH = 600
size = (WIDTH, WIDTH)
WIN = pygame.display.set_mode(size)
pygame.init()
pygame.display.set_caption("Astar Algorithm")

LavenderBlue = (150, 184, 255) # lavender blue
GREEN = (170, 184, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (204, 247, 255)  # (179,229,255) # light cyan
BLACK = (0, 0, 0)
PURPLE = (24,92,144)
SGREEN = (0, 255, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = CYAN  # all nodes/spots are white initially
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # Utility boolean functions
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == LavenderBlue

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == SGREEN

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = CYAN

    # Utility functions
    def make_closed(self):
        self.color = LavenderBlue

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = SGREEN

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # main stuff
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])


    def __lt__(self, other):
        return False


# heuristic function
def h(n1, n2):
    x1, y1 = n1
    x2, y2 = n2
    result = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)  # It includes diagonal path
    # result = abs(x1 - x2) + abs(y1 - y2)  # Ignores diagonal path
    return result

def path(came_from, current, draw):  # reconstructs path
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    # draw is a lambda function
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    came_from = {}

    while not open_set.empty():
        # for event in pygame.event.get():
        #     if event.key == pygame.K_x:
        #         pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows  # finding the size of a spot
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    # For drawing the lines to make it look like a grid
    # for i in range(rows):
    #     pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    # for j in range(rows):#####  ###
    #     pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(CYAN)  # fills the screen white

    # drawing the colours of boxes
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)  # draws the grid lines
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

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

            if pygame.mouse.get_pressed()[0]: # When left mouse button is clicked
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

            elif pygame.mouse.get_pressed()[2]: # When right mouse button is clicked
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()  # resets the clicked spot
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # Runs the algorithm
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    foundPath = algorithm(lambda:draw(win, grid, ROWS, width), grid, start, end)
                    if not foundPath:
                        Tk().wm_withdraw()
                        messagebox.showinfo("Path not found", "There was no solution")

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

# gap == width // rows
if __name__ == '__main__':

    main(WIN, WIDTH)

