import subprocess as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys,os

if os.path.exists('./data.csv'):
  df = pd.read_csv('data.csv')
else:
  # sp.call("wget https://raw.githubusercontent.com/kanako68/medicalworkers/main/data.csv")
  df = pd.read_csv('https://raw.githubusercontent.com/kanako68/medicalworkers/main/data.csv')
  import subprocess as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys,os

if os.path.exists('./data.csv'):
  df = pd.read_csv('data.csv')
else:
  df = pd.read_csv('https://raw.githubusercontent.com/kanako68/medicalworkers/main/data.csv')
  population = pd.read_csv('https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv')
  
df = df[["Location","Period","FactValueNumeric"]]
population = population[["Location","Time","PopTotal"]]
population[['Time', 'PopTotal']] = population[['Time', 'PopTotal']].astype('int')
population["PopTotal"] = population["PopTotal"]*1000

#国リストに国入れる
countries=[]
for i in df.Location:
  if i not in countries :
    countries.append(i)
# print(len(countries),': ',countries)
print(len(countries))

kari=sys.argv

#ナンバーリスト
no=len(kari)-1
cnt=[]
pop=[]
print(no)
#国リストに入力値があったらプリントして、gropbyしてcntリストに入れる

for i in range(no):
  if kari[i+1] in countries:
    print(kari[i+1])
    pop.append(population.groupby('Location').get_group(kari[i+1]))
    cnt.append(df.groupby('Location').get_group(kari[i+1]))
  else: 
    print('correct the name of ',kari[i+1])
print(len(pop))

x=[]
for i in range(2010,2021):
  x.append(i)
print(x)

#リストに変換・欠損地埋める
#リストに変換・欠損地埋める
newdata=[]
newpopdata=[]
x=[]
for i in range(2010,2021):
  x.append(int(i))

for j in range(len(cnt)):
  df=cnt[j]
  df=df.loc[: , ['Period','FactValueNumeric']]
  print(df)
  new = sorted(df.values.tolist())
  cntry=[]
  no=0
  
  print(len(new))
  for i in range(2010,2021):
    if no >= len(new) or i not in new[no]:
      cntry.append(0)
      # print('0')
    else:
      cntry.append(new[no][1])
      no+=1    
  print("cntry",cntry)
  newdata.append(cntry)

for j in range(len(pop)):

  pop_=pop[j]
  pop_=pop_.loc[: , ['Time','PopTotal']]
  newpop = sorted(pop_.values.tolist())
  cntry=[]
  pop_list=[]
  no=0
  # print(newpop)
  

  for i in range(len(newpop)):
    if no >= len(x) or x[no] not in newpop[i]:
      pass
    else:
      pop_list.append(newpop[i][1])  
      no+=1

  print("pop",pop_list)
  newpopdata.append(pop_list)

cal=[]
df_ = pd.DataFrame(newdata).replace([0], np.nan).T
print(df_)
medi=sum((df_.fillna(method='ffill').fillna(method='bfill').T).values.tolist(), [])
pop = sum(newpopdata,[])
for j in range(len(medi)):
  medi[j] = int(medi[j])
  cal.append(pop[j]/medi[j])
print(cal)

if len(cnt)==1:
  plt.plot(x,cal,'k-',label=kari[1])
if len(cnt)==2:
  plt.plot(x,cal[0:11],'k-',label=kari[1])
  plt.plot(x,cal[11:22],'k--',label=kari[2])
if len(cnt)==3:
  plt.plot(x,cal[0:11],'k-',label=kari[1])
  plt.plot(x,cal[11:22],'k--',label=kari[2])
  plt.plot(x,cal[22:33],'k:',label=kari[3])
if len(cnt)==4:
  plt.plot(x,cal[0:11],'k-',label=kari[1])
  plt.plot(x,cal[11:22],'k--',label=kari[2])
  plt.plot(x,cal[22:33],'k:',label=kari[3])
  plt.plot(x,cal[33:44],'k-.',label=kari[4])


def main():
  plt.legend()
  plt.savefig('result.png')
  plt.yticks( np.arange(min(cal), max(cal),  (max(cal)-min(cal))/15))
  plt.show()
  
if __name__ == "__main__":
  main()
df = df[["Location","Period","FactValueNumeric"]]

#国リストに国入れる
countries=[]
for i in df.Location:
  if i not in countries :
    countries.append(i)
# print(len(countries),': ',countries)
print(len(countries))

kari=sys.argv
# kari=['unti','Japan','Yemen','New Zealand','India']
no=len(kari)-1
print(kari)

#ナンバーリスト
no=len(kari)-1
cnt=[]
print(no)
#国リストに入力値があったらプリントして、gropbyしてcntリストに入れる

for i in range(no):
  if kari[i+1] in countries:
    print(kari[i+1])
    # cnt.append(df.loc[df.Location==kari[i+1]])
    cnt.append(df.groupby('Location').get_group(kari[i+1]))
    # print(cnt)
  else: 
    print('correct the name of ',kari[i+1])

# print(cnt)

#リストに変換・欠損地埋める
newdata=[]
for j in range(len(cnt)):
  df=cnt[j]
  df=df.loc[: , ['Period','FactValueNumeric']]
  print(df)
  new = sorted(df.values.tolist())
  cntry=[]
  no=0
  

  for i in range(2010,2021):
    if no >= len(new) or i not in new[no]:
      cntry.append(0)
    else:
      cntry.append(new[no][1])  
      no+=1    
  newdata.append(cntry)

# print(newdata)
print(len(newdata))

df_ = pd.DataFrame(newdata).replace([0], np.nan).T
# print(df_)
pltdata=sum((df_.fillna(method='ffill').fillna(method='bfill').T).values.tolist(), [])
print(pltdata)
print(len(pltdata))

x=[]
for i in range(2010,2021):
  x.append(i)

if len(cnt)==1:
  plt.plot(x,pltdata,'k-',label=kari[1])
if len(cnt)==2:
  plt.plot(x,pltdata[0:11],'k-',label=kari[1])
  plt.plot(x,pltdata[11:22],'k--',label=kari[2])
if len(cnt)==3:
  plt.plot(x,pltdata[0:11],'k-',label=kari[1])
  plt.plot(x,pltdata[11:22],'k--',label=kari[2])
  plt.plot(x,pltdata[22:33],'k:',label=kari[3])
if len(cnt)==4:
  plt.plot(x,pltdata[0:11],'k-',label=kari[1])
  plt.plot(x,pltdata[11:22],'k--',label=kari[2])
  plt.plot(x,pltdata[22:33],'k:',label=kari[3])
  plt.plot(x,pltdata[33:44],'k-.',label=kari[4])


def main():
  plt.legend()
  plt.savefig('result.png')
  plt.yticks( np.arange(min(pltdata), max(pltdata),  (max(pltdata)-min(pltdata))/10))
  plt.show()
  
if __name__ == "__main__":
  main()