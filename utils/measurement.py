class Measurement:
    def __init__(self, duration, pkg, dram, name = None, path_to_data = None):
        if duration < 0:
            raise ValueError(f"Duration must be positive. {duration}")
        for cpu_energy in pkg:
            if cpu_energy < 0:
                raise ValueError(f"All elements of pkg must be positive. {pkg}")
        for ram_energy in dram:
            if ram_energy < 0:
                raise ValueError(f"All elements of pkg must be positive. {dram}")
        if name is not None:
            if not isinstance(name, str):
                raise TypeError(f"name must be of type string.")
        if path_to_data is not None:
            if not isinstance(path_to_data, str):
                raise TypeError(f"path_to_data must be of type string.")
        
        self.duration = duration
        self.pkg = pkg
        self.dram = dram
        self.name = name
        self.path_to_data = path_to_data

    def __add__(self, other):
        name = None
        if self.name is not None: 
            name = self.name
        if other.name is not None:
            name = other.name
        
        path_to_data = None
        if self.path_to_data is not None:
            path_to_data = self.path_to_data
        if other.name is not None:
            path_to_data = other.path_to_data

        self.__validate_other(other)
        duration = self.duration + other.duration
        pkg = [x + y for x, y in zip(self.pkg, other.pkg)]
        dram = [x + y for x, y in zip(self.dram, other.dram)]
        return Measurement(duration, pkg, dram, name = name, path_to_data = path_to_data)

    def __truediv__(self, dividend):
        duration = self.duration / dividend
        pkg = [x / dividend for x in self.pkg]
        dram = [x / dividend for x in self.dram]
        return Measurement(duration, pkg, dram, name = self.name, path_to_data = self.path_to_data)

    def __validate_other(self, other):
        if len(self.pkg) != len(other.pkg):
            raise ValueError(f"pkg lists must be same length.")
        if len(self.dram) != len(other.dram):
            raise ValueError(f"dram lists must be same length.")

    def __str__(self):
        as_str = f"Duration: {self.duration} pkg: {self.pkg} dram: {self.dram}"
        if self.name is not None:
            as_str = f"Name: {self.name} " + as_str
        if self.path_to_data is not None:
            as_str += f" path to data: {self.path_to_data}"
        return as_str