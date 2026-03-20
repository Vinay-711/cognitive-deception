from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AttackGraph:
    nodes: Dict[str, dict] = field(default_factory=dict)
    edges: List[dict] = field(default_factory=list)

    def add_node(self, node_id: str, **attrs) -> None:
        if node_id not in self.nodes:
            self.nodes[node_id] = {}
        self.nodes[node_id].update(attrs)

    def add_edge(self, source: str, target: str, **attrs) -> None:
        self.edges.append({"source": source, "target": target, **attrs})


class AttackGraphBuilder:
    """Builds a lightweight graph of attackers, tools, techniques, and targets."""

    def __init__(self) -> None:
        self.graph = AttackGraph()

    def record_event(self, attacker: str, technique: str, tool: str, target: str) -> AttackGraph:
        self.graph.add_node(attacker, kind="attacker")
        self.graph.add_node(tool, kind="tool")
        self.graph.add_node(technique, kind="technique")
        self.graph.add_node(target, kind="target")

        self.graph.add_edge(attacker, tool, relation="uses")
        self.graph.add_edge(tool, technique, relation="executes")
        self.graph.add_edge(technique, target, relation="targets")

        return self.graph
