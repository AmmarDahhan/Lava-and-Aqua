import collections
import time
import heapq
from game_logic import get_available_transitions, apply_transition, is_goal, state_id, would_cause_immediate_death, count_lava, is_terminal

def calculate_heuristic(state):
    goal_pos = None
    coins_count = 0
    
    for r in range(len(state.board)):
        for c in range(len(state.board[0])):
            cell = state.board[r][c]
            if cell == 'T':
                goal_pos = (r, c)
            elif cell == 'C':
                coins_count += 1
                
    if goal_pos is None: return float('inf') 
    
    pr, pc = state.player_pos
    gr, gc = goal_pos
    dist = abs(pr - gr) + abs(pc - gc)
    
    return dist + (coins_count * 10)

class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
            return self.cost < other.cost

def reconstruct_path(goal_node):
    path = []
    current_node = goal_node
    
    while current_node.parent is not None:
        path.append(current_node.action)
        current_node = current_node.parent
        
    path.reverse()
    return path

class UCSSolver:
    def solve(self, initial_state):
        start_time = time.time()
        pq = []
        start_node = Node(initial_state, cost=0)
        heapq.heappush(pq, start_node)
        
        visited = set()
                
        generated_states_count = 1
        discovered_states_count = 0 
        
        while pq:
            current_node = heapq.heappop(pq)
            
            sid = state_id(current_node.state)
            if sid in visited:
                continue
            
            visited.add(sid)
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
                    "solver_name": "UCS"
                }

            for action in get_available_transitions(current_node.state):                
                if would_cause_immediate_death(current_node.state, action):
                    continue

                new_state = apply_transition(current_node.state, action)
                
                if is_terminal(new_state) and not is_goal(new_state):
                    continue

                move_cost = 1 + count_lava(new_state)
                new_total_cost = current_node.cost + move_cost
                
                new_node = Node(new_state, current_node, action, new_total_cost)
                heapq.heappush(pq, new_node)
                generated_states_count += 1
                      
        end_time = time.time()
        return {
            "path": None,
            "execution_time": end_time - start_time,
            "generated_states_count": generated_states_count,
            "discovered_states_count": discovered_states_count,
            "path_length": 0,
            "solver_name": "UCS"
        }
    
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

                if is_terminal(new_state) and not is_goal(new_state):
                    continue

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

                if is_terminal(new_state) and not is_goal(new_state):
                    continue

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
    

        
class AStarSolver:
    def solve(self, initial_state):
        start_time = time.time()
        
        # Priority Queue: (Priority, Count, Node)
        # Count is used as a tie-breaker so Python doesn't try to compare Node objects directly
        queue = []
        count = 0 
        
        start_node = Node(initial_state)
        
        # التكلفة الأولية g=0
        g_score = {state_id(initial_state): 0}
        
        # التكلفة الكلية f = g + h
        f_score = calculate_heuristic(initial_state)
        
        heapq.heappush(queue, (f_score, count, start_node))
        
        visited = set()
        generated_states_count = 1
        discovered_states_count = 0

        while queue:
            # نسحب العنصر صاحب أقل تكلفة f
            current_f, _, current_node = heapq.heappop(queue)
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
                    "solver_name": "A*"
                }

            current_sid = state_id(current_node.state)
            
            # إذا كنا قد وصلنا لهذه الحالة سابقاً بتكلفة أقل، نتجاهلها
            if current_sid in visited and g_score.get(current_sid, float('inf')) < (current_f - calculate_heuristic(current_node.state)):
                continue
            
            visited.add(current_sid)
            
            # تكلفة الخطوات الحالية (g) هي طول المسار حتى الآن
            current_g = g_score[current_sid]

            for action in get_available_transitions(current_node.state):
                # نستخدم الدالة المعدلة (الآمنة) التي اتفقنا عليها سابقاً
                if would_cause_immediate_death(current_node.state, action):
                    continue

                new_state = apply_transition(current_node.state, action)
                
                # فحص الموت بعد الحركة (كما ناقشنا سابقاً)
                r, c = new_state.player_pos
                if new_state.board[r][c] == 'L': continue

                new_sid = state_id(new_state)
                new_g = current_g + 1 # تكلفة الحركة دائماً 1
                
                # إذا وجدنا مساراً أفضل لهذه الحالة أو أنها حالة جديدة
                if new_g < g_score.get(new_sid, float('inf')):
                    g_score[new_sid] = new_g
                    f_new = new_g + calculate_heuristic(new_state)
                    
                    new_node = Node(new_state, current_node, action)
                    count += 1
                    heapq.heappush(queue, (f_new, count, new_node))
                    generated_states_count += 1

        return { "path": None, "solver_name": "A*", "execution_time": time.time() - start_time }
    
class GreedySolver:
    def solve(self, initial_state):
        start_time = time.time()
        
        queue = []
        count = 0
        
        start_node = Node(initial_state)
        # الأولوية هنا هي فقط المسافة المتبقية للهدف
        priority = calculate_heuristic(initial_state)
        
        heapq.heappush(queue, (priority, count, start_node))
        
        visited = set()
        visited.add(state_id(initial_state))
        
        generated_states_count = 1
        discovered_states_count = 0

        while queue:
            _, _, current_node = heapq.heappop(queue)
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
                    "solver_name": "Greedy"
                }

            for action in get_available_transitions(current_node.state):
                if would_cause_immediate_death(current_node.state, action):
                    continue

                new_state = apply_transition(current_node.state, action)
                r, c = new_state.player_pos
                if new_state.board[r][c] == 'L': continue

                sid = state_id(new_state)
                
                if sid not in visited:
                    visited.add(sid)
                    new_node = Node(new_state, current_node, action)
                    
                    # الأولوية هي الـ Heuristic فقط
                    h_score = calculate_heuristic(new_state)
                    
                    count += 1
                    heapq.heappush(queue, (h_score, count, new_node))
                    generated_states_count += 1

        return { "path": None, "solver_name": "Greedy", "execution_time": time.time() - start_time }