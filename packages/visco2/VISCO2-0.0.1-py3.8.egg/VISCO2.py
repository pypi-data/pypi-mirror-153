import subprocess as sp
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import sys,os


if os.path.exists('/Dataco2.xlsx'):
 wb=openpyxl.load_workbook('Dataco2.xlsx')
else:
 sp.call("wget https://github.com/Marinakanno/data/raw/main/Dataco2.xlsx",shell=True)
 wb=openpyxl.load_workbook('Dataco2.xlsx')


sheet=wb['Data']
# sheet.delete_rows(sheet.min_row,5)
wb.save('result.xlsx')
d=pd.read_excel('result.xlsx',engine='openpyxl',sheet_name='Data')
size=0
countries=[]
for i in d.Country:
 if i!='World':
  countries.append(i)
  size=size+1
 else: 
  countries.append(i)
  size=size+1
  break
print(len(countries),': ',countries)
no=len(sys.argv)-1
x=[]
for i in range(2000,2021):
 x.append(i)
cnt=[]
for i in range(no):
 if sys.argv[i+1] in countries:
  #print(sys.argv[i+1])
  cnt.append(d.loc[d.Country==sys.argv[i+1]])
 else: 
  print('correct the name of ',sys.argv[i+1])
cntry=[]
#print(len(cnt))
for j in range(len(cnt)):
 for i in range(1990,2021):
  cntry.append(int(cnt[j][i]))
if len(cnt)==1:
 plt.plot(x,cntry,'k-',label=sys.argv[1])
if len(cnt)==2:
 plt.plot(x,cntry[0:2000],'k-',label=sys.argv[1])
 plt.plot(x,cntry[2001:4000],'k--',label=sys.argv[2])
if len(cnt)==3:
 plt.plot(x,cntry[0:2000],'k-',label=sys.argv[1])
 plt.plot(x,cntry[2001:4000],'k--',label=sys.argv[2])
 plt.plot(x,cntry[4001:6000],'k:',label=sys.argv[3])
if len(cnt)==4:
 plt.plot(x,cntry[0:2000],'k-',label=sys.argv[1])
 plt.plot(x,cntry[2001:4000],'k--',label=sys.argv[2])
 plt.plot(x,cntry[4001:6000],'k:',label=sys.argv[3])
 plt.plot(x,cntry[6001:8000],'k-.',label=sys.argv[4])
def main():
 plt.legend()
 plt.savefig('result.png')
 plt.show()
