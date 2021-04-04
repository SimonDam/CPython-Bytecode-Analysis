import tensorflow.keras as keras
import tensorflow.keras.layers as layers
from data.preparation import prepare_data
import numpy as np

def get_results(train, test):
    train_measurement_paths, train_xs, train_ys = prepare_data(train)
    test_measurement_paths, test_xs, test_ys = prepare_data(test)

    size = train_xs[0].shape[0]

    input = layers.Input((size))
  
    dense = layers.Dense(size, activation="relu")(input)
    dense = layers.Dense(size//2, activation="relu")(dense)
    dense = layers.Dense(size//4, activation="relu")(dense)
    
    output = layers.Dense(1, activation="relu")(dense)

    model = keras.Model(inputs=[input], outputs=[output])
    model.compile(optimizer="adam", loss=keras.losses.MeanSquaredError(reduction="auto", name="mean_squared_error"))

    train_xs = np.array(train_xs)
    train_ys = np.array(train_ys)
    test_xs = np.array(test_xs)
    test_ys = np.array(test_ys)
    model.fit(train_xs, train_ys, validation_data=(test_xs, test_ys), epochs=25, batch_size=16)
    result_arr = np.array(model.predict(test_xs))
    return list(zip(test_measurement_paths, list(result_arr), list(test_ys)))
