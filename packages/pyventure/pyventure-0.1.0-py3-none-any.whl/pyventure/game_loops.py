import re

from .message import msg
from .place import Place
from .player import Player
from .save import save_game, load_game
from .user_answer import get_answer_no_confirm, get_answer_confirm


def explore_place(place: Place, player: Player, all_places: dict) -> Place|None:
    msg.scroll_narrate(place.description)
    while True:
        command = input('> ')
        if command.lower() == 'status':
            player.status()
            continue
        elif command.lower().startswith('investigate'):
            target = command.replace('investigate', '').strip()
            for feature in place.features:
                if feature.name in target:
                    break
            else:
                msg.warning('\nInvestigate what, exactly?\n')
                continue
            msg.scroll_narrate(feature.interact_msg)
            if feature.danger:
                msg.scroll_danger(feature.danger_msg)
                player.wound(feature.danger)
        elif command.lower().startswith('take'):
            target = command.replace('take', '').strip()
            for feature in place.features:
                if feature.name in target:
                    break
            else:
                msg.warning('Take what now?')
                continue
            if not feature.takeable:
                msg.warning(f'That {feature.name} is not going to help you much. Try something else.')
                continue
            else:
                player.take(feature.takeable)
                place.features.remove(feature)
        elif command.lower().startswith('read'):
            target = command.replace('read', '').strip()
            player.read(target)
        elif command.lower().startswith('use'):
            tool_target = re.sub(r'use|on|the|in', '', command).split()
            tool = tool_target[0]
            target = tool_target[1]
            player.use(tool, place, target)
        elif command.lower().startswith('go'):
            target = re.sub(r'go|to|the|through|', '', command).strip()
            for node in place.nodes:
                if target in node.name:
                    break
            else:
                msg.warning("Go where now?")
                continue
            if node.accessible:
                msg.scroll_narrate(node.travel_msg)
                return all_places[node.place_name]
            else:
                msg.warning('That way is inaccessible to you right now.')
                continue
        elif command.lower() in ('backpack', 'inventory'):
            player.show_inventory()
        elif command.lower().startswith('eat'):
            target = command.replace('eat', '').strip()
            player.eat(target)
        elif command.lower() in ('quit', 'stop', 'exit', 'close'):
            msg.warning('Do you want to save first?')
            answer = get_answer_no_confirm(('yes', 'no'))
            if answer == 'yes':
                save_game(player, place, all_places)
            return
        elif command.lower() == 'save':
            save_game(player, place, all_places)

def new_game(new_game_msg: str, all_places: dict[str, Place]):
    msg.orange(new_game_msg)
    name = get_answer_confirm()
    player = Player(name)
    msg.dialogue(f'Hello, {player.name}. You can "continue" or ask for "help"')
    get_answer_no_confirm(('continue'))
    current_place = list(all_places.values())[0]
    return player, current_place, all_places

def main_loop(current_place: Place, player: Player, all_places: dict):
    while True:
        if isinstance(current_place, Place):
            current_place = explore_place(current_place, player, all_places)
        else:
            break
    msg.dialogue('\n[bold]Thanks for playing!\n')

def start(new_game_msg: str, all_places: dict[str, Place]):
    msg.dialogue('[u]Load[/u] game or start a [u]new[/u] game?\n')
    answer = get_answer_no_confirm(('load', 'new'))
    if answer == 'load':
        data = load_game()
        if None in (data):
            player, current_place, all_places = new_game(new_game_msg, all_places)
        else:
            player, current_place, all_places = data
    elif answer == 'new':
        player, current_place, all_places = new_game(new_game_msg, all_places)
    main_loop(current_place, player, all_places)
