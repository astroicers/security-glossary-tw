"""測試術語庫核心功能"""

import pytest

from security_glossary_tw import Glossary


@pytest.fixture
def glossary():
    """建立術語庫實例"""
    return Glossary()


class TestGlossaryBasic:
    """基本功能測試"""

    def test_load_terms(self, glossary):
        """測試載入術語"""
        terms = list(glossary._terms.values())
        assert len(terms) > 0, "應該載入至少一個術語"

    def test_get_term_by_id(self, glossary):
        """測試用 ID 取得術語"""
        term = glossary.get("phishing")
        assert term is not None
        assert term.id == "phishing"
        assert term.term_en == "Phishing"
        assert term.term_zh == "網路釣魚"

    def test_get_nonexistent_term(self, glossary):
        """測試取得不存在的術語"""
        term = glossary.get("nonexistent_term_xyz")
        assert term is None

    def test_term_has_definitions(self, glossary):
        """測試術語有定義"""
        term = glossary.get("phishing")
        assert term.definitions is not None
        assert term.definitions.brief is not None
        assert len(term.definitions.brief) > 0


class TestTermCategories:
    """術語分類測試"""

    def test_has_attack_types(self, glossary):
        """測試有攻擊類型術語"""
        terms = [t for t in glossary._terms.values() if t.category == "attack_types"]
        assert len(terms) > 0

    def test_has_vulnerabilities(self, glossary):
        """測試有漏洞類型術語"""
        terms = [t for t in glossary._terms.values() if t.category == "vulnerabilities"]
        assert len(terms) > 0

    def test_has_malware(self, glossary):
        """測試有惡意程式術語"""
        terms = [t for t in glossary._terms.values() if t.category == "malware"]
        assert len(terms) > 0

    def test_has_threat_actors(self, glossary):
        """測試有威脅行為者術語"""
        terms = [t for t in glossary._terms.values() if t.category == "threat_actors"]
        assert len(terms) > 0


class TestSpecificTerms:
    """特定術語測試"""

    def test_apt_term(self, glossary):
        """測試 APT 術語"""
        term = glossary.get("apt")
        assert term is not None
        assert term.term_zh == "進階持續性威脅"

    def test_ransomware_term(self, glossary):
        """測試勒索軟體術語"""
        term = glossary.get("ransomware")
        assert term is not None
        assert term.term_zh == "勒索軟體"

    def test_sql_injection_term(self, glossary):
        """測試 SQL 注入術語"""
        term = glossary.get("sql_injection")
        assert term is not None
        assert "SQL" in term.term_en or "sql" in term.term_en.lower()


class TestTermSearch:
    """術語搜尋測試"""

    def test_search_by_name(self, glossary):
        """測試用名稱搜尋"""
        # 使用內部 _terms_by_name 索引
        if hasattr(glossary, "_terms_by_name"):
            assert "phishing" in glossary._terms_by_name or "Phishing" in glossary._terms_by_name
