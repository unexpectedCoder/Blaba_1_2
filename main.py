from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random


class Agent:
    mur = 8
    dirs = {
        'n': (-1, 0), 's': (1, 0), 'w': (0, -1), 'e': (0, 1),
        'nw': (-1, -1), 'ne': (-1, 1), 'se': (1, 1), 'sw': (1, -1)
    }

    def __init__(self, parent: 'CellAutomata', name: str, val: int, pos: np.ndarray):
        self._parent = parent
        self.name = name
        self.value = val
        self.position = pos.copy()
        self.isAlive = True

    def __repr__(self):
        return f"Agent {self.name}: val={self.value}\tpos={self.position}"

    def __eq__(self, other: 'Agent'):
        if self is other:
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

    def move(self):
        if self._parent.isEmptyNeighborhood(self.position):
            self._moveEmptyCase()
        elif self._parent.isFriendlyNeighborhood(self.value, self.position):
            self._moveFriendlyCase()

    def _moveEmptyCase(self):
        for _ in range(self.mur):
            key = random.choice(tuple(self.dirs.keys()))
            d = np.array(self.dirs[key])
            d = self._sideCells(d)
            if self._parent.isEmptyCell(self.position + d):
                self.position += d
                break

    def _sideCells(self, d: np.ndarray) -> np.ndarray:
        if (self.position[0] < 2 and d[0] == -1) or (self.position[0] >= self._parent.size[0] - 2 and d[0] == 1):
            d[0] = -d[0]
        if (self.position[1] < 2 and d[1] == -1) or (self.position[1] >= self._parent.size[1] - 2 and d[1] == 1):
            d[1] = -d[1]
        return d

    def _moveFriendlyCase(self):
        for _ in range(self.mur):
            key = random.choice(tuple(self.dirs.keys()))
            d = np.array(self.dirs[key])
            d = self._sideCells(d)

            if self._parent.isEmptyCell(self.position + d):
                self.position += d
                break


class CellAutomata:
    def __init__(self, n_agents: int = 1, size: np.ndarray = np.array((100, 100))):
        random.seed(1251)
        self._cells = self._initCells(size+2)
        self._fillCells(n_agents, 1)
        self._fillCells(n_agents, 2)

        self._agents = self._initAgents()

    def _initCells(self, size: np.ndarray) -> np.ndarray:
        return np.zeros(size, dtype='int')

    def _fillCells(self, n_agents: int, val: int):
        for _ in range(n_agents):
            i = random.randint(1, self._cells.shape[0] - 2)
            j = random.randint(1, self._cells.shape[1] - 2)
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

    def update(self, iters: int = 1):
        for _ in range(iters):
            for agent in self._agents:
                agent.move()
                self._updateCells()

    def isEmptyNeighborhood(self, pos: np.ndarray) -> bool:
        i, j = pos
        if any(self._cells[i-1, j-1:j+2] != 0):
            return False
        if any(self._cells[i+1, j-1:j+2] != 0):
            return False
        if self._cells[i, j-1] != 0 or self._cells[i, j+1] != 0:
            return False
        return True

    def isFriendlyNeighborhood(self, val: int, pos: np.ndarray) -> bool:
        for x in range(-1, 2):
            for y in range(-1, 2):
                if self._cells[pos[0]+x, pos[1]+y] != val and self._cells[pos[0]+x, pos[1]+y] != 0:
                    return False
        return True

    def _updateCells(self):
        self._cells = np.zeros_like(self._cells)
        for a in self._agents:
            self._cells[a.position[0], a.position[1]] = a.value

    def show(self, i: int = 0, save=False):
        fig = plt.figure(f'Результат итерации #{i}', figsize=(10, 8))
        ax = fig.add_subplot(1, 1, 1)
        p = ax.matshow(self._cells, cmap='jet')
        plt.colorbar(p)
        plt.title(f'Итерация #{i}')
        if save:
            plt.savefig(f'plot_{i}.png')
        plt.show()

    def isEmptyCell(self, pos: np.ndarray) -> bool:
        if self._cells[pos[0], pos[1]] == 0:
            return True
        return False

    def isFriendlyCell(self, val: int, pos: np.ndarray) -> bool:
        if self._cells[pos[0], pos[1]] == val:
            return True
        return False

    def getCells(self) -> np.ndarray:
        return self._cells

    @property
    def size(self) -> Tuple[int, int]:
        return self._cells.shape


def main():
    iters = 200
    agents = 100

    # Для требующихся промежуточных графиков
    # ca = CellAutomata(n_agents=agents)
    # ca.show(save=True)
    # ca.update(iters=iters//10)
    # ca.show(iters//10, save=True)
    # ca.update(iters=iters//2)
    # ca.show(iters//2, save=True)
    # ca.update(iters=iters)
    # ca.show(iters, save=True)

    datafile = 'data.npz'
    ca = CellAutomata(n_agents=agents)
    res = [ca.getCells()]
    for _ in range(iters):
        ca.update()
        res.append(ca.getCells())
    np.savez(datafile, *np.array(res))

    showAnimated(datafile, iters)

    return 0


def showAnimated(datafile, iters: int):
    """Показать анимацию эволюции клеточного автомата.
    :param datafile: имя файла с данными numpy.
    :param iters: количество проведенных итераций эволюции клеточного автомата (кол-во матриц в файле).
    """
    data = np.load(datafile)
    fig = plt.figure('Анимация', figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ani = animation.FuncAnimation(fig, animate, fargs=(ax, data, iters), interval=300)
    plt.show()


def animate(i, ax, data, iters: int):
    """Функция анимации."""
    if i < iters:
        ax.clear()
        d = data[f'arr_{i}']        # arr_0, arr_1 и т.д. - это ключи по-умолчанию для numpy.savez()
        ax.matshow(d, cmap='jet')
        plt.title(f'Итерация #{i + 1}')
    else:
        print("Усё")


if __name__ == '__main__':
    main()
