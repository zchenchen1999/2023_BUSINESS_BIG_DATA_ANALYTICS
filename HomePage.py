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
ptt_df_list = []

# 雲端連線方式
try:
    conn = st.experimental_connection('gcs', type=FilesConnection)
    internal = conn.read("big-data-class-2023/nissan_internal.csv", input_format="csv", ttl=600)
    for b in car_brand:
        ptt_df_list.addend(conn.read(f"big-data-class-2023/{b}_ptt_data.csv", input_format="csv", ttl=600))
# 本機讀取自己的路徑
except:
    print("本機")
    pass

# 內部資料
st.header("內部資料")
st.dataframe(internal)


# 外部 ptt 資料
st.header("外部原始資料")
car_brand_tabs = st.tabs(car_brand)
for p in range(len(ptt_df_list)):
    car_brand_tabs[p].dataframe(ptt_df_list[p])


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
