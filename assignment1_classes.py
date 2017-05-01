import search
from search import (breadth_first_tree_search,
                    breadth_first_search,
                    depth_first_graph_search,
                    iterative_deepening_search,
                    depth_limited_search,
                    recursive_best_first_search)
from utils import (name, print_table)


class BoardProblem(search.Problem):
    # MOVES
    MOVE_RIGHT = {'id': 0, 'value': 1}
    MOVE_LEFT = {'id': 1, 'value': -1}
    JUMP_RIGHT = {'id': 2, 'value': 1}
    JUMP_LEFT = {'id': 3, 'value': -1}

    # THE STATE IS A STRING OF CHARACTERS
    # Each character represents a piece, it can be W, B or a space.
    state = ""

    # ACTIONS
    # Each action is represented by a tuple of two components:
    # - The piece that makes the action
    # - The move that the piece is making
    #
    # For example, the tuple (1,0) with the following state: "WB BB"
    # means that the black piece of the left has to move to its right.

    # The result function executes the given action to the current state
    # and returns the result of that action.
    def result(self, state, action):
        if action[1] in (self.MOVE_RIGHT, self.MOVE_LEFT):
            return self.move(state, action[0], action[1])
        elif action[1] in (self.JUMP_RIGHT, self.JUMP_LEFT):
            return self.jump(state, action[0], action[1])
        else:
            raise AttributeError

    # The move function moves the given piece to the given direction
    def move(self, state, piece, direction):
        char_list = list(state)
        char = char_list[piece]
        char_list[piece] = ' '
        char_list[piece + direction['value']] = char
        return ''.join(char_list)

    # The jump function makes the piece to jump to the given direction
    # getting the target between the old site and the new one and it
    # swaps its color.
    def jump(self, state, piece, direction):
        char_list = list(state)
        char = char_list[piece]
        char_list[piece] = ' '
        for i in (1, 2):
            char_list[piece + i * direction['value']] = char
        return ''.join(char_list)

    # The actions function returns all possible moves that all pieces
    # can make in the given state.
    def actions(self, state):
        char_list = list(state)
        actions = []
        # As the only possible moves are near the spaces, these will become
        # the guides for the possible actions, checking the possible moves of
        # the nearer pieces (-2,-1,+1,+2).
        last_space_index = 0
        for _ in range(char_list.count(' ')):
            space_index = char_list.index(' ', last_space_index)
            for near_position in [-2, -1, 1, 2]:
                for move in self.moves(state, space_index, near_position):
                    actions.append(move)
            last_space_index = space_index
        return actions

    # The moves function returns all possible moves and jumps of a given piece
    # position relative to the space_index in the given state
    # It checks if the piece can move or jump to the space, if so, it returns
    # the move or jump as an action
    def moves(self, state, space_index, near_position):
        moves = []
        piece = space_index + near_position
        if piece in range(len(state)):
            if near_position == -2 and not self.is_last_black(state, piece, self.JUMP_RIGHT):
                # It's a jump from the left and it's not the same color
                moves.append((piece, self.JUMP_RIGHT))  # So we make the piece to jump to the right

            elif near_position == -1:  # It's a move from the left
                moves.append((piece, self.MOVE_RIGHT))  # So we make the piece to move to the right

            elif near_position == 1:  # It's a move from the right
                moves.append((piece, self.MOVE_LEFT))  # So we make the piece to move to the left

            elif near_position == 2 and not self.is_last_black(state, piece, self.JUMP_LEFT):
                # It's a jump from the right and it's not the same color
                moves.append((piece, self.JUMP_LEFT))  # So we make the piece to jump to the left
        return moves

    # The last_black function returns true if the piece that is jumped over is the last black piece in the board
    def is_last_black(self, state, piece, jump):
        return state.count("B") == 1 and state[piece + jump['value']] == "B"

    # todo value function
    # The value function sets a cost to make the decision making optimized
    def value(self, state):
        pass

    # The goal_test function tests if the given state is a solution or it
    # has to still searching for it.
    def goal_test(self, state):
        return state.count(self.goal['char']) == self.goal['cant']

    # The path_cost function gets the cost of the action made from state1
    # to state2.
    def path_cost(self, c, state1, action, state2):
        return 1


class InstrumentedBoardProblem(search.InstrumentedProblem):
    moves = ["moves right", "moves left", "jumps right", "jumps left"]
    def __init__(self, problem):
        super().__init__(problem)
        self.final_solution = None

    def __repr__(self):
        repr_final_solution = ""
        for node in self.final_solution:
            repr_final_solution += "Piece {} {}. ".format(node[0], self.moves[node[1]['id']])
        return '<{:4d}/{:4d}/{:4d}/{}/{}>'.format(self.succs, self.goal_tests,
                                               self.states, repr_final_solution, str(self.found))


def compare_searchers(problems, header,
                      searchers=[breadth_first_tree_search,
                                 breadth_first_search,
                                 depth_first_graph_search,
                                 iterative_deepening_search,
                                 depth_limited_search,
                                 recursive_best_first_search]):
    def do(searcher, problem):
        p = InstrumentedBoardProblem(problem)
        solution = searcher(p)
        p.final_solution = solution.solution()
        return p
    table = [[name(s)] + [do(s, p) for p in problems] for s in searchers]
    print_table(table, header)