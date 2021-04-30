import pandas as pd

class Simulator:

    def __init__(self):
        self.database = None 

    def load_perry(self):
        self.database =  pd.read_csv("./properties/Database.csv",index_col=("Name"))
        return self.database

