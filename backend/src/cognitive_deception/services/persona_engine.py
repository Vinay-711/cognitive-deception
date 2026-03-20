from __future__ import annotations

from typing import Any


class PersonaEngine:
    """Creates and responds as synthetic human personas for social-engineering bait."""

    def respond(self, persona: dict[str, Any], prompt: str) -> str:
        name = persona.get("name", "Alex Mercer")
        role = persona.get("role", "Operations Analyst")
        email = persona.get("email", "ops@example.corp")

        return (
            f"From: {name} <{email}>\n"
            f"Role: {role}\n"
            f"Response: I can share a sanitized access bundle once security approves your request ticket."
            f" Reference token: HR-{abs(hash(prompt)) % 9999:04d}"
        )
