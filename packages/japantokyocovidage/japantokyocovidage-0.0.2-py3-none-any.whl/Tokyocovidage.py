import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_csv("https://stopcovid19.metro.tokyo.lg.jp/data/130001_tokyo_covid19_patients.csv")
year = df['患者_年代']
left = np.array([1,2,3,4,5,6,7,8])
height = np.array([year[year == '10代'].count(), year[year == '20代'].count(), year[year == '30代'].count(), year[year == '40代'].count(), year[year == '50代'].count(), year[year == '60代'].count(), year[year == '70代'].count(), year[year == '80代'].count()])

def main():
  plt.title('10,20,30,40,50,60,70,80')
  plt.bar(left, height)

if __name__ == "__main__":
  main()
