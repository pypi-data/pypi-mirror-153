"""
Main functions to run FODGE.
"""
from .evaluation_tasks.temporal_link_prediction import *
from .evaluation_tasks.calculate_non_edges import *
from .evaluation_tasks.linear_regression_link_prediction import *

func = data_loader


def link_prediction_1(name, datasets_path, save_path, non_edges_file=None, initial_method='node2vec', dim=128, epsilon=0.01,
                      alpha=0.2, beta=0.3, number=1000,
                      test_ratio=0.2, file_tags=None):
    if non_edges_file is None:  # create non_edges_file if the user does not give one
        non_edges_file = create_non_edges_file(name, datasets_path, func)
        path_non_edges_file = os.path.join("evaluation_tasks", non_edges_file)
    else:
        path_non_edges_file = os.path.join("evaluation_tasks", non_edges_file)
    TemporalLinkPrediction1(name, datasets_path, save_path, func=func,
                            initial_method=initial_method, dim=dim, epsilon=epsilon,
                            alpha_exist=alpha, beta=beta, number=number, test_ratio=test_ratio,
                            non_edges_file=path_non_edges_file, file_tags=file_tags)


def link_prediction_2(name, datasets_path, save_path, initial_method='node2vec', dim=128, epsilon=0.01,
                      alpha=0.2, beta=0.3, number=1000,
                      test_ratio=0.2, val_ratio=0.3, file_tags=None):
    TemporalLinkPrediction2(name, save_path, datasets_path, func=func,
                            initial_method=initial_method, dim=dim, epsilon=epsilon,
                            alpha_exist=alpha, beta=beta, number=number, test_ratio=test_ratio,
                            val_ratio=val_ratio, file_tags=file_tags)
