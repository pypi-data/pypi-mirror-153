"""
FODGE - Fast Online Dynamic Graph Embedding

The package has 3 main functions:

1. FODGE:

    >>> from FODGE import FODGE
    >>> FODGE(name='catalano', graph_path=".", save_path=".", initial_method="node2vec", dim=128,
    >>>       epsilon=0.04, alpha_exist=0.2, beta=0.7, number=50)

2. link_prediction_1:

    >>> from FODGE import link_prediction_1
    >>> link_prediction_1(name='catalano', graph_path=".", save_path=".", initial_method="node2vec", dim=128,
    >>>                   epsilon=0.04, alpha=0.2, beta=0.7, number=50)

2. link_prediction_2:

    >>> from FODGE import link_prediction_2
    >>> link_prediction_2(name='catalano', graph_path=".", save_path=".", initial_method="node2vec", dim=128,
    >>>                   epsilon=0.04, alpha=0.2, beta=0.7, number=50)
"""

from .evaluation_tasks.temporal_link_prediction import *
from .evaluation_tasks.calculate_non_edges import *
from .evaluation_tasks.linear_regression_link_prediction import *
from .main_functions import link_prediction_1, link_prediction_2
