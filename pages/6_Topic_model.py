import streamlit as st
import streamlit.components.v1 as components
# from st_files_connection import FilesConnection

# 負責人：畇彤

# ---------------------------------------------------------- Streamlit ----------------------------------------------------------#

# 預設顯示 wide mode
st.set_page_config(layout="wide")

# title
st.title("主題模型")


st.sidebar.header('')

## 品牌選擇
# brand_list = ['nissan', 'toyota', 'ford', 'honda', 'mazda']

# selected_brand = st.sidebar.selectbox('選擇品牌', brand_list)



with open('../html_files/nissan_lda.html', 'r') as f:
    html_string = f.read()
components.html(html_string, height=660, scrolling=True)
