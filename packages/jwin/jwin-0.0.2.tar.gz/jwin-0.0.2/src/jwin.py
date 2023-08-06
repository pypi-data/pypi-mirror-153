import pandas as pd
import subprocess as sp
import matplotlib.pyplot as plt
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--team", help='team name', type=str, default='札幌')
    args = parser.parse_args()
    return args


def main():
    sp.call("wget https://raw.githubusercontent.com/Doraemon-desu/J-league/main/J-league.csv",shell=True)
    args = get_args()
    df = pd.read_csv('J-league.csv',encoding='utf-8',index_col='team')
    name = args.team
    victory = df.loc[name,:]
    x = df.columns.values
    y = victory.values
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.savefig(name+".png")
    plt.show()
    

if __name__ == '__main__':
    main()
