import streamlit as st
import pandas as pd
import plotly.express as px
from st_files_connection import FilesConnection

# 預設顯示 wide mode
st.set_page_config(page_title="內部資料統計分析", layout="wide", page_icon="📈")
st.set_option('deprecation.showPyplotGlobalUse', False)

# 負責人：祐陞


# 設定資料連結
url = 'big-data-class-2023/nissan_preprocessing_data.csv'

# 利用catche讀取資料
conn = st.experimental_connection('gcs', type=FilesConnection)

@st.cache_data(persist=True)  # 👈 Add the caching decorator
def load_data(url):
    csv_data = conn.read(url, input_format="csv", ttl=None)
    return csv_data


df_interact = load_data(url)

# 轉換日期欄位為 datetime
# df_interact[['有望客生日', '試乘日', '交車日']] = pd.to_datetime(df_interact[['有望客生日', '試乘日', '交車日']],format='%Y-%m-%d')
df_interact['建檔日'] = pd.to_datetime(df_interact['建檔日'],format='%Y/%m/%d')
df_interact['有望客生日'] = pd.to_datetime(df_interact['有望客生日'],format='%Y-%m-%d')
df_interact['試乘日'] = pd.to_datetime(df_interact['試乘日'],format='%Y-%m-%d')
df_interact['交車日'] = pd.to_datetime(df_interact['交車日'],format='%Y-%m-%d')

# 新增kicks, sentra, 其他
df_interact['KicksSentra'] = '無試乘/交車'
df_interact.loc[(df_interact['成交車系'] == 'P15') |
                (df_interact['試乘_P15'] >= 1)]['KicksSentra'] = 'Kicks'

df_interact.loc[(df_interact['成交車系'] == 'B18') |
                (df_interact['試乘_B18'] >= 1)]['KicksSentra'] = 'Sentra'

df_interact.loc[(df_interact['成交車系'] != 'NULL') |
                (df_interact['試乘車輛'] != 0)]['KicksSentra'] = '試乘/交車其他車系'

# Set header title
st.title("Nissan 內部資料統計")
st.sidebar.subheader('參數調整')
# st.markdown('文字雲')

# Define list of selection options and sort alphabetically
chart_list = ['有望客來店數', '有望客年齡', '成交車系', '試乘車輛數']
dealer_list = ['YK', 'ES', 'UL', 'YJ', 'YF', 'EM', 'HL', 'KT', 'YA', 'UT', 'LA']
test_buy_list = ['Kicks', 'Sentra', '試乘/交車其他車系', '無試乘/交車']

# chart_list.sort()

default_index = chart_list.index("有望客來店數")
# Implement multiselect dropdown menu for option selection (returns a list)
# st.sidebar.title('選擇視覺化圖表')
select_chart = st.sidebar.selectbox('選擇圖表', chart_list, index=default_index)
# selected_brands = st.sidebar.multiselect('選擇品牌', brand_list, default=['Nissan'])

# st.sidebar.title('選擇經銷商')
select_dealer = st.sidebar.multiselect('選擇經銷商', dealer_list, default=dealer_list)

# st.sidebar.title('選擇經銷商')
select_test_buy = st.sidebar.multiselect('選擇車系', test_buy_list, default=test_buy_list)

# st.sidebar.divider()  # 分隔線

# 選擇月份
# st.sidebar.title('選擇月份區間')
st.sidebar.caption('有效月份範圍：2021-01 - 2023-01')

# 取得所有的月份選項
all_months = pd.period_range(start='2021-01', end='2023-01', freq='M')

# 轉換日期選項為字串格式
month_options = [str(month) for month in all_months]

# 選擇資料起始月份
selected_beginning_month = st.sidebar.selectbox(
    "選擇資料起始月份",
    month_options, index=0    # 設定預設選項為索引 0，即 2020-12
)

# 選擇資料結束月份
selected_ending_month = st.sidebar.selectbox(
    "選擇資料結束月份",
    month_options, index=len(month_options)-1   # 設定預設選項為索引最大值，即 2023-1
)

# 將選擇的月份轉換為 datetime 格式
selected_beginning_date = pd.to_datetime(selected_beginning_month, format='%Y-%m')
selected_ending_date = pd.to_datetime(selected_ending_month, format='%Y-%m')

# 防呆機制：結束月份不能選擇比起始月份還前面的日期
if selected_ending_date < selected_beginning_date:
    st.sidebar.error("結束月份不能早於起始月份")

# Filter the dataframe based on selected brands and dates
df_select = df_interact.loc[(df_interact['DEALERCODE'].isin(list(select_dealer))) &
                            (df_interact['KicksSentra'].isin(list(select_test_buy))) &
                            (df_interact['建檔日'].dt.to_period('M') >= selected_beginning_date.to_period('M')) &
                            (df_interact['建檔日'].dt.to_period('M') <= selected_ending_date.to_period('M'))]

if df_select.empty:
    st.markdown(":red[篩選後資料表為空值，請重新篩選動作]")

