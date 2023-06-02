import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
import datetime
from pyvis.network import Network
from datetime import datetime, timedelta

# 預設顯示 wide mode
st.set_page_config(layout="wide")

# title
st.title("品牌情緒趨勢圖")

## content
# Read dataset (CSV)
ford = pd.read_csv('/Users/jerry/Library/CloudStorage/OneDrive-輔仁大學/中山企管/碩一下/CM505/rawData/ford_ptt_clean.csv')
honda = pd.read_csv('/Users/jerry/Library/CloudStorage/OneDrive-輔仁大學/中山企管/碩一下/CM505/rawData/honda_ptt_clean.csv')
mazda = pd.read_csv('/Users/jerry/Library/CloudStorage/OneDrive-輔仁大學/中山企管/碩一下/CM505/rawData/mazda_ptt_clean.csv')
toyota = pd.read_csv('/Users/jerry/Library/CloudStorage/OneDrive-輔仁大學/中山企管/碩一下/CM505/rawData/toyota_ptt_clean.csv')
nissan = pd.read_csv('/Users/jerry/Library/CloudStorage/OneDrive-輔仁大學/中山企管/碩一下/CM505/rawData/nissan_ptt_clean.csv')

# Set header title
st.title('Brand Sentiment Trend Chart')

# Define list of selection options and sort alphabetically
brand_list = ['Ford', 'Honda', 'Mazda', 'Toyota',
            'Nissan']
brand_list.sort()

#Define list of time
start_date = datetime.date(2020, 12, 1)
end_date = datetime.date(2023, 1, 1)
date_range = pd.date_range(start_date, end_date, freq= 'MS').strftime("%Y/%m").tolist()
selected_month = st.selectbox("Select a month", date_range)
st.write("Selected Month", selected_month)


# # Implement multiselect dropdown menu for option selection (returns a list)
# selected_brand = st.multiselect('Select brand(s) to visualize', brand_list)

# # Set info message on initial site load
# if len(selected_brand) == 0:
#     st.text('Choose at least 1 brand to start')

# # Create network graph when user selects >= 1 item
# else:
#     df_select = df_interact.loc[df_interact['brand_1_name'].isin(selected_brand) | \
#                                 df_interact['brand_2_name'].isin(selected_brand)]
#     df_select = df_select.reset_index(drop=True)

#     # Create networkx graph object from pandas dataframe
#     G = nx.from_pandas_edgelist(df_select, 'drug_1_name', 'drug_2_name', 'weight')

#     # Initiate PyVis network object
#     drug_net = Network(
#                        height='400px',
#                        width='100%',
#                        bgcolor='#222222',
#                        font_color='white'
#                       )

#     # Take Networkx graph and translate it to a PyVis graph format
#     drug_net.from_nx(G)

#     # Generate network with specific layout settings
#     drug_net.repulsion(
#                         node_distance=420,
#                         central_gravity=0.33,
#                         spring_length=110,
#                         spring_strength=0.10,
#                         damping=0.95
#                        )

#     # Save and read graph as HTML file (on Streamlit Sharing)
#     try:
#         path = '/tmp'
#         drug_net.save_graph(f'{path}/pyvis_graph.html')
#         HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

#     # Save and read graph as HTML file (locally)
#     except:
#         path = '/html_files'
#         drug_net.save_graph(f'{path}/pyvis_graph.html')
#         HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

#     # Load HTML file in HTML component for display on Streamlit page
#     components.html(HtmlFile.read(), height=435)

# # Footer
# st.markdown(
#     """
#     <br>
#     <h6><a href="https://github.com/kennethleungty/Pyvis-Network-Graph-Streamlit" target="_blank">GitHub Repo</a></h6>
#     <h6><a href="https://kennethleungty.medium.com" target="_blank">Medium article</a></h6>
#     <h6>Disclaimer: This app is NOT intended to provide any form of medical advice or recommendations. Please consult your doctor or pharmacist for professional advice relating to any drug therapy.</h6>
#     """, unsafe_allow_html=True
#     )

# 負責人：誠哲
