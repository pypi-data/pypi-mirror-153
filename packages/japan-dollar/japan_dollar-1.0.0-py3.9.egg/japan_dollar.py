import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("https://raw.githubusercontent.com/SotaChira/codeocean/main/japan_dollar.csv")

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(df["年月"],df["月末"])

    fig.savefig("img.png")


if __name__ == "__main__":
    main()