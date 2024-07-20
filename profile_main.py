import cProfile
import io
import pstats

import networkx as nx

from main import CopsAndRobbersGame, GameState


def profile_minimax(game, state, visited):
    profiler = cProfile.Profile()
    profiler.enable()
    result = game.minimax(state, visited)
    profiler.disable()

    s = io.StringIO()
    sortby = "cumulative"
    ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
    return result


edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0), (0, 4), (1, 5), (2, 6), (3, 7)]
cop_position = 0
robber_position = 3
graph = nx.Graph()
graph.add_edges_from(edges)
for node in graph.nodes:
    graph.add_edge(node, node)

initial_state = GameState(
    cop_position=cop_position,
    robber_position=robber_position,
    damaged_vertices=frozenset(),
    is_cop_turn=True,
)
visited = set()
game = CopsAndRobbersGame(graph, cop_position)
profile_minimax(game, initial_state, visited=set())
