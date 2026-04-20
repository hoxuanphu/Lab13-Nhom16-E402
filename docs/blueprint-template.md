# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: 
- [REPO_URL]: 
- [MEMBERS]:
  - Member A: [Name] | Role: Logging & PII
  - Member B: [Name] | Role: Tracing & Enrichment
  - Member C: Nguyễn Minh Trí | Role: SLO & Alerts
  - Member D:  |Load test & incident injection
  - Member E: Phạm Anh Quân | Dashboard & evidence
  - Member F: [Name] | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: /100
- [TOTAL_TRACES_COUNT]: 
- [PII_LEAKS_FOUND]: 

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Path to image]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Path to image]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: [Path to image]
- [TRACE_WATERFALL_EXPLANATION]: (Briefly explain one interesting span in your trace)

### 3.2 Dashboard & SLOs

- [DASHBOARD_6_PANELS_SCREENSHOT]: ![alt text](Lab13-Nhom16-E402\screenshots\dashboard.png)
- [SLO_TABLE]:  

| SLI | Target | Window | Current Value |  
| --- | --- | --- | --- |  
| Latency P95 | < 2500ms | 28d | 150.0ms |  
| Error Rate | < 1% | 28d | 0.00% |  
| Cost Budget | < $2.0/day | 1d | $0.11 |  
=======


### 3.3 Alerts & Runbook
- ALERT_RULES_SCREENSHOT: [docs/screenshots/current_dashboard.png](https://github.com/hoxuanphu/Lab13-Nhom16-E402/blob/main/screenshots/alert.png)
- SAMPLE_RUNBOOK_LINK: [docs/alerts.md#1-high-latency-p95](https://github.com/hoxuanphu/Lab13-Nhom16-E402/blob/main/docs/alerts.md#1-high-latency-p95)

---

## 4. Incident Response (Group)
- SCENARIO_NAME: rag_slow  
- SYMPTOMS_OBSERVED: During the load test, the P95 latency for API requests climbed towards the 2500ms threshold. While the system remained functional, tracing revealed significant bottlenecks in the vector retrieval phase, resulting in a degraded user experience.
- ROOT_CAUSE_PROVED_BY: Proven by log entry at 2026-04-20T07:49:34.226583Z (Correlation ID: req-b3a6d363) which explicitly captured the `incident_enabled` event for the `rag_slow` scenario. Subsequent traces confirmed retrieval spans taking >90% of the request time.
- FIX_ACTION: The emergency response was to disable the mock incident and transition the retrieval pipeline to a fallback keyword-based search to restore acceptable performance.
- PREVENTIVE_MEASURE: We recommend implementing a circuit breaker pattern for the RAG service and scaling the vector store horizontally to handle higher concurrency.
---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: (Link to specific commit or PR)

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### Nguyễn Minh Trí
- [TASKS_COMPLETED]: 
  - Defined SLIs/SLOs for Latency, Error Rate, Cost, and Quality.
  - Configured Alertmanager-style alert rules for incident scenarios.
  - Authored runbooks with specific mitigation steps for RAG and LLM failures.
- [EVIDENCE_LINK]: [first commit](https://github.com/hoxuanphu/Lab13-Nhom16-E402/commit/aaea471954ab6e42c985a54145c98c8392f92e84)

### [MEMBER_D_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_E_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)
