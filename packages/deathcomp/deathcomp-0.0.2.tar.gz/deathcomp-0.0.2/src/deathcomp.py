import pandas as pd
import numpy as np
import sys
import subprocess as sp
import matplotlib.pyplot as plt

def main(country, country2, days):
  sp.call("wget https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_deaths.csv", shell=True)
  data = pd.read_csv("new_deaths.csv")
  sp.call("rm new_deaths.csv ", shell=True)

  n = len(data[country])
  
  y = data[country][n-days:n]
  x = np.arange(n-days, n)

  y2 = data[country2][n-days:n]
  x2 = np.arange(n-days, n)

  plt.plot(x, y, label=country)
  plt.plot(x2, y2, label=country2)
  plt.legend()

  plt.savefig(country + "_" + country2 + ".png")
  plt.show()

country = str(sys.argv[1])
country2 = str(sys.argv[2])
days = int(sys.argv[3])

main(country, country2, days)
