# 負責人：誠哲
'''
import streamlit as st
import pandas as pd
import datetime
from pyvis.network import Network
import plotly.express as px

# 預設顯示 wide mode
st.set_page_config(layout="wide")

# title
st.title("品牌情緒趨勢圖")

## content
# Read dataset (CSV)
df_interact = pd.read_csv('/Users/jerry/Downloads/CM505_App/data/ptt_data.csv')

# 轉換日期欄位為 datetime
df_interact['artDate'] = pd.to_datetime(df_interact['artDate'], format='%Y-%m-%d')

# Set header title
st.title('品牌網路情緒趨勢')
st.markdown('情緒：該月份的PTT情緒總數')

# Define list of selection options and sort alphabetically
brand_list = ['Ford', 'Honda', 'Mazda', 'Toyota', 'Nissan']
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

# Filter the dataframe based on selected brands and dates
df_select = df_interact.loc[(df_interact['Brand'].isin(list(selected_brands))) &
                            (df_interact['artDate'].dt.to_period('M') >= selected_beginning_date.to_period('M')) &
                            (df_interact['artDate'].dt.to_period('M') <= selected_ending_date.to_period('M'))]

st.sidebar.divider() #分隔線

# 選擇正負向文章
st.sidebar.title('選擇正負向文章類別')
sentiment_list = ['positive', 'negative']
selected_sentiment = st.sidebar.multiselect('選擇正向或負向類別', sentiment_list, default=['positive'])

# Filter dataframe based on selected sentimentRatio
df_filtered_sentiment = df_select[(df_select['sentimentRatio'] > 0.6) | (df_select['sentimentRatio'] < 0.4)]

# Group by brand, artDate, and sentiment, then calculate total volume
brand_sentiment_count = df_filtered_sentiment.groupby(['Brand', df_filtered_sentiment['artDate'].dt.to_period('M').astype(str)])['artUrl'].count().reset_index()

# Pivot the data to have sentiment as columns
brand_sentiment_count_pivot = brand_sentiment_count.pivot_table(index=['Brand', 'artDate'],
                                                               columns='sentimentRatio',
                                                               values='artUrl',
                                                               fill_value=0).reset_index()

# Plot line chart
fig = px.line(brand_sentiment_count_pivot, x="artDate", y=selected_sentiment,
              color="Brand", title="品牌情緒趨勢")

fig.update_layout(
    xaxis_title="月份",
    yaxis_title="文章數量",
    title="品牌情緒趨勢"
)
st.plotly_chart(fig)
'''

import streamlit as st
import pandas as pd
import plotly.express as px

# 預設顯示 wide mode
st.set_page_config(layout="wide")

#讀取品牌ptt資料
ford = pd.read_csv('/Users/jerry/Downloads/CM505_App/data/ford_clean_data.csv')
honda = pd.read_csv('/Users/jerry/Downloads/CM505_App/data/honda_clean_data.csv')
mazda = pd.read_csv('/Users/jerry/Downloads/CM505_App/data/mazda_clean_data.csv')
toyota = pd.read_csv('/Users/jerry/Downloads/CM505_App/data/toyota_clean_data.csv')
nissan = pd.read_csv('/Users/jerry/Downloads/CM505_App/data/nissan_clean_data.csv')

#新增品牌欄位
ford = ford.assign(Brand='Ford')
honda = honda.assign(Brand='Honda')
mazda = mazda.assign(Brand='Mazda')
nissan = nissan.assign(Brand='Nissan')
toyota = toyota.assign(Brand='Toyota')

# 資料框合併
df_interact = pd.concat([ford, honda, mazda, nissan, toyota], ignore_index=True)

# 轉換日期欄位為 datetime
df_interact['artDate'] = pd.to_datetime(df_interact['artDate'], format='%Y-%m-%d')

# Set header title
st.title('品牌網路情緒趨勢')
st.markdown('情緒：該月份的PTT情緒總數')

# Define list of selection options and sort alphabetically
brand_list = ['Ford', 'Honda', 'Mazda', 'Toyota', 'Nissan']
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

# Filter the dataframe based on selected brands and dates
df_select = df_interact.loc[(df_interact['Brand'].isin(list(selected_brands))) &
                            (df_interact['artDate'].dt.to_period('M') >= selected_beginning_date.to_period('M')) &
                            (df_interact['artDate'].dt.to_period('M') <= selected_ending_date.to_period('M'))]

st.sidebar.divider() #分隔線

# 選擇正負向文章
st.sidebar.title('選擇正負向文章類別')
sentiment_list = ['positive', 'negative']
selected_sentiment = st.sidebar.multiselect('選擇正向或負向類別', sentiment_list, default=['positive'])

# Filter dataframe based on selected sentimentRatio
if 'positive' in selected_sentiment:
    df_filtered_sentiment_positive = df_select[df_select['sentimentRatio'] > 0.6]
else:
    df_filtered_sentiment_positive = pd.DataFrame(columns=df_select.columns)  # 空的 DataFrame

if 'negative' in selected_sentiment:
    df_filtered_sentiment_negative = df_select[df_select['sentimentRatio'] < 0.4]
else:
    df_filtered_sentiment_negative = pd.DataFrame(columns=df_select.columns)  # 空的 DataFrame

df_filtered_sentiment_positive['artDate'] = pd.to_datetime(df_filtered_sentiment_positive['artDate'])
df_filtered_sentiment_negative['artDate'] = pd.to_datetime(df_filtered_sentiment_negative['artDate'])

# Group by brand, artDate, and sentiment, then calculate total volume
brand_sentiment_count_positive = df_filtered_sentiment_positive.groupby(['Brand', pd.Grouper(key='artDate', freq='M', sort=False)])['Brand'].count().reset_index(name='count').rename(columns={'count': 'positive_count'})

brand_sentiment_count_negative = df_filtered_sentiment_negative.groupby(['Brand', pd.Grouper(key='artDate', freq='M', sort=False)])['Brand'].count().reset_index(name='count').rename(columns={'count': 'negative_count'})


# Merge positive and negative counts
brand_sentiment_count_merged = pd.merge(brand_sentiment_count_positive, brand_sentiment_count_negative, on=['Brand', 'artDate'], how='outer').fillna(0)

# Pivot the table to have sentimentRatio as columns
brand_sentiment_count_pivot = brand_sentiment_count_merged.pivot_table(index='artDate',
                                                                      columns='Brand',
                                                                      values='count',
                                                                      fill_value=0)

# Plot line chart
fig = px.line(brand_sentiment_count_pivot, x=brand_sentiment_count_pivot.index, y=selected_sentiment,
              color_discrete_map={"positive": "green", "negative": "red"},
              title="品牌情緒趨勢")

fig.update_layout(
    xaxis_title="月份",
    yaxis_title="文章數量",
    title="品牌情緒趨勢"
)

st.plotly_chart(fig)

fig.update_layout(
    xaxis_title="月份",
    yaxis_title="文章數量",
    title="品牌情緒趨勢"
)
st.plotly_chart(fig)

