# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: 
- [REPO_URL]: 
- [MEMBERS]:
  - Member A: [Name] | Role: Logging & PII
  - Member B: Đào Danh Đăng Phụng | Role: Tracing & Enrichment
  - Member C: Nguyễn Minh Trí | Role: SLO & Alerts
  - Member D: [Name] | Role: Load Test & Dashboard
  - Member E: [Name] | Role: Demo & Report

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
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: screenshots/langfuse_trace_detail_input_output.png
- [TRACE_WATERFALL_EXPLANATION]: Ảnh hiện tại là màn hình chi tiết của trace trên Langfuse, hiển thị rõ phần `Input`, `Output` và `Metadata` của cùng một request. Trong đó, `Input` cho thấy các trường `user_id`, `feature`, `session_id`, `message`, `correlation_id`, `env`; còn `Metadata` cho thấy các thông tin enrichment như `env`, `model`, `user_id_hash`, `usage_input_tokens`, `usage_output_tokens`, `correlation_id`, `feature`, `query_preview`, `doc_count`, `trace_name`. Đây là bằng chứng rằng tracing và enrichment đã hoạt động đúng với role Member B. Ảnh này không phải waterfall timeline mà là trace detail/preview view, nên nếu nhóm muốn có watermark/waterfall đúng nghĩa thì cần chụp thêm một ảnh span timeline riêng từ cùng trace đó.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 2500ms | 28d | (Pending Load Test) |
| Error Rate | < 1% | 28d | (Pending Load Test) |
| Quality Score | > 0.8 | 28d | (Pending Load Test) |
| Cost Budget | < $2.0/day | 1d | (Pending Load Test) |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: [docs/screenshots/alert_rules.png]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#1-high-latency-p95]

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: (e.g., rag_slow)
- [SYMPTOMS_OBSERVED]: 
- [ROOT_CAUSE_PROVED_BY]: (List specific Trace ID or Log Line)
- [FIX_ACTION]: 
- [PREVENTIVE_MEASURE]: 

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: (Link to specific commit or PR)

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]:
  - Mình phụ trách phần tracing và enrichment cho Langfuse. Mình đã nâng và sửa tích hợp theo SDK v4, để ứng dụng có thể gửi trace thành công lên Langfuse Cloud và hiển thị đúng môi trường `dev`.
  - Trong `app/agent.py`, mình đã instrument từng request `/chat` thành một trace có root name `qa-s07`/`qa-s10` tùy phiên, rồi tách thêm các bước con `retrieve`, `generate`, `quality_check` để waterfall hiện rõ hơn.
  - Mình đã enrich trace bằng các trường: `user_id_hash`, `session_id`, `feature`, `model`, `env`, `correlation_id`, `doc_count`, `query_preview`, `usage_input_tokens`, `usage_output_tokens`. Nhờ vậy trace có đủ ngữ cảnh để truy vết và lọc theo từng phiên.
  - Mình đã cấu hình client để flush sớm sau mỗi request, đồng thời kiểm tra end-to-end bằng `scripts/load_test.py --concurrency 5`. Kết quả là hệ thống tạo được ít nhất 10 traces và toàn bộ trace đều có `environment=dev`.
  - Ảnh waterfall hiện tại trong report cho thấy root trace `qa-s10` và các bước con `retrieve`, `generate`. Đây là bằng chứng tracing đã hoạt động đúng với role Member B.
- [EVIDENCE_LINK]: `app/tracing.py`, `app/agent.py`, `app/main.py`, `.env` (local only), `screenshots/langfuse_trace_waterfall_qa_s10.png`, `screenshots/langfuse_trace_detail_input_output.png`, `screenshots/langfuse_trace_metadata.png`

### Nguyễn Minh Trí
- [TASKS_COMPLETED]: 
  - Defined SLIs/SLOs for Latency, Error Rate, Cost, and Quality.
  - Configured Alertmanager-style alert rules for incident scenarios.
  - Authored runbooks with specific mitigation steps for RAG and LLM failures.
- [EVIDENCE_LINK]: (config/slo.yaml), (config/alert_rules.yaml)

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
