import streamlit as st

# 預設顯示 wide mode
st.set_page_config(layout="wide")

# 負責人：伊廷

import streamlit as st
from st_files_connection import FilesConnection
import pandas as pd
import plotly.express as px

conn = st.experimental_connection('gcs', type=FilesConnection)

@st.cache_data(persist=True)  # 👈 Add the caching decorator
def load_data(url):
    csv_data = conn.read(url, input_format="csv", ttl=None)
    return csv_data
    
# 讀取品牌ptt資料
nissan = load_data("big-data-class-2023/nissan_clean_data.csv")
toyota = load_data("big-data-class-2023/toyota_clean_data.csv")
ford = load_data("big-data-class-2023/ford_clean_data.csv")
honda = load_data("big-data-class-2023/honda_clean_data.csv")
mazda = load_data("big-data-class-2023/mazda_clean_data.csv")

# 新增品牌欄位
ford = ford.assign(Brand='Ford')
honda = honda.assign(Brand='Honda')
mazda = mazda.assign(Brand='Mazda')
nissan = nissan.assign(Brand='Nissan')
toyota = toyota.assign(Brand='Toyota')

# 資料框合併
df_interact = pd.concat([ford, honda, mazda, nissan, toyota], ignore_index=True)

# 轉換日期欄位為 datetime
df_interact['artDate'] = pd.to_datetime(df_interact['artDate'],format='%Y-%m-%d')

# Set header title
st.title('品牌網路聲量趨勢')
st.markdown('聲量：該月份的PTT文章總數')

# Define list of selection options and sort alphabetically
brand_list = ['Nissan', 'Toyota', 'Ford', 'Honda', 'Mazda']
brand_list.sort()

# Implement multiselect dropdown menu for option selection (returns a list)
st.sidebar.title('選擇品牌')
selected_brands = st.sidebar.multiselect('選擇品牌', brand_list, default=['Nissan'])

st.sidebar.divider()  # 分隔線

# 選擇月份
st.sidebar.title('選擇月份區間')
st.sidebar.caption('有效月份範圍：2020-12 - 2023-01')

# 取得所有的月份選項
all_months = pd.period_range(start='2020-12', end='2023-01', freq='M')

# 轉換日期選項為字串格式
month_options = [str(month) for month in all_months]

# 選擇資料起始月份
selected_beginning_month = st.sidebar.selectbox(
    "選擇資料起始月份",
    month_options, index=0    # 設定預設選項為索引 0，即 2020-12
)

# 選擇資料結束月份
selected_ending_month = st.sidebar.selectbox(
    "選擇資料結束月份",
    month_options, index=len(month_options)-1   # 設定預設選項為索引最大值，即 2023-1
)

# 將選擇的月份轉換為 datetime 格式
selected_beginning_date = pd.to_datetime(selected_beginning_month, format='%Y-%m')
selected_ending_date = pd.to_datetime(selected_ending_month, format='%Y-%m')

# 防呆機制：結束月份不能選擇比起始月份還前面的日期
if selected_ending_date < selected_beginning_date:
    st.sidebar.error("結束月份不能早於起始月份")

# Filter the dataframe based on selected brands and dates
df_select = df_interact.loc[(df_interact['Brand'].isin(list(selected_brands))) &
                            (df_interact['artDate'].dt.to_period('M') >= selected_beginning_date.to_period('M')) &
                            (df_interact['artDate'].dt.to_period('M') <= selected_ending_date.to_period('M'))]

# Group by brand & artDate, then calculate total volume
brand_volume = df_select.groupby(['Brand', df_select['artDate'].dt.to_period('M').astype(str)])['system_id'].count().reset_index()

# Plot line chart
fig = px.line(brand_volume, x="artDate", y="system_id", color="Brand")
fig.update_layout(
    xaxis_title="月份",
    yaxis_title="網路聲量",
    title="品牌網路聲量趨勢"
)
st.plotly_chart(fig, use_container_width = True)

st.dataframe(
    df_select[["artTitle", "artDate", "artCatagory", "artContent", "Brand"]],
    columns={
        "artTitle": "文章標題",
        "artDate": "發文日期",
        "artCatagory": "文章版面",
        "artContent": "文章內容",
        "Brand": "品牌",
    },
    hide_index=True,
)