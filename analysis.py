from data import processing
from typing import Callable

class Analysis():
    def __init__(self, name, run_func):
        if not isinstance(name, str):
            raise TypeError(f"name should be string, {type(name)} given.")
        if not isinstance(run_func, Callable):
            raise TypeError(f"run_func should be callable, {type(run_func)} given.")
        
        self.name = name
        self.run_func = run_func

    def run(self, *args, **kwargs):
        return self.run_func(*args, **kwargs)

def regression(additional_name = ""):
    if additional_name:
        additional_name = f"- {additional_name}"

    with_func = lambda train, test : processing.regression.get_results(train, test, use_baseline = True)
    without_func = lambda train, test : processing.regression.get_results(train, test, use_baseline = False)
    return [
        Analysis(f"Linear Regression (with baselines) {additional_name}", with_func),
        Analysis(f"Linear Regression (no baselines) {additional_name}", without_func)
    ]

def fraction_of_totals(additional_name = "", force = False):
    if additional_name:
        additional_name = f"- {additional_name}"
    
    with_func = lambda train, test : processing.fraction_of_totals.get_results(train, test, use_baselines = True, force = force)
    without_func = lambda train, test : processing.fraction_of_totals.get_results(train, test, use_baselines = False, force = force)

    return [
        Analysis(f"Fraction of totals (with baselines) {additional_name}", with_func),
        Analysis(f"Fraction of totals (no baselines) {additional_name}", without_func)
    ]