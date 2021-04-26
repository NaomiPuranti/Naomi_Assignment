# from typing import Optional
from fastapi import FastAPI
from urllib.request import urlopen
from pandas.io.json import json_normalize
import json
import urllib
import pandas as pd
import numpy as np

app = FastAPI()

data = []
url = 'https://date.nager.at/api/v2/PublicHolidays/2017/AT'
response = urllib.request.urlopen(url)
data.extend(json.load(response))
df = pd.DataFrame(data)
df['month'] = df['date'].str[5:7]
#Define Conditions
conditions = [
(df['month'] == '01'),
(df['month'] == '04'),
(df['month'] == '05'),
(df['month'] == '06'),
(df['month'] == '08'),
(df['month'] == '10'),
(df['month'] == '11'),
(df['month'] == '12'),
]
#Define Condition Name
label = ['Januari','April','Mei','Juni','Agustus','Oktober','November','Desember']
#Assign label and condition
df['month'] = np.select(conditions, label)

df.rename(columns = {'fixed' : 'public holiday every year on the same date', 'global' : 'public holiday in every county (federal state)'}, inplace = True)
df = df[['date','public holiday every year on the same date','public holiday in every county (federal state)','launchYear','localName','name','type','month']]


@app.get('/')
def read_root():
    return {"Naomi": "Hello World"}

@app.get('/JumlahHariLiburDalamSetahun')
def Hari_Libur():
    a = df.groupby('month').count()
    return a.to_dict(orient='dict')

@app.get('/NamaHariLibur')
def Nama_Hari_Libur():
    b = df.groupby('public holiday every year on the same date').count()
    return b.to_dict(orient='dict')

@app.get('/KeteranganHariLiburPadaSetiapTahun')
def Keterangan_Hari_Libur():
    c = df.groupby('name').count()
    return c.to_dict(orient='dict')


