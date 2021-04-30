
import numpy as np
from scipy.integrate import quad
import pandas as pd
from simulator import *
from units import *

U = UnitConverter()
S = Simulator()
## This file contains the Compound class
class Compound:
    
    def __init__(self, name, mw = None, Perry = True):
        
        self.name = name
        # Pure properties
        self.mw = mw
        self.Hig_f = [None, None]
        self.Gig_f = [None, None]
        self.Sig = [None, None]
        self.Hstd_c = [None, None]
        self.acentric = None
        self.dipole = [None, None]
        self.Heat_f = [None, None]         
        # Critical properties
        self.Tc = [None, None]
        self.Pc = [None, None]
        self.Vmc = [None, None]
        self.Zc = None
        # Thermodynamic properties
        self.Z = None
        self.Pvap = [None, None]
        self.mCPig = [None, None]
        self.mCPl = [None, None]
        self.CPig = [None, None]
        self.CPl = [None, None]
        self.LMV = [None, None]
        self.density = [None, None]
        # Transport properties
        self.GasVis = [None, None]
        self.LiqVis = [None, None]
        self.GasTC = [None, None]
        self.LiqTC = [None, None]

        if Perry:
            # data
            self.data = S.load_perry()
            # Pure compound proprerties
            self.wt = self.data.at[self.name, "wt"]
            self.Hig_f = [self.data.at[self.name, "Hig_f"], "kJ/mol"]
            self.Gig_f = [self.data.at[self.name, "Gig_f"], "kJ/mol"]
            self.Sig = [self.data.at[self.name, "Sig"], "kJ/mol*K"]
            self.Hstd_c = [self.data.at[self.name, "Hstd_c"], "kJ/mol"]
            # Critical properties from Perry's handbook
            self.Tc = [self.data.at[self.name, "Tc"], "K"]
            self.Pc = [self.data.at[self.name, "Pc"], "MPa"]
            self.Vmc = [self.data.at[self.name, "Vc"], "m3/kmol"]
            self.Zc = self.data.at[self.name, "Zc"]
            self.acentric = self.data.at[self.name, "Acentric factor"]
            
        else:
            self.data = None

        
    def CP_liquid(self, T, Report = False):
        # Liquid heat capacity, Perrys' handobook method.
        # T is a temperature which LCP will be calculated.
        # Report is a boolean, if True, then print the result.

        # Convert temperature units into Kelvin,
        T = U.Temperature_Converter(T, "K")
        # Equation 2 for calculating LCP     
        eq2 = ["1,2-Butanediol", "1,3-Butanediol", "Carbon monoxide", \
               "1,1-Difluoroethane", "Ethane", "Heptane", "Hydrogen", \
               "Hydrogen sulfide", "Methane", "Propane"]
        # Read parameters from the database
        C1 = self.data.loc[self.name, "CPLC1"]
        C2 = self.data.loc[self.name, "CPLC2"]
        C3 = self.data.loc[self.name, "CPLC3"]
        C4 = self.data.loc[self.name, "CPLC4"]
        C5 = self.data.loc[self.name, "CPLC5"]
        # Equaion 2
        if self.name in eq2:
            
            Tr = T[0] / U.Temperature_Converter(self.Tc,"K")[0]
            t = 1- Tr
            CPL = (C1 * C1 / t) + C2 - 2 * C1 * C3 * t - C1 * C4 * t * t \
                  - ((C3 **2) * (t ** 3) / 3) - ((C3 * C4) * (t ** 4) / 2) \
                  - ((C4 **2) * (t ** 5) / 5)
            
            pass
        
        else:
        # Equation 1
            CPL = C1 +( C2 * T[0]) +( C3 * (T[0] **2)) +( C4 * (T[0] ** 3)) + (C5 * (T[0] ** 4))
            
        self.CPl = [CPL, 'J/kmol*K']
        
            
        if Report:
            return print(f'The Liquid Heat Capacity of {self.name} is {self.CPl[0]:,.2f} {self.CPl[1]}')
        
        

        
        
if __name__ == '__main__':
    A = Compound("Water")
    A.CP_liquid([533.15, "K"],Report = True)
    E = Compound("Ethane")
    E.CP_liquid([290, "K"], Report = True)
    
        
        
        
        