import numpy as np

from automata import CellAutomata
import visualizer as vis


def main():
    nAgents = 500
    fieldSize = np.array((100, 100))

    choice = input("Только анимация? (+/-): ")
    if choice == '-':
        nIters = startModeling(nAgents, fieldSize)
        print("Итоговое число итераций:", nIters)
        show('data.npz')
    else:
        show('data.npz')

    return 0


def startModeling(n_agents: int, field_size: np.ndarray, iters: int = None) -> int:
    """Анимированное моделирование эволюции клеточного автомата.

    :param iters: кол-во итераций эволюции клеточного автомата.
    :param n_agents: кол-во агентов с каждой стороны.
    :param field_size: размер клеточного автомата.
    :return: Итоговое количесво итераций.
    """
    print("Идёт моделирование...")

    datafile = 'data.npz'
    ca = CellAutomata(n_agents=n_agents, size=field_size)
    res = [ca.getCells()]

    if iters:
        for _ in range(iters):
            if not ca.update():         # остались клетки одной стороны
                break
            res.append(ca.getCells())
    else:
        while ca.update():              # моделировать до победного...
            res.append(ca.getCells())
    np.savez(datafile, *np.array(res))

    return ca.totalIters


def show(datafile: str):
    data = np.load(datafile)
    dataList = [d for d in data.values()]

    v = vis.Visualizer()
    v.show(dataList, len(dataList))


if __name__ == '__main__':
    main()
