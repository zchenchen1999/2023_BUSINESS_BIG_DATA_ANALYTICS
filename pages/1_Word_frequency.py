# 負責人：祐陞
import streamlit as st
import streamlit.components.v1 as components
from streamlit_plotly_events import plotly_events
import pandas as pd
import numpy as np
import networkx as nx
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import plotly.express as px
from wordcloud import WordCloud
from collections import Counter
from ast import literal_eval

# 預設顯示 wide mode
st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
# title
st.title("詞頻分析/文字雲")




# 設定資料連結
url1 = 'nissan_clean_data.csv'
url2 = 'ford_clean_data.csv'
url3 = 'toyota_clean_data.csv'
url4 = 'honda_clean_data.csv'
url5 = 'mazda_clean_data.csv'

# 利用catche讀取資料
@st.cache_data
def load_df(url1, url2, url3, url4, url5):
    df1 = pd.read_csv(url1)
    df2 = pd.read_csv(url2)
    df3 = pd.read_csv(url3)
    df4 = pd.read_csv(url4)
    df5 = pd.read_csv(url5)

    df1['brand'] = "Nissan"
    df2['brand'] = "Ford"
    df3['brand'] = "Toyota"
    df4['brand'] = "Honda"
    df5['brand'] = "Mazda"

    merged_df = pd.concat([df1, df2, df3, df4, df5])
    return merged_df

df_interact = load_df(url1, url2, url3, url4, url5)

# 轉換日期欄位為 datetime
df_interact['artDate'] = pd.to_datetime(df_interact['artDate'],format='%Y-%m-%d')

# Set header title
st.title('時間區間品牌網路詞頻計算')
st.markdown('文字雲')

# Define list of selection options and sort alphabetically
brand_list = ['Nissan', 'Toyota', 'Ford', 'Honda', 'Mazda']
brand_list.sort()

# Implement multiselect dropdown menu for option selection (returns a list)
st.sidebar.title('選擇品牌')
selected_brands = st.sidebar.multiselect('選擇品牌', brand_list, default=['Nissan'])

# st.sidebar.divider()  # 分隔線

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
df_select = df_interact.loc[(df_interact['brand'].isin(list(selected_brands))) &
                            (df_interact['artDate'].dt.to_period('M') >= selected_beginning_date.to_period('M')) &
                            (df_interact['artDate'].dt.to_period('M') <= selected_ending_date.to_period('M'))]

# 生成詞頻dataframe
df_select['words'] = df_select['words'].apply(lambda x: literal_eval(x))

df_temp = df_select.copy()
df_temp['words'] = df_temp['words'].apply(lambda x: ' '.join(x))

# 將所有的詞彙合併為一個大字串
all_words = ' '.join(df_temp['words'])

# 使用Counter計算詞彙的出現次數
word_counts = Counter(all_words.split())

freq_df_2 = pd.DataFrame.from_dict(word_counts, orient='index').reset_index()
freq_df_2.columns = ['word', 'freq']
freq_df_2.sort_values(ascending=False, by='freq',inplace=True)

# 取出filter後詞頻前20的詞
voc = []
voc.append("未選擇")
for i in freq_df_2.iloc[:20]['word']:
    voc.append(i)

# 選擇要篩選含有哪個詞的文章
default_index = voc.index("未選擇")
st.sidebar.divider()
st.sidebar.title('斷詞篩選')
select_voc = st.sidebar.selectbox('選擇斷詞', voc, index=default_index)

if select_voc == '未選擇':

    freq_dict = freq_df_2.set_index('word', inplace=False).to_dict()
    freq_dict = freq_dict['freq']

    # 文字雲
    FontPath = 'SourceHanSansTW-Regular.otf' # 設定字型
    wordcloud = WordCloud(background_color='white',width=800, height = 400, font_path=FontPath, max_words=200)
    wordcloud.generate_from_frequencies(freq_dict)
    plt.figure(figsize = (14,7))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    st.pyplot()

    # 詞頻長條圖
    fig = px.bar(freq_df_2.iloc[:20], x='word', y='freq',width=1000, height = 500)
    fig.update_layout(
        xaxis_title="斷詞",
        yaxis_title="數量",
        title="詞頻長條圖"
    )
    st.plotly_chart(fig)

    st.markdown('資料表')

    st.dataframe(
        df_select[["artTitle", "artDate", "artCatagory", "artContent"]],
        column_config={
            "artTitle": "文章標題",
            "artDate": "發文日期",
            "artCatagory": "文章版面",
            "artContent": "文章內容",
        },
        hide_index=True,
    )

else:
    # 篩選後的dataframe
    select_id = df_select['words'].apply(lambda x: select_voc in x)

    df_select2 = df_select[select_id]

    df_temp2 = df_select2.copy()
    df_temp2['words'] = df_temp2['words'].apply(lambda x: ' '.join(x))

    # 將所有的詞彙合併為一個大字串
    all_words2 = ' '.join(df_temp2['words'])

    # 使用Counter計算詞彙的出現次數
    word_counts2 = Counter(all_words2.split())

    freq_df_3 = pd.DataFrame.from_dict(word_counts2, orient='index').reset_index()
    freq_df_3.columns = ['word', 'freq']
    freq_df_3.sort_values(ascending=False, by='freq',inplace=True)

    freq_dict = freq_df_3.set_index('word', inplace=False).to_dict()
    freq_dict = freq_dict['freq']

    # 文字雲
    FontPath = 'SourceHanSansTW-Regular.otf' # 設定字型
    wordcloud = WordCloud(background_color='white',width=800, height = 400, font_path=FontPath, max_words=200)
    wordcloud.generate_from_frequencies(freq_dict)
    plt.figure(figsize = (14,7))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    st.pyplot()

    # 詞頻長條圖
    fig = px.bar(freq_df_3.iloc[:20], x='word', y='freq',width=1000, height = 500)
    fig.update_layout(
        # yaxis = list(autorange = "reversed"),
        xaxis_title="斷詞",
        yaxis_title="數量",
        title="詞頻長條圖"
    )
    st.plotly_chart(fig)

    st.markdown('資料表')

    st.dataframe(
        df_select2[["artTitle", "artDate", "artCatagory", "artContent"]],
        column_config={
            "artTitle": "文章標題",
            "artDate": "發文日期",
            "artCatagory": "文章版面",
            "artContent": "文章內容",
        },
        hide_index=True,
    )