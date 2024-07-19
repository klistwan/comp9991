from typing import NamedTuple

import networkx as nx


class GameState(NamedTuple):
    cop_position: int
    robber_position: int
    damaged_vertices: set[int]
    is_cop_turn: bool


def minimax(graph: nx.Graph, state: GameState, visited: set[GameState]) -> int:
    """Calculate damage number given a graph and initial game state."""
    if state.cop_position == state.robber_position:
        return len(state.damaged_vertices)
    if len(state.damaged_vertices) == graph.order():
        return len(state.damaged_vertices)
    if state in visited:
        return len(state.damaged_vertices)
    visited.add(state)

    if state.is_cop_turn:
        if graph.has_edge(state.cop_position, state.robber_position):
            return len(state.damaged_vertices)
        next_states = [
            GameState(
                pos,
                state.robber_position,
                state.damaged_vertices,
                False,
            )
            for pos in graph.neighbors(state.cop_position)
        ]
        results = [minimax(graph, state, visited) for state in next_states if state not in visited]
        if results == []:
            return len(state.damaged_vertices)
        best_result = min(results)
    else:
        next_states = []
        for next_pos in graph.neighbors(state.robber_position):
            # Avoid vertices adjacent to the cop.
            if graph.has_edge(state.cop_position, next_pos):
                continue
            next_states.append(
                GameState(state.cop_position, next_pos, state.damaged_vertices.union({state.robber_position}), True)
            )
        # If impossible to avoid capture, just damage current vertex.
        if next_states == []:
            best_result = len(state.damaged_vertices.union({state.robber_position}))
        else:
            results = [minimax(graph, state, visited) for state in next_states]
            best_result = max(results)

    visited.remove(state)
    return best_result
