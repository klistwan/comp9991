from typing import NamedTuple

import networkx as nx


class GameState(NamedTuple):
    cop_position: int
    robber_position: int
    damaged_vertices: set[int]


def minimax(graph: nx.Graph, state: GameState, is_cop_turn: bool, visited: set[GameState]) -> int:
    """Calculate damage number given a graph and initial game state."""
    if state.cop_position == state.robber_position:
        return len(state.damaged_vertices)
    if len(state.damaged_vertices) == graph.order():
        return len(state.damaged_vertices)
    if state in visited:
        return len(state.damaged_vertices)
    visited.add(state)

    if is_cop_turn:
        next_positions = list(graph.neighbors(state.cop_position)) + [state.cop_position]
        next_states = [GameState(pos, state.robber_position, state.damaged_vertices) for pos in next_positions]
        results = [minimax(graph, state, False, visited) for state in next_states if state not in visited]
        if results == []:
            return len(state.damaged_vertices)
        best_result = min(results)
    else:
        next_positions = list(graph.neighbors(state.robber_position)) + [state.robber_position]
        next_states = [
            GameState(state.cop_position, pos, state.damaged_vertices.union({state.robber_position}))
            for pos in next_positions
        ]
        results = [minimax(graph, state, True, visited) for state in next_states]
        best_result = max(results)

    return best_result


def game_decision(graph: nx.Graph, initial_cop_position: int, initial_robber_position: int, k: int) -> bool:
    initial_state = GameState(initial_cop_position, initial_robber_position, frozenset())
    damage_number = minimax(graph, initial_state, True, set())
    return damage_number >= k
