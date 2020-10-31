from typing import List, Tuple
import numpy as np

from agent import Agent


class CellAutomata:
    """Класс клеточного автомата."""

    def __init__(self, n_agents: int = 1, size: np.ndarray = np.array((100, 100))):
        self._iter = 0

        self._cells = self._initCells(size+2)
        self._fillCells(n_agents, 1)
        self._fillCells(n_agents, 2)

        self._agents = self._initAgents()

    def _initCells(self, size: np.ndarray) -> np.ndarray:
        return np.zeros(size, dtype='int')

    def _fillCells(self, n_agents: int, val: int):
        for _ in range(n_agents):
            i = np.random.randint(1, self._cells.shape[0] - 2)
            j = np.random.randint(1, self._cells.shape[1] - 2)
            self._cells[i, j] = val

    def _initAgents(self) -> List[Agent]:
        agents = []
        for i in range(1, self._cells.shape[0] - 1):
            for j in range(1, self._cells.shape[1] - 1):
                val = self._cells[i, j]
                if val == 1:
                    agents.append(Agent(self, 'A', val, np.array((i, j))))
                elif val == 2:
                    agents.append(Agent(self, 'B', val, np.array((i, j))))
        return agents

    def update(self) -> bool:
        """Функция эволюции клеточного автомата.

        :return: Флаг *True*, если есть клетки-противники или *False*, если остались клетки одной стороны.
        """
        vals = np.array([a.value for a in self._agents])
        if not np.all(vals == np.full_like(vals, self._agents[0].value)):
            agents = self._agents.copy()
            np.random.shuffle(agents)
            for agent in agents:
                agent.move()
                self._updateCells()
            self._iter += 1
            return True
        return False

    def _updateCells(self):
        deads = []
        self._cells = np.zeros_like(self._cells)
        for a in self._agents:
            if a.isAlive:
                self._cells[a.position[0], a.position[1]] = a.value
            else:
                self._cells[a.position[0], a.position[1]] = 0
                deads.append(a)
        for dead in deads:
            self._agents.remove(dead)

    def isEmptyNeighborhood(self, pos: np.ndarray) -> bool:
        """Проверить, пуста ли окрестность Мура для клетки с позицией pos.

        :param pos: позиция рассматриваемой клетки.
        """
        i, j = pos
        if any(self._cells[i-1, j-1:j+2] != 0):
            return False
        if any(self._cells[i+1, j-1:j+2] != 0):
            return False
        if self._cells[i, j-1] != 0 or self._cells[i, j+1] != 0:
            return False
        return True

    def isFriendlyNeighborhood(self, val: int, pos: np.ndarray) -> bool:
        """Проверить, только ли "союзники" в окрестности Мура для клетки с позицией pos.

        :param val: идентификатор "союзников" (должно быть таким же, как у вызвавшего экземпляра).
        :param pos: позиция рассматриваемой клетки.
        """
        for x in range(-1, 2):
            for y in range(-1, 2):
                if self._cells[pos[0]+x, pos[1]+y] != val and self._cells[pos[0]+x, pos[1]+y] != 0:
                    return False
        return True

    def isEmptyCell(self, pos: np.ndarray) -> bool:
        """Проверить, является ли клетка в позиции pos пустой.

        :param pos: позиция интересующей клетки.
        :return: Флаг - так или не так.
        """
        if self._cells[pos[0], pos[1]] == 0:
            return True
        return False

    def isFriendlyCell(self, val: int, pos: np.ndarray) -> bool:
        """Проверить, что клетка в позиции pos дружественная.

        :param val: идентификатор "союзников" (должно быть таким же, как у вызвавшего экземпляра).
        :param pos: позиция интересующей клетки.
        :return: Флаг - так или не так.
        """
        if self._cells[pos[0], pos[1]] == val:
            return True
        return False

    def calcFriendsEnemies(self, val: int, pos: np.ndarray) -> Tuple[int, int]:
        fr, en = 0, 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if self._cells[pos[0]+x, pos[1]+y] != val and self._cells[pos[0]+x, pos[1]+y] != 0:
                    en += 1
                elif self._cells[pos[0]+x, pos[1]+y] == val:
                    fr += 1
        return fr - 1, en

    @property
    def size(self) -> Tuple[int, int]:
        """Размер клеточного автомата."""
        return self._cells.shape

    @property
    def totalIters(self) -> int:
        return self._iter

    def getCells(self) -> np.ndarray:
        """Текущее состояние клеточного автомата."""
        return self._cells
