import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from st_files_connection import FilesConnection

# 負責人：畇彤


# 預設顯示 wide mode
st.set_page_config(page_title="Nissan PTT 討論主題分析", layout="wide", page_icon="📈")
# st.set_option('dataframe.fit_columns_to_available_width', True)

# title
st.title("Nissan PTT 討論主題分析")


st.markdown(
    f""" #### 主題模型說明:
    - 左邊的圓圈代表不同的主題，圓圈大小代表該主題的討論量
    - 右邊藍色的長條圖代表 PTT 中提到該詞彙的總次數
    - 右邊紅色的長條圖比例越高代表該詞彙越集中在當前的主題中
    """, unsafe_allow_html=True)

# 主題模型 html 讀取
path = './html_files/nissan_lda.html'
with open(path, 'r') as f :
    HtmlFile = f.read()
components.html(HtmlFile, height=900, scrolling=True)


# 主題模型描述 dataframe
st.markdown('#### 分析結果說明')
topic = {
    '': ['Topic1', 'Topic2', 'Topic3', 'Topic4', 'Topic5'],
    '主題關鍵字 (僅列出部分)': ['業務、預算、空間、價格、不錯、隔音、安全、試乘、後座', 
              '裕隆、中國、日本、豐田、市場、進口、美國、電動車、國產、銷量、歐洲、成本',
              '原廠、保養、變速箱、里程、油耗、外觀、保固、引擎、市區、內裝、妥善、維修',
              '折價、空車、贈送、換新、北部、現金、交車裡、旗艦版、菜單',
              '顏色、排檔、形式、自用、一手、白色、稅金、規費、看車'],
    '主題': ['購車基本考量', '全球市場及相關議題', '汽車時常討論議題', '購車菜單', '汽車買賣']
}

topic_df = pd.DataFrame(topic)
st.dataframe(topic_df, use_container_width=True, hide_index=True)



# 關鍵字查詢
conn = st.experimental_connection('gcs', type=FilesConnection)

@st.cache_data(persist=True)  # 👈 Add the caching decorator
def load_data(url):
    csv_data = conn.read(url, input_format="csv", ttl=None)
    return csv_data
nissan = load_data("big-data-class-2023/nissan_clean_data.csv")

## 定義文章查找 function
def get_article(word):
    try:
        findword = nissan.loc[nissan['words'].str.contains(word)]
        findword = findword[['artTitle', 'artDate', 'artCatagory', 'artContent', 'artUrl']]
        return findword
    except KeyError:
        return []

st.markdown('#### 關鍵字搜尋')

word = st.text_input("請輸入關鍵字:")

if word:
    relative_art = get_article(word)
    if relative_art.empty:
        st.write("沒有找到相關文章.")
    else:
        st.dataframe(relative_art,     
                     column_config = {
                        "artTitle": "文章標題",
                        "artDate": "發文日期",
                        "artCatagory": "文章版別",
                        "artContent": "文章內容",
                        "artUrl": "文章連結",
                    },
                    use_container_width=True,
                    hide_index=True)
        st.write('關鍵字', word,'共找到 ',len(relative_art), ' 篇文章')