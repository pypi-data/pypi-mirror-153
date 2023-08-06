# coding:utf-8
import sys
import plotly
import plotly.graph_objs as go
import plotly.offline as offline
import plotly.express as px
import subprocess as sp
import pandas as pd
import os

if os.path.exists('result.png') == True:
    sp.call("rm result.png",shell=True)

year = sys.argv[1]
url = 'https://www.data.jma.go.jp/fcd/yoho/typhoon/position_table/table'+ year + '.csv'

df = pd.read_csv(url, encoding='shift_jis')

typhoon_name = df['台風名'].unique()

num_ = 0

list_ = []

fig = go.Figure()

for i in typhoon_name:
    df_ = df[df['台風名'] == i]
    num_ = len(df[df['台風名'] == i])
    df_['length'] = range(1, num_+1)
    fig.add_trace(go.Scatter(x = df_['length'], y = df_['中心気圧'], name=i))
    fig.update_layout(xaxis=dict(title='Number of days elapsed'), yaxis=dict(title='Central pressure'))
    
fig.show()

fig.write_image("result.png")