# 2023_BUSINESS_BIG_DATA_ANALYTICS
## 檔案說明
* HomePage: APP 主頁面
* Pages: APP 子頁面，包含
    * 內部資料統計
    * 品牌網路聲量趨勢
    * 詞頻分析
    * 品牌網路情緒趨勢
    * 主題模型分析
    * 品牌字詞網路圖
    * 內外部相關性分析
* code: 程式碼放置處，包含
    * 資料前處理程式
    * LDA 主題模型訓練程式
    * Word2Vec 訓練程式
* html_files: 網路圖、主題模型 html 檔
* data 放置視覺化檔案

## 使用說明
1. Clone 此專案
2. 在環境中安裝 requirement.txt 中的套件
3. 將欲視覺化之資料放入 data 資料夾中
4. 更改各 Page 中資料讀取方式
    - 原本：Google Cloud Storage 連線
        ```python=
        conn = st.experimental_connection('gcs', type=FilesConnection)

        @st.cache_data(persist=True)  # 👈 Add the caching decorator
        def load_data(url):
            csv_data = conn.read(url, input_format="csv", ttl=None)
            return csv_data

        # 讀取品牌ptt資料
        nissan = load_data("big-data-class-2023/nissan_clean_data.csv")
        toyota = load_data("big-data-class-2023/toyota_clean_data.csv")
        ford = load_data("big-data-class-2023/ford_clean_data.csv")
        honda = load_data("big-data-class-2023/honda_clean_data.csv")
        mazda = load_data("big-data-class-2023/mazda_clean_data.csv")
        ```
    * 更改為：本地資料夾讀取
        ```python=
        # 讀取品牌ptt資料
        file = pd.read_csv("<檔案路徑>")
        ```
5. 在終端機輸入以下指令啟動 streamlit APP
    ```
    streamlit run HomePage.py
    ```
