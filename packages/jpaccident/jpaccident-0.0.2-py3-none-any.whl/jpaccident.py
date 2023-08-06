import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
#import japanize_matplotlib


url = 'https://raw.githubusercontent.com/s2022027/jpaccident/main/src/jpaccident-new.csv'
res = urllib.request.urlopen(url)
df = pd.read_csv(res, encoding="utf_8", header=0)


def main():
    plt.figure(figsize=(15, 5))
    print('これは月別の交通事故死亡者数のグラフを出します。')
    print('-----')
    print('1970年,2007年,2008年,2009年,2010年,2012年,2013年,2014年,2015年,2016年,2017年,2018年,2019年,,2020年,2021年の中から選択')
    print('-----')
    print('増減数のグラフを見たい場合はaを入力')
    print('-----')
    year = str(input('調べたい年数(英数字のみ)：'))
    if year == 'a':
        print('比較する年数を二つ入力')
        print('-----')
        year1 = str(input('一つ目(数字のみ)：'))
        year2 = str(input('二つ目(数字のみ)：'))
        df['増減人数'] = df[year1] + df[year2]
        plt.bar(df['month'],df['増減人数'])
        plt.title(year1 + '年の死者数-' + year2 +'年の死者数')
        plt.xlabel('1月〜12月')
        plt.ylabel('増減数')
        plt.show
        plt.savefig('jpaccident-dif.png')


    else:
        plt.bar(df['month'],df[year])
        plt.title(year +"年の交通事故死亡者数")
        plt.xlabel('1月〜12月')
        plt.ylabel('死亡者数')
        plt.show
        plt.savefig('jpaccident.png')

if __name__ == '__main__':
    main()