from typing import List, Tuple
from pygame.locals import *
import pygame
import numpy as np


WHITE = 255, 255, 255
RED = 255, 0, 0
BLUE = 0, 0, 255
GREY = 150, 150, 150
BLACK = 0, 0, 0


class Visualizer:
    def __init__(self, win_size: Tuple[int, int] = (900, 900)):
        self._winSize = win_size
        self.lx, self.ly = None, None
        self.xmargin, self.ymargin = None, None

        self.FPS = 25
        self.fpsClock = pygame.time.Clock()

        # PyGame
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode(self._winSize)
        pygame.display.set_caption("Cellular Automata")

    def show(self, data: List[np.ndarray], iters: int):
        i = 0
        isRun = True
        while True:
            self.fpsClock.tick(self.FPS)
            self.drawField(data[i])

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    isRun = False
            if not isRun:
                break
            pygame.display.update()
            if i < iters:
                i += 1

    def drawField(self, data: np.ndarray):
        self.DISPLAYSURF.fill(WHITE)

        self.lx = int(self._winSize[0] / data.shape[1])
        self.ly = int(self._winSize[1] / data.shape[0])
        self.xmargin = int(self._winSize[0] - data.shape[1] * self.lx) // 2
        self.ymargin = int(self._winSize[1] - data.shape[0] * self.ly) // 2

        rects = []
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                width = 0
                if data[i, j] == 1:
                    color = BLUE
                elif data[i, j] == 2:
                    color = RED
                else:
                    color = GREY
                    width = 1
                rects.append(((j * self.lx + self.xmargin, i * self.ly + self.ymargin, self.lx, self.ly), color, width))

        for rect in rects:
            pygame.draw.rect(self.DISPLAYSURF, rect[1], rect[0], rect[2])
