import os
import subprocess as sp
import sys
import shutil

# import urllib.request
import matplotlib.pyplot as plt
import japanize_matplotlib
import requests
# import openpyxl
import pandas as pd


file_path = "./horse_data.tsv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path, delimiter="\t")
else:
    r = requests.get('https://raw.githubusercontent.com/tama2101-s/horse_racing_database/main/horse_data.tsv').content
    with open(file_path,mode='wb') as f: # wb でバイト型を書き込める
        f.write(r)
    df = pd.read_csv(file_path, delimiter="\t")



df["month"] = df["日付"].replace('(.*?)/(.*?)(?=\().*', r'\1', regex=True)
df["day"] = df["日付"].replace('(.*?)/(.*?)(?=\().*', r'\2', regex=True)
df = df.drop(columns=['通過', '上り', '調教師', '馬主'])
df['距離'] = df['距離'].str[1:]
df['距離'] = df['距離'].str.strip('m')
df["year"] = 2002
year = 2002
T_F = False
for index, data in df.iterrows():
    if df.loc[index, 'month'] == "01" and T_F == False:
        year += 1
        T_F = True
    if df.loc[index, 'month'] == "02":
        T_F = False
    df.loc[index, 'year'] = year
# print(df)



def main():
    global df
    if int(sys.argv[1]) == 1:
        df = df[df["着順"] == str(sys.argv[2])]
        df = df[df["レース"] == sys.argv[3]]
        df = df.drop(columns=["着差", "単勝", "人気", "距離",
        "ランク", "芝orダート", "馬体重", "枠番", "年齢"])
        pd.set_option('display.max_rows', None)
        # print(df)
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.axis('off')
        ax.axis('tight')
        table = ax.table(cellText=df.values,
        colLabels=df.columns,
        colWidths=[0.5, 0.7, 0.3, 0.2, 0.2, 0.2,0.2, 0.9, 0.3, 0.5, 0.5, 0.3, 0.2, 0.2],
        bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(2, 2)

        plt.savefig("result.png")
        plt.show()

    elif int(sys.argv[1]) == 2:
        times = df["タイム"]
        base_time = pd.to_datetime('00:00.0', format='%M:%S.%f')
        date_dt = pd.to_datetime(times, format='%M:%S.%f') - base_time
        dt_scond = date_dt.dt.total_seconds()
        df["time_scond"] = dt_scond
        df = df[df["レース"] == sys.argv[2]]
        df_one = df[df["着順"] == str(1)]
        df_2 = df_one.loc[:, ["year", "time_scond"]]
        fig, ax = plt.subplots()
        ax.plot(df_2["year"], df_2["time_scond"])
        ax.set_title(sys.argv[2]+"のレースタイム")
        plt.savefig("result.png")
        plt.show()

# print(df)
if __name__ == "__main__":
    main()