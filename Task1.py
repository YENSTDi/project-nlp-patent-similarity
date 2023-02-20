import os
import pandas as pd
from tqdm import tqdm
from glob import glob

class Task1():
    def __init__(self, task1_data:str='./data/A61B005.xlsx', task1_folder:str="./data/A61B005專利_1996-2020/*") -> None:
        self.task1_data = task1_data
        self.task1_folder = task1_folder
        self.data = self.get_data()
        pass
    
    def get_data(self):
        if os.path.exists(self.task1_data):
            return pd.read_excel(self.task1_data)
        else:
            tmp_data = []
            for i in tqdm(glob(self.task1_folder)):
                data = pd.read_excel(i)
                tmp_data.append(data)
            data = pd.concat(tmp_data)
            data.to_excel(self.task1_data)
            return data
    def clean(self):
        pass

if __name__=="__main__":
    task1_data = Task1().get_data()
    print(len(task1_data))