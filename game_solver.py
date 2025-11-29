import collections
import time
from game_logic import get_available_transitions, apply_transition, is_goal

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
        visited_states = {initial_state} 

        start_node = Node(initial_state)
        queue.append(start_node)
                
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
                new_state = apply_transition(current_node.state, action)
                
                if new_state not in visited_states:
                    new_node = Node(new_state, current_node, action)
                    visited_states.add(new_state)
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
    def solve(self, initial_state, max_nodes=200000, max_depth=1000):
        start_time = time.time()
        
        stack = collections.deque() 
        visited_states = {initial_state} 

        start_node = Node(initial_state)
        stack.append((start_node, 0))
                
        generated_states_count = 1
        discovered_states_count = 0 

        while stack:
            if generated_states_count >= max_nodes:
                break
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
            if current_depth >= max_depth:
                continue 

            for action in get_available_transitions(current_node.state):
                new_state = apply_transition(current_node.state, action)
                
                if new_state not in visited_states:
                    new_node = Node(new_state, current_node, action)
                    
                    visited_states.add(new_state)
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
        
# class DFSSolver:
#     def solve(self, initial_state, max_nodes=200000, max_depth=1000):
#         start_time = time.time()

#         start_node = Node(initial_state)
#         generated_states_count = 1 
#         discovered_states_count = 0
#         nodes_visited = 0 

#         found_goal_node = None
#         stop_flag = False

#         def dfs(node, visited, depth):
#             nonlocal found_goal_node, generated_states_count, nodes_visited, stop_flag

#             if stop_flag:
#                 return False

#             nodes_visited += 1
#             if nodes_visited > max_nodes:
#                 stop_flag = True
#                 return False
 
#             if is_goal(node.state):
#                 found_goal_node = node
#                 return True

#             if depth >= max_depth:
#                 return False

#             for action in get_available_transitions(node.state):
#                 new_state = apply_transition(node.state, action)

#                 if new_state in visited:
#                     continue
                
#                 visited.add(new_state)
#                 generated_states_count += 1

#                 child = Node(new_state, node, action)
#                 got = dfs(child, visited, depth + 1)
#                 if got:
#                     return True
                
#                 visited.remove(new_state)

#                 if stop_flag:
#                     return False

#             return False

#         visited = {initial_state}
#         dfs(start_node, visited, 0)

#         end_time = time.time()
        
#         if found_goal_node:
#             path = reconstruct_path(found_goal_node)
#             solved = True
#             path_length = len(path)
#         else:
#             path = None
#             solved = False
#             path_length = 0

#         return {
#             "path": path,
#             "execution_time": end_time - start_time,
#             "generated_states_count": generated_states_count,
#             "discovered_states_count": nodes_visited,
#             "path_length": path_length,
#             "solver_name": "DFS",
#             "solved": solved,
#             "stopped_early": stop_flag
#         }

    