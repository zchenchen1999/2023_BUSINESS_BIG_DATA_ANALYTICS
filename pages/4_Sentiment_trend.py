# 負責人：誠哲

import streamlit as st
import pandas as pd
import plotly.express as px
from st_files_connection import FilesConnection

# 預設顯示 wide mode
st.set_page_config(page_title="品牌網路情緒趨勢", layout="wide", page_icon="📈")

# 雲端讀取檔案
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

# #讀取品牌ptt資料
# ford = pd.read_csv('/Users/jerry/Downloads/CM505_App/data/ford_clean_data.csv')
# honda = pd.read_csv('/Users/jerry/Downloads/CM505_App/data/honda_clean_data.csv')
# mazda = pd.read_csv('/Users/jerry/Downloads/CM505_App/data/mazda_clean_data.csv')
# toyota = pd.read_csv('/Users/jerry/Downloads/CM505_App/data/toyota_clean_data.csv')
# nissan = pd.read_csv('/Users/jerry/Downloads/CM505_App/data/nissan_clean_data.csv')

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
st.sidebar.subheader('參數調整')
selected_brands = st.sidebar.multiselect('選擇品牌', brand_list, default=['Nissan'])


# 選擇月份
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



# 選擇正負向文章
sentiment_list = ['正向', '負向']
selected_sentiment = st.sidebar.multiselect('選擇文章情緒類別', sentiment_list, default=['正向', '負向'])

if (selected_brands and selected_sentiment):
    # Filter dataframe based on selected sentimentRatio
    if '正向' in selected_sentiment:
        df_filtered_sentiment_positive = df_select[df_select['sentimentRatio'] > 0.6]
    else:
        df_filtered_sentiment_positive = pd.DataFrame(columns=df_select.columns)  # 空的 DataFrame

    if '負向' in selected_sentiment:
        df_filtered_sentiment_negative = df_select[df_select['sentimentRatio'] < 0.4]
    else:
        df_filtered_sentiment_negative = pd.DataFrame(columns=df_select.columns)  # 空的 DataFrame

    df_filtered_sentiment_positive['artDate'] = pd.to_datetime(df_filtered_sentiment_positive['artDate'])
    df_filtered_sentiment_negative['artDate'] = pd.to_datetime(df_filtered_sentiment_negative['artDate'])

    # Group by brand, artDate, and sentiment, then calculate total volume
    brand_sentiment_count_positive = df_filtered_sentiment_positive.groupby(['Brand', pd.Grouper(key='artDate', freq='M', sort=False)])['Brand'].count().reset_index(name='count').rename(columns={'count': 'positive_count'})

    brand_sentiment_count_negative = df_filtered_sentiment_negative.groupby(['Brand', pd.Grouper(key='artDate', freq='M', sort=False)])['Brand'].count().reset_index(name='count').rename(columns={'count': 'negative_count'})

    # Calculate total count for each brand and date
    brand_total_count = df_select.groupby(['Brand', pd.Grouper(key='artDate', freq='M', sort=False)])['Brand'].count().reset_index(name='total_count')

    # Merge positive and negative counts
    brand_sentiment_count_merged = pd.merge(brand_sentiment_count_positive, brand_sentiment_count_negative, on=['Brand', 'artDate'], how='outer').fillna(0)
    # Merge positive and negative counts with total count
    brand_sentiment_ratio = pd.merge(brand_sentiment_count_merged, brand_total_count, on=['Brand', 'artDate'], how='left')
    # Calculate sentiment ratio
    brand_sentiment_ratio['positive_ratio'] = brand_sentiment_ratio['positive_count'] / brand_sentiment_ratio['total_count']
    brand_sentiment_ratio['negative_ratio'] = brand_sentiment_ratio['negative_count'] / brand_sentiment_ratio['total_count']

   
    # # Pivot the table to have sentimentRatio as columns
    # brand_sentiment_count_pivot = brand_sentiment_count_merged.pivot_table(index='artDate',
    #                                                                       columns='Brand',
    #                                                                       values='count',
    #                                                                       fill_value=0)

    # # Plot line chart
    # fig = px.line(brand_sentiment_count_pivot, x=brand_sentiment_count_pivot.index, y=selected_sentiment,
    #               color_discrete_map={"positive": "green", "negative": "red"},
    #               title="品牌情緒趨勢")
    # fig = px.line(brand_sentiment_count_merged, x="artDate", y=selected_sentiment,
    #               color_discrete_map={"positive": "green", "negative": "red"},
    #               title="品牌情緒趨勢")

    # fig.update_layout(
    #     xaxis_title="月份",
    #     yaxis_title="文章數量",
    #     title="品牌情緒趨勢"
    # )

    # st.plotly_chart(fig)

    # fig.update_layout(
    #     xaxis_title="月份",
    #     yaxis_title="文章數量",
    #     title="品牌情緒趨勢"
    # )
    # st.plotly_chart(fig)


    brand_sentiment_count_merged.rename(columns = {'Brand':'品牌', 'artDate':'發文日期', 'positive_count':'正向', 'negative_count':'負向'}, inplace = True)
    brand_sentiment_melt = pd.melt(brand_sentiment_count_merged, id_vars=['品牌', '發文日期'], value_vars=['正向', '負向'])

    brand_sentiment_ratio.rename(columns = {'Brand':'品牌', 'artDate':'發文日期', 'positive_ratio':'正向', 'negative_ratio':'負向'}, inplace = True)
    # Melt the dataframe for plotting
    brand_sentiment_melt_ratio = pd.melt(brand_sentiment_ratio, id_vars=['品牌', '發文日期'], value_vars=['正向', '負向'])
    #print(brand_sentiment_melt_ratio)

    # 以情緒為主 => 查看品牌
    st.markdown("#### 不同品牌間情緒比較")
    sentiment_tabs = st.tabs(sentiment_list)
    for i in range (len(sentiment_tabs)):
        #tmp_df = brand_sentiment_melt[brand_sentiment_melt['variable'] == sentiment_list[i]]
        tmp_df = brand_sentiment_melt_ratio[brand_sentiment_melt_ratio['variable'] == sentiment_list[i]]
        fig = px.line(tmp_df, x="發文日期", y="value", color="品牌",title=sentiment_list[i])
        fig.update_layout(
            xaxis_title="月份",
            yaxis_title="比率"
        )
        sentiment_tabs[i].plotly_chart(fig, use_container_width=True)

    st.sidebar.divider()
    # 以品牌為主 => 查看正向情緒與負向情緒
    st.markdown("#### 品牌正負情緒比較")
    brand_tabs = st.tabs(selected_brands)
    for i in range (len(brand_tabs)):
        tmp_df = brand_sentiment_melt[brand_sentiment_melt['品牌'] == selected_brands[i]]
        fig = px.line(tmp_df, x="發文日期", y="value", color="variable",title=selected_brands[i])
                #   color_discrete_map={"positive": "green", "negative": "red"},
        fig.update_layout(
            xaxis_title="月份",
            yaxis_title="文章數量"
        )
        brand_tabs[i].plotly_chart(fig, use_container_width=True)
        brand_tabs[i].dataframe(brand_sentiment_count_merged[brand_sentiment_count_merged['品牌'] == selected_brands[i]], use_container_width=True)
else:
    st.error("請至少選擇一項品牌與情緒")