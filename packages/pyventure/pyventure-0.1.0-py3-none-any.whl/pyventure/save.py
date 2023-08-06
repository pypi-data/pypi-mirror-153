from pathlib import Path
import pickle

from .message import msg
from .player import Player
from .place import Place
from .user_answer import get_answer_no_confirm

BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / 'save_files'

def save_game(player: Player, current_place: Place, all_places: dict[str, Place]):
    OUTPUT_DIR.mkdir(exist_ok=True)
    output = OUTPUT_DIR / player.name
    data = (player, current_place, all_places)
    with open(output, 'wb') as f:
        pickle.dump(data, f)
    msg.success(f'Successfully saved game as {player.name}')
    

def load_game() -> tuple[Player, Place, dict[str, Place]]:
    save_dir = OUTPUT_DIR.glob('*')
    saved_games: list[Path] = []
    for f in save_dir:
        if f.is_file():
            saved_games.append(f)
    total_saved = len(saved_games)
    if total_saved == 0:
        msg.warning('Sorry, there were no saved game files found. Starting a new game...')
        return None, None, None
    number = ('are', 's') if total_saved >= 2 else ('is', '')
    msg.orange(f'There {number[0]} {total_saved} saved game{number[1]}. Enter a name to load it.')
    for game in saved_games:
        msg.plain(game.stem)
    game = get_answer_no_confirm([f.stem for f in saved_games])
    game_dir = OUTPUT_DIR / game
    with open(game_dir, 'rb') as f:
        data = pickle.load(f)
    msg.success(f'Loaded {data[0].name}')
    return data
