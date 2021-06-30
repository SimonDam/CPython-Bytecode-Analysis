# CPython-Bytecode-Counter
This is a fork of CPython 3.8.2 to analyze CPython bytecodes.

Source taken from [here](https://www.python.org/downloads/release/python-382/).


## Overview
This solution can analyze Python programs by creating ```.csv``` files containing each bytecode that was executed and how long that took.
It also measures how much energy was used to run the same program on an unmodified CPython intepreter.

## The modified CPython Interpreter
In ```/Python-BCT``` is the modified Python interpreter.
In order to compile it, see https://devguide.python.org/setup/.
This should also be done for the interpreter in ```/Python```.
It should be run on a Linux machine, as the implementation uses a clock that is too low resolution.
The machine's CPU should also support RDTSC, as this is the unit the bytecodes are measured in.
After all the requirements are installed, (as the setup guide states), just running ```make``` should work in order to recompile it.
Before running the modified intepreter, the first line in ```BCC.txt``` must be set to a path where the intepreter can dump the bytecode files.
This should be the only thing in that file.

## Measure
```measure.py``` has functions for getting the bytecode counts/timings and power consumption.
```measure_programs``` measures every file in a folder.
The results are dumped in the folder.
Since this uses pyRAPL, this must be run on a Linux machine.
## Analyze
```/analysis/analyze.py``` has a command line interface for analyzing the bytecode files saved in the folder.
This will create caches, since this parsing can take quite a long time.

## synthesize/
This is a folder where you can create versions of existing Python programs.
```min_max.py``` benchmarks a Python program with different values for n, in order to find a minimum value (a run with no error) and a maximum value, which attempts to make the program run for a certain amount of time (like n = 1000 makes the program run for ~10 seconds).
The Python program must be in a file where there is a function, with one input (n), which returns the source code of the program (see ```/pythonprograms``` for examples).
Then running the ```synthesize.py``` script will generate different source code files with different values of n.
