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

**Feed URL**: `https://astroicers.github.io/security-glossary-tw/weekly/feed.xml`

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

  // 已知的週報列表（由 CI 自動更新）
  const reports = [
    { id: 'SEC-WEEKLY-2026-07', title: '2026 年第 7 週', date: '2026-02-10' },
    { id: 'SEC-WEEKLY-2026-06', title: '2026 年第 6 週', date: '2026-02-03' },
    { id: 'SEC-WEEKLY-2026-05', title: '2026 年第 5 週', date: '2026-01-27' },
    { id: 'SEC-WEEKLY-2026-04', title: '2026 年第 4 週', date: '2026-01-20' },
    { id: 'SEC-WEEKLY-2026-03', title: '2026 年第 3 週', date: '2026-01-13' },
    { id: 'SEC-WEEKLY-2026-02', title: '2026 年第 2 週', date: '2026-01-06' },
    { id: 'SEC-WEEKLY-2026-01', title: '2026 年第 1 週', date: '2026-01-01' },
  ];

  if (reports.length === 0) {
    reportList.innerHTML = '<p>尚無週報，請訂閱 RSS 以獲取最新通知。</p>';
    return;
  }

  let html = '<div class="report-grid">';
  reports.forEach(report => {
    html += `
      <a href="${reportsDir}${report.id}.html" class="report-card">
        <div class="report-id">${report.id}</div>
        <div class="report-title">${report.title}</div>
        <div class="report-date">${report.date}</div>
      </a>
    `;
  });
  html += '</div>';

  reportList.innerHTML = html;
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
