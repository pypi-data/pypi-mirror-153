from PIL import Image
import sys
import csv
import requests,re
import pandas as pd
import subprocess as sp

def main():
 url_1='https://www.worldometers.info/world-population/population-by-country/'
 print('scraping population...')
 page_1=requests.get(url_1)
 df1 = pd.read_html(page_1.text)[0]
 df1.columns.values[1]='Country'
 df1.columns.values[2]='Population'
 #df = pd.read_html(page.text,flavor='html5lib')[0]
 df1.to_csv('pop.csv')
 print('pop.csv was created')

# print('downloading total_deaths.csv file')
# import subprocess as sp
# sp.call("wget https://github.com/owid/covid-19-data/raw/master/public/data/jhu/total_deaths.csv",shell=True)
# p=pd.read_csv('total_deaths.csv')
# date=p['date'][len(p)-1]


 url_2='https://www.worldometers.info/energy/'
 print('scraping energy...')
 page_2=requests.get(url_2)
 df2 = pd.read_html(page_2.text)[0]
 df2.columns.values[1]='country'
 df2.columns.values[2]='energy_consumption'
 p=df2.to_csv('energy.csv')
 print('energy.csv was created')

#
#from urllib.request import Request, urlopen
#url='https://www.worldometers.info/coronavirus/#nav-today/'
#print('scraping deaths informationi...')
#req = Request(url, headers={'User-Agent': 'Firefox/76.0.1'})
#page = re.sub(r'<.*?>', lambda g: g.group(0).upper(), urlopen(req).read().decode('utf-8') )
#df = pd.read_html(page)[0]
#df.to_csv('deaths.csv')
#print('deaths.csv was created')
#
 import os.path
 if os.path.exists('countries'):
  print('countries file was read...')
  d=open('countries').read().strip()
  d=d.split(',')
 else:
  sp.call("wget https://github.com/ytakefuji/score-covid-19-policy/raw/main/countries",shell=True)
  print('countries file was read...')
  d=open('countries').read().strip()
  d=d.split(',')
 print('scoring the following ',len(d),' countries...')
 print(d)
 
 dd=pd.DataFrame(
  { 
   "country": d,
   "population": range(len(d)),
   "energy_consumption": range(len(d)),
   "per_capital_yearly": range(len(d)),
  })
 
 pp=pd.read_csv('pop.csv')
 ee=pd.read_csv('energy.csv')
 print('calculating scores of countries\n')
 print('score is created in result.csv')
# print('date is ',date)
# print(type(p["energy_consumption"].dtype))
 
 for i in d:
  dd.loc[dd.country==i,'population']=int(pp.loc[pp.Country==i,'Population'])
  dd.loc[dd.country==i,'energy_consumption']=int(ee.loc[ee.country==i,'energy_consumption'])
  dd.loc[dd.country==i,'per_capital_yearly']=round(int(ee.loc[ee.country==i,'energy_consumption'])/int(pp.loc[pp.Country==i,'Population']))
 dd=dd.sort_values(by=['per_capital_yearly'])
 dd.to_csv('result.csv',index=False)
 dd=pd.read_csv('result.csv',index_col=0)
 print(dd)
 sp.call("rm energy.csv pop.csv",shell=True)
 
# csv to png
# with open('result.csv') as f:
#  reader = csv.reader(f)
#  l = [row for row in reader]
# l_t = [list(x) for x in zip(*l)]
#
# w = int(len(l[0]))
# h = int(len(l))
# size = (w, h)
#
# img = Image.new('L', size)
# for x in range(0, w):
#  for y in range(0, h):
#   img.putpixel((x, y), int(l_t[x][y]))
# img.save('result.png')
 

if __name__ == "__main__":
 main()
