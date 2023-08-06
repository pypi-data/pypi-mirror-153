import subprocess as sp
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import sys,os
import pandas as pd
import math

if os.path.exists('./API_ST.INT.RCPT.CD_DS2_en_excel_v2_4150995.xlsx'):
 print('if!!!')
 wb=openpyxl.load_workbook('API_ST.INT.RCPT.CD_DS2_en_excel_v2_4150995.xlsx')
else:
 print('else!!!!')
 sp.call("wget -O mydata.xls https://api.worldbank.org/v2/en/indicator/ST.INT.RCPT.CD?downloadformat=excel",shell=True)
 df=pd.read_excel('mydata.xls',header=None)
 df.to_excel('mydata.xlsx',index=False)
 wb=openpyxl.load_workbook('mydata.xlsx')
sheet=wb['Sheet1']
sheet.delete_rows(sheet.min_row,4)
wb.save('resultconan.xlsx')
pd_tmp=pd.read_excel('resultconan.xlsx',sheet_name='Sheet1')
size=0
countries=[]
d=pd_tmp.rename(columns={'Country Name':'Country'})
d.info()
for i in d.Country:
 if i!='Yemen':
  countries.append(i)
  size=size+1
 else:
  countries.append(i)
  size=size+1
  break
print(len(countries),':',countries)
no=len(sys.argv)-1
x=[]
for i in range(1995,2020):
 x.append(i)
cnt=[]
for i in range(no):
 if sys.argv[i+1]in countries:
  #print(sys.argv[i+1])
  cnt.append(d.loc[d.Country==sys.argv[i+1]])
 else:
  print('correct the name of ',sys.argv[i+1])
cntry=[]
#print(len(cnt))
for j in range (len(cnt)):
 for i in range (1995,2020):
  if (math.isnan(cnt[j][i])):
   cntry.append(int(0))
  else:
   cntry.append(int(cnt[j][i]))
print(cntry)
data_num=2020-1995
if len(cnt)==1:
 plt.plot(x,cntry,'k-',label=sys.argv[1])
if len(cnt)==2:
 plt.plot(x,cntry[0:25],'k-',label=sys.argv[1])
 plt.plot(x,cntry[25:50],'k--',label=sys.argv[2])
if len(cnt)==3:
 plt.plot(x,cntry[0:25],'k-',label=sys.argv[1])
 plt.plot(x,cntry[25:50],'k--',label=sys.argv[2])
 plt.plot(x,cntry[50:75],'k:',label=sys.argv[3])
if len(cnt)==4:
 plt.plot(x,cntry[0:25],'k-',label=sys.argv[1])
 plt.plot(x,cntry[25:50],'k--',label=sys.argv[2])
 plt.plot(x,cntry[50:75],'k:',label=sys.argv[3])
 plt.plot(x,cntry[75:100],'k-.',label=sys.argv[4])


def main():
 plt.legend()
 plt.savefig('result.png')
 plt.show()

if __name__ == "__main__":
 main()

