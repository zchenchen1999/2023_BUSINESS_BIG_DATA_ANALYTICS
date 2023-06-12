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

# 讀取載入 data，若輸入參數在先前 streamlit 已看過，則會直接讀去 cache 中的 data
@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    try:
        conn = st.experimental_connection('gcs', type=FilesConnection)
        csv_data = conn.read(url, input_format="csv", ttl=1000)
        return csv_data
    # 本機讀取自己的路徑
    except:
        print("本機")
        return None

@st.cache_data
def load_ptt_data(string):
    st.header("外部原始資料")
    car_brand_tabs = st.tabs(car_brand)
    for p in range(len(car_brand_tabs)):
        try:
            car_brand_tabs[p].dataframe(data=load_data(f"big-data-class-2023/{car_brand[p]}_ptt_data.csv"), use_container_width=True)
        except:
            print("本機")
    # try:
    #     ptt_df_list = []
    #     ptt_df_list.append(load_data("big-data-class-2023/nissan_ptt_data.csv"))
    #     ptt_df_list.append(load_data("big-data-class-2023/toyota_ptt_data.csv"))
    #     ptt_df_list.append(load_data("big-data-class-2023/ford_ptt_data.csv"))
    #     ptt_df_list.append(load_data("big-data-class-2023/honda_ptt_data.csv"))
    #     ptt_df_list.append(load_data("big-data-class-2023/mazda_ptt_data.csv"))
    #     return ptt_df_list
    # # 本機讀取自己的路徑
    # except:
    #     print("本機")
    #     return None


internal = load_data("big-data-class-2023/nissan_internal.csv")

# ptt_df_list = load_ptt_data("ptt")
# ptt_df_list.append(load_data("big-data-class-2023/nissan_ptt_data.csv"))
# ptt_df_list.append(load_data("big-data-class-2023/toyota_ptt_data.csv"))
# ptt_df_list.append(load_data("big-data-class-2023/ford_ptt_data.csv"))
# ptt_df_list.append(load_data("big-data-class-2023/honda_ptt_data.csv"))
# ptt_df_list.append(load_data("big-data-class-2023/mazda_ptt_data.csv"))

# 內部資料
st.header("內部資料")
st.dataframe(internal)
load_ptt_data("ptt")
# 外部 ptt 資料
# st.header("外部原始資料")
# car_brand_tabs = st.tabs(car_brand)
# for p in range(len(ptt_df_list)):
#     car_brand_tabs[p].dataframe(data=ptt_df_list[p], use_container_width=True)


# SECRET = st.secrets["gcp_service_account"]

# # 取得 SECRET 範例： SECRET.get("type")

# # 與 google sheet 連結
# # Create a connection object.
# credentials = service_account.Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"],
#     scopes=[
#         "https://www.googleapis.com/auth/spreadsheets",
#     ],
# )
# conn = connect(credentials=credentials)

# def run_query(query):
#     rows = conn.execute(query, headers=1)
#     rows = pd.DataFrame(rows.fetchall())
#     return rows

# sheet_url = st.secrets["private_gsheets_url"]
# df = run_query(f'SELECT * FROM "{sheet_url}"')

# st.dataframe(df)
