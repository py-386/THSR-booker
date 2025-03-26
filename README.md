# 高鐵訂票系統

這是一個基於 Selenium 爬蟲、LINE Bot、OpenAI API、OCR 和 MySQL 的高鐵訂票自動化系統。使用者可以透過 LINE 與系統互動，進行高鐵票務訂購，並且能夠自動處理驗證碼和回傳訂票資訊。系統會將每次訂票的資料存入 MySQL 資料庫以便後續查詢。

## 功能

- **LINE Bot 整合**：接收使用者訊息，進行自然語言處理並返回訂票資訊。
- **Selenium 爬蟲**：自動化爬取高鐵訂票網站，取得可用的班次資訊。
- **OpenAI API 語意判讀**：分析用戶訊息，判斷出用戶需求（如班次、日期等）。
- **OCR 驗證碼處理**：使用 `ddddocr` 套件自動識別並填寫訂票頁面的驗證碼。
- **MySQL 儲存資料**：將用戶訂票資料存入 MySQL 資料庫，便於後續查詢。

## 專案結構

. ├── app.py # 伺服器啟動檔案，提供給 LINE Bot 使用
  ├── main.py # 本地端程式，終端機操作 
  └── codes/ # 存放 Selenium 爬蟲、OCR 和其他相關代碼


## 安裝與設定

1. **安裝必要套件**：

    使用 `requirements.txt` 安裝所有依賴：

    ```bash
    pip install -r requirements.txt
    ```

2. **設定環境變數**：

    你需要在環境中設置 `OPENAI_API_KEY`，該金鑰用於與 OpenAI API 進行交互。

    ```bash
    export OPENAI_API_KEY="你的API金鑰"
    ```

3. **配置 MySQL 資料庫**：

    - 在 `codes/database.sql` 中提供了資料庫結構及初始化資料，請根據需求導入。

4. **啟動 NGROK 來暴露本地伺服器**：

    由於 LINE Bot 需要公開網址來接收訊息，你可以使用 NGROK 來將本地伺服器暴露至外部網路。安裝 NGROK 並啟動隧道：

    ```bash
    ngrok http 5000
    ```

    這會為你的本地伺服器創建一個公開的 URL（例如：`http://<ngrok_subdomain>.ngrok.io`）。將這個 URL 設定為 LINE Bot 的 webhook URL。

5. **啟動伺服器**：

    使用 `app.py` 啟動 LINE Bot 伺服器：

    ```bash
    python app.py
    ```

6. **執行本地終端機操作**：

    若要手動操作，請使用 `main.py`，通過終端機輸入來模擬訂票流程：

    ```bash
    python main.py
    ```

## 使用流程

1. **LINE 與系統互動**：
    - 用戶通過 LINE 與 Bot 互動，傳送需要訂票的班次、日期等資訊。
    - 系統會使用 OpenAI API 解析訊息並返回符合條件的可用班次。

2. **選擇班次並填寫資料**：
    - 用戶選擇需要的班次，系統自動填寫驗證碼並完成訂票操作。
    - 訂票完成後，系統會回傳訂票號碼以供用戶取票。

3. **資料存儲與查詢**：
    - 每筆訂票資料都會存入 MySQL 資料庫，便於後續查詢和分析。

## 技術與工具

- **Selenium**：自動化爬取高鐵網站並模擬訂票流程。
- **LINE Bot**：與使用者進行互動。
- **OpenAI API**：進行語意理解與自然語言處理。
- **ddddocr**：用於識別訂票頁面中的驗證碼。
- **MySQL**：儲存用戶訂票資料。
- **NGROK**：將本地伺服器暴露至外部網路，方便 LINE Bot 連接。

## 注意事項

- 使用前請確保你的環境已經設置好 `OPENAI_API_KEY`。
- 請遵守高鐵訂票網站的使用條款，並僅用於個人學習或測試目的。
- 如果有多筆訂票需求，系統會依照順序處理。


