import networkx as nx
from typing import Set, List, Dict, NamedTuple


class GameState(NamedTuple):
    cop_pos: int
    robber_pos: int
    damaged: Set[int]


def get_adjacent_vertices(graph: nx.Graph, vertex: int) -> List[int]:
    return list(graph.neighbors(vertex))


def minimax(graph: nx.Graph, state: GameState, is_cop_turn: bool, memo: Dict[GameState, int]) -> int:
    current_cop_pos, current_robber_pos, damaged_set = state.cop_pos, state.robber_pos, state.damaged

    if current_cop_pos == current_robber_pos or len(damaged_set) == len(graph.nodes):
        return len(damaged_set)

    memo_key = GameState(current_cop_pos, current_robber_pos, frozenset(damaged_set))
    if memo_key in memo:
        return memo[memo_key]

    if is_cop_turn:
        next_positions = get_adjacent_vertices(graph, current_cop_pos) + [current_cop_pos]
        results = [
            minimax(graph, GameState(pos, current_robber_pos, damaged_set), False, memo) for pos in next_positions
        ]
        best_result = min(results)
    else:
        next_positions = get_adjacent_vertices(graph, current_robber_pos)
        next_states = [GameState(current_cop_pos, pos, damaged_set.union({pos})) for pos in next_positions]
        results = [minimax(graph, state, True, memo) for state in next_states]
        best_result = max(results)

    memo[memo_key] = best_result
    return best_result


def game_decision(graph: nx.Graph, initial_cop_position: int, initial_robber_position: int, k: int) -> bool:
    initial_state = GameState(initial_cop_position, initial_robber_position, frozenset())
    memo: Dict[GameState, int] = {}
    damage_number = minimax(graph, initial_state, True, memo)
    return damage_number >= k


# Create a simple graph
G = nx.Graph()
edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
G.add_edges_from(edges)

# Decision query
k = 3  # We want to check if the robber can damage at least 3 vertices
initial_cop_position = 0
initial_robber_position = 4
result = game_decision(G, initial_cop_position, initial_robber_position, k)
print("Can the robber damage at least", k, "vertices?", result)
