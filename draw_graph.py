import argparse
import ast

import matplotlib.pyplot as plt
import networkx as nx


def parse_edges(edge_list_str):
    return ast.literal_eval(edge_list_str)


def draw_graph(edges) -> None:
    G = nx.Graph()
    G.add_edges_from(edges)

    # Draw the graph
    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=500, edge_color="gray", font_weight="bold")
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw a graph from a list of edges.")
    parser.add_argument("edges", type=parse_edges, help="Edges in the format '[(0, 1), (1, 2), (2, 3)]'")
    args = parser.parse_args()

    draw_graph(args.edges)


if __name__ == "__main__":
    main()
