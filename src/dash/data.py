"""
Generate Data
"""


import numpy as np

from src import config


def _get_data():
    dx = np.random.normal(0, config.plot_std, config.plot_n_points * config.plot_n_lines).reshape(
        config.plot_n_points, config.plot_n_lines
    )
    dx[0, :] = 0
    x = np.cumsum(dx, axis=0)
    return x
