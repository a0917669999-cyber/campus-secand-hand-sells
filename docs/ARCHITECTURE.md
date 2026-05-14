# 系統架構設計 (CampuSwap Architecture)

本文件依據 `PRD.md` 的需求，定義 CampuSwap 的技術架構、資料夾結構與元件職責。

## 1. 技術架構說明

CampuSwap 採用經典的 **MVC (Model-View-Controller)** 模式進行單體式架構 (Monolith) 開發。

- **技術選型與原因**：
  - **後端框架：Flask (Python)** - 輕量級且靈活，適合快速建立 MVP 與 API 串接 (如 AI 估價)。
  - **模板引擎：Jinja2** - Flask 內建，能夠直接在伺服器端渲染 HTML 畫面，不需要建立複雜的前端 SPA (Single Page Application)，降低初期開發成本。
  - **資料庫：SQLite (sqlite3)** - 輕巧、無需額外架設伺服器，非常適合校園專案與小型 MVP 階段。
  - **前端設計：HTML/CSS/JS + Bootstrap 5** - 提供響應式 (Responsive) 且美觀的使用者介面。

- **MVC 各自負責的項目**：
  - **Model (模型)**：負責與 SQLite 互動，處理資料庫的 CRUD（新增、讀取、更新、刪除）邏輯。
  - **View (視圖)**：Jinja2 模板，負責將 Controller 準備好的資料渲染成使用者可見的 HTML 網頁。
  - **Controller (控制器)**：Flask 路由 (Routes)，負責接收使用者的 HTTP 請求、呼叫對應的 Model、並決定要回傳哪個 View 或進行重新導向。

## 2. 專案資料夾結構

```text
campu-swap/
├── app/
│   ├── __init__.py       # 初始化 Flask 應用與註冊 Blueprint
│   ├── models/           # (Model) 資料庫存取層
│   │   ├── user.py       # 使用者資料模型
│   │   └── item.py       # 商品資料模型
│   ├── routes/           # (Controller) 路由控制器
│   │   ├── auth.py       # 註冊、登入與權限路由
│   │   ├── items.py      # 商品瀏覽、搜尋、發布路由
│   │   └── api.py        # 提供給前端非同步呼叫的 API (如 AI 估價)
│   ├── templates/        # (View) Jinja2 HTML 模板
│   │   ├── base.html     # 所有頁面的共用基礎模板 (導覽列、Flash 訊息)
│   │   ├── auth/         # 登入與註冊頁面
│   │   └── items/        # 商品列表 (首頁)、新增商品、商品詳情頁
│   └── static/           # CSS / JS / 圖片靜態資源
│       ├── css/style.css # 自訂樣式表
│       └── js/main.js    # 處理 AI 估價非同步請求等邏輯
├── database/
│   └── schema.sql        # 建立資料表的 SQL 語法
├── docs/                 # 設計文件
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── DB_DESIGN.md
│   └── ROUTES.md
├── instance/
│   └── database.db       # 運行時動態生成的 SQLite 資料庫檔案
├── app.py                # 應用程式入口點，執行 `flask run` 的起點
└── requirements.txt      # 記錄套件依賴 (如 flask, requests 等)
```

## 3. 元件關係圖

```mermaid
flowchart TD
    Browser[瀏覽器 (使用者介面)]
    
    subgraph Flask App [Flask 應用程式]
        Controller[路由 Controller (app/routes/)]
        Template[Jinja2 Template (app/templates/)]
        Model[資料模型 Model (app/models/)]
    end
    
    Database[(SQLite 資料庫)]
    AI_API[外部 AI 模型 API]

    %% 請求流程
    Browser -- "HTTP 請求 (GET/POST)" --> Controller
    Controller -- "1. 呼叫取得或寫入資料" --> Model
    Model -- "2. SQL 查詢" --> Database
    Database -. "3. 回傳資料" .-> Model
    Model -. "4. 回傳 Python 物件" .-> Controller
    
    %% AI 估價流程
    Controller -- "API 呼叫 (取得估價)" --> AI_API
    AI_API -. "回傳估價區間" .-> Controller

    %% 回應流程
    Controller -- "5. 傳遞資料給模板" --> Template
    Template -- "6. 渲染 HTML" --> Controller
    Controller -- "HTTP 回應 (HTML/JSON)" --> Browser
```

## 4. 關鍵設計決策

1. **捨棄前後端分離架構**：
   考量到開發速度與團隊組成，初期採用 Jinja2 進行 Server-Side Rendering (SSR)。這能簡化跨網域 (CORS) 與狀態管理的複雜度，專注於完成「搜尋/過濾」與「AI估價」兩大核心價值。

2. **AI 估價採用獨立 API Route**：
   在發布商品時，使用者填寫完分類與品牌後，前端將透過 AJAX (JavaScript) 呼叫 `/api/estimate-price` 來即時取得建議價格，而不需重新整理頁面。這讓使用者體驗更順暢。

3. **使用 SQLite + sqlite3 模組**：
   為求輕量與易於理解，直接使用 Python 內建的 `sqlite3` 而非龐大的 ORM（如 SQLAlchemy）。搭配 `sqlite3.Row` factory，能讓資料操作像字典一樣直覺，且方便直接撰寫 SQL 處理複雜的搜尋與過濾邏輯。
