# SPEC-001：術語庫核心 API

| 欄位 | 內容 |
|------|------|
| **SPEC ID** | SPEC-001 |
| **狀態** | Accepted |
| **ADR 關聯** | ADR-001 |
| **建立日期** | 2026-05-10 |
| **最後更新** | 2026-05-10 |
| **追溯性（Traceability）** | `src/security_glossary_tw/glossary.py`, `src/security_glossary_tw/matcher.py`, `src/security_glossary_tw/validator.py` |

---

## 目標（Goal）

提供結構化、可機器讀取的繁體中文資安術語庫，並以 Python 套件形式對外提供查詢、比對、驗證 API。

---

## 使用情境（User Stories）

| ID | 角色 | 需求 | 接受條件 |
|----|------|------|---------|
| US-01 | 開發者 | 依 ID 查詢術語 | `glossary.get("apt")` 回傳含所有欄位的 `Term` 物件 |
| US-02 | 開發者 | 模糊比對文本中的術語 | `glossary.find_terms(text)` 回傳 `TermMatch` 列表，含位置資訊 |
| US-03 | 編輯者 | 驗證文本用詞是否符合規範 | `glossary.validate(text)` 回傳 `ValidationIssue` 列表 |
| US-04 | 整合方 | 以 JSON API 取得全部術語 | GET `/api/v1/terms.json` 回傳所有術語 |
| US-05 | 貢獻者 | 新增術語至對應分類 YAML | 術語通過 YAML schema 驗證後可被 `Glossary` 載入 |

---

## 介面定義（Interface）

### Python API

```python
from security_glossary_tw import Glossary

g = Glossary()

# 查詢
term = g.get("apt")           # -> Term | None
results = g.search("釣魚")    # -> list[Term]

# 比對
matches = g.find_terms(text)  # -> list[TermMatch]

# 驗證
issues = g.validate(text)     # -> list[ValidationIssue]
```

### 資料模型（關鍵欄位）

```
Term:
  id: str                      # 唯一識別碼（小寫底線）
  term_en: str
  term_zh: str
  definitions.brief: str       # ≤30 字
  definitions.standard: str    # ≤100 字（選填）
  definitions.detailed: str    # 完整說明（選填）
  category: Category
  metadata.status: approved | pending | deprecated
```

---

## 副作用（Side Effects）

- `Glossary()` 初始化時從磁碟讀取所有 `terms/*.yaml`，記憶體佔用與術語數量線性成長（目前 ~428 筆，約 5-10 MB）
- `validate()` 不修改輸入文本，只回傳 `ValidationIssue` 列表（無副作用）
- `find_terms()` 不修改術語庫狀態（唯讀）
- JSON API 由 CI 靜態產生，不支援即時新增術語

---

## 邊界情況（Edge Cases）

| 情境 | 預期行為 |
|------|---------|
| `get()` 傳入不存在 ID | 回傳 `None`，不拋例外 |
| `find_terms()` 輸入空字串 | 回傳空列表 |
| `validate()` 輸入純英文 | 回傳空列表（無禁止用詞）|
| YAML 術語有重複 ID | `Glossary()` 初始化時覆蓋前一筆（最後一筆勝出），CI 驗證應捕捉此情況 |
| `definitions.brief` 超過 30 字 | `validate()` 不檢查，由 YAML schema CI 測試捕捉 |

---

## 完成條件（Done When）

- [ ] `Glossary().get(id)` 對所有現存 YAML 術語回傳正確物件
- [ ] `find_terms()` 對已知術語名稱的文本回傳至少一個 match
- [ ] `validate()` 對包含禁止用詞的文本回傳對應 `ValidationIssue`
- [ ] 所有 YAML 術語通過 CI schema 驗證（`pytest`）
- [ ] JSON API 可由 GitHub Pages 存取（`/api/v1/terms.json`）

---

## 測試矩陣

| 測試場景 | 輸入 | 預期輸出 | 對應 Done When |
|---------|------|---------|--------------|
| 查詢存在術語 | `g.get("apt")` | `Term(id="apt", term_zh="進階持續性威脅")` | US-01 |
| 查詢不存在術語 | `g.get("notexist")` | `None` | US-01 |
| 模糊搜尋中文 | `g.search("釣魚")` | 含 `spear_phishing` 的列表 | US-02 |
| 文本術語比對 | `"APT 攻擊"` | `[TermMatch(term_id="apt", ...)]` | US-02 |
| 禁止用詞驗證 | `"黑客入侵"` | `[ValidationIssue(word="黑客", suggestion="駭客")]` | US-03 |
| 合規文本驗證 | `"駭客利用漏洞"` | `[]` | US-03 |

---

## 排除範圍（Out of Scope）

- 即時 API Server（本 SPEC 只涵蓋靜態 GitHub Pages JSON API）
- 術語審核 UI（由 security-weekly-mcp 的 MCP tools 負責）
- 多語系支援（目前只有繁體中文 / 英文）
