from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cognitive_deception.core.config import get_settings

try:
    from neo4j import GraphDatabase
except Exception:  # pragma: no cover
    GraphDatabase = None


@dataclass
class GraphEdge:
    source: str
    relation: str
    target: str
    properties: dict[str, Any]


class KnowledgeGraphEngine:
    """Hybrid knowledge graph sink: Neo4j when enabled, in-memory graph fallback otherwise."""

    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self._driver = None
        self._edges: list[GraphEdge] = []

        if settings.enable_neo4j and GraphDatabase is not None:
            try:
                self._driver = GraphDatabase.driver(
                    settings.neo4j_uri,
                    auth=(settings.neo4j_user, settings.neo4j_password),
                )
            except Exception:
                self._driver = None

    def record_attack_edge(self, attacker: str, tool: str, technique: str, target: str, metadata: dict[str, Any]) -> None:
        edge = GraphEdge(
            source=f"Attacker:{attacker}",
            relation="USED",
            target=f"Technique:{technique}",
            properties={"tool": tool, "target": target, **metadata},
        )
        self._edges.append(edge)

        if self._driver is None:
            return

        query = (
            "MERGE (a:Attacker {id: $attacker}) "
            "MERGE (t:Technique {id: $technique}) "
            "MERGE (srv:Target {id: $target}) "
            "MERGE (a)-[r:USED {tool: $tool}]->(t) "
            "MERGE (a)-[:TARGETED]->(srv) "
            "SET r += $metadata"
        )
        try:
            with self._driver.session() as session:
                session.run(
                    query,
                    attacker=attacker,
                    technique=technique,
                    target=target,
                    tool=tool,
                    metadata=metadata,
                )
        except Exception:
            pass

    def get_local_snapshot(self) -> list[dict[str, Any]]:
        return [
            {
                "source": edge.source,
                "relation": edge.relation,
                "target": edge.target,
                "properties": edge.properties,
            }
            for edge in self._edges[-100:]
        ]
