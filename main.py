from typing import NamedTuple
import argparse
import networkx as nx


class GameState(NamedTuple):
    cop_position: int
    robber_position: int
    damaged_vertices: set[int] = frozenset()
    is_cop_turn: bool = True


def find_optimal_starting_vertices(graph: nx.Graph) -> list[int]:
    least_damage = float("inf")
    optimal_vertices = []
    for cop_position in graph.nodes:
        results = []
        for robber_position in graph.nodes:
            game = CopsAndRobbersGame(graph, cop_position)
            initial_state = GameState(cop_position, robber_position)
            result = game.minimax(initial_state, set())
            results.append(result)
        if max(results) == least_damage:
            optimal_vertices.append(cop_position)
        elif max(results) < least_damage:
            least_damage = max(results)
            optimal_vertices = [cop_position]
    return optimal_vertices


def find_damage_number(graph: nx.Graph, cop_position=None, robber_position=None) -> int:
    damage_number = graph.number_of_nodes() - 1
    cop_positions = [cop_position] if cop_position is not None else graph.nodes
    robber_positions = [robber_position] if robber_position is not None else graph.nodes

    for cop_position in cop_positions:
        results = []
        for robber_position in robber_positions:
            game = CopsAndRobbersGame(graph, cop_position)
            initial_state = GameState(cop_position, robber_position)
            result = game.minimax(initial_state, set())
            results.append(result)
        damage_number = min(damage_number, max(results))
    return damage_number


class CopsAndRobbersGame:
    def __init__(self, graph: nx.Graph, cop_position: int) -> None:
        self.graph = graph
        self.upper_bound = graph.number_of_nodes() - (graph.degree(cop_position) - 1)
        self.has_cycle = len([cycle for cycle in nx.cycle_basis(graph) if len(cycle) > 1]) > 0

    def is_game_over(self, state: GameState, visited: set[GameState]) -> bool:
        if state.cop_position == state.robber_position:
            return True
        if len(state.damaged_vertices) == self.upper_bound:
            return True
        return state in visited

    def minimax(self, state: GameState, visited: set[GameState], alpha: int = 0, beta: int = float("inf")) -> int:
        if self.is_game_over(state, visited):
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
            for next_state in next_states:
                result = self.minimax(next_state, visited, alpha, beta)
                best_result = min(best_result, result)
                beta = min(beta, result)
                if beta <= alpha:
                    break
        else:
            new_damaged_vertices = state.damaged_vertices.union({state.robber_position})
            next_states = [
                GameState(
                    state.cop_position,
                    next_pos,
                    new_damaged_vertices,
                    is_cop_turn=True,
                )
                for next_pos in self.graph.neighbors(state.robber_position)
                if not self.graph.has_edge(state.cop_position, next_pos)
            ]
            best_result = len(new_damaged_vertices)
            for next_state in next_states:
                result = self.minimax(next_state, visited, alpha, beta)
                best_result = max(best_result, result)
                alpha = max(alpha, result)
                if beta <= alpha:
                    break

        visited.remove(state)
        return best_result


def main():
    parser = argparse.ArgumentParser(
        description="Simulate the Damage Number variant of the Cops and Robbers game on a graph."
    )
    parser.add_argument("--edges", type=str, required=True, help="List of edges")
    parser.add_argument("--cop", type=int, required=True, help="Position of the cop")
    parser.add_argument("--robber", type=int, required=True, help="Position of the robber")

    args = parser.parse_args()

    edges = eval(args.edges)
    cop_position = args.cop
    robber_position = args.robber

    graph = nx.Graph()
    graph.add_edges_from(edges)
    for node in graph.nodes:
        graph.add_edge(node, node)

    initial_state = GameState(cop_position=cop_position, robber_position=robber_position)
    visited = set()
    game = CopsAndRobbersGame(graph, cop_position)
    result = game.minimax(initial_state, visited)
    print(f"The robber is able to damage {result} vertices")


if __name__ == "__main__":
    main()
