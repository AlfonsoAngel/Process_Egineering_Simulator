from compound import Compound
from simulator import *


    
        


class Mixture(Compound):

    def __init__(self, composition, basis):
        
        self.composition = composition


        if basis == "molar":

            self.to_mass()         



        elif basis == "mass":

            self.to_mole()

        else:
             print('Basis not defined')

      

        # Pure properties
        #self.mw = MolarWeight(mw)                # molecular weight
        self.Hig_f = None   # ideal gas enthalpy of formation
        self.Gig_f = None   # ideal gas Gibbs free energy of formation
        self.Sig = None     # ideal gas entropy
        self.Hstd_c = None  # standard heat of combustion
        self.acentric = None        # acentric factor
        self.dipole = None  # magnetic dipole
        # Critical properties
        self.Tc = None      # critical temperature
        self.Pc = None      # critical pressure
        self.Vmc = None     # critical molar volume
        self.Zc = None              # critical compressibility factor
        # Thermodynamic properties
        self.Z = None               # compresibility factor
        self.Pvap = None    # vapor pressure
        self.mCPig = None   # mean ideas gas heat capacity
        self.mCPl = None    # mean liquid heat capacity    
        self.CPig = None    # ideal gas heat capacity
        self.CPl = None     # liquid heat capacity
        self.density = None # density
        # Transport properties
        self.GasVis = None  # gas viscosity
        self.LiqVis = None  # liquid viscosity
        self.GasTC = None   # gas thermal conductivity
        self.LiqTC = None   # liquid therml conductivity

    def to_mass(self):
        

        #normalize 
        frac = sum([y.mole_frac for y in self.composition])
        if not frac == 1.0:
            for y in self.composition:
                y.mole_frac = y.mole_frac / frac

        total_mass = sum([y.mole_frac * y.mw for y in self.composition])

        for x in self.composition:
            x.mass_frac = x.mole_frac * x.mw / total_mass

        self.mw = sum([y.mw * y.mole_frac for y in self.composition])

    def to_mole(self):
        frac = sum([x.mass_frac for x in self.composition])
        if not frac == 1.0:
            for x in self.composition:
                x.mass_frac = x.mass_frac / frac

        total_mole = sum([x.mass_frac / x.mw for x in self.composition])

        for y in self.composition:
            y.mole_frac = (y.mass_frac / y.mw) / total_mole

        self.mw = pow(sum([x.mass_frac / x.mw for x in self.composition ]), -1)