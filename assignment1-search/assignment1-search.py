import search


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
        if action['id'] in (self.MOVE_RIGHT['id'], self.MOVE_LEFT['id']):
            return self.move(state, state[action[0]], action[1])
        elif action['id'] in (self.JUMP_RIGHT['id'], self.JUMP_LEFT['id']):
            return self.jump(state, state[action[0]], action[1])
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
                if space_index + near_position in range(len(state)):
                    for move in self.moves(state, space_index, near_position):
                        actions.append((space_index + near_position, move))
            last_space_index = space_index
        return actions

    # todo the moves function
    # The moves function returns all possible moves and jumps of a given piece
    # position relative to the space_index in the given state
    # It checks if the piece can move or jump to the space, if so, it returns
    # the move or jump as an action
    def moves(self, state, space_index, piece):
        moves = []
        return moves

    # todo value function
    # The value function sets a cost to make the decision making optimized
    def value(self, state):
        pass

    # The goal_test function tests if the given state is a solution or it
    # has to still searching for it.
    def goal_test(self, state):
        return state.count(self.goal['char']) == self.goal['cant']

    # todo path_cost function
    # The path_cost function gets the cost of the action made from state1
    # to state2.
    def path_cost(self, c, state1, action, state2):
        return 1
