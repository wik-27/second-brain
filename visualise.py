# visualise.py
# This file takes the graph object and renders it as an interactive map in a browser
# Every node becomes a bubble, and every connection becomes a line between the bubbles

import json
from pathlib import Path
from pyvis.network import Network
from graph import Graph

EXTRAS_FILE = Path(__file__).parent / "visual_extras.html"

def visualise(graph, output_file="second_brain.html"):
    # takes graph object and produces an interactive html network map
    # 'output_file' is the name of the html file generated
    net = Network(
        height = "750px",
        width = "100%",
        bgcolor = "#1a1a2e",
        font_color = "white",
        directed = True
    )

    for node in graph.nodes.values():
        size = 28 + (len(node.connections)) * 6
        tooltip = f"{node.name}\nCategory: {node.category}"
        if node.description:
            tooltip += f"\n{node.description}"

        net.add_node(
            node.name,
            label = node.name,
            size = size,
            title = tooltip,
            category = node.category
        )

    for node in graph.nodes.values():
        for conn in node.connections:
            net.add_edge(
                node.name,
                conn["to"],
                label = conn["relationship"]
            )

    options = {
        "nodes": {
            "shape": "dot",
            "borderWidth": 2,
            "font": {"size": 0}
        },
        "edges": {
            "arrows": {"to": {"enabled": True, "scaleFactor": 0.6}},
            "smooth": {"type": "curvedCW", "roundness": 0.2},
            "font": {
                "face": "Menlo",
                "size": 11,
                "color": "#c8c8d8",
                "strokeWidth": 0,
                "background": "#1a1a2e"
            }
        },
        "physics": {
            "enabled": True,
            "stabilization": {"iterations": 100},
            "barnesHut": {
                "gravitationalConstant": -8000,
                "springConstant": 0.001,
                "springLength": 200
            }
        },
        "interaction": {
            "hover": True,
            "tooltipDelay": 100
        }
    }

    net.set_options(json.dumps(options))
    net.write_html(output_file)
 
    page = Path(output_file).read_text(encoding = "utf-8")
    extras = EXTRAS_FILE.read_text(encoding = "utf-8")
    page = page.replace("</body>", extras + "\n</body>")
    Path(output_file).write_text(page, encoding = "utf-8")

    print(f"Visualisation saved to {output_file}")


# ======================================================================
# Test Area
# ======================================================================

if __name__ == "__main__":

    # Load the existing graph from the JSON file.
    brain = Graph()

    # Generate the visualisation.
    visualise(brain)