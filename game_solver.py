import collections
import time
from game_logic import get_available_transitions, apply_transition, is_goal, state_id, would_cause_immediate_death

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

def reconstruct_path(goal_node):
    path = []
    current_node = goal_node
    
    while current_node.parent is not None:
        path.append(current_node.action)
        current_node = current_node.parent
        
    path.reverse()
    return path


class BFSSolver:
    def solve(self, initial_state):
        start_time = time.time()
        
        queue = collections.deque()
        visited = set()
        start_node = Node(initial_state)
        queue.append(start_node)
        visited.add(state_id(initial_state))
                
        generated_states_count = 1
        discovered_states_count = 0 
        
        while queue:
            current_node = queue.popleft()
            discovered_states_count += 1
            
            if is_goal(current_node.state):
                path = reconstruct_path(current_node)
                end_time = time.time()
                return {
                    "path": path,
                    "execution_time": end_time - start_time,
                    "generated_states_count": generated_states_count,
                    "discovered_states_count": discovered_states_count,
                    "path_length": len(path),
                    "solver_name": "BFS"
                }

            for action in get_available_transitions(current_node.state):                
                if would_cause_immediate_death(current_node.state, action):
                    continue

                new_state = apply_transition(current_node.state, action)
                sid = state_id(new_state)
                
                if sid not in visited:
                    new_node = Node(new_state, current_node, action)
                    visited.add(sid)
                    queue.append(new_node)
                    generated_states_count += 1
                     
        end_time = time.time()
        return {
            "path": None,
            "execution_time": end_time - start_time,
            "generated_states_count": generated_states_count,
            "discovered_states_count": discovered_states_count,
            "path_length": 0,
            "solver_name": "BFS"
        }

class DFSSolver:
    def solve(self, initial_state):
        start_time = time.time()
        
        stack = collections.deque()
        visited = set()
        start_node = Node(initial_state)
        stack.append((start_node, 0))
        visited.add(state_id(initial_state))
                
        generated_states_count = 1
        discovered_states_count = 0 

        while stack: 
            current_node, current_depth = stack.pop()
            discovered_states_count += 1
            
            if is_goal(current_node.state):
                path = reconstruct_path(current_node)
                end_time = time.time()
                return {
                    "path": path,
                    "execution_time": end_time - start_time,
                    "generated_states_count": generated_states_count,
                    "discovered_states_count": discovered_states_count,
                    "path_length": len(path),
                    "solver_name": "DFS"
                }

            for action in get_available_transitions(current_node.state):
                if would_cause_immediate_death(current_node.state, action):
                    continue

                new_state = apply_transition(current_node.state, action)
                sid = state_id(new_state)
                
                if sid not in visited:
                    new_node = Node(new_state, current_node, action)
                    visited.add(sid)
                    stack.append((new_node, current_depth + 1))
                    generated_states_count += 1
                    
        end_time = time.time()
        return {
            "path": None,
            "execution_time": end_time - start_time,
            "generated_states_count": generated_states_count,
            "discovered_states_count": discovered_states_count,
            "path_length": 0,
            "solver_name": "DFS"
        }
        
