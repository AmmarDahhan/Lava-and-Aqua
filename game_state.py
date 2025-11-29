from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class GameState:
    board: Tuple[Tuple[str, ...], ...]
    player_pos: Tuple[int, int]

    def __hash__(self):
        return hash((self.board, self.player_pos))