from typing import NamedTuple

import networkx as nx


class GameState(NamedTuple):
    cop_position: int
    robber_position: int
    damaged_vertices: set[int]
    is_cop_turn: bool


class CopsAndRobbersGame:
    def __init__(self, graph: nx.Graph, cop_position: int) -> None:
        self.graph = graph
        self.upper_bound = graph.number_of_nodes() - (graph.degree(cop_position) - 1)
        self.has_cycle = len([cycle for cycle in nx.cycle_basis(graph) if len(cycle) > 1]) > 0

    def minimax(self, state: GameState, visited: set[GameState], alpha: int = 0, beta: int = float("inf")) -> int:
        if state.cop_position == state.robber_position:
            return len(state.damaged_vertices)
        if len(state.damaged_vertices) == self.upper_bound:
            return self.upper_bound
        if state in visited:
            return len(state.damaged_vertices)
        visited.add(state)

        if state.is_cop_turn:
            if self.graph.has_edge(state.cop_position, state.robber_position):
                return len(state.damaged_vertices)
            # If graph has no cycles, cop should move to a vertex closer to the robber.
            if not self.has_cycle:
                neighbors = self.graph.neighbors(state.cop_position)
                shortest_paths = {
                    neighbor: nx.shortest_path_length(self.graph, source=neighbor, target=state.robber_position)
                    for neighbor in neighbors
                }
                closest_neighbor = min(shortest_paths, key=shortest_paths.get)
                next_states = [
                    GameState(
                        closest_neighbor,
                        state.robber_position,
                        state.damaged_vertices,
                        is_cop_turn=False,
                    )
                ]
            else:
                # Otherwise, if graph has a cycle, cop should consider all neighbors.
                next_states = [
                    GameState(
                        pos,
                        state.robber_position,
                        state.damaged_vertices,
                        is_cop_turn=False,
                    )
                    for pos in self.graph.neighbors(state.cop_position)
                ]
            best_result = float("inf")
            if next_states == []:
                best_result = len(state.damaged_vertices)
            for next_state in next_states:
                result = self.minimax(next_state, visited, alpha, beta)
                best_result = min(best_result, result)
                beta = min(beta, result)
                if beta <= alpha:
                    break
        else:
            next_states = []
            for next_pos in self.graph.neighbors(state.robber_position):
                # Avoid vertices adjacent to the cop.
                if self.graph.has_edge(state.cop_position, next_pos):
                    continue
                next_states.append(
                    GameState(
                        state.cop_position,
                        next_pos,
                        state.damaged_vertices.union({state.robber_position}),
                        is_cop_turn=True,
                    )
                )
            best_result = 0
            if next_states == []:
                best_result = len(state.damaged_vertices.union({state.robber_position}))
            for next_state in next_states:
                result = self.minimax(next_state, visited, alpha, beta)
                best_result = max(best_result, result)
                alpha = max(alpha, result)
                if beta <= alpha:
                    break

        visited.remove(state)
        return best_result
