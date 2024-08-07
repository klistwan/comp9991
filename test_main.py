import networkx as nx
import pytest

from main import CopsAndRobbersGame, GameState, find_optimal_starting_vertices, find_damage_number

# Test cases defined as tuples of graph edges, cop position, robber position, and expected damage number.
test_cases = [
    # Path graph with 3 vertices where cop and robber start on opposite ends.
    ([(0, 1), (1, 2)], 0, 2, 1),
    # Path graph with 3 vertices where cop and robber start adjacent to each other.
    ([(0, 1), (1, 2)], 0, 1, 0),
    # Path graph with 4 vertices where robber starts distance zero from cop.
    ([(0, 1), (1, 2), (2, 3)], 2, 2, 0),
    # Path graph with 4 vertices where robber starts distance one from cop.
    ([(0, 1), (1, 2), (2, 3)], 1, 2, 0),
    # Path graph with 4 vertices where robber starts distance two from cop.
    ([(0, 1), (1, 2), (2, 3)], 0, 2, 2),
    # Path graph with 4 vertices where robber starts distance three from cop.
    ([(0, 1), (1, 2), (2, 3)], 0, 3, 1),
    # Path graph with 5 vertices where cop and robber start on opposite ends.
    ([(0, 1), (1, 2), (2, 3), (3, 4)], 0, 4, 2),
    # Path graph with 5 vertices where robber starts distance two from cop.
    ([(0, 1), (1, 2), (2, 3), (3, 4)], 0, 2, 3),
    # Path graph with 5 vertices where robber starts distance two from cop.
    ([(0, 1), (1, 2), (2, 3), (3, 4)], 2, 4, 1),
    # Path graph with 6 vertices.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)], 2, 4, 2),
    # Path graph with 6 vertices where cop starts on a leaf and robber can damage vertices 2, 3, 4, and 5.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)], 0, 2, 4),
    # 3-cycle.
    ([(0, 1), (1, 2), (2, 0)], 0, 1, 0),
    # 4-cycle where cop and robber start adjacent.
    ([(0, 1), (1, 2), (2, 3), (3, 0)], 0, 1, 0),
    # 4-cycle where cop and robber start opposite.
    ([(0, 1), (1, 2), (2, 3), (3, 0)], 1, 3, 1),
    # 5-cycle where cop and robber start adjacent.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)], 0, 1, 0),
    # 5-cycle where cop and robber start distance 2 away.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)], 0, 2, 2),
    # 6-cycle where cop and robber start adjacent.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)], 0, 1, 0),
    # 6-cycle where cop and robber start distance 2 away.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)], 0, 2, 2),
    # 6-cycle where cop and robber start distance 3 away.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)], 0, 3, 2),
    # 7-cycle where cop and robber start distance 2 away.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)], 0, 2, 3),
    # 7-cycle where cop and robber start distance 3 away.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)], 0, 3, 3),
    # Star graph S_5 where the cop starts on the central vertex.
    ([(0, 1), (0, 2), (0, 3), (0, 4)], 0, 1, 0),
    # Star graph S_5 where neither player starts on the central vertex.
    ([(0, 1), (0, 2), (0, 3), (0, 4)], 1, 2, 1),
    # Complete graph K_4.
    ([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)], 0, 1, 0),
    # Balanced binary tree with 7 nodes (cop at root, robber at leaf).
    ([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)], 0, 3, 1),
    # Balanced binary tree with 7 nodes (cop and robber at leaf vertices within the same branch).
    ([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)], 3, 4, 1),
    # Balanced binary tree with 7 nodes (cop at leaf, robber at root).
    ([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)], 3, 0, 3),
    # Complete bipartite graph K_{3,3} where cop and robber start on different partitions.
    ([(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)], 0, 5, 0),
    # Complete bipartite graph K_{3,3} where cop and robber start on the same partition.
    ([(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)], 0, 1, 1),
    # Wheel graph W_6 where cop starts at 0 (central vertex) and robber starts at 3
    ([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (2, 3), (3, 4), (4, 5), (5, 1)], 0, 3, 0),
    # A 3-barbell graph where cop and robber start distance 2 away from each other.
    ([(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (2, 3)], 2, 5, 1),
    # A 3-barbell graph where cop and robber start distance 3 away from each other.
    ([(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (2, 3)], 0, 5, 2),
    # A (4,3)-lollipop graph where the cop starts on the cut vertex of the clique.
    ([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6)], 3, 5, 2),
    # 3x3 Grid graph where cop starts in the centre and robber starts on a corner.
    ([(0, 1), (1, 2), (0, 3), (1, 4), (2, 5), (3, 4), (4, 5), (3, 6), (4, 7), (5, 8), (6, 7), (7, 8)], 4, 8, 1),
    # Möbius ladder M4.
    ([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)], 0, 2, 0),
    # Möbius ladder M6 where robber starts distance 2 away from the cop.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3), (1, 4), (2, 5)], 0, 4, 1),
    # Möbius ladder M8 where cop starts at vertex 0 and robber starts at vertex 3.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0), (0, 4), (1, 5), (2, 6), (3, 7)], 0, 3, 4),
    # Cubical graph where cop and robber start on opposite ends.
    ([(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)], 0, 2, 2),
    # 8-cycle where cop and robber start distance 2 away.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)], 0, 2, 3),
    # Graph where the cop starting on the centre allows the robber to damage more vertices than the damage number.
    (
        [
            (2, 1),
            (1, 10),
            (10, 6),
            (6, 8),
            (8, 7),
            (7, 3),
            (3, 10),
            (10, 9),
            (9, 4),
            (4, 3),
            (4, 7),
            (4, 5),
            (5, 8),
            (5, 6),
            (5, 9),
        ],
        10,
        5,
        3,
    ),
]


@pytest.mark.parametrize("edges, cop_position, robber_position, expected_damage", test_cases)
def test_minimax(edges, cop_position, robber_position, expected_damage):
    graph = nx.Graph()
    graph.add_edges_from(edges)
    for node in graph.nodes:
        graph.add_edge(node, node)

    initial_state = GameState(
        cop_position=cop_position,
        robber_position=robber_position,
    )
    visited = set()
    game = CopsAndRobbersGame(graph, cop_position)
    result = game.minimax(initial_state, visited)
    assert result == expected_damage, f"Expected dmg(G) = {expected_damage} but got {result}"


def test_find_optimal_starting_vertices_for_path():
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
    for node in graph.nodes:
        graph.add_edge(node, node)

    result = find_optimal_starting_vertices(graph)

    assert result == [2, 3]


def test_find_optimal_starting_vertices_for_cycle():
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])
    for node in graph.nodes:
        graph.add_edge(node, node)

    result = find_optimal_starting_vertices(graph)

    assert result == [0, 1, 2, 3, 4]


def test_find_damage_number_for_path():
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)])
    for node in graph.nodes:
        graph.add_edge(node, node)

    result = find_damage_number(graph)

    assert result == 2


def test_find_damage_number_for_cycle():
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
    for node in graph.nodes:
        graph.add_edge(node, node)

    result = find_damage_number(graph)

    assert result == 1
