import os
from glob import glob

import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm


class Data():
    def __init__(self,
                 other_data: str = './data-2/other.xlsx',
                 other_folder: str = "./data-2/A61B005專利_1996-2020/*",
                 apple_data: str = "./data-2/Apple.xlsx",
                 apple_file: str = "./data-2/Apple_Full text.XML"
                 ) -> None:
        self.other_data = other_data
        self.other_folder = other_folder
        self.apple_data = apple_data
        self.apple_file = apple_file

        pass

    def other(self):
        if os.path.exists(self.other_data):
            print("other company file exist.")
            return pd.read_excel(self.other_data)
        else:
            tmp_data = []
            for i in tqdm(glob(self.other_folder)):
                data = pd.read_excel(i)
                tmp_data.append(data)
            data = pd.concat(tmp_data)
            data.to_excel(self.other_data, index=False)
            return data

    def clean(self):
        pass

    # @staticmethod
    def apple(self):
        if os.path.exists(self.apple_data):
            print("apple company file exist.")
            return pd.read_excel(self.apple_data)

        with open(self.apple_file, 'r') as f:
            data = f.read()

        soup = BeautifulSoup(data, "html.parser")
        apple_case = soup.findAll("doc")
        result = []
        for i in apple_case:
            uid = i.find("uuid").text
            content1 = i.find("str", {"name": "權利要求"})
            content2 = i.find("str", {"name": "說明書"})

            content1 = content1.text if content1 is not None else ""
            content2 = content2.text if content2 is not None else ""

            tmp_df = pd.DataFrame({
                "uid": [uid],
                "content": [content1+" "+content2]
            })
            result.append(tmp_df)

        result = pd.concat(result)
        result.to_excel(self.apple_data, index=False)
        return result
        pass


if __name__ == "__main__":
    task1_data = Data().other()
    print(len(task1_data))
