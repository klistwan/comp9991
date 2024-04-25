import networkx as nx
from typing import Set, List, Dict, NamedTuple


class GameState(NamedTuple):
    cop_position: int
    robber_position: int
    damaged_vertices: Set[int]


def get_adjacent_vertices(graph: nx.Graph, vertex: int) -> List[int]:
    return list(graph.neighbors(vertex))


def minimax(graph: nx.Graph, state: GameState, is_cop_turn: bool, memo: Dict[GameState, int]) -> int:
    """Calculates damage number given a graph and initial game state."""
    if state.cop_position == state.robber_position or len(state.damaged_vertices) == graph.order():
        return len(state.damaged_vertices)

    memo_key = GameState(state.cop_position, state.robber_position, frozenset(state.damaged_vertices))
    if memo_key in memo:
        return memo[memo_key]

    if is_cop_turn:
        next_positions = list(graph.neighbors(state.cop_position)) + [state.cop_position]
        if state.robber_position in next_positions:
            return len(state.damaged_vertices)
        next_states = [GameState(pos, state.robber_position, state.damaged_vertices) for pos in next_positions]
        results = [minimax(graph, state, False, memo) for state in next_states]
        best_result = min(results)
    else:
        next_positions = list(graph.neighbours(state.robber_position)) + [state.robber_position]
        next_states = [
            GameState(state.cop_position, pos, state.damaged_vertices.union({state.robber_position}))
            for pos in next_positions
        ]
        results = [minimax(graph, state, True, memo) for state in next_states]
        best_result = max(results)

    memo[memo_key] = best_result
    return best_result


def game_decision(graph: nx.Graph, initial_cop_position: int, initial_robber_position: int, k: int) -> bool:
    initial_state = GameState(initial_cop_position, initial_robber_position, frozenset())
    memo: Dict[GameState, int] = {}
    damage_number = minimax(graph, initial_state, True, memo)
    return damage_number >= k
