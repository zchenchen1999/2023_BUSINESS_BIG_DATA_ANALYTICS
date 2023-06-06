import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df_total_monthly = pd.read_excel('月頻total內外部資料.xlsx')
df_sentra_monthly = pd.read_excel('月頻sentra內外部資料.xlsx')
df_kicks_monthly = pd.read_excel('月頻kicks內外部資料.xlsx')
df_total_weekly = pd.read_excel('週頻total內外部資料.xlsx')
df_sentra_weekly = pd.read_excel('週頻sentra內外部資料.xlsx')
df_kicks_weekly = pd.read_excel('週頻kicks內外部資料.xlsx')



# app: sidebar
optionName = st.sidebar.selectbox(
    '品牌名稱',
    ('Nissan', 'Kicks', 'Sentra'))

optionTime = st.sidebar.selectbox(
    '資料時間頻率',
    ('週頻', '月頻'))

optionVariable = st.sidebar.selectbox(
    '內部資料變數',
    ('來店數', '交車數'))

if optionTime == '週頻':
  optionCor = st.sidebar.multiselect(
      '外部資料變數（可多選）',
      ('當週總文章數', '前一週總文章數', '前二週總文章數', '前三週總文章數', '當週文章正向比例', '當週文章負向比例', '前一週文章正向比例', '前一週文章負向比例', '前二週文章正向比例', '前二週文章負向比例', '前三週文章正向比例', '前三週文章負向比例')
      )
else :
  optionCor = st.sidebar.multiselect(
    '外部資料變數',
    ('當月總文章數', '前一月總文章數', '前二月總文章數', '前三月總文章數', '前四月總文章數', '當月文章正向比例', '當月文章負向比例', '前一月文章正向比例', '前一月文章負向比例', '前二月文章正向比例', '前二月文章負向比例', '前三月文章正向比例', '前三月文章負向比例', '前四月文章正向比例', '前四月文章負向比例')
    )



# app: 給出對應資料  
if optionName == 'Nissan':
  if optionTime == '月頻':
    data = df_total_monthly
  elif optionTime == '週頻':
    data = df_total_weekly
if optionName == 'Kicks': 
  if optionTime == '月頻':
    data = df_kicks_monthly
  elif optionTime == '週頻':
    data = df_kicks_weekly
if optionName == 'Sentra':
  if optionTime == '月頻':
    data = df_sentra_monthly
  elif optionTime == '週頻':
    data = df_sentra_weekly

if optionTime == '月頻':
  date = '當期月份'
elif optionTime == '週頻':
  date = '當期週數'

# Streamlit App
st.title('Nissan內外部相關性')


# 給出對應的表格
chart_data = pd.DataFrame(data[[date, optionVariable, *optionCor]])
rows = st.columns(2)
rows[0].markdown("### Data")
rows[0].dataframe(chart_data)
rows[1].markdown("### 相關係數")
rows[1].dataframe(chart_data.corr())


# 建立子圖
st.header(optionName + '\t' + optionTime + '\t' + '內外部相關性趨勢圖')
fig = make_subplots(specs=[[{"secondary_y": True}]])

# 添加長條圖
fig.add_trace(go.Bar(x=chart_data[date], y=chart_data[optionVariable], name=optionVariable, marker_color='grey'), secondary_y=False)

# 添加折線圖
for cor in optionCor:
  fig.add_trace(go.Scatter(x=chart_data[date], y=chart_data[cor], name=cor), secondary_y=True)

# 設定圖表標題和軸標籤
fig.update_xaxes(title_text=date)
fig.update_yaxes(title_text=optionVariable, secondary_y=False)
fig.update_layout(xaxis_tickangle=45)



# 顯示圖表
st.plotly_chart(fig)


