import streamlit as st
# from google.oauth2 import service_account
# from gsheetsdb import connect
import pandas as pd
from st_files_connection import FilesConnection

# 預設顯示 wide mode
st.set_page_config(page_title="裕日有望客分析系統", layout="wide", page_icon="📈")

# title
st.title("裕日有望客分析系統")

car_brand = ["nissan", "toyota", "ford", "honda", "mazda"]

# 讀取載入 data，若輸入參數在先前 streamlit 已看過，則會直接讀去 cache 中的結果（不執行 def）
#              若輸入參數沒看過，則會執行 def
#              不只有讀取 data 可使用， UI 也可以（如果覺得每次畫圖話很久，可以放在 cache 中的 function 執行）=> 輸入參數沒變會直接顯示之前畫好的圖
conn = st.experimental_connection('gcs', type=FilesConnection)

@st.cache_data(persist=True)  # 👈 Add the caching decorator
def load_data(url):
    csv_data = conn.read(url, input_format="csv", ttl=None)
    return csv_data
    
# nissan = load_data("big-data-class-2023/rawData/nissan_ptt_data.csv")
# toyota = load_data("big-data-class-2023/rawData/toyota_ptt_data.csv")
# ford = load_data("big-data-class-2023/rawData/ford_ptt_data.csv")
# honda = load_data("big-data-class-2023/rawData/honda_ptt_data.csv")
# mazda = load_data("big-data-class-2023/rawData/mazda_ptt_data.csv")

# @st.cache_data(persist=True)
# def show_ptt_data():
#     st.header("外部原始資料")
#     nissan_tab, toyota_tab, ford_tab, honda_tab, mazda_tab = st.tabs(car_brand)
#     nissan_tab.dataframe(nissan)
#     toyota_tab.dataframe(toyota)
#     ford_tab.dataframe(ford)
#     honda_tab.dataframe(honda)
#     mazda_tab.dataframe(mazda)


st.markdown(
    f""" #### 專案目標:
    - 鎖定Kicks及Sentra兩車型，透過爬蟲收集外部輿情等標籤，分析國內市場動態與有望客之關聯性，了解目標消費者當前討論之熱門議題與興趣輪廓，擬定行銷策略，並藉由市場反應進行策略優化。
    """, unsafe_allow_html=True)


# 內部資料
st.markdown("#### 內部資料")
# 讀取內部資料
internal = load_data("big-data-class-2023/rawData/nissan_internal.csv")
st.dataframe(internal)

# # 顯示外部資料
st.markdown(
    f""" #### 外部資料:
    - 資料取得方式 : PTT 爬蟲
    - 資料來源 : 汽車版、汽車買賣版
    - 資料區間：2020/12/01 ~ 2023/01/31

    `資料清理之定義為清除有空值的資料`

    | 廠牌 | 爬蟲關鍵字 | 資料總筆數 | 清理後筆數 |
    | --- | --- | --- | --- |
    | Nissan | Nissan、裕隆、裕日,日產、Sentra、Kicks、仙草 | 2,464 | 2,079 |
    | Toyota | Toyota、Altis、Cross、豐田、和泰、阿提斯、卡羅拉 | 8,755 | 7,420 |
    | Ford | 福特、六和、九和、上正、ford、Focus | 4,684 | 4,011 |
    | Honda | honda、HRV、本田 | 2,488 | 2,171 |
    | Mazda | mazda、CX-3、CX-30、馬三、mazda 3 | 3,321 | 2,787 |
    """, unsafe_allow_html=True)
# show_ptt_data()
