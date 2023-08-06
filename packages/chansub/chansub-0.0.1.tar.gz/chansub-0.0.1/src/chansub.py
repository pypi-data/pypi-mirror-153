import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from io import StringIO

url = "https://raw.githubusercontent.com/ayaka-wada/chansub/main/src/Number_of_channel_subscribers.csv"
# print(url)
# res = urllib.request.urlopen(url)
# res = res.read().decode('utf-8"')
csv = pd.read_csv(url, parse_dates=['date'], index_col='date')
df = csv.interpolate(limit_direction='both')


def main():
    fig, ax = plt.subplots()
    ax.plot(df.index, df['Tokino Sora'], label="Tokino Sora")
    ax.plot(df.index, df['Houshyou Marine'], label="Houshyou Marine")
    ax.plot(df.index, df['Shiranui Flare'], label="Shiranui Flare")
    ax.plot(df.index, df['Usada Pekora'], label="Usada Pekora")
    ax.plot(df.index, df['Shirogane Noel'], label="Shirogane Noel")
    ax.plot(df.index, df['Kiryu Coco'], label="Kiryu Coco")


    # ラベルの名前付け
    ax.set_xlabel('Date')
    ax.set_ylabel('channel subscribers')
    # y軸の範囲設定
    ax.set_ylim(0, 2300000)
    # 指数表記から普通の表記に変換
    plt.ticklabel_format(style='plain', axis='y')
    # 凡例
    plt.legend(loc="upper left", fontsize=10)
    # x軸の文字を回転
    plt.xticks(rotation=60)
    plt.show()
    plt.savefig("result.png")

if __name__ == '__main__':
    main()

