# Alert Rules and Runbooks

## 1. High latency P95 (Symptom: rag_slow)
- Severity: P2
- Trigger: `latency_p95_ms > 2500 for 5m`
- Impact: Retrieval latency spike causing slow responses for users.
- First checks:
  1. Open Langfuse dashboard and sort traces by `latency`.
  2. Identify if the `rag_retrieval` span is the bottleneck (latency > 1500ms).
  3. Validate if `scripts/inject_incident.py --scenario rag_slow` was executed.
- Mitigation:
  1. Disable `rag_slow` incident: `python scripts/inject_incident.py --scenario rag_slow --disable`.
  2. Implement caching for common RAG queries.
  3. Reduce the number of retrieved documents (`top_k`).

## 2. High error rate (Symptom: tool_fail)
- Severity: P1
- Trigger: `error_rate_pct > 2 for 2m`
- Impact: Users receiving 500 Internal Server Errors; critical system failure.
- First checks:
  1. Inspect `data/logs.jsonl` and group by `error_type`.
  2. Check for `VectorStoreError` or `LLMTimeoutError` in the logs.
  3. Verify the status of incident toggles via `/health` endpoint.
- Mitigation:
  1. Disable `tool_fail` incident.
  2. Fallback to a basic keyword search if the vector store is down.
  3. Implement a retry mechanism with exponential backoff for LLM calls.

## 3. Cost budget spike (Symptom: cost_spike)
- Severity: P2
- Trigger: `avg_cost_usd > 0.05 for 1m`
- Impact: Rapid depletion of API credit budget.
- First checks:
  1. Check `tokens_out` in `response_sent` logs.
  2. Identify if a specific user or session is generating abnormally long outputs.
  3. Compare `input_tokens` vs `output_tokens` in Langfuse spans.
- Mitigation:
  1. Disable `cost_spike` incident.
  2. Enforce `max_tokens` limit on LLM generation.
  3. Route requests to a cheaper model (e.g., GPT-3.5-Turbo instead of GPT-4) for non-critical tasks.
