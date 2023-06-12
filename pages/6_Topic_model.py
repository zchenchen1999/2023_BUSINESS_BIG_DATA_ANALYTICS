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

path = '/html_files'
HtmlFile = open(f'{path}/nissan_lda.html', 'r', encoding='utf-8')

# Load HTML file in HTML component for display on Streamlit page
components.html(HtmlFile.read(), height=660, scrolling=True)