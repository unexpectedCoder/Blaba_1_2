import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from automata import CellAutomata


def main():
    iters = 500
    nAgents = 100
    size = np.array((100, 100))

    createPicsForReport(iters, nAgents, size)
    computingWithAnimation(iters, nAgents, size)

    return 0


def createPicsForReport(iters: int, n_agents: int, size=np.array((100, 100))):
    """Для требующихся в отчете 4-х графиков (начальное и конечное состояние + 2 промежуточных состояния).

    :param iters: кол-во итераций эволюции клеточного автомата.
    :param n_agents: кол-во агентов с каждой стороны.
    :param size: размер клеточного автомата.
    """
    ca = CellAutomata(n_agents=n_agents, size=size)
    ca.show(save=True)
    for _ in range(0, iters // 10):
        ca.update()
    ca.show(save=True)
    for _ in range(0, iters // 2 - iters // 10):
        ca.update()
    ca.show(save=True)
    for _ in range(0, iters // 2):
        ca.update()
    ca.show(save=True)


def computingWithAnimation(iters: int, n_agents: int, size=np.array((100, 100))):
    """Анимированное моделирование эволюции клеточного автомата.

    :param iters: кол-во итераций эволюции клеточного автомата.
    :param n_agents: кол-во агентов с каждой стороны.
    :param size: размер клеточного автомата.
    """
    datafile = 'data.npz'
    ca = CellAutomata(n_agents=n_agents, size=size)
    res = [ca.getCells()]

    for _ in range(iters):
        ca.update()
        res.append(ca.getCells())
    np.savez(datafile, *np.array(res))

    showAnimated(datafile, iters)


def showAnimated(datafile, iters: int):
    """Показать анимацию эволюции клеточного автомата.

    :param datafile: имя файла с данными numpy.
    :param iters: количество проведенных итераций эволюции клеточного автомата (кол-во матриц в файле).
    """
    data = np.load(datafile)
    fig = plt.figure('Анимация', figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ani = animation.FuncAnimation(fig, animate, fargs=(ax, data, iters), interval=100)
    plt.show()


def animate(i, ax, data, iters: int):
    """Функция анимации."""
    if i < iters:
        ax.clear()
        d = data[f'arr_{i}']        # arr_0, arr_1 и т.д. - это ключи по-умолчанию для numpy.savez()
        ax.matshow(d, cmap='jet')
        plt.title(f'Итерация #{i+1}')
    return


if __name__ == '__main__':
    main()
