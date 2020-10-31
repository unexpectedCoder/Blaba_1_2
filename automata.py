from typing import List, Tuple
import numpy as np

from agent import Agent


class CellAutomata:
    """Класс клеточного автомата."""

    def __init__(self, n_agents: int, field_size: np.ndarray):
        self._iter = 0
        self._cells = self._initCells(field_size+2)
        self._initAgents(n_agents)
        self._updateCells()

    def _initCells(self, size: np.ndarray) -> np.ndarray:
        return np.zeros(size, dtype='int')

    def _initAgents(self, n_agents: int):
        self._agents = []
        positions = self._genPositions(n_agents)
        for pos1, pos2 in zip(positions[::2], positions[1::2]):
            self._agents.append(Agent(self, 'A', 1, np.array(pos1)))
            self._agents.append(Agent(self, 'B', 2, np.array(pos2)))

    def _genPositions(self, n_agents: int) -> List[List[int]]:
        positions = []
        for i in range(1, self._cells.shape[0] - 1):
            for j in range(1, self._cells.shape[1] - 1):
                positions.append([i, j])
        positions = np.array(positions)
        np.random.shuffle(positions)
        return positions[:2*n_agents + 1]

    def update(self) -> bool:
        """Функция эволюции клеточного автомата.

        :return: Флаг *True*, если есть клетки-противники или *False*, если остались клетки одной стороны.
        """
        vals = np.array([a.value for a in self._agents])
        if not np.all(vals == np.full_like(vals, self._agents[0].value)):
            for agent in self._agents:
                agent.update()
                self._updateAgentsList()
                self._updateCells()
            self._iter += 1
            return True
        return False

    def _updateAgentsList(self):
        for a in self._agents:
            if not a.isAlive:
                self._agents.remove(a)

    def _updateCells(self):
        self._cells = np.zeros_like(self._cells)
        for a in self._agents:
            self._cells[a.position[0], a.position[1]] = a.value

    def isEmptyNeighborhood(self, pos: np.ndarray) -> bool:
        """Проверить, пуста ли окрестность Мура для клетки с позицией pos.

        :param pos: позиция рассматриваемой клетки.
        """
        i, j = pos
        if np.any(self._cells[i-1, j-1:j+2] != 0):
            return False
        if np.any(self._cells[i+1, j-1:j+2] != 0):
            return False
        if self._cells[i, j-1] != 0 or self._cells[i, j+1] != 0:
            return False
        return True

    def isFriendlyNeighborhood(self, val: int, pos: np.ndarray) -> bool:
        """Проверить, только ли "союзники" в окрестности Мура для клетки с позицией pos.

        :param val: идентификатор "союзников" (должно быть таким же, как у вызвавшего экземпляра).
        :param pos: позиция рассматриваемой клетки.
        :return: Флаг - так или не так.
        """
        sub = self._cells[pos[0]-1:pos[0]+2, pos[1]-1:pos[1]+2]
        if np.any(sub[sub != val] != 0):
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
        sub = self._cells[pos[0] - 1:pos[0] + 2, pos[1] - 1:pos[1] + 2]
        friends = np.sum(sub == val) - 1
        enemies = 8 - friends - np.sum(sub == 0)
        return friends, enemies

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

    def getAgents(self) -> List[Agent]:
        return self._agents
