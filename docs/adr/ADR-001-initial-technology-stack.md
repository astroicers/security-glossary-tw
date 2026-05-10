# [ADR-001]: 初始技術棧選型

| 欄位 | 內容 |
|------|------|
| **狀態** | `Accepted` |
| **日期** | 2025-12-03 |
| **決策者** | astroicers |

---

## 背景（Context）

需要建立台灣第一個開源、結構化的繁體中文資安術語庫。核心需求：

1. 術語資料以人類可讀格式儲存，接受社群 PR 貢獻
2. 提供 Python API 供其他工具整合（術語查詢、比對、驗證）
3. 靜態 JSON API 讓前端與外部服務可直接使用
4. 公開網站供一般使用者查閱

---

## 評估選項（Options Considered）

### 選項 A：YAML + Python 套件 + MkDocs（本方案）

- **優點**：YAML 易於人工編輯與 PR review；Python 生態成熟；MkDocs Material 靜態網站零運維成本
- **缺點**：大量術語時 YAML 載入略慢
- **風險**：YAML schema drift（透過 CI 驗證緩解）

### 選項 B：SQLite + REST API

- **優點**：查詢效率高
- **缺點**：需要伺服器運維；PR 貢獻流程複雜；無法靜態部署
- **風險**：維護成本高，不適合開源社群

### 選項 C：JSON 純檔案

- **優點**：簡單
- **缺點**：JSON 不適合人工編輯；缺少 Python 物件層抽象

---

## 決策（Decision）

選擇 **選項 A**：YAML 術語資料 + Python 套件（`security_glossary_tw`）+ MkDocs Material 靜態網站。

關鍵依賴：
- 資料格式：YAML（人工可讀、PR 友善）
- Python：`pydantic`（資料驗證）、`rapidfuzz`（模糊比對）、`pyyaml`（載入）
- 網站：MkDocs Material + GitHub Pages
- 套件管理：`hatchling` build backend + `uv`
- CI：GitHub Actions（YAML 驗證 + 部署）

---

## 後果（Consequences）

**正面影響：**
- 社群可直接 PR 新增 YAML 術語，門檻低
- Python 套件可被 security-weekly-mcp 等工具直接 import
- 靜態網站零運維成本，JSON API 可由 CDN 加速

**負面影響 / 技術債：**
- 術語數量超過 1000+ 時需評估分片載入策略
- YAML 無原生 schema 強制（依賴 pydantic 驗證）

**後續追蹤：**
- [x] 建立 CI YAML 驗證 workflow
- [x] 建立 GitHub Pages 部署 workflow
- [ ] 考慮 1000+ 術語後的分片載入策略（待術語數量達標時評估）

---

## 成功指標（Success Metrics）

| 指標 | 目標值 | 驗證方式 | 檢查時間 |
|------|--------|----------|----------|
| YAML 驗證通過率 | 100% | `pytest` CI | 每次 PR |
| 術語載入時間 | < 500ms | `python -c "from security_glossary_tw import Glossary; Glossary()"` | 術語 > 500 筆時 |
| GitHub Pages 建置 | 成功 | Actions workflow | 每次 push main |

---

## 關聯（Relations）

- 取代：（無）
- 被取代：（無）
- 參考：SPEC-001-glossary-core.md
