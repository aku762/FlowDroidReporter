import matplotlib.pyplot as plt
import networkx as nx
from textwrap import wrap


def wrap_label(label, width=40):
    """
    Wrap a label into multiple lines to make it more readable.
    """
    return "\n".join(wrap(label, width))

def generate_static_graph(df, file_name, layout_type="circular", k=0.5, scale=2.0):
    """
    Generate a static graph visualization with better spacing and layout options.
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

    # Choose layout
    if layout_type == "spring":
        pos = nx.spring_layout(G, k=k, iterations=50, scale=scale)  # Spring layout with custom repulsion
    elif layout_type == "circular":
        pos = nx.circular_layout(G, scale=scale)  # Circular layout
    elif layout_type == "shell":
        pos = nx.shell_layout(G, scale=scale)  # Shell layout
    elif layout_type == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G, scale=scale)  # Kamada-Kawai layout
    else:
        raise ValueError(f"Unknown layout type: {layout_type}")

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
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        x_mid = (x1 + x2) / 2
        y_mid = (y1 + y2) / 2
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

    # Set the title with the file name
    plt.title("Enhanced Data Flow Graph")
    plt.show()


def generate_static_graph_old(df, file_name):
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
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        x_mid = (x1 + x2) / 2
        y_mid = (y1 + y2) / 2
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

    # Set the title with the file name
    plt.title("Enhanced Data Flow Graph")
    plt.show()
