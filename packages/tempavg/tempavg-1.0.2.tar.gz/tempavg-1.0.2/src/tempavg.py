import shutil
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import urllib.error
import urllib.request
import zipfile

data_dir_path = "./data/"
if os.path.exists(data_dir_path):
    shutil.rmtree(data_dir_path)
os.mkdir(data_dir_path)

file_url = "https://github.com/Shimpo-Yumiko/tempavg_data/archive/refs/heads/main.zip"
save_path = "./data/tempavg_data.zip"
try:
    with urllib.request.urlopen(file_url) as download_file:
        data = download_file.read()
        with open(save_path, mode='wb') as save_file:
            save_file.write(data)
except urllib.error.URLError as e:
    print(e)

with zipfile.ZipFile("./data/tempavg_data.zip") as obj_zip:
    obj_zip.extractall("./data/")

df = pd.read_csv("data/tempavg_data-main/tempavg.csv")
# df.head()

year = df['year_month'].str.extract('(\w+)', expand=True)
start = int(year.iloc[0])
last = int(year.iloc[-1])

years = [i for i in range(start, last, 5)]
for num in years:
    if num == start:
        df_year = pd.DataFrame(df[df["year_month"].str.startswith(f"{num}")].mean(numeric_only=True))
        # print(type(df_year))
        df_year = df_year.T
        df_year.insert(0, 'year', num)
    else:
        append_year = pd.DataFrame(df[df["year_month"].str.startswith(f"{num}")].mean(numeric_only=True))
        # print(append_year)
        append_year = append_year.T
        append_year.insert(0, 'year', num)
        df_year = pd.concat([df_year, append_year], axis=0)
# for i in range(47):
#     print(type(df_year.size()))
# print(df_year.size)

area = "Tokyo"
x = df_year['year']
y = df_year[f'{area}'].to_numpy()

def main():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(x, y)

    plt.title(f"{area}")
    plt.xlabel("year")
    plt.ylabel("℃")
    plt.ylim(0, df_year.max().iloc[1:].max())
    plt.grid(linewidth=0.1, color="gray")
    # plt.legend()
    plt.savefig("result.jpg")
    plt.show()
    print("保存しました")
    
main()