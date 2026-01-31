# Security Glossary TW - 繁體中文資安術語庫

> 台灣第一個開源、結構化、可機器讀取的繁體中文資安專有名詞庫

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Terms Count](https://img.shields.io/badge/術語數量-437-blue.svg)](https://astroicers.github.io/security-glossary-tw/glossary/)

---

## 🎯 專案目標

1. **標準化** - 統一台灣資安社群的專業用詞
2. **可存取** - 提供 YAML、JSON、API 多種格式
3. **可貢獻** - 開源接受社群 PR 貢獻
4. **可整合** - 供其他資安工具/網站串接使用

---

## 📦 安裝方式

### 方式 1：直接使用 YAML 檔案

```bash
git clone https://github.com/astroicers/security-glossary-tw.git
```

### 方式 2：Python 套件

```bash
pip install security-glossary-tw
```

```python
from security_glossary_tw import Glossary

glossary = Glossary()

# 查詢術語
term = glossary.get("apt")
print(term.term_zh)  # 進階持續性威脅
print(term.definitions.brief)  # 國家級駭客組織發動的長期網路攻擊

# 比對文本中的術語
text = "本週發現 APT 組織使用魚叉式釣魚攻擊"
matches = glossary.find_terms(text)
# [Match(term_id='apt', ...), Match(term_id='spear_phishing', ...)]

# 驗證用詞
issues = glossary.validate(text)
# [Issue(line=1, word='病毒', suggestion='惡意程式')]
```

### 方式 3：JSON API

```
https://astroicers.github.io/security-glossary-tw/api/v1/terms.json
https://astroicers.github.io/security-glossary-tw/api/v1/terms/apt.json
```

---

## 📁 專案結構

```
security-glossary-tw/
│
├── terms/                          # 📚 術語定義 (YAML)
│   ├── attack_types.yaml           # 攻擊類型 (79)
│   ├── vulnerabilities.yaml        # 漏洞類型 (51)
│   ├── threat_actors.yaml          # 威脅行為者 (66)
│   ├── malware.yaml                # 惡意程式 (64)
│   ├── technologies.yaml           # 技術名詞 (136)
│   ├── frameworks.yaml             # 框架標準 (27)
│   └── compliance.yaml             # 法規合規 (14)
│
├── meta/                           # 📋 元資料
│   ├── categories.yaml             # 分類定義
│   ├── aliases.yaml                # 別名對照表
│   └── style_guide.yaml            # 用詞風格指南
│
├── src/                            # 🐍 Python 套件
│   └── security_glossary_tw/
│       ├── __init__.py
│       ├── glossary.py             # 主要 API
│       ├── loader.py               # YAML 載入
│       ├── matcher.py              # 術語比對
│       ├── linker.py               # 連結產生
│       ├── validator.py            # 用詞驗證
│       └── models.py               # 資料模型
│
├── site/                           # 🌐 靜態網站
│   ├── index.html
│   ├── glossary/
│   │   └── [term_id].html
│   └── assets/
│
├── api/                            # 📡 JSON API (自動產生)
│   ├── terms.json                  # 全部術語
│   ├── terms/
│   │   └── [term_id].json          # 單一術語
│   └── categories.json             # 分類列表
│
├── scripts/                        # 🔧 工具腳本
│   ├── build_api.py                # 產生 JSON API
│   ├── build_site.py               # 產生靜態網站
│   ├── validate.py                 # 驗證術語庫
│   └── import_external.py          # 匯入外部術語
│
├── tests/                          # 🧪 測試
│   ├── test_glossary.py
│   ├── test_matcher.py
│   └── test_validator.py
│
├── .github/
│   └── workflows/
│       ├── validate.yml            # PR 驗證
│       └── deploy.yml              # 網站部署
│
├── pyproject.toml                  # Python 套件設定
├── requirements.txt
├── LICENSE                         # CC BY 4.0
├── CONTRIBUTING.md                 # 貢獻指南
└── README.md
```

---

## 📖 術語格式

### 完整格式

```yaml
- id: "apt"                                    # 唯一識別碼
  
  # === 基本資訊 ===
  term_en: "APT"                               # 英文術語
  term_zh: "進階持續性威脅"                     # 中文術語
  full_name_en: "Advanced Persistent Threat"   # 英文全稱
  full_name_zh: "進階持續性威脅"                # 中文全稱
  
  # === 定義 ===
  definitions:
    brief: "國家級駭客組織發動的長期網路攻擊"   # ≤30 字
    standard: |                                # ≤100 字
      進階持續性威脅是指由國家政府支持或高度組織化的駭客團體，
      針對特定目標進行長期、隱蔽的網路入侵活動。
    detailed: |                                # 完整說明
      [詳細技術說明...]
  
  # === 分類 ===
  category: "threat_actors"
  subcategory: "actor_type"
  tags: ["國家級攻擊", "長期潛伏", "針對性"]
  
  # === 關聯 ===
  related_terms: ["nation_state_actor", "cyber_espionage"]
  
  # === 別名 ===
  aliases:
    en: ["Advanced Persistent Threat"]
    zh: ["高級持續性威脅", "APT 攻擊"]
  
  # === 使用指南 ===
  usage:
    preferred: true
    context: "描述國家級駭客組織時使用"
    examples:
      - "本週觀察到 APT 組織針對金融業發動攻擊"
    avoid: ["高級黑客攻擊", "APT 病毒"]
  
  # === 參考 ===
  references:
    mitre_attack: "https://attack.mitre.org/groups/"
    nist: "https://csrc.nist.gov/glossary/term/apt"
  
  # === 元資料 ===
  metadata:
    status: "approved"                         # approved | pending | deprecated
    created: "2024-01-01"
    updated: "2024-12-01"
    contributors: ["contributor1"]
```

### 最小格式

```yaml
- id: "apt"
  term_en: "APT"
  term_zh: "進階持續性威脅"
  definitions:
    brief: "國家級駭客組織發動的長期網路攻擊"
  category: "threat_actors"
```

---

## 🏷️ 分類架構

| 分類 ID | 中文名稱 | 數量 |
|---------|----------|------|
| `attack_types` | 攻擊類型 | ~30 |
| `vulnerabilities` | 漏洞類型 | ~25 |
| `threat_actors` | 威脅行為者 | ~20 |
| `malware` | 惡意程式 | ~20 |
| `technologies` | 技術名詞 | ~30 |
| `frameworks` | 框架標準 | ~15 |
| `compliance` | 法規合規 | ~10 |

---

## 🤝 貢獻指南

### 新增術語

1. Fork 此專案
2. 在對應的 `terms/*.yaml` 新增術語
3. 執行驗證：`python scripts/validate.py`
4. 提交 PR

### 術語命名規則

- `id`：小寫英文，底線分隔（如 `sql_injection`）
- `term_en`：業界通用英文術語
- `term_zh`：繁體中文，使用台灣慣用翻譯

### 禁止用詞

請參考 `meta/style_guide.yaml`，避免使用：

| ❌ 避免 | ✅ 使用 |
|--------|--------|
| 黑客 | 駭客 |
| 病毒 | 惡意程式 |
| 軟件 | 軟體 |
| 信息 | 資訊 |

---

## 📜 授權

本專案採用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權。

你可以自由：
- **分享** — 以任何媒介或格式重製及散布本素材
- **改編** — 重混、轉換、以及依照本素材建立新素材

唯須：
- **標示姓名** — 標示出處

---

## 📊 統計

- 術語總數：437
- 分類數：7
- 標籤數：500+
- 最後更新：2026-01-31
