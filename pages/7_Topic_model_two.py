import streamlit as st
import streamlit.components.v1 as components
# from st_files_connection import FilesConnection

# 負責人：畇彤

# ---------------------------------------------------------- Streamlit ----------------------------------------------------------#

# 預設顯示 wide mode
st.set_page_config(layout="wide")

# title
st.title("主題模型")

# st.sidebar.header('')
path = './html_files/nissan_lda.html'
with open(path, 'r') as f :
    HtmlFile = f.read()
st.header("測試")
components.html(HtmlFile, height=850, scrolling=True)