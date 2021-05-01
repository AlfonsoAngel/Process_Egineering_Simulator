from simulator import *
from compound import *


T1 = Temperature(533.15, "K")
T2 = Temperature(290, "K")
T3 = Temperature(273, "K")
T4 = Temperature(450, "K")
T5 = Temperature(260, "K")
A = Compound("Water")
A.CP_liquid(T1, Report = True)
A.mean_CP(A.CP_liquid, T3, T4, "J/kmol*K", "liquid", True)
E = Compound("Ethane")
E.CP_liquid(T2, Report = True)
E.mean_CP(E.CP_liquid, T5, T2,"J/kmol*K", "liquid", True)