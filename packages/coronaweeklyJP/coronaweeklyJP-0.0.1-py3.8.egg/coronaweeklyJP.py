import json, requests ,re
import pandas as pd
import matplotlib.pyplot as plt
import sys

def main():
    args = sys.argv
    if len(args) != 2:
        print("Please write a prefecture. (e.g. coronaweeklyJP Hokkaido)")
    else:
        url = requests.get("https://opendata.corona.go.jp/api/Covid19JapanAll")
        text = url.text
        data = json.loads(text)
        df = pd.DataFrame(data["itemList"])

        pref_en = {"北海道": "Hokkaido", "青森県": "Aomori", "岩手県": "Iwate", "宮城県": "Miyagi", "秋田県": "Akita", "山形県": "Yamagata", "福島県": "Fukushima", "茨城県": "Ibaraki", "栃木県": "Tochigi", "群馬県": "Gumma", "埼玉県": "Saitama", "千葉県": "Chiba", "東京都": "Tokyo", "神奈川県": "Kanagawa", "新潟県": "Niigata", "富山県": "Toyama", "石川県": "Ishikawa", "福井県": "Fukui", "山梨県": "Yamanashi", "長野県": "Nagano", "岐阜県": "Gifu", "静岡県": "Shizuoka", "愛知県": "Aichi", "三重県": "Mie", "滋賀県": "Shiga", "京都府": "Kyoto", "大阪府": "Osaka", "兵庫県": "Hyogo", "奈良県": "Nara", "和歌山県": "Wakayama", "鳥取県": "Tottori", "島根県": "Shimane", "岡山県": "Okayama", "広島県": "Hiroshima", "山口県": "Yamaguchi", "徳島県": "Tokushima", "香川県": "Kagawa", "愛媛県": "Ehime", "高知県": "Kochi", "福岡県": "Fukuoka", "佐賀県": "Saga", "長崎県": "Nagasaki", "熊本県": "Kumamoto", "大分県": "Oita", "宮崎県": "Miyazaki", "鹿児島県": "Kagoshima", "沖縄県": "Okinawa"}
        df = df.replace(pref_en)

        pr = df[df["name_jp"]==args[1]]
        if len(pr) == 0:
            print("There are no data. Please change the name of prefecture.")
        else:
            pr = pr.iloc[:200,:]
            pr = pr.iloc[::-1]
            pr["dp"] = pr["npatients"].astype("i8").diff()
            pr["dd"] = 0
            for i in range(7,len(pr)):
                pr.iloc[i,-1] = pr.iloc[i,-2] / pr.iloc[i-7,-2]
            pr["date"] = pd.to_datetime(pr["date"])
            pr = pr.iloc[7:]

            plt.figure(figsize=(20,5))
            plt.plot(pr["date"], pr["dd"], marker=".")
            plt.axhline(y=1, color="red", linewidth=0.5)
            plt.title(f"Number of Corona Patients compared to The Previous Week({args[1]})")
            plt.savefig("./result.png", bbox_inches="tight")
            plt.show();

if __name__ == "__main__":
      main()