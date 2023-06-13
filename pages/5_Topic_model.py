import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
# from st_files_connection import FilesConnection

# 負責人：畇彤

# 主題結果 dataframe 之建立
topic = {
    '': [1, 2, 3, 4, 5],
    '主題關鍵字': ['業務、預算、空間、價格、不錯、隔音、安全、試乘、後座', 
              '裕隆、中國、日本、豐田、市場、進口、美國、電動車、國產、銷量、歐洲、成本',
              '原廠、保養、變速箱、里程、油耗、外觀、保固、引擎、市區、內裝、妥善、維修',
              '折價、空車、贈送、換新、北部、現金、交車裡、旗艦版、菜單',
              '顏色、排檔、形式、自用、一手、白色、稅金、規費、看車'],
    '主題': ['購車基本考量', '全球市場及相關議題', '汽車時常討論議題', '購車菜單', '汽車買賣']
}

topic_df = pd.DataFrame(topic)

# ---------------------------------------------------------- Streamlit ----------------------------------------------------------#

# 預設顯示 wide mode
st.set_page_config(layout="wide")

# title
st.title("主題模型")

st.dataframe(topic_df)
# st.sidebar.header('')
path = './html_files/nissan_lda.html'
with open(path, 'r') as f :
    HtmlFile = f.read()
components.html(HtmlFile, height=900, scrolling=True)