from typing import Union
import numpy as np
import random


class Agent:
    mur = 8
    dirs = {
        'n': (-1, 0), 's': (1, 0), 'w': (0, -1), 'e': (0, 1),
        'nw': (-1, -1), 'ne': (-1, 1), 'se': (1, 1), 'sw': (1, -1)
    }

    def __init__(self, parent, name: str, val: int, pos: np.ndarray):
        self._parent = parent
        self.name = name
        self.value = val
        self.position = pos.copy()
        self.isAlive = True

    def __repr__(self):
        return f"Agent {self.name}: val={self.value}\tpos={self.position}"

    def __eq__(self, other: Union['Agent', np.ndarray]):
        if self is other:
            return True
        if isinstance(other, np.ndarray):
            if all(self.position == other):
                return True
        if all(self.position == other.position):
            return True
        return False

    @property
    def isAlive(self) -> bool:
        return self._isAlive

    @isAlive.setter
    def isAlive(self, flag: bool):
        self._isAlive = flag

    @property
    def position(self) -> np.ndarray:
        """Текущая позиция агента на клеточном поле."""
        return self._pos

    @position.setter
    def position(self, pos):
        if not isinstance(pos, np.ndarray):
            self._pos = np.array(pos)
        else:
            self._pos = pos.copy()

    @property
    def value(self) -> int:
        """Значение, которое присваивается клетке с агентом с данным именем."""
        return self._val

    @value.setter
    def value(self, val: int):
        self._val = val

    def update(self):
        """Обновить состояние агента (клетки)."""
        if self._parent.isEmptyNeighborhood(self.position):
            self._updatePosition()
        elif self._parent.isFriendlyNeighborhood(self.value, self.position):
            self._updatePosition()
        else:
            friends, enemies = self._parent.calcFriendsEnemies(self.value, self.position)
            if friends == 0 and enemies == 1:
                self.isAlive = np.random.choice((True, False))
            elif enemies > friends:
                self.isAlive = False

    def _updatePosition(self):
        for _ in range(self.mur):
            key = random.choice(tuple(self.dirs.keys()))
            d = np.array(self.dirs[key])
            self._sideCellCase(d)
            if self._parent.isEmptyCell(self.position + d):
                self.position += d
                break

    def _sideCellCase(self, d: np.ndarray):
        if (self.position[0] < 2 and d[0] == -1) or (self.position[0] >= self._parent.size[0] - 2 and d[0] == 1):
            d[0] = -d[0]
        if (self.position[1] < 2 and d[1] == -1) or (self.position[1] >= self._parent.size[1] - 2 and d[1] == 1):
            d[1] = -d[1]
