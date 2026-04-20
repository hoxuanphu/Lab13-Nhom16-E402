from __future__ import annotations

import os
from typing import Any

try:
    from langfuse import get_client, observe, propagate_attributes
    print("✅ Langfuse SDK loaded successfully!")
    langfuse = get_client()
except Exception as e:
    print(f"❌ Langfuse SDK FAILED to load: {e}")

    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func
        return decorator

    class _DummyLangfuse:
        def auth_check(self) -> bool:
            return False

        def flush(self) -> None:
            return None

    class _DummyPropagate:
        def __call__(self, **kwargs: Any):
            from contextlib import nullcontext
            return nullcontext()

    langfuse = _DummyLangfuse()
    propagate_attributes = _DummyPropagate()


def tracing_enabled() -> bool:
    pub = os.getenv("LANGFUSE_PUBLIC_KEY")
    sec = os.getenv("LANGFUSE_SECRET_KEY")
    base_url = os.getenv("LANGFUSE_BASE_URL") or os.getenv("LANGFUSE_HOST")

    enabled = bool(pub and sec)
    if enabled:
        print(f"📈 Tracing is active. Base URL: {base_url}")
        try:
            print(f"🔐 Langfuse auth_check: {langfuse.auth_check()}")
        except Exception as e:
            print(f"⚠️ auth_check failed: {e}")
    else:
        print("⚠️ Tracing is DISABLED: Missing API keys in environment")

    return enabled