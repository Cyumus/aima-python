from assignment1_classes import (BoardProblem, compare_searchers)
from search import (
    breadth_first_search,
    compare_graph_searchers,
    depth_first_graph_search,
    iterative_deepening_search,
    astar_search
)

initial = "BBWW "
goal = {'char': "B", 'cant': 4}
problem = [BoardProblem(initial=initial, goal=goal)]

compare_searchers(problems=problem,
                  header=["Searcher", "Actions succeeded / States tested / Actions taken / Moves / Final state"],
                  searchers=[breadth_first_search,
                             depth_first_graph_search,
                             iterative_deepening_search,
                             # astar_search todo A* search
                             # todo IDA* search
                    ])
