import xml.etree.ElementTree as ET
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import textwrap
import sys
from pyvis.network import Network


def wrap_label(label, width=40):
    """
    Wrap a label into multiple lines to make it more readable.
    """
    return "\n".join(textwrap.wrap(label, width))


def generate_static_graph_with_wrapped_labels(df, file_name):
    """
    Generate a static graph visualization with line-wrapped labels for better readability.
    Includes the file name in the figure window title bar.
    """
    G = nx.DiGraph()
    node_colors = []
    text_colors = {}
    enhanced_labels = {}

    # Categorize nodes and determine roles
    for _, row in df.iterrows():
        # Add edges
        G.add_edge(row["SourceMethod"], row["SinkMethod"], label=wrap_label(row["SourceStatement"]))

        # Mark nodes as Source, Sink, or Both
        if row["SourceMethod"] not in enhanced_labels:
            enhanced_labels[row["SourceMethod"]] = "Source"
        elif enhanced_labels[row["SourceMethod"]] == "Sink":
            enhanced_labels[row["SourceMethod"]] = "Source + Sink"

        if row["SinkMethod"] not in enhanced_labels:
            enhanced_labels[row["SinkMethod"]] = "Sink"
        elif enhanced_labels[row["SinkMethod"]] == "Source":
            enhanced_labels[row["SinkMethod"]] = "Source + Sink"

    # Set node colors and text colors based on roles
    for node in G.nodes:
        role = enhanced_labels.get(node, "Intermediate")
        if role == "Source":
            node_colors.append("lightgreen")
            text_colors[node] = "darkgreen"
        elif role == "Sink":
            node_colors.append("lightcoral")
            text_colors[node] = "darkred"
        elif role == "Source + Sink":
            node_colors.append("plum")
            text_colors[node] = "purple"
        else:
            node_colors.append("lightblue")
            text_colors[node] = "darkblue"

    # Adjust graph layout
    pos = nx.spring_layout(G, k=0.5)  # Spring layout with adjusted spacing
    plt.figure(figsize=(14, 14))  # Larger figure for better readability

    # Set the window title to the file name
    plt.gcf().canvas.manager.set_window_title(file_name)

    # Draw nodes with reduced size and lighter colors
    nx.draw(
        G,
        pos,
        with_labels=False,
        node_size=1500,  # Reduced size for better text visibility
        node_color=node_colors,
    )

    # Draw node labels with colors and line wrapping
    for node, (x, y) in pos.items():
        plt.text(
            x,
            y + 0.03,
            f"{enhanced_labels[node]}:\n{wrap_label(node)}",
            fontsize=8,
            color=text_colors[node],
            horizontalalignment="center",
        )

    # Draw edge labels with line wrapping
    edge_labels = {(u, v): wrap_label(d["label"]) for u, v, d in G.edges(data=True)}
    for (u, v), label in edge_labels.items():
        # Get positions of source and target nodes
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        # Calculate the mid-point of the edge
        x_mid = (x1 + x2) / 2
        y_mid = (y1 + y2) / 2
        # Draw the label at the mid-point
        plt.text(
            x_mid,
            y_mid,
            label,
            fontsize=8,
            color="black",
            horizontalalignment="center",
            verticalalignment="center",
        )

    # Add legend
    plt.legend(
        handles=[
            plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="lightgreen", markersize=10, label="Source Node"),
            plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="lightcoral", markersize=10, label="Sink Node"),
            plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="plum", markersize=10, label="Source + Sink Node"),
            plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="lightblue", markersize=10, label="Intermediate Node"),
        ],
        loc="upper left",
        title="Node Types",
    )

    # Set the title within the plot
    plt.title("Enhanced Data Flow Graph")
    plt.show()


def generate_interactive_graph_with_wrapped_labels(df, file_name, output_file="dataflow_graph_with_wrapped_labels.html"):
    """
    Generate an interactive graph visualization using PyVis, highlighting roles (Source, Sink, Both).
    Includes line-wrapped labels for better readability.
    """
    net = Network(notebook=False, directed=True)

    # Add nodes and edges with roles
    node_roles = {}
    for _, row in df.iterrows():
        # Track roles for nodes
        node_roles[row["SourceMethod"]] = node_roles.get(row["SourceMethod"], "Source")
        if node_roles[row["SourceMethod"]] == "Sink":
            node_roles[row["SourceMethod"]] = "Source + Sink"

        node_roles[row["SinkMethod"]] = node_roles.get(row["SinkMethod"], "Sink")
        if node_roles[row["SinkMethod"]] == "Source":
            node_roles[row["SinkMethod"]] = "Source + Sink"

        # Add edge
        wrapped_statement = wrap_label(row["SourceStatement"]).replace("\n", "<br>")
        net.add_edge(
            row["SourceMethod"],
            row["SinkMethod"],
            title=f"Taint Flow:<br>{wrapped_statement}",
        )

    # Add nodes with role-based colors and line-wrapped labels
    for node, role in node_roles.items():
        color = "green" if role == "Source" else "red" if role == "Sink" else "purple" if role == "Source + Sink" else "blue"
        wrapped_label = wrap_label(node).replace("\n", "<br>")  # Preprocess label
        label = f"{role}: {wrapped_label}"
        net.add_node(node, label=label, color=color)

    # Customize and save the interactive graph
    net.toggle_physics(True)  # Enable physics for better layout
    net.show_buttons(filter_=["physics"])  # Add physics controls
    net.show(output_file)
    print(f"Interactive graph saved to {output_file}")


def main(file_path):
    try:
        # Parse the XML
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract and structure data
        results = []
        for result in root.findall(".//Result"):
            sink = result.find(".//Sink")
            sources = result.findall(".//Source")
            for source in sources:
                results.append({
                    "SinkStatement": sink.get("Statement"),
                    "SinkMethod": sink.get("Method"),
                    "SourceStatement": source.get("Statement"),
                    "SourceMethod": source.get("Method"),
                })

        # Create a DataFrame
        df = pd.DataFrame(results)

        # Truncate argv[1] to get the file name (without the path)
        file_name = file_path.split("/")[-1].split("\\")[-1]

        # Display the first few rows for quick overview
        print("Extracted Data:")
        print(df.head())

        # Generate a static graph
        print("Generating Static Graph with Wrapped Labels...")
        generate_static_graph_with_wrapped_labels(df, file_name)

        # Generate an interactive graph
        print("Generating Interactive Graph with Wrapped Labels...")
        generate_interactive_graph_with_wrapped_labels(df, file_name)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except ET.ParseError:
        print("Error: Failed to parse the XML file. Ensure it is a valid XML document.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_xml_file>")
    else:
        file_path = sys.argv[1]
        main(file_path)
