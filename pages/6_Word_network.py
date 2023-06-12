import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pyvis.network import Network
from st_files_connection import FilesConnection


# 負責人：畇彤

# ---------------------------------------------------------- Streamlit ----------------------------------------------------------#

# 預設顯示 wide mode
st.set_page_config(layout="wide")

# title
st.title("廠牌字詞網路圖")


st.sidebar.header('參數調整')

## 品牌選擇
brand_list = ['nissan', 'toyota', 'ford', 'honda', 'mazda']
# brand_list.sort()

selected_brand = st.sidebar.selectbox('選擇品牌', brand_list)


# 關聯度設定
corr_values = st.sidebar.slider('選擇關聯度區間', 0.0, 1.0, (0.9, 1.0))
st.sidebar.write('關聯度:', corr_values)



# ---------------------------------------------------------- Load Data ----------------------------------------------------------#


conn = st.experimental_connection('gcs', type=FilesConnection)
# df = conn.read('big-data-class-2023/word2vec/' + selected_brand + '_correlation.csv', input_format='csv', ttl=600)

@st.cache_data(persist=True)  # 👈 Add the caching decorator
def load_data(url):
    csv_data = conn.read(url, input_format="csv", ttl=None)
    return csv_data

df = load_data(f"big-data-class-2023/word2vec/" + selected_brand + "_correlation.csv")



df = df.drop('Unnamed: 0', axis = 1)

# 根據條件篩選 data
df = df[(df['correlation'] > corr_values[0]) & (df['correlation'] < corr_values[1])]
df = df.reset_index(drop=True)
# 移除 corr 為 1 的資料
df = df[df['item1'] != df['item2']]

# -------------------------------------------------------- Pyvis ----------------------------------------------------------#
Cor_Graph = {}
correlation_net = Network(height='650px',width="100%")
nid=1


# 加入 node
for i in df['item1']:
    if (i not in Cor_Graph.keys()): 
        correlation_net.add_node(n_id=nid, label=i)
        Cor_Graph[i] = nid
        nid += 1

for i in df['item2']:
    if (i not in Cor_Graph.keys()): 
        correlation_net.add_node(n_id=nid, label=i)
        Cor_Graph[i] = nid
        nid += 1

# 加入 edge
for i, row in df.iterrows():
    correlation_net.add_edge(Cor_Graph[row['item1']], Cor_Graph[row['item2']], weight=row['correlation'], title=row['correlation'], value=row['correlation'])

try:
    path = '/tmp'
    correlation_net.save_graph(f'{path}/pyvis_graph.html')
    HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

# Save and read graph as HTML file (locally)
except:
    path = '../html_files'
    correlation_net.save_graph(f'{path}/pyvis_graph.html')
    HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

# Load HTML file in HTML component for display on Streamlit page
components.html(HtmlFile.read(), height=660, scrolling=True)
