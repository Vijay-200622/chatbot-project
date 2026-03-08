"""Concept map generator using LLM + Graphviz."""

import graphviz
import tempfile
from pathlib import Path

from backend.services.llm_engine import generate_response
from data.system_prompts import CONCEPT_MAP_PROMPT


def generate_concept_map(topic: str) -> dict:
    """Generate a concept map for a topic.

    Returns dict with keys: dot_source, svg, edges, image_path.
    """
    prompt = f"Create a concept map for NCERT topic: {topic}"
    raw = generate_response(prompt, CONCEPT_MAP_PROMPT, max_tokens=600)

    # Parse "parent -> child" lines
    edges = []
    for line in raw.strip().split("\n"):
        line = line.strip()
        if "->" in line:
            parts = line.split("->", 1)
            if len(parts) == 2:
                parent = parts[0].strip().strip('"').strip("'")
                child = parts[1].strip().strip('"').strip("'")
                if parent and child:
                    edges.append((parent, child))

    # Fallback if LLM didn't give proper format
    if not edges:
        edges = [(topic, "Sub-concept 1"), (topic, "Sub-concept 2"), (topic, "Sub-concept 3")]

    # Build Graphviz diagram
    dot = graphviz.Digraph(
        comment=f"Concept Map: {topic}",
        format="svg",
        graph_attr={
            "rankdir": "TB",
            "bgcolor": "#FAFAFA",
            "fontname": "Arial",
            "pad": "0.5",
        },
        node_attr={
            "shape": "roundedbox",
            "style": "filled",
            "fillcolor": "#E3F2FD",
            "fontname": "Arial",
            "fontsize": "11",
            "color": "#1565C0",
        },
        edge_attr={
            "color": "#42A5F5",
            "arrowsize": "0.8",
        },
    )

    # Root node gets special styling
    root_nodes = set()
    child_nodes = set()
    for parent, child in edges:
        root_nodes.add(parent)
        child_nodes.add(child)
    true_roots = root_nodes - child_nodes

    for node in true_roots:
        dot.node(node, node, fillcolor="#FF8A65", fontcolor="white", fontsize="13")

    for parent, child in edges:
        if parent not in true_roots:
            dot.node(parent, parent)
        dot.node(child, child)
        dot.edge(parent, child)

    # Render to temp file
    tmp_dir = tempfile.mkdtemp()
    output_path = Path(tmp_dir) / "concept_map"
    rendered_path = dot.render(filename=str(output_path), cleanup=True)

    svg_content = Path(rendered_path).read_text(encoding="utf-8")

    return {
        "dot_source": dot.source,
        "svg": svg_content,
        "edges": edges,
        "image_path": rendered_path,
    }
