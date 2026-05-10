# Changelog

本檔案依照 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/) 格式記錄版本變更。

---

## [Unreleased]

### Added
- 新增 ASP 合規文件：`docs/adr/ADR-001-initial-technology-stack.md`（Accepted）
- 新增 SPEC-001 核心 API 規格：`docs/specs/SPEC-001-glossary-core.md`（含 7 欄位 + Done When）
- 新增 `requirements.txt` 列出 runtime 依賴（pyyaml, pydantic, rapidfuzz）
- 新增測試覆蓋：`TestFindTerms`（3 項）、`TestValidate`（3 項）對應 SPEC-001 DW-2/DW-3

### Changed
- 更新 README：移除 Monorepo 遷移警告，修正術語數量至實際值（428），新增 `pending/` 說明
- 更新 `.gitignore`：改為精確排除 docs 子目錄（保留 docs/adr、docs/specs）

---

## [0.2.0] - 2026-02-01

### Added
- 新增 104 個術語，涵蓋各分類（2026-01-31）
- 新增 58 個 related_terms 連結以完整化術語關聯
- 新增 18+ 個術語擴展詞彙表
- 新增可點擊的 tag 頁面與熱門標籤區
- 新增分類側邊欄導航

### Changed
- 更新 README，移除舊版相關專案連結

---

## [0.1.0] - 2025-12-04

### Added
- 初始建立：160 個資安術語（attack_types, vulnerabilities, threat_actors, malware, technologies, frameworks, compliance）
- GitHub Pages 網站（MkDocs Material）
- YAML 驗證測試與 CI workflow
- 術語 JSON API（`/api/v1/terms.json`）
- 版本標籤 tag 系統

### Fixed
- 移除 YAML 檔案中的 trailing spaces
- 修復 snake_case ID 格式
- 移除重複 term ID

---

## [0.0.1] - 2025-12-03

### Added
- Initial commit：專案骨架、Python 套件（`security_glossary_tw`）、基本 YAML 術語庫
