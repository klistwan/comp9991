import networkx as nx
import pytest

from main import GameState, minimax

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
]


@pytest.mark.parametrize("edges, cop_position, robber_position, expected_damage", test_cases)
def test_minimax(edges, cop_position, robber_position, expected_damage):
    graph = nx.Graph()
    graph.add_edges_from(edges)
    for node in graph.nodes:
        graph.add_edge(node, node)
    is_cop_turn = True
    initial_state = GameState(
        cop_position=cop_position,
        robber_position=robber_position,
        damaged_vertices=frozenset(),
        is_cop_turn=is_cop_turn,
    )
    visited = set()

    result = minimax(graph, initial_state, visited)

    assert result == expected_damage, f"Expected damage number to be {expected_damage}, got {result}"
