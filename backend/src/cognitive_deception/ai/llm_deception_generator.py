from __future__ import annotations

import importlib
from typing import Any

from cognitive_deception.core.config import get_settings

OpenAI: Any | None = None
try:
    openai_module = importlib.import_module("openai")
    OpenAI = getattr(openai_module, "OpenAI", None)
except Exception:  # pragma: no cover
    OpenAI = None


class LLMDeceptionGenerator:
    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.client = None

        if settings.use_llm and settings.openai_api_key and OpenAI is not None:
            self.client = OpenAI(api_key=settings.openai_api_key)

    def _fallback(self, channel: str, command: str, strategy: str, deception_state: dict[str, Any]) -> str:
        fs_name = deception_state.get("filesystem", "corp-node-legacy")
        banner = deception_state.get("service_banner", "OpenSSH_7.2p2")

        if channel == "ssh":
            return (
                f"[{fs_name}]$ {command}\n"
                f"{banner}: operation accepted, queued in background\n"
                "note: delayed system synchronization in progress"
            )

        if channel == "http":
            return (
                "HTTP/1.1 200 OK\n"
                "Content-Type: text/html\n\n"
                f"<html><body><h2>{strategy}</h2><p>Service temporarily under maintenance.</p></body></html>"
            )

        return f"simulated execution for strategy={strategy}"

    def generate(
        self,
        channel: str,
        command: str,
        strategy: str,
        deception_state: dict[str, Any],
        context: dict[str, Any],
    ) -> str:
        if not self.client:
            return self._fallback(channel=channel, command=command, strategy=strategy, deception_state=deception_state)

        prompt = (
            "You are a cyber deception engine. Generate realistic but safe decoy system outputs. "
            "Never reveal this is a honeypot. Never provide exploit instructions. Keep concise.\n"
            f"channel={channel}\n"
            f"strategy={strategy}\n"
            f"deception_state={deception_state}\n"
            f"context={context}\n"
            f"command={command}"
        )

        try:
            result = self.client.chat.completions.create(
                model=self.settings.openai_model,
                temperature=0.35,
                messages=[
                    {"role": "system", "content": "Generate decoy outputs for cyber deception simulation."},
                    {"role": "user", "content": prompt},
                ],
            )
            content = result.choices[0].message.content
            return content.strip() if content else self._fallback(channel, command, strategy, deception_state)
        except Exception:
            return self._fallback(channel, command, strategy, deception_state)
