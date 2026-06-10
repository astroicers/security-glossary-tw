---
title: 資安週報
description: 台灣資安週報，每週更新最新資安威脅、漏洞與新聞
hide:
  - navigation
  - toc
---

# 資安週報

透過 RSS 訂閱，每週自動接收最新資安週報。

[**訂閱 RSS Feed**](feed.xml){ .md-button .md-button--primary }

**Feed URL**: `https://glossary.astroicers.link/weekly/feed.xml`

---

## 週報內容

| | |
|---|---|
| **📰 資安新聞** | 每週整理來自 30+ 來源的重要資安新聞 |
| **🔒 漏洞追蹤** | NVD 高風險漏洞與 CISA KEV 已知被利用漏洞 |
| **📊 威脅趨勢** | 威脅等級評估與行動建議 |
| **📚 術語連結** | 報告內的術語自動連結至術語庫 |
| **🇹🇼 繁體中文** | 使用標準化繁體中文資安術語 |

---

## 歷史週報

<div class="report-list" id="report-list">
載入中...
</div>

<script>
(function() {
  const reportList = document.getElementById('report-list');
  const reportsDir = 'reports/';

  // 從 feed.xml 動態讀取週報清單
  fetch('feed.xml')
    .then(r => r.text())
    .then(xml => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(xml, 'application/xml');
      const items = doc.querySelectorAll('item');
      if (items.length === 0) {
        reportList.innerHTML = '<p>尚無週報，請訂閱 RSS 以獲取最新通知。</p>';
        return;
      }
      let html = '<div class="report-grid">';
      items.forEach(item => {
        const title = item.querySelector('title').textContent;
        const guid = item.querySelector('guid').textContent;
        const pubDate = item.querySelector('pubDate').textContent;
        const date = new Date(pubDate).toISOString().slice(0, 10);
        const weekMatch = guid.match(/(\d+)$/);
        const weekNum = weekMatch ? weekMatch[1] : '';
        const year = guid.match(/(\d{4})/);
        const yearStr = year ? year[1] : '';
        html += `
          <a href="${reportsDir}${guid}.html" class="report-card">
            <div class="report-id">${guid}</div>
            <div class="report-title">${yearStr} 年第 ${parseInt(weekNum)} 週</div>
            <div class="report-date">${date}</div>
          </a>
        `;
      });
      html += '</div>';
      reportList.innerHTML = html;
    })
    .catch(() => {
      reportList.innerHTML = '<p>無法載入週報清單，請<a href="feed.xml">查看 RSS Feed</a>。</p>';
    });
})();
</script>

<style>
.report-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}
.report-card {
  display: block;
  padding: 1.5rem;
  background: var(--md-code-bg-color, #f5f5f5);
  border-radius: 8px;
  border: 1px solid var(--md-default-fg-color--lightest, #ddd);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
}
.report-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.report-id {
  font-family: monospace;
  font-size: 0.9rem;
  color: var(--md-default-fg-color--light, #666);
  margin-bottom: 0.5rem;
}
.report-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.report-date {
  font-size: 0.85rem;
  color: var(--md-default-fg-color--light, #666);
}
</style>

---

## 關於週報

每篇週報包含：

- 威脅等級摘要
- 本週重要資安事件
- CVE 漏洞清單（含 CVSS 評分）
- 行動建議
- **本期術語** - 報告中出現的資安術語及定義

週報由 [security-weekly-mcp](https://github.com/astroicers/security-weekly-mcp) 系統自動產生，整合 [資安術語庫](../glossary/index.md) 提供術語標準化與連結。
