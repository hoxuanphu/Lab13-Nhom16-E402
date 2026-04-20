from __future__ import annotations

import time
from dataclasses import dataclass

from . import metrics
from .mock_llm import FakeLLM
from .mock_rag import retrieve
from .pii import hash_user_id, summarize_text
from .tracing import langfuse_context, observe, propagate_attributes


@dataclass
class AgentResult:
    answer: str
    latency_ms: int
    tokens_in: int
    tokens_out: int
    cost_usd: float
    quality_score: float


class LabAgent:
    def __init__(self, model: str = "claude-sonnet-4-5") -> None:
        self.model = model
        self.llm = FakeLLM(model=model)

    @observe()
    def run(
        self,
        user_id: str,
        feature: str,
        session_id: str,
        message: str,
        correlation_id: str,
        env: str,
    ) -> AgentResult:
        started = time.perf_counter()
        with propagate_attributes(
            user_id=hash_user_id(user_id),
            session_id=session_id,
            metadata={
                "feature": feature,
                "correlation_id": correlation_id,
                "model": self.model,
                "env": env,
            },
            tags=[feature, env],
        ):
            with langfuse_context.start_as_current_observation(
                as_type="span",
                name=f"{feature}-{session_id}",
                input={
                    "user_id": user_id,
                    "feature": feature,
                    "session_id": session_id,
                    "message": message,
                    "correlation_id": correlation_id,
                    "env": env,
                },
            ) as root_span:
                root_span.update(
                    metadata={
                        "trace_name": f"{feature}-{session_id}",
                        "user_id_hash": hash_user_id(user_id),
                        "model": self.model,
                        "env": env,
                        "feature": feature,
                        "correlation_id": correlation_id,
                    }
                )

                with langfuse_context.start_as_current_observation(
                    as_type="span",
                    name="retrieve",
                    input={"message": message, "feature": feature},
                ) as retrieve_span:
                    docs = retrieve(message)
                    retrieve_span.update(
                        output={"doc_count": len(docs), "docs": docs},
                        metadata={"feature": feature, "correlation_id": correlation_id},
                    )

                prompt = f"Feature={feature}\nDocs={docs}\nQuestion={message}"

                with langfuse_context.start_as_current_observation(
                    as_type="generation",
                    name="generate",
                    input={"prompt": prompt},
                ) as generation_span:
                    response = self.llm.generate(prompt)
                    generation_span.update(
                        output={"answer": response.text},
                        metadata={
                            "feature": feature,
                            "correlation_id": correlation_id,
                            "usage_input_tokens": response.usage.input_tokens,
                            "usage_output_tokens": response.usage.output_tokens,
                        },
                    )

                with langfuse_context.start_as_current_observation(
                    as_type="span",
                    name="quality_check",
                    input={"message": message, "answer_preview": summarize_text(response.text)},
                ) as quality_span:
                    quality_score = self._heuristic_quality(message, response.text, docs)
                    quality_span.update(
                        output={"quality_score": quality_score},
                        metadata={
                            "feature": feature,
                            "correlation_id": correlation_id,
                            "doc_count": len(docs),
                        },
                    )

        latency_ms = int((time.perf_counter() - started) * 1000)
        cost_usd = self._estimate_cost(response.usage.input_tokens, response.usage.output_tokens)

        langfuse_context.set_current_trace_io(
            input={
                "user_id": user_id,
                "feature": feature,
                "session_id": session_id,
                "message": message,
                "correlation_id": correlation_id,
                "env": env,
            },
            output={
                "answer": response.text,
                "latency_ms": latency_ms,
                "tokens_in": response.usage.input_tokens,
                "tokens_out": response.usage.output_tokens,
                "cost_usd": cost_usd,
                "quality_score": quality_score,
            },
        )
        langfuse_context.flush()

        metrics.record_request(
            latency_ms=latency_ms,
            cost_usd=cost_usd,
            tokens_in=response.usage.input_tokens,
            tokens_out=response.usage.output_tokens,
            quality_score=quality_score,
        )

        return AgentResult(
            answer=response.text,
            latency_ms=latency_ms,
            tokens_in=response.usage.input_tokens,
            tokens_out=response.usage.output_tokens,
            cost_usd=cost_usd,
            quality_score=quality_score,
        )

    def _estimate_cost(self, tokens_in: int, tokens_out: int) -> float:
        input_cost = (tokens_in / 1_000_000) * 3
        output_cost = (tokens_out / 1_000_000) * 15
        return round(input_cost + output_cost, 6)

    def _heuristic_quality(self, question: str, answer: str, docs: list[str]) -> float:
        score = 0.5
        if docs:
            score += 0.2
        if len(answer) > 40:
            score += 0.1
        if question.lower().split()[0:1] and any(token in answer.lower() for token in question.lower().split()[:3]):
            score += 0.1
        if "[REDACTED" in answer:
            score -= 0.2
        return round(max(0.0, min(1.0, score)), 2)