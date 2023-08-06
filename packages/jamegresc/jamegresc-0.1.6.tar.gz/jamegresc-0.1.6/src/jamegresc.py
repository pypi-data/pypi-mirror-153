import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import sys
import argparse
from time import sleep
import subprocess as sp


sleep(20)
sp.run(["wget", "https://data.bodik.jp/dataset/28417a5e-ec57-4676-9dbf-8c116fba12ce/resource/966c2391-0d93-45ef-b908-e200ac365a9f/download/131105_recyclable_waste.csv"], capture_output=True, text=True, encoding='utf-8').returncode
data=pd.read_csv("131105_recyclable_waste.csv", encoding="shift-jis")
data = data.rename(columns={'分別回収_ﾌﾟﾗｽﾁｯｸ製容器包装（ｔ）': '分別回収_プラスチック製容器包装（ｔ）', '分別回収_売薬駅_ﾌﾟﾗｽﾁｯｸ製容器包装（円）': '分別回収_売却益_プラスチック製容器包装（円）'})
data = data.iloc[:, :14]
data.fillna(0,inplace=True)

sp.run(["rm", "131105_recyclable_waste.csv"], capture_output=True)


def main():
    parser = argparse.ArgumentParser(prog='jamegresc', description="default：びん")
    parser.add_argument("--resource", "-r", default="びん", 
    choices=["びん", "アルミ缶", "スチール缶", "ペットボトル", "古紙", "プラスチック製容器包装"])
    args = parser.parse_args()
    column = args.resource
    
    t=data['分別回収_拠点数']
    print(t)
    n = len(data[:])

    y_t = data['分別回収_{}（ｔ）'.format(column)][0:n]
    y_en = data['分別回収_売却益_{}（円）'.format(column)][0:n]

    x=np.arange(0,n)+2011
    y1 = np.array([])
    for i in y_t:
        try:
            y1 = np.append(y1, int(i.replace(',', '')))
        except AttributeError:
            y1 = np.append(y1, int(i))


    y2 = np.array([])
    for i in y_en:
        try:
            y2 = np.append(y2, int(i.replace(',', ''))/1000)
        except AttributeError:
            y2 = np.append(y2, int(i)/1000)

    fig = plt.figure(figsize=(11, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(x, y1, label="t", marker='*', color='r')
    ax2 = ax1.twinx()
    ax3 = ax2.plot(x, y2, label="1000yen", marker='*', color='b')
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper left")
    ax1.set_ylabel("t", fontsize=12)
    ax2.set_ylabel("1000円", fontsize=12)
    ax1.set_title('{}'.format(column))
    plt.savefig(column+".png")
    
main()