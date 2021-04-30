# Here the file contains the class or functions necessary to changue units in variables
import pandas as pd


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