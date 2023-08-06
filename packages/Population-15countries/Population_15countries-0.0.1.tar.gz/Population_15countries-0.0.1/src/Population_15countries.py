import subprocess as sp
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import sys, os
import japanize_matplotlib


if os.path.exists('./pop_area_2009.xlsx'):
  wb = openpyxl.load_workbook('pop_area_2009.xlsx')
else:
  sp.call("wget https://atelierkobato.com/wp-content/uploads/pop_area_2009.xlsx||wget https://github.com/MiyuIwamoto/Population/blob/main/pop_area_2009.xlsx", shell=True)
  wb = openpyxl.load_workbook('pop_area_2009.xlsx')
wb.delete_rows(wb.min_row.4)
wb.save('result.xlsx')


d = pd.read_excel('result.xlsx', engine='openpyxl')
d = d.drop(columns=d.columns[0])


X = d['国名'][:15]
y = d['面積'][:15]
fig = plt.figure(figsize=(18.0, 4.0))
ax = fig.add_subplot(111)
plt.bar(X,y);
plt.title("人口TOP15の国の人口密度")
plt.xlabel("国名")
plt.ylabel("人口密度(人/km2)")
plt.savefig('result.png')
plt.show();
