from sklearn.linear_model import LinearRegression
from data.preparation import prepare_data
import baselines.baselines as baselines

def get_results(train, test, use_baseline = False, force = False):
    train_measurement_paths, train_xs, train_ys = prepare_data(train)
    test_measurement_paths, test_xs, test_ys = prepare_data(test)

    result_arr = _predict(train_xs, train_ys, test_xs, test_ys)    
    if use_baseline:
        empty_baselines = baselines.get_empty(use_cached = not force)
        for i, value in enumerate(result_arr):
            result_arr[i] = value - empty_baselines.get_total_energy()

    return list(zip(test_measurement_paths, list(result_arr), list(test_ys)))

def _predict(train_xs, train_ys, test_xs, test_ys):
    reg = LinearRegression().fit(train_xs, train_ys)
    return reg.predict(test_xs)
