import collections
import time
from game_logic import get_available_transitions, apply_transition, is_goal

class Node: 
    def __init__(self,state,parent=None,action=None):
        self.state = state
        self.parent = parent
        self.action = action

    def revers_path(goal_node):
        path = []
        current_node = goal_node

        while current_node.parent is not None:
            path.append(current_node.action)
            current_node = current_node.parent

        path.reverse()
        return path
    
class BFS:

    def solve(self,initial_state):
        start_time = time.time()

        queue = collections.deque()
        visited_state = {initial_state}

        start_node = Node(initial_state)
        queue.append(start_node)

        generated = 1
        discovered = 0

        while queue:
            current_node = queue.popleft()
            discovered +=1

            if is_goal(current_node.state):
                path = reversed(current_node)
                end_time = time.time()

            return{

            }
        
        
