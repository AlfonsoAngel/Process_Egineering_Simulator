from simulator import *
from compound import *

S = Simulator()
T1 = Temperature(300, "K")
T2 = Temperature(500, "K")

A = Compound("Air")
A.CP_ig(T1,'K', True)
A.mean_CP(A.CP_ig, T1, T2, "J/kmol*K", 'gas', True)
A.Vapor_pressure(T1, True)
A.Vapor_pressure(T2, True)

