import streamlit as st
# from google.oauth2 import service_account
# from gsheetsdb import connect
import pandas as pd
from st_files_connection import FilesConnection

# 預設顯示 wide mode
st.set_page_config(page_title="裕日有望客分析系統", layout="wide")

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



# 內部資料
st.header("內部資料")
# 讀取內部資料
internal = load_data("big-data-class-2023/rawData/nissan_internal.csv")
st.dataframe(internal)
# # 顯示外部資料
# show_ptt_data()
