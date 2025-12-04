import pygame
import sys
import game_logic
from game_state import GameState
from game_renderer import gameRenderer
from game_solver import BFSSolver, DFSSolver, UCSSolver, AStarSolver

class PygameApp:
    def __init__(self, level_file, tile_size=40):
        self.level_file = level_file
        self.tile_size = tile_size
        
        initial_state = game_logic.parse_level_file(level_file)
        board_rows = len(initial_state.board)
        board_cols = len(initial_state.board[0])
        
        self.renderer = gameRenderer(
            width=board_cols * tile_size,
            height=board_rows * tile_size + 60,
            tile_size=tile_size
        )
        
        self.current_state = initial_state
        self.move_count = 0
        self.history = []
        self.move_history = []

        self.solver_path = None
        self.solver_index = 0

        self.current_solver_moves = []

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

        self.last_move_time = 0
        self.path_coords = set()

    def calculate_path_coordinates(self):
        self.path_coords.clear()
                
        simulated_state = self.current_state 
        self.path_coords.add(simulated_state.player_pos)
        
        if self.solver_path:
            for action in self.solver_path:                
                simulated_state = game_logic.apply_transition(simulated_state, action)
                self.path_coords.add(simulated_state.player_pos)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart_game()
                return

            if event.type == pygame.KEYDOWN:
                action = None                
                if event.key == pygame.K_b:
                    print("Running BFS Solver : ")                                        
                    solver = BFSSolver()
                    results = solver.solve(self.current_state)
                    self.process_solver_results(results)

                elif event.key == pygame.K_d:
                    print("Running DFS Solver : ")
                    solver = DFSSolver()
                    results = solver.solve(self.current_state)
                    self.process_solver_results(results)
                        
                elif event.key == pygame.K_u:
                    print("Running UCS Solver : ")
                    solver = UCSSolver()
                    results = solver.solve(self.current_state)
                    self.process_solver_results(results)

                elif event.key == pygame.K_a:
                    print("Running A* Solver : ")
                    solver = AStarSolver()
                    results = solver.solve(self.current_state)
                    self.process_solver_results(results)

                elif event.key == pygame.K_m: self.undo_move()
                elif event.key == pygame.K_r: self.restart_game()
                elif event.key == pygame.K_q: self.running = False
                                
                elif self.solver_path is None:
                    if event.key == pygame.K_UP: action = 'w' 
                    elif event.key == pygame.K_DOWN: action = 's'
                    elif event.key == pygame.K_LEFT: action = 'a'
                    elif event.key == pygame.K_RIGHT: action = 'd'

                if action and action in game_logic.get_available_transitions(self.current_state):
                    self.save_state()
                    self.current_state = game_logic.apply_transition(self.current_state, action)
                    self.move_count += 1

                    if game_logic.is_terminal(self.current_state):
                        self.game_over = True

    def save_state(self):
        self.history.append(self.current_state)
        self.move_history.append(self.move_count)

    def undo_move(self):
        if self.history:
            self.current_state = self.history.pop()
            self.move_count = self.move_history.pop()

    def restart_game(self):
        self.current_state = game_logic.parse_level_file(self.level_file)
        self.move_count = 0
        self.history.clear()
        self.move_history.clear()
        self.game_over = False

    def process_solver_results(self, results):

        self.solver_path = results.get("path")
        self.solver_index = 0
        
        if self.solver_path:
            self.current_solver_moves.clear()

        solver_name = results.get("solver_name", "Solver")
        
        print("\n" + "="*70)
        print(f"Performance analysis results for{solver_name} ")
        print("="*70)
               
        print(f"Implementation period : {results.get('execution_time', 0.0):.4f} seconds")
        print(f"Number of births : {results.get('generated_states_count', 0)}")
        print(f"Number of cases detected (Processed) : {results.get('discovered_states_count', 0)}")
        
        if self.solver_path is not None:
            path_length = results.get('path_length', 0)
            print(f"Length of the detected path : {path_length} steps")
            print(f"path : {'-'.join(self.solver_path)}")
            
            self.calculate_path_coordinates() 
        else:
            print("No solution has been found at this stage.")
            self.path_coords.clear()
        
        print("="*70 + "\n")
        
    def run(self):
        MOVE_DELAY = 300

        while self.running:
            self.handle_events()

            if self.solver_path and not self.game_over:
                current_time = pygame.time.get_ticks()
            
                if current_time - self.last_move_time > MOVE_DELAY:
                
                    if self.solver_index < len(self.solver_path):
                        action = self.solver_path[self.solver_index]
                    
                        if action in game_logic.get_available_transitions(self.current_state):
                            self.save_state()
                            self.current_state = game_logic.apply_transition(self.current_state, action)
                            self.move_count += 1

                            self.current_solver_moves.append(action)
                        
                            if game_logic.is_terminal(self.current_state):
                                self.game_over = True
                    
                        self.solver_index += 1
                        self.last_move_time = current_time
                    else:
                        self.solver_path = None

            available_moves = game_logic.get_available_transitions(self.current_state)

            if self.game_over:
                won = game_logic.is_goal(self.current_state)
                self.renderer.show_end_screen(self.current_state, self.move_count, won)
            else:

                self.renderer.render(self.current_state, self.move_count, available_moves, self.path_coords, self.current_solver_moves)
            
            self.clock.tick(30)

        pygame.quit()
        sys.exit()
 
if __name__ == "__main__":
    app = PygameApp('level12.txt')
    app.run()