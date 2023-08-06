from bs4 import BeautifulSoup
from urllib import request
from urllib.request import urlopen
from urllib.error import HTTPError
import time
import requests
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import sys

num = str(sys.argv[1])
if num == '2016' or num == '2017' or num == '2018' or num == '2019' or num == '2020' or num == '2021':
    pass
else:
    print('Please enter a single-byte number from 2016~2021')
    sys.exit()

url = ('https://www.bleague.jp/stats/?tab=1&year=' + num)
response = request.urlopen(url)
time.sleep(1)
soup = BeautifulSoup(response)
response.close()

table = soup.find_all('tr')

standing = []
list_ = []
uPER = []

for row in table:
    tmp = []
    for item in row.find_all('td'):
        if item.a:
            tmp.append(item.text[0:len(item.text) // 2])
        else:
            tmp.append(item.text)
    standing.append(tmp)

for i in range(len(standing)):
    if standing[i] != [] and '\n\n' not in standing[i][0]:
        list_.append(standing[i])
    else:
        pass

for i in range(len(list_)):
    for j in range(len(list_[i])):
        if '%' in list_[i][j]:
            list_[i][j] = list_[i][j].replace('%','')
        elif ':' in list_[i][j]:
            list_[i][j] = list_[i][j].replace(':','.')

df = pd.DataFrame(list_,dtype=float)

# uPER = (1 / MP) * 
#        [ 3P + (2/3) * AST 
#        + (2 – factor * (team_AST / team_FG)) * FG 
#        + (FT *0.5 * (1 + (1 – (team_AST / team_FG)) 
#        + (2/3) * (team_AST / team_FG))) 
#        – VOP * TOV – VOP * DRB% * (FGA – FG) 
#        – VOP * 0.44 * (0.44 + (0.56 * DRB%)) * (FTA – FT) 
#        + VOP * (1 – DRB%) * (TRB – ORB) 
#        + VOP * DRB% * ORB + VOP * STL 
#        + VOP * DRB% * BLK – PF * ((lg_FT / lg_PF) 
#        – 0.44 * (lg_FTA / lg_PF) * VOP)]

for i in range(len(df)):
    uper = 0
    # try:
    uper = (1/df[5][i]) * ((df[14][i]) + (2/3) * df[22][i] + (2 - 0.6) * df[9][i]
    + df[15][i] * 0.5 * (1 + (1 - 0.4) + (2/3)) *  df[22][i]
    + df[15][i] * (1 - (df[22][i]/6)
    - 1 * df[24][i]
    - 1 * 0.7 * (df[10][i] - df[11][i]) + df[10][i])
    - 1*0.44*(0.44+(0.56*0.7)) * (df[16][i] - df[15][i])
    + 1 * (1 - 0.7) * (df[20][i] - df[18][i]) 
    + 1 * 0.7 * df[18][i]
    + 1 * df[25][i]
    + 1 * 0.7 *  df[26][i]
    - (df[28][i] * (df[29][i]/df[15][i])
    - 0.44 * (df[29][i] / df[16][i]) * 1))
    uper = round(uper, 3)
    uper = float(uper)
    if math.isnan(uper):
        uper = 0
        uPER.append(uper)
    elif math.isinf(uper):
        uper = 0
        uPER.append(uper)
    else:
        uPER.append(uper)

df2 = pd.DataFrame({'EFF': df[30],'uPER': uPER})

def main():
    fig = plt.figure()
    plt.title("Evaluation Comparison")
    plt.scatter(df2['EFF'], df2['uPER'])
    plt.xlabel("EFF")
    plt.ylabel("uPER")
    plt.savefig('result.png')
    plt.show()

if __name__ == "__main__":
    main()