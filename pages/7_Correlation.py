# 負責人：詣超
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from st_files_connection import FilesConnection

# 預設顯示 wide mode
st.set_page_config(page_title="Nissan 內外部相關性分析", layout="wide", page_icon="📈")

# 設定資料連結
conn = st.experimental_connection('gcs', type=FilesConnection)

@st.cache_data(persist=True)  # 👈 Add the caching decorator
def load_data(url):
    csv_data = conn.read(url, input_format="csv", ttl=None)
    return csv_data

# title
st.title("Nissan 內外部相關性分析")

# app: sidebar
st.sidebar.subheader("參數調整")
optionName = st.sidebar.selectbox(
    '關鍵字',
    ('Nissan', 'Kicks', 'Sentra'))

optionVariable = st.sidebar.selectbox(
    '內部資料變數',
    ('來店數', '交車數'))

optionFrequency = st.sidebar.selectbox(
    '資料時間頻率',
    ('週頻', '月頻'))

if optionFrequency == '月頻':
  optionCor = st.sidebar.multiselect(
    '外部資料變數（可多選）',
    ('當月總文章數', '前一月總文章數', '前二月總文章數', '前三月總文章數', '前四月總文章數', '當月文章正向比例', '當月文章負向比例', '前一月文章正向比例', '前一月文章負向比例', '前二月文章正向比例', '前二月文章負向比例', '前三月文章正向比例', '前三月文章負向比例', '前四月文章正向比例', '前四月文章負向比例')
    )

elif optionFrequency == '週頻':
  optionCor = st.sidebar.multiselect(
      '外部資料變數（可多選）',
      ('當週總文章數', '前一週總文章數', '前二週總文章數', '前三週總文章數', '當週文章正向比例', '當週文章負向比例', '前一週文章正向比例', '前一週文章負向比例', '前二週文章正向比例', '前二週文章負向比例', '前三週文章正向比例', '前三週文章負向比例')
      )
  

# app: 給出對應資料  
if optionName == 'Nissan':
  if optionFrequency == '月頻':
    data = load_data("big-data-class-2023/correlation/月頻total內外部資料.csv")
  elif optionFrequency == '週頻':
    data = load_data("big-data-class-2023/correlation/週頻total內外部資料.csv")
if optionName == 'Kicks': 
  if optionFrequency == '月頻':
    data = load_data("big-data-class-2023/correlation/月頻kicks內外部資料.csv")
  elif optionFrequency == '週頻':
    data = load_data("big-data-class-2023/correlation/週頻kicks內外部資料.csv")
if optionName == 'Sentra':
  if optionFrequency == '月頻':
    data = load_data("big-data-class-2023/correlation/月頻sentra內外部資料.csv")
  elif optionFrequency == '週頻':
    data = load_data("big-data-class-2023/correlation/週頻sentra內外部資料.csv")


# sidebar condition
if optionFrequency == '月頻':
  date = '當期月份'
  date_int = '當期月份_int'
  default_value = 202301

elif optionFrequency == '週頻':
  date = '當期週數'
  date_int = '當期週數_int'
  default_value = 202305

# app: sidebar
if optionFrequency == '月頻':
  optionStartTime = st.sidebar.selectbox(
      '起始時間(月)',
      data[[date_int]])
  optionEndTime = st.sidebar.selectbox(
      '結束時間(月)',
      data[[date_int]],
      index=data[date_int].tolist().index(default_value))
elif optionFrequency == '週頻':
  optionStartTime = st.sidebar.selectbox(
      '起始時間(週)',
      data[[date_int]])
  optionEndTime = st.sidebar.selectbox(
      '結束時間(週)',
      data[[date_int]],
      index=data[date_int].tolist().index(default_value))

# 防呆機制：結束月份不能選擇比起始月份還前面的日期
if int(optionEndTime) < int(optionStartTime):
    st.sidebar.error("結束月份不能早於起始月份")

# 給出對應的表格
raw_chart_data = pd.DataFrame(data[[date, optionVariable, *optionCor, date_int]])
chart_data = raw_chart_data[(raw_chart_data[date_int] >= optionStartTime) & (raw_chart_data[date_int] <= optionEndTime)].drop(columns=[date_int])
rows = st.columns(2)
rows[0].markdown("#### Data")
rows[0].dataframe(chart_data, use_container_width=True)
rows[1].markdown("#### 相關係數矩陣")
rows[1].dataframe(chart_data.corr(), use_container_width=True)


# 建立子圖
st.subheader(optionName + '\t`' + optionFrequency + '`\t' + '內外部相關性趨勢圖')
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
st.plotly_chart(fig, use_container_width=True)
