import networkx as nx
import pytest

from main import GameState, minimax

# Test cases defined as tuples of graph edges, cop position, robber position, and expected damage number.
test_cases = [
    # Path graph with 3 vertices where cop and robber start on opposite ends.
    ([(0, 1), (1, 2)], 0, 2, 1),
    # Path graph with 3 vertices where cop and robber start adjacent to each other.
    ([(0, 1), (1, 2)], 0, 1, 0),
    # Path graph with 4 vertices where cop and robber start on opposite ends.
    ([(0, 1), (1, 2), (2, 3)], 0, 3, 1),
    # Path graph with 4 vertices where robber starts distance two from cop.
    ([(0, 1), (1, 2), (2, 3)], 0, 2, 2),
    # Path graph with 5 vertices where cop and robber start on opposite ends.
    ([(0, 1), (1, 2), (2, 3), (3, 4)], 0, 4, 2),
    # 3-cycle.
    ([(0, 1), (1, 2), (2, 0)], 0, 1, 0),
    # 4-cycle where cop and robber start adjacent to each other.
    ([(0, 1), (1, 2), (2, 3), (3, 0)], 0, 3, 0),
    # 4-cycle where cop and robber start opposite to each other.
    ([(0, 1), (1, 2), (2, 3), (3, 0)], 0, 2, 1),
    # 5-cycle where robber starts adjacent from cop.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)], 0, 1, 0),
    # 5-cycle where robber starts distance two from cop.
    ([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)], 0, 2, 2),
]


@pytest.mark.parametrize("edges, cop_position, robber_position, expected_damage", test_cases)
def test_minimax(edges, cop_position, robber_position, expected_damage):
    graph = nx.Graph()
    graph.add_edges_from(edges)
    initial_state = GameState(cop_position, robber_position, frozenset())
    is_cop_turn = True
    visited = set()

    result = minimax(graph, initial_state, is_cop_turn, visited)

    assert result == expected_damage, f"Expected damage number to be {expected_damage}, got {result}"
