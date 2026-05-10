# Changelog

本檔案依照 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/) 格式記錄版本變更。

---

## [Unreleased]

### Changed
- 更新 README：移除 Monorepo 遷移警告，修正術語數量至實際值（428）

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
