# 路由與 API 設計 (Routes & API Design)

本文件依據 PRD 與架構設計，定義 CampuSwap 的 HTTP 路由與對應的 Jinja2 模板，做為實作階段的指南。

## 1. 路由總覽表

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 / 處理方式 | 說明 |
| ---- | --------- | -------- | ------------------- | ---- |
| **首頁 (搜尋/列表)** | GET | `/` | `items/index.html` | 顯示所有商品，包含關鍵字搜尋、分類與價格過濾表單 |
| **註冊頁面** | GET | `/auth/register` | `auth/register.html` | 顯示使用者註冊表單 |
| **註冊處理** | POST | `/auth/register` | — | 接收註冊資料，存入 DB，重導向至登入頁 |
| **登入頁面** | GET | `/auth/login` | `auth/login.html` | 顯示使用者登入表單 |
| **登入處理** | POST | `/auth/login` | — | 驗證帳號密碼，設定 session，重導向至首頁 |
| **登出** | GET | `/auth/logout` | — | 清除 session，重導向至首頁 |
| **發布商品頁面** | GET | `/items/new` | `items/new.html` | 顯示商品新增表單，需登入 |
| **發布商品處理** | POST | `/items/new` | — | 接收商品資料，存入 DB，重導向至商品詳情或首頁 |
| **商品詳情** | GET | `/items/<id>` | `items/detail.html` | 顯示單一商品的詳細資訊與賣家聯絡方式 |
| **刪除商品** | POST | `/items/<id>/delete` | — | 刪除指定商品 (限發布者)，重導向至首頁 |
| **AI 估價 (API)**| POST | `/api/estimate-price`| `JSON 回傳` | 接收 JSON 格式的商品屬性，回傳推薦價格區間 |

---

## 2. 路由詳細說明

### 2.1 首頁與搜尋 (F-04)
- **輸入**: URL Query Parameters (`q`=關鍵字, `category`=分類, `min_price`=最低價, `max_price`=最高價)
- **處理**: 從 `request.args` 取得參數，呼叫 `app.models.item.search_and_filter()`。
- **輸出**: 渲染 `items/index.html` 並傳入 `items` 列表。
- **錯誤處理**: 若無商品符合，於畫面上顯示「找不到相關商品」。

### 2.2 註冊與登入 (F-01)
- **輸入**: 表單資料 (`email`, `password`, `confirm_password`)。
- **處理**:
  - 註冊：檢查 email 是否重複，確認密碼相符，雜湊後呼叫 `app.models.user.create()`。
  - 登入：呼叫 `app.models.user.get_by_email()`，比對密碼。
- **輸出**: 成功則重導向 (Redirect) 至 `/`，失敗則使用 `flash` 顯示錯誤訊息並重新渲染表單。

### 2.3 發布商品 (F-03)
- **輸入**: 表單資料 (`title`, `description`, `category`, `brand`, `condition`, `price`，以及 AI 估價結果的隱藏欄位)。
- **處理**: 確認必要欄位填寫，呼叫 `app.models.item.create()`。
- **輸出**: 成功建立後重導向至首頁或該商品詳情頁。

### 2.4 AI 估價 API (F-02)
- **輸入**: JSON Payload `{"category": "Books", "brand": "Pearson", "condition": "New"}`。
- **處理**: 內部邏輯呼叫外部 AI 模型 API（或暫時使用 mock 邏輯模擬），取得推薦價格。
- **輸出**: 回傳 JSON `{ "min_price": 300, "max_price": 500 }`。
- **錯誤處理**: 若缺少欄位或 AI 服務異常，回傳 400 或 500 狀態碼及錯誤訊息。

---

## 3. Jinja2 模板清單

將建立於 `app/templates/` 資料夾下：

1. **`base.html`**：所有頁面的根模板。包含 `<head>`、Bootstrap 5 引用、導覽列與 `<div class="container">`，以及 `flash` 訊息顯示區塊與 `{% block content %}`。
2. **`auth/register.html`**：繼承 `base.html`。
3. **`auth/login.html`**：繼承 `base.html`。
4. **`items/index.html`**：繼承 `base.html`。包含搜尋列、左側過濾面板，與右側商品卡片列表 (Grid)。
5. **`items/new.html`**：繼承 `base.html`。包含輸入表單與「AI 估價」按鈕 (觸發 JavaScript)。
6. **`items/detail.html`**：繼承 `base.html`。顯示大張圖片(若有)與詳細資訊。

---

## 4. 路由骨架程式碼
請參考 `app/routes/auth.py`, `app/routes/items.py` 及 `app/routes/api.py` 的實作檔案。
