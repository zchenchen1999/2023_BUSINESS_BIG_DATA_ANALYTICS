import streamlit as st
# from google.oauth2 import service_account
# from gsheetsdb import connect
import pandas as pd
from st_files_connection import FilesConnection

# 預設顯示 wide mode
st.set_page_config(page_title="裕日有望客分析系統", layout="wide")

# title
st.title("裕日有望客分析系統")

conn = st.experimental_connection('gcs', type=FilesConnection)
df = conn.read("big-data-class-2023/pttData.csv", input_format="csv", ttl=600)

st.dataframe(df)
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
