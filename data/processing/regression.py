from sklearn.linear_model import LinearRegression
from data.preparation import prepare_data

def get_results(train, test):
    train_measurement_paths, train_xs, train_ys = prepare_data(train)
    test_measurement_paths, test_xs, test_ys = prepare_data(test)
    
    result_arr = _predict(train_xs, train_ys, test_xs, test_ys)
    return list(zip(test_measurement_paths, list(result_arr), list(test_ys)))

def _predict(train_xs, train_ys, test_xs, test_ys):
    reg = LinearRegression().fit(train_xs, train_ys)
    print("Score:", reg.score(test_xs, test_ys))
    return reg.predict(test_xs)
