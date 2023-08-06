import numpy as _np
from matplotlib import pyplot as _plt


def fetch_data(size, mu, sigma):
    return _np.random.randn(size) * sigma + mu

def load_ex4_data():
    size = 500
    x1 = fetch_data(size, 1, 2)
    y1 = fetch_data(size, 1, 2)
    c1 = _np.full_like(x1, 1)

    x2 = fetch_data(size, 10, 2)
    y2 = fetch_data(size, 10, 2)
    c2 = _np.full_like(x2, 2)

    x3 = fetch_data(size, -8, 1)
    y3 = fetch_data(size, -3, 2)
    c3 = _np.full_like(x2, 3)

    x4 = fetch_data(size, -20, 3)
    y4 = fetch_data(size, 8, 2)
    c4 = _np.full_like(x2, 4)

    x5 = fetch_data(size, -5, 4)
    y5 = fetch_data(size, 12, 4)
    c5 = _np.full_like(x2, 5)

    x6 = fetch_data(size, -20, 2)
    y6 = fetch_data(size, -8, 2)
    c6 = _np.full_like(x2, 6)

    x7 = fetch_data(size, 5, 2)
    y7 = fetch_data(size, -8, 2)
    c7 = _np.full_like(x2, 7)

    x8 = fetch_data(size, -5, 3)
    y8 = fetch_data(size, -20, 3)
    c8 = _np.full_like(x2, 8)

    x = _np.concatenate((x1, x2, x3, x4, x5, x6, x7, x8))
    y = _np.concatenate((y1, y2, y3, y4, y5, y6, y7, y8))
    c = _np.concatenate((c1, c2, c3, c4, c5, c6, c7, c8))
    return _np.vstack((x, y)).T, c

def show_exp4_data(X, y):
    _plt.scatter(X.T[0, :], X.T[1, :], c=y, s=10)
    _plt.show()
