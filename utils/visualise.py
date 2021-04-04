from pathlib import Path
from numpy.lib.function_base import average
import matplotlib.pyplot as plt
import numpy as np

def create_graphs(data, name, dest = None, show = True):
    xs = []
    ys = []
    paths = []
    errors = []
    for path, estimated_energy, actual_energy in data:
        paths.append(path)
        xs.append(actual_energy)
        ys.append(estimated_energy)
        error = abs(actual_energy-estimated_energy)/actual_energy
        errors.append(error*100)
    
    avg_error = average(errors)
    correlation_matrix = np.corrcoef(xs, ys)
    correlation_xy = correlation_matrix[0,1]
    r_squared = correlation_xy ** 2
    
    # Fit a linear line to data.
    z = np.polyfit(xs, ys, 1)
    p = np.poly1d(z)
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,6))
    fig.suptitle(f"{name} - Average error: {avg_error:.1f}%")
    x_lims = [0, 4.5*10**7]

    ax1.plot(xs, ys, '.', label="Predictions")
    ax1.plot(xs, xs, label="Perfect predictions")
    ax1.plot(xs,p(xs),"r--", label=f"Trendline, R^2 = {r_squared:.3f}")
    ax1.set_title("Estimated energy consumption vs.\nActual energy consumption")
    ax1.legend(loc='upper left')
    ax1.set(xlabel='Actual energy [µJ]', ylabel='Estimated energy [µJ]')
    ax1.set_xlim(x_lims)

    ax2.plot(xs, errors, '.')
    ax2.set_title("Error over actual energy consumption")
    ax2.set(xlabel='Actual energy [µJ]', ylabel='Error [%]')
    ax2.set_xlim(x_lims)

    ax3.hist(xs, bins=50)
    ax3.set_title("Distribution of samples")
    ax3.set(xlabel='Actual energy [µJ]', ylabel='# of sampels')
    ax3.set_xlim(x_lims)

    if dest is not None:
        plt.savefig(Path(f"{dest}/{name}.pdf"))
        with open(Path(f"{dest}/{name}.csv"), 'w') as file:
            file.write("path, actual, estimated, error\n")
            for path, x, y, error in zip(paths, xs, ys, errors):
                file.write(f"{path},{x},{y},{error}\n")

    if show:
        plt.show()