else:

    if select_chart == '有望客來店數':

        cust_list = ['來店數', '來店數X性別', '來店數X初始分級', '來店數X經銷商', '來店數X試乘/成交車系']
        default_index1 = cust_list.index("來店數")
        select_comp = st.selectbox('選擇圖表', cust_list, index=default_index1)

        if select_comp == '來店數':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby([df_select['建檔日'].dt.to_period('M').astype(str)])['有望客ID'].count().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="有望客ID")
            st.markdown('#### 有望客來店數趨勢')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="來客數",
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '來店數X性別':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['性別',df_select['建檔日'].dt.to_period('M').astype(str)])['有望客ID'].count().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="有望客ID", color='性別')
            st.markdown('#### 有望客來店數趨勢 - 性別')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="來客數"
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '來店數X初始分級':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['初始分級',df_select['建檔日'].dt.to_period('M').astype(str)])['有望客ID'].count().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="有望客ID", color='初始分級')
            st.markdown('#### 有望客來店數趨勢 - 初始分級')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="來客數"
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '來店數X經銷商':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['DEALERCODE',df_select['建檔日'].dt.to_period('M').astype(str)])['有望客ID'].count().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="有望客ID", color='DEALERCODE')
            st.markdown('#### 有望客來店數趨勢 - 經銷商')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="來客數"
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '來店數X試乘/成交車系':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['KicksSentra',df_select['建檔日'].dt.to_period('M').astype(str)])['有望客ID'].count().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="有望客ID", color='KicksSentra')
            st.markdown('#### 有望客來店數趨勢 - 試乘/成交車系')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="來客數"
            )
            st.plotly_chart(fig, use_container_width = True)
        

    elif select_chart == '有望客年齡':

        age_list = ['年齡', '年齡X性別', '年齡X初始分級', '年齡X經銷商', '年齡X試乘/成交車系']
        default_index2 = age_list.index("年齡")
        select_comp = st.selectbox('選擇圖表', age_list, index=default_index2)

        if select_comp == '年齡':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby([df_select['建檔日'].dt.to_period('M').astype(str)])['年齡'].mean().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="年齡")
            st.markdown('#### 有望客年齡趨勢')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="平均年齡"
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '年齡X性別':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['性別',df_select['建檔日'].dt.to_period('M').astype(str)])['年齡'].mean().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="年齡", color='性別')
            st.markdown('#### 有望客年齡趨勢 - 性別')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="平均年齡"
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '年齡X初始分級':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['初始分級',df_select['建檔日'].dt.to_period('M').astype(str)])['年齡'].mean().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="年齡", color='初始分級')
            st.markdown('#### 有望客年齡趨勢 - 初始分級')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="平均年齡"
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '年齡X經銷商':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['DEALERCODE',df_select['建檔日'].dt.to_period('M').astype(str)])['年齡'].mean().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="年齡", color='DEALERCODE')
            st.markdown('#### 有望客年齡趨勢 - 經銷商')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="平均年齡"
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '年齡X試乘/成交車系':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['KicksSentra',df_select['建檔日'].dt.to_period('M').astype(str)])['年齡'].mean().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="年齡", color='KicksSentra')
            st.markdown('#### 有望客年齡趨勢 - 試乘/成交車系')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="平均年齡"
            )
            st.plotly_chart(fig, use_container_width = True)


    elif select_chart == '成交車系':

        df_car = df_select.loc[(df_select['成交車系'] != "NULL")]

        freq_df = pd.DataFrame({'freq':df_car.groupby(['成交車系']).size().sort_values(ascending=False)}).reset_index(drop = False)
        clist = ['成交車系','freq']  
        freq_df = freq_df[clist]
        freq_df.sort_values(ascending=False, by='freq',inplace=True)

        fig = px.bar(freq_df.iloc[:20], x='成交車系', y='freq')
        st.markdown('#### 各車系交車數長條圖')
        fig.update_layout(
            xaxis_title="車系",
            yaxis_title="數量"
        )
        st.plotly_chart(fig, use_container_width = True)

    elif select_chart == '試乘車輛數':

        # Group by brand & artDate, then calculate total volume
        car_list = ['試乘車輛數', '試乘車輛數X性別', '試乘車輛數X初始分級', '試乘車輛數X經銷商', '試乘車輛數X試乘/成交車系']
        default_index3 = car_list.index("試乘車輛數")
        select_comp = st.selectbox('選擇圖表', car_list, index=default_index3)

        if select_comp == '試乘車輛數':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby([df_select['建檔日'].dt.to_period('M').astype(str)])['試乘車輛'].sum().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="試乘車輛")
            st.markdown('#### 有望客試乘車輛數趨勢')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="試乘車輛數"
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '試乘車輛數X性別':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['性別',df_select['建檔日'].dt.to_period('M').astype(str)])['試乘車輛'].sum().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="試乘車輛", color='性別')
            st.markdown('#### 有望客試乘車輛數趨勢 - 性別')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="試乘車輛數"
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '試乘車輛數X初始分級':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['初始分級',df_select['建檔日'].dt.to_period('M').astype(str)])['試乘車輛'].sum().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="試乘車輛", color='初始分級')
            st.markdown('#### 有望客試乘車輛數趨勢 - 初始分級')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="試乘車輛數"
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '試乘車輛數X經銷商':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['DEALERCODE',df_select['建檔日'].dt.to_period('M').astype(str)])['試乘車輛'].sum().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="試乘車輛", color='DEALERCODE')
            st.markdown('#### 有望客試乘車輛數趨勢 - 經銷商')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="試乘車輛數"
            )
            st.plotly_chart(fig, use_container_width = True)

        elif select_comp == '試乘車輛數X試乘/成交車系':

            # Group by brand & artDate, then calculate total volume
            customer = df_select.groupby(['KicksSentra',df_select['建檔日'].dt.to_period('M').astype(str)])['試乘車輛'].sum().reset_index()

            # Plot line chart
            fig = px.line(customer, x="建檔日", y="試乘車輛", color='KicksSentra')
            st.markdown('#### 有望客試乘車輛數趨勢 - 試乘/成交車系')
            fig.update_layout(
                xaxis_title="月份",
                yaxis_title="試乘車輛數"
            )
            st.plotly_chart(fig, use_container_width = True)