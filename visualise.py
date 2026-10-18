# visualise.py
# This file takes the graph object and renders it as an interactive map in a browser
# Every node becomes a bubble, and every connection becomes a line between the bubbles

from pyvis.network import Network
from graph import Graph

def visualise (graph, output_file="second_brain.html"):
    # takes graph object and produces an interactive html network map
    # 'output_file' is the name of the html file generated
    net = Network(
        height = "750px",
        width = "100%",
        bgcolor = "#1a1a2e",
        font_color = "white"
    )

    category_colours = {
        "Geography": "#e94560",
        "Technology": "#0f3460",
        "Person": "#533483",
        "Concept": "#e94560",
    }

    default_colour = "#457b9d"

    for node in graph.nodes.values():
        colour = category_colours.get(node.category, default_colour)
        size = 20 + (len(node.connections)) * 5
        tooltip = f"{node.name}\nCategory: {node.category}"
        if node.description:
            tooltip += f"\n{node.description}"

        net.add_node(
            node.name,
            label = node.name,
            color = colour,
            size = size,
            title = tooltip
        )

    for node in graph.nodes.values():
        for conn in node.connections:
            net.add_edge(
                node.name,
                conn["to"],
                label = conn["relationship"],
                color = "#888888"
            )

    net.set_options("""
    {
        "physics": {
            "enabled": true,
            "stabilization": {"iterations": 100},
            "barnesHut": {
                "gravitationalConstant": -8000,
                "springConstant": 0.001,
                "springLength": 200
            }
        },
        "edges": {
            "smooth": {"type": "continuous"},
            "font": {"size": 10, "color": "#aaaaaa"}
        },
        "interaction": {
            "hover": true,
            "tooltipDelay": 100
        }
    }
    """)

    net.write_html(output_file)
    print(f"Visualisation saved to {output_file}")
    print("Open that file in your browser to see your second brain!")


# ======================================================================
# Test Area
# ======================================================================

if __name__ == "__main__":

    # Load the existing graph from the JSON file.
    brain = Graph()

    # Generate the visualisation.
    visualise(brain)