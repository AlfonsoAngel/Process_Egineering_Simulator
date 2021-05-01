import pandas as pd

class Simulator:

    def __init__(self):
        self.database = None 
        self.errors = []
        self.warnings = []

    def load_perry(self):
        self.database =  pd.read_csv("./properties/Database.csv",index_col=("Name"))
        return self.database

    def add_errors(self, new_error):
        self.errors.append(new_error)

    def show_erros(self):
        for i in self.errors:
            print(i)

    def add_warning(self, new_warning):
        self.warnings.append(new_warning)

    def show_warning(self):
        for i in self.warnings:
            print(i)


class  UnitConverter:

    def __init__(self):

        self.Pu = pd.read_csv('./units/Pressure.csv', index_col = 0)   
        self.Tu = pd.DataFrame({"K":[lambda T: T , lambda T: T + 273.15, lambda T: (T + 459.67) * 5 / 9, lambda T: T * 5 / 9],
          "°C":[lambda T: T - 273.15, lambda T: T, lambda T: (T - 32) * 5 /9, lambda T: (T - 491.67) * 5 / 9],
          "°F":[lambda T: (T * 9 / 5) -459.67, lambda T: (T * 9 / 5) + 32, lambda T: T, lambda T: T - 459.67],
          "R":[lambda T: T * 9 / 5, lambda T: (T + 273.15) * 9 / 5, lambda T: T + 459.67, lambda T: T]}, 
          index = ["K", "°C", "°F", "R"]) 
        self.Vmu = pd.read_csv('./units/MolarVolume.csv', index_col = 0)

        

    def Pressure_Converter(self, P, Punits):

        factor = self.Pu.at[P[1], Punits]
        return [P[0] * factor, Punits]

    def Temperature_Converter(self, T, Tunits):

        return [round(self.Tu.at[T[1], Tunits](T[0]), 2), Tunits]

    def MolarVolume_Converter(self, Vm, Vmunits):

        factor = self.Vmu.at[Vm[1], Vmunits]
        return [Vm[0] * factor, Vmunits]


