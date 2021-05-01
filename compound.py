
import numpy as np
from scipy.integrate import quad
import pandas as pd
from simulator import *

U = UnitConverter()
S = Simulator()
## This file contains the Compound class
class Compound:
    
    def __init__(self, name, mw = None, Perry = True):
        
        self.name = name            # Compound name
        # Pure properties
        self.mw = mw                # molecular weight
        self.Hig_f = [None, None]   # ideal gas enthalpy of formation
        self.Gig_f = [None, None]   # ideal gas Gibbs free energy of formation
        self.Sig = [None, None]     # ideal gas entropy
        self.Hstd_c = [None, None]  # standard heat of combustion
        self.acentric = None        # acentric factor
        self.dipole = [None, None]  # magnetic dipole
        # Critical properties
        self.Tc = [None, None]      # critical temperature
        self.Pc = [None, None]      # critical pressure
        self.Vmc = [None, None]     # critical molar volume
        self.Zc = None              # critical compressibility factor
        # Thermodynamic properties
        self.Z = None               # compresibility factor
        self.Pvap = [None, None]    # vapor pressure
        self.mCPig = [None, None]   # mean ideas gas heat capacity
        self.mCPl = [None, None]    # mean liquid heat capacity    
        self.CPig = [None, None]    # ideal gas heat capacity
        self.CPl = [None, None]     # liquid heat capacity
        self.density = [None, None] # density
        # Transport properties
        self.GasVis = [None, None]  # gas viscosity
        self.LiqVis = [None, None]  # liquid viscosity
        self.GasTC = [None, None]   # gas thermal conductivity
        self.LiqTC = [None, None]   # liquid therml conductivity

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

        
    def CP_liquid(self, T, units = "K", Report = False, f_output = False):
        # Liquid heat capacity, Perrys' handobook method.
        # T is a temperature which LCP will be calculated.
        # Report is a boolean, if True, then print the result.

        # Convert temperature units into Kelvin.
        if isinstance(T,(int, float)):
            T = [T, units]

        else:
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
            print(f'The Liquid Heat Capacity of {self.name} is {self.CPl[0]:,.2f} {self.CPl[1]}')

        if f_output:
            return CPL#, 'J/kmol*K'
        
    def mean_CP(self, f_CP, T1, T2, units, phase, Report = False):
        # This method calculate de mean heat capacity
        T1 = U.Temperature_Converter(T1,"K")
        T2 = U.Temperature_Converter(T2,"K")
        mCP, err = quad(f_CP, T1[0], T2[0], args = (T1[1], False, True))
        S.add_warning(f'The integral error for the mean heat capacity of {self.name} is {err:.2e}.') ## ADD TIME
        
        if phase == "liquid":
            self.mCPl = [mCP / (T2[0] - T1[0]), units]

            if Report:
                print(f'The Mean Liquid Heat Capacity of {self.name} is {self.mCPl[0]:,.2f} {self.mCPl[1]}')

        elif phase == "gas":
            self.mCPig = [mCP / (T2[0] - T1[0]), units]
            if Report:
                print(f'The Mean Ideal gas Heat Capacity of {self.name} is {self.mCPig[0]:,.2f} {self.mCPig[1]}')
            


        
        
if __name__ == '__main__':
    A = Compound("Water")
    A.CP_liquid([533.15, "K"],Report = True)
    A.mean_CP(A.CP_liquid, [273, "K"], [450, "K"], "J/kmol*K", "liquid", True)
    E = Compound("Ethane")
    E.CP_liquid([290, "K"], Report = True)
    E.mean_CP(E.CP_liquid, [260, "K"], [290, "K"],"J/kmol*K", "liquid", True)
    
        
        
        
        