from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

load_dotenv(override=True)


def _resolve_host() -> str:
    return (
        os.getenv("LANGFUSE_HOST")
        or os.getenv("LANGFUSE_BASE_URL")
        or "https://cloud.langfuse.com"
    )


def _resolve_environment() -> str:
    return (
        os.getenv("LANGFUSE_TRACING_ENVIRONMENT")
        or os.getenv("APP_ENV")
        or "dev"
    )


try:
    from langfuse import Langfuse, observe, propagate_attributes

    langfuse_context = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        base_url=_resolve_host(),
        environment=_resolve_environment(),
        flush_at=1,
        flush_interval=0.5,
    )
except Exception:  # pragma: no cover
    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    def propagate_attributes(*args: Any, **kwargs: Any):
        class _DummyCtx:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        return _DummyCtx()

    class _DummyContext:
        def start_as_current_observation(self, **kwargs: Any):
            class _Span:
                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc, tb):
                    return False

                def update(self, **kwargs: Any) -> None:
                    return None

            return _Span()

        def set_current_trace_io(self, **kwargs: Any) -> None:
            return None

        def update_current_span(self, **kwargs: Any) -> None:
            return None

        def flush(self) -> None:
            return None

    langfuse_context = _DummyContext()


def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))