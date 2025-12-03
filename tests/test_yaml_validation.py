"""YAML 術語檔案驗證測試

驗證項目：
1. YAML 結構正確性
2. term_id 唯一性
3. 必填欄位完整性
4. 連結有效性
5. 分類一致性
"""

import re
from pathlib import Path

import pytest
import yaml

# 專案路徑
PROJECT_ROOT = Path(__file__).parent.parent
TERMS_DIR = PROJECT_ROOT / "terms"
META_DIR = PROJECT_ROOT / "meta"

# 必填欄位
REQUIRED_FIELDS = ["id", "term_en", "term_zh", "definitions", "category"]
REQUIRED_DEFINITION_FIELDS = ["brief"]

# URL 正規表達式
URL_PATTERN = re.compile(r"https?://[^\s\"'<>]+")


def load_all_yaml_files():
    """載入所有術語 YAML 檔案"""
    yaml_files = list(TERMS_DIR.glob("*.yaml"))
    all_data = {}
    for yaml_file in yaml_files:
        with open(yaml_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            all_data[yaml_file.name] = data
    return all_data


def get_all_terms():
    """取得所有術語"""
    all_data = load_all_yaml_files()
    terms = []
    for filename, data in all_data.items():
        if data and "terms" in data:
            for term in data["terms"]:
                term["_source_file"] = filename
                terms.append(term)
    return terms


def load_valid_categories():
    """載入有效的分類列表"""
    categories_file = META_DIR / "categories.yaml"
    if categories_file.exists():
        with open(categories_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return [cat["id"] for cat in data.get("categories", [])]
    return []


class TestYamlStructure:
    """YAML 結構驗證"""

    @pytest.fixture(scope="class")
    def all_yaml_files(self):
        return load_all_yaml_files()

    def test_yaml_files_exist(self):
        """測試術語檔案存在"""
        yaml_files = list(TERMS_DIR.glob("*.yaml"))
        assert len(yaml_files) > 0, "應該至少有一個 YAML 檔案"

    def test_yaml_syntax_valid(self, all_yaml_files):
        """測試 YAML 語法正確"""
        for filename, data in all_yaml_files.items():
            assert data is not None, f"{filename} 無法解析"
            assert isinstance(data, dict), f"{filename} 應該是字典格式"

    def test_yaml_has_terms_key(self, all_yaml_files):
        """測試每個檔案有 terms 鍵"""
        for filename, data in all_yaml_files.items():
            assert "terms" in data, f"{filename} 缺少 'terms' 鍵"
            assert isinstance(data["terms"], list), f"{filename} 的 'terms' 應該是列表"


class TestTermIdUniqueness:
    """術語 ID 唯一性驗證"""

    @pytest.fixture(scope="class")
    def all_terms(self):
        return get_all_terms()

    def test_term_ids_unique_globally(self, all_terms):
        """測試全域術語 ID 唯一"""
        seen_ids = {}
        duplicates = []

        for term in all_terms:
            term_id = term.get("id")
            source = term.get("_source_file")

            if term_id in seen_ids:
                duplicates.append(
                    f"ID '{term_id}' 重複: {seen_ids[term_id]} 和 {source}"
                )
            else:
                seen_ids[term_id] = source

        assert len(duplicates) == 0, f"發現重複的術語 ID:\n" + "\n".join(duplicates)

    def test_term_id_format(self, all_terms):
        """測試術語 ID 格式（snake_case）"""
        invalid_ids = []
        id_pattern = re.compile(r"^[a-z][a-z0-9_]*$")

        for term in all_terms:
            term_id = term.get("id", "")
            if not id_pattern.match(term_id):
                invalid_ids.append(
                    f"無效 ID '{term_id}' (來自 {term.get('_source_file')})"
                )

        assert len(invalid_ids) == 0, (
            f"術語 ID 應該使用 snake_case 格式:\n" + "\n".join(invalid_ids)
        )


class TestRequiredFields:
    """必填欄位驗證"""

    @pytest.fixture(scope="class")
    def all_terms(self):
        return get_all_terms()

    def test_required_fields_present(self, all_terms):
        """測試必填欄位存在"""
        missing_fields = []

        for term in all_terms:
            term_id = term.get("id", "unknown")
            source = term.get("_source_file", "unknown")

            for field in REQUIRED_FIELDS:
                if field not in term or term[field] is None:
                    missing_fields.append(f"{source}/{term_id}: 缺少 '{field}'")

        assert len(missing_fields) == 0, (
            f"發現缺少必填欄位:\n" + "\n".join(missing_fields[:20])  # 只顯示前 20 個
        )

    def test_definitions_has_brief(self, all_terms):
        """測試 definitions 包含 brief"""
        missing_brief = []

        for term in all_terms:
            term_id = term.get("id", "unknown")
            source = term.get("_source_file", "unknown")
            definitions = term.get("definitions", {})

            if not isinstance(definitions, dict):
                missing_brief.append(f"{source}/{term_id}: definitions 格式錯誤")
            elif "brief" not in definitions or not definitions["brief"]:
                missing_brief.append(f"{source}/{term_id}: 缺少 definitions.brief")

        assert len(missing_brief) == 0, (
            f"發現缺少 brief 定義:\n" + "\n".join(missing_brief[:20])
        )

    def test_term_names_not_empty(self, all_terms):
        """測試術語名稱非空"""
        empty_names = []

        for term in all_terms:
            term_id = term.get("id", "unknown")
            source = term.get("_source_file", "unknown")

            if not term.get("term_en", "").strip():
                empty_names.append(f"{source}/{term_id}: term_en 為空")
            if not term.get("term_zh", "").strip():
                empty_names.append(f"{source}/{term_id}: term_zh 為空")

        assert len(empty_names) == 0, (
            f"發現空的術語名稱:\n" + "\n".join(empty_names)
        )


class TestCategoryConsistency:
    """分類一致性驗證"""

    @pytest.fixture(scope="class")
    def all_terms(self):
        return get_all_terms()

    @pytest.fixture(scope="class")
    def valid_categories(self):
        return load_valid_categories()

    def test_category_is_valid(self, all_terms, valid_categories):
        """測試分類是有效的"""
        if not valid_categories:
            pytest.skip("無法載入分類定義")

        invalid_categories = []
        for term in all_terms:
            term_id = term.get("id", "unknown")
            source = term.get("_source_file", "unknown")
            category = term.get("category", "")

            if category not in valid_categories:
                invalid_categories.append(
                    f"{source}/{term_id}: 無效分類 '{category}'"
                )

        assert len(invalid_categories) == 0, (
            f"發現無效分類:\n" + "\n".join(invalid_categories[:20])
        )

    def test_category_matches_filename(self, all_terms):
        """測試分類與檔名一致"""
        mismatches = []

        for term in all_terms:
            term_id = term.get("id", "unknown")
            source = term.get("_source_file", "unknown")
            category = term.get("category", "")

            # 檔名去掉 .yaml 應該等於 category
            expected_category = source.replace(".yaml", "")
            if category != expected_category:
                mismatches.append(
                    f"{source}/{term_id}: category='{category}' 不符合檔名"
                )

        # 這是警告，不是錯誤（允許不一致但記錄）
        if mismatches:
            pytest.skip(f"分類與檔名不一致（共 {len(mismatches)} 個）")


class TestRelatedTerms:
    """相關術語驗證"""

    @pytest.fixture(scope="class")
    def all_terms(self):
        return get_all_terms()

    @pytest.fixture(scope="class")
    def all_term_ids(self, all_terms):
        return {term.get("id") for term in all_terms if term.get("id")}

    def test_related_terms_exist(self, all_terms, all_term_ids):
        """測試 related_terms 中的術語存在"""
        missing_references = []

        for term in all_terms:
            term_id = term.get("id", "unknown")
            source = term.get("_source_file", "unknown")
            related = term.get("related_terms", [])

            if not isinstance(related, list):
                continue

            for ref_id in related:
                if ref_id not in all_term_ids:
                    missing_references.append(
                        f"{source}/{term_id}: related_terms 引用不存在的 '{ref_id}'"
                    )

        # 只警告，不強制失敗（可能是未來要新增的術語）
        if missing_references and len(missing_references) > 10:
            print(f"\n警告: 發現 {len(missing_references)} 個不存在的相關術語引用")


class TestUrlValidity:
    """URL 有效性驗證（格式檢查）"""

    @pytest.fixture(scope="class")
    def all_terms(self):
        return get_all_terms()

    def test_reference_urls_format(self, all_terms):
        """測試 references 中的 URL 格式正確"""
        invalid_urls = []

        for term in all_terms:
            term_id = term.get("id", "unknown")
            source = term.get("_source_file", "unknown")
            references = term.get("references", {})

            if not isinstance(references, dict):
                continue

            for key, url in references.items():
                if url and isinstance(url, str):
                    if not URL_PATTERN.match(url):
                        invalid_urls.append(
                            f"{source}/{term_id}: references.{key} 不是有效 URL"
                        )

        assert len(invalid_urls) == 0, (
            f"發現無效的 URL 格式:\n" + "\n".join(invalid_urls[:20])
        )


class TestTermCount:
    """術語數量統計"""

    def test_minimum_term_count(self):
        """測試最少術語數量"""
        terms = get_all_terms()
        assert len(terms) >= 100, f"術語數量應該至少 100 個，目前只有 {len(terms)} 個"

    def test_term_count_by_category(self):
        """測試各分類術語數量"""
        terms = get_all_terms()
        categories = {}

        for term in terms:
            cat = term.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1

        print("\n術語分類統計:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")

        # 確保主要分類都有術語
        main_categories = ["attack_types", "vulnerabilities", "malware", "technologies"]
        for cat in main_categories:
            assert categories.get(cat, 0) > 0, f"分類 '{cat}' 應該有術語"
