import copy
from typing import List, Tuple, Optional
from game_state import GameState

# --- Constants for cell types ---
PLAYER = '@'
WALL = '#'
GOAL = 'T'
LAVA = 'L'
WATER = 'W'
ICE = 'I'
EMPTY = ' '
BLOCK = 'B'
MESH = 'M'
MESH_LAVA = 'ML'
MESH_WATER = 'MW'

def parse_level_file(level_file: str) -> GameState:
    #Reads a level file and returns the initial GameState
    board = []
    player_pos = None
    with open(level_file, 'r') as f:
        for r_idx, line in enumerate(f):
            row = tuple(line.strip().split(','))
            board.append(row)
            if PLAYER in row and player_pos is None:
                c_idx = row.index(PLAYER)
                player_pos = (r_idx, c_idx)
    
    if player_pos is None:
        raise ValueError("Player position '@' not found in level file.")
        
    return GameState(board=tuple(board), player_pos=player_pos)

def get_available_transitions(state: GameState) -> List[str]:
    #Returns a list of valid moves from the current state.
    moves = []
    r, c = state.player_pos
    directions = {
        'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)
    }
    
    for move, (dr, dc) in directions.items():
        new_r, new_c = r + dr, c + dc
        
        if not (0 <= new_r < len(state.board) and 0 <= new_c < len(state.board[0])):
            continue
            
        target_cell = state.board[new_r][new_c]
        
        if target_cell in [WALL, BLOCK, MESH] or target_cell.isdigit():
            continue
            
        if target_cell == ICE:
            ice_new_r, ice_new_c = new_r + dr, new_c + dc
            if not (0 <= ice_new_r < len(state.board) and 0 <= ice_new_c < len(state.board[0])):
                continue
            ice_target = state.board[ice_new_r][ice_new_c]
            if ice_target not in [EMPTY, LAVA]:
                continue
                
        moves.append(move)
        
    return moves

def apply_transition(state: GameState, action: str) -> GameState:
    #Applies a full game turn and returns a new state
    if action not in get_available_transitions(state):
        return state

    new_board_list = [list(row) for row in state.board]
    r, c = state.player_pos
    dr, dc = 0, 0
    if action == 'w': dr, dc = -1, 0
    elif action == 's': dr, dc = 1, 0
    elif action == 'a': dr, dc = 0, -1
    elif action == 'd': dr, dc = 0, 1

    new_r, new_c = r + dr, c + dc
    target_cell = new_board_list[new_r][new_c]

    # Handle ice pushing
    if target_cell == ICE:
        ice_new_r, ice_new_c = new_r + dr, new_c + dc
        new_board_list[ice_new_r][ice_new_c] = ICE

    # Clear the player's old position
    new_board_list[r][c] = EMPTY
    
    new_player_pos = (new_r, new_c)

    # Update numbered squares
    for r_idx, row in enumerate(new_board_list):
        for c_idx, cell in enumerate(row):
            if cell.isdigit():
                num = int(cell) - 1
                new_board_list[r_idx][c_idx] = str(num) if num > 0 else EMPTY

    # Spread Lava and Water
    new_lava = set()
    new_water = set()
    water_to_block = set()
    new_mesh_lava = set()
    new_mesh_water = set()
    rows, cols = len(new_board_list), len(new_board_list[0])
    
    player_dies_this_turn = False

    for r_idx in range(rows):
        for c_idx in range(cols):
            cell = new_board_list[r_idx][c_idx]
            if cell in [LAVA, WATER]:
                spread_char = LAVA if cell == LAVA else WATER
                for dr_spread, dc_spread in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r_idx + dr_spread, c_idx + dc_spread
                    if not (0 <= nr < rows and 0 <= nc < cols):
                        continue

                    target = new_board_list[nr][nc]
                                        
                    if (nr, nc) == new_player_pos and spread_char == LAVA:
                        player_dies_this_turn = True

                    if target == EMPTY:
                        if spread_char == LAVA: new_lava.add((nr, nc))
                        else: new_water.add((nr, nc))
                    elif target == MESH:
                        if spread_char == LAVA: new_mesh_lava.add((nr, nc))
                        else: new_mesh_water.add((nr, nc))
                    elif spread_char == LAVA and target == WATER:
                        water_to_block.add((nr, nc))
                            
    for r, c in new_lava: new_board_list[r][c] = LAVA
    for r, c in new_water: new_board_list[r][c] = WATER
    for r, c in water_to_block: new_board_list[r][c] = BLOCK
    for r,c in new_mesh_lava: new_board_list[r][c] = MESH_LAVA
    for r,c in new_mesh_water: new_board_list[r][c] = MESH_WATER

    if player_dies_this_turn:
        pr, pc = new_player_pos
        new_board_list[pr][pc] = LAVA

    final_board_tuple = tuple(tuple(row) for row in new_board_list)
    return GameState(board=final_board_tuple, player_pos=new_player_pos)

def is_terminal(state: GameState) -> bool:
    #Checks if the game is in a terminal state (win or lose)
    r, c = state.player_pos 
    cell_at_player_pos = state.board[r][c]
    return cell_at_player_pos in [GOAL, LAVA]

def is_goal(state: GameState) -> bool:
    #Checks if the game is in a winning state
    r, c = state.player_pos
    return state.board[r][c] == GOAL