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
@st.cache_data  # 👈 Add the caching decorator
async def load_data(url):
    try:
        conn = st.experimental_connection('gcs', type=FilesConnection)
        csv_data = await conn.read(url, input_format="csv", ttl=1000)
        return csv_data
    # 本機讀取自己的路徑
    except:
        print("本機")
        return None

@st.cache_data
async def show_ptt_data():
    st.header("外部原始資料")
    car_brand_tabs = st.tabs(car_brand)
    for p in range(len(car_brand_tabs)):
        try:
            await car_brand_tabs[p].dataframe(data=load_data(f"big-data-class-2023/{car_brand[p]}_ptt_data.csv"), use_container_width=True)
        except:
            print("本機")



# 內部資料
st.header("內部資料")
# 讀取內部資料
internal = load_data("big-data-class-2023/nissan_internal.csv")
st.dataframe(internal)
# 顯示外部資料
show_ptt_data()