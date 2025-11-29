import pygame
import game_logic
import os

class gameRenderer:
    def __init__(self, width, height, tile_size):
        pygame.init()
        self.tile_size = tile_size
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Lava and Aqua")

        self.assets = {}
        asset_names = {
            'player': 'player.png', 'wall': 'wall.png', 'lava': 'lava.png',
            'water': 'water.png', 'goal': 'goal.png', 'ice': 'ice.png',
            'block': 'block.png', 'empty': 'empty.png', 'mesh': 'mesh.png',
            'digital': 'digital.png', 'coin': 'coin.png'
        }
        for key, filename in asset_names.items():
            path = f'assets/{filename}'
            try:
                if os.path.exists(path):
                    image = pygame.image.load(path).convert_alpha()
                    self.assets[key] = pygame.transform.scale(image, (tile_size, tile_size))
                else:
                    raise FileNotFoundError 
            except (pygame.error, FileNotFoundError):
                print(f"Drawing asset programmatically for: {key}") 
                self.assets[key] = self._create_placeholder_surface(key)

        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 74)

    def _create_placeholder_surface(self, key):
        surface = pygame.Surface((self.tile_size, self.tile_size))
        colors = {
            'player': (255, 255, 0), 'wall': (128, 128, 128), 'lava': (255, 0, 0),
            'water': (0, 0, 255), 'goal': (0, 255, 0), 'ice': (173, 216, 230),
            'block': (64, 64, 64), 'empty': (50, 50, 50) , 'mesh': (255, 165, 0),
            'digital': (255, 255, 255), 'coin': (255, 223, 0)
        }
        surface.fill(colors.get(key, (255, 0, 255)))
        color = colors.get(key, (255, 0, 255))
        if key == 'coin': 
            center = (self.tile_size // 2, self.tile_size // 2)
            radius = self.tile_size // 3
            pygame.draw.circle(surface, color, center, radius)
            pygame.draw.circle(surface, (200, 150, 0), center, radius, 2)
            pygame.draw.circle(surface, (255, 255, 200), (center[0] - 5, center[1] - 5), 3)

        elif key == 'mesh':
            surface.fill(color)
            surface.set_alpha(128)
        else:
            surface.fill(color)

        return surface

    def render(self, state, move_count, available_moves, path_coords=set(), action_log=None):
        self.screen.fill((20, 20, 20))

        path_color = (255, 255, 0, 80) 
        path_surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        path_surface.fill(path_color)

        for r_idx, c_idx in path_coords:
            x, y = c_idx * self.tile_size, r_idx * self.tile_size
            self.screen.blit(path_surface, (x, y))
 
        for r_idx, row in enumerate(state.board):
            for c_idx, cell in enumerate(row):
                x, y = c_idx * self.tile_size, r_idx * self.tile_size
                if cell == game_logic.WALL: self.screen.blit(self.assets['wall'], (x, y))
                elif cell == game_logic.COIN: self.screen.blit(self.assets['coin'], (x, y))
                elif cell == game_logic.LAVA: self.screen.blit(self.assets['lava'], (x, y))
                elif cell == game_logic.WATER: self.screen.blit(self.assets['water'], (x, y))
                elif cell == game_logic.GOAL: self.screen.blit(self.assets['goal'], (x, y))
                elif cell == game_logic.ICE: self.screen.blit(self.assets['ice'], (x, y))
                elif cell == game_logic.BLOCK: self.screen.blit(self.assets['block'], (x, y))
                elif cell == game_logic.MESH: self.screen.blit(self.assets['mesh'], (x, y))
                elif cell == game_logic.MESH_LAVA:
                    self.screen.blit(self.assets['lava'], (x, y)) 
                    self.screen.blit(self.assets['mesh'], (x, y)) 
                elif cell == game_logic.MESH_WATER:
                    self.screen.blit(self.assets['water'], (x, y))
                    self.screen.blit(self.assets['mesh'], (x, y))
                elif cell.isdigit():
                    self.screen.blit(self.assets['digital'], (x, y))
                    text = self.font.render(cell, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
                    self.screen.blit(text, text_rect)
                else:
                    self.screen.blit(self.assets['empty'], (x, y))

        pr, pc = state.player_pos
        cell_under = state.board[pr][pc]    
        overlay_radius = self.tile_size // 4
        overlay_center = (pc * self.tile_size + self.tile_size//2, pr * self.tile_size + self.tile_size//2)
        if cell_under == game_logic.WATER:
            s = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            pygame.draw.circle(s, (0, 0, 255, 120), (self.tile_size//2, self.tile_size//2), overlay_radius)
            self.screen.blit(s, (pc * self.tile_size, pr * self.tile_size))
        elif cell_under == game_logic.LAVA:
            s = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 50, 0, 160), (self.tile_size//2, self.tile_size//2), overlay_radius)
            self.screen.blit(s, (pc * self.tile_size, pr * self.tile_size))

        self.screen.blit(self.assets['player'], (pc * self.tile_size, pr * self.tile_size))


        info_y = self.height - 50
        move_text = self.font.render(f"Moves: {move_count}", True, (255, 255, 255))
        self.screen.blit(move_text, (10, info_y))

        moves_str = ', '.join(available_moves).upper()
        available_text = self.font.render(f"Available: {moves_str}", True, (200, 200, 200))
        self.screen.blit(available_text, (200, info_y))
        
        controls_text = self.font.render("U: Undo | R: Restart | B: BFS | D: DFS | Q: Quit", True, (150, 150, 150))
        self.screen.blit(controls_text, (10, info_y + 25))

        if action_log and len(action_log) > 0: 
            action_log_str = "-".join(action_log)
            
            if len(action_log_str) > 70:
                action_log_str = "..." + action_log_str[-70:]
                
            solver_moves_text = self.font.render(f"Path: {action_log_str}", True, (100, 255, 100))
            self.screen.blit(solver_moves_text, (400, info_y))
        
        pygame.display.flip()

    def show_end_screen(self, state, move_count, won):        
        self.render(state, move_count, [],path_coords=set(),action_log=None) 
        
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        if won:
            text = self.large_font.render("YOU WIN!", True, (0, 255, 0))
        else:
            text = self.large_font.render("GAME OVER", True, (255, 0, 0))
        
        text_rect = text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(text, text_rect)

        sub_text = self.font.render(f"Moves: {move_count}", True, (255, 255, 255))
        sub_rect = sub_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(sub_text, sub_rect)

        restart_text = self.font.render("Press R to Restart", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()