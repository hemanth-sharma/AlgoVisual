import pygame
import sys
import random, math

from collections import deque
from tkinter import messagebox, Tk

screen_size = (width, height) = 640, 480
pygame.init()

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

cols, rows = 64, 48

w = width//cols
h = height//rows

grid = []
queue, visited = deque(), []
path = []

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.isVisited = False

        if(i + j) % 7 == 0:
            self.wall == True






