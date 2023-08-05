import datetime
import csv
import os
import shutil
import sys
import urllib
import zipfile
import glob
import time
import matplotlib.pyplot as plt
import pandas as pd
import urllib.error
import urllib.request

# 日本と各国のGDPの比較をしたい
# 各国の自分好みの国とのGDP比較表示がない
# 日本の現状や世界の現状を知ることに役立つ

DATA_DIR = "./data/"
DOWNLOAD_PATH = DATA_DIR + "download.zip"
# DATA_DIR = DATA_PATH + "download"
DATA_URL = "https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv"

COUNTRY_LIST = ["China", "Japan", "France", "Finland"]



class GDP():
    def __init__(self, country_list=COUNTRY_LIST):
        self.country_list = country_list


    def read_textfile(self):
        # input textfile
        f = open(self.country_list)
        data = f.read()
        data.strip()
        data.replace("\n","").replace(" ","")
        country_list = data.split(",")
        
        return country_list


    def use_col_list(self):
        col_list = []
        for i in range(65):
            if i == 0 or i >= 5:
                col_list.append(i)
        return col_list

    def choose_file(self):
        # filename in search_name
        search_name = DATA_DIR + "API"
        file_name = ""
        # for in downloadfile
        for f_name in glob.glob(DATA_DIR+"/*"):
            if search_name in f_name:
                file_name = f_name
                break
        return file_name


    
    def unzip(self):
        # rm data_dir if it exists
        if os.path.exists(DATA_DIR) == True:
            shutil.rmtree(DATA_DIR)
        # mkdir
        os.mkdir(DATA_DIR)

        # download
        try:
            with urllib.request.urlopen(DATA_URL) as f:
                data = f.read()
                with open(DOWNLOAD_PATH, "wb") as download_f:
                    download_f.write(data)
        except urllib.error.URLError as e:
            print(e)

        # unzip
        with zipfile.ZipFile(DOWNLOAD_PATH) as f_zip:
            f_zip.extractall(DATA_DIR)

    def create_columns_list(self):
        c_list = []
        for i in range(67):
            if i >= 4:
                i += 1956
            c_list.append(i)
        return c_list


    def create_dataframe(self, f_dir):
        print(self.country_list)
        # escape column error

        
        df = pd.read_csv(
            f_dir,
            names=self.create_columns_list(),
            index_col=0,
            # usecols=self.use_col_list(),
            # skiprows=lambda x: x not in self.country_list
            )
        # drop index
        drop_list = []
        for ind in df.index:
            if ind not in self.country_list:
                drop_list.append(ind)
        # inplace because changing origine df
        df.drop(index=drop_list, inplace=True)


        # df.drop(lambda x: x not in self.country_list)

        return df
    ### 先頭の空白行の処理！！！！！

    def make_fig(self, dataframe):
        fig,ax = plt.subplots()
        ax.grid()
        x = dataframe.columns[4:]
        for row in self.country_list:
            # extract row
            r = dataframe.loc[row]
            Y = r[4:]
            ax.plot(x, Y, label=row)
        ax.set_xlabel("Period")
        ax.set_ylabel("GDP")
        ax.legend()
        fig.savefig(DATA_DIR + "result.png")
        plt.show()



    def run(self):
        # setting countrylist
        if self.country_list != COUNTRY_LIST:
            self.country_list = self.read_textfile()
        self.unzip()
        filename = self.choose_file()
        df = self.create_dataframe(filename)
        self.make_fig(df)

    def test(self):
        # self.unzip()
        filename = self.choose_file()
        # time.sleep(10)
        df = self.create_dataframe(filename)
        self.make_fig(df)



def main():
    if len(sys.argv) != 1:
        gdp = GDP(country_list=sys.argv[1])
    elif len(sys.argv) == 1:
        gdp = GDP()

    gdp.run()

main()