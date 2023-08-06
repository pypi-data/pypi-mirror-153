from .message import msg
from .items import Consumable, Tool, Clue
from .place import Place


class Player:
    def __init__(self, name: str) -> None:
        self.score = 0
        self.name = name
        self.health = 100
        # self.strength = 1
        self.inventory: list[Tool|Consumable|Clue] = []
    
    def take(self, item: Consumable|Tool|Clue):
        self.inventory.append(item)
        msg.success(f'You put the {item.name} in your inventory.')

    def drop(self, name: str):
        new_inventory: list[Tool|Consumable|Clue] = []
        for item in self.inventory:
            if item.name != name:
                new_inventory.append(item)
        self.inventory = new_inventory
        msg.warning(f'You take {name} out of your inventory and toss it away.\nYour pack does feel a little lighter.')

    def __consume(self, item: Consumable):
        old_health = self.health
        self.health += item.value
        item.total -= 1
        if item.total == 0:
            for i, x in enumerate(self.inventory):
                if x.name == item.name:
                    self.inventory.pop(i)
                    msg.scroll_narrate(x.on_use)
                    break
        msg.success(f"Tasty. Your health has increased from {old_health} to {self.health}.")

    def __use_tool(self, tool: Tool, place: Place, target: str):
        for feature in place.features:
            if feature.name == target:
                break
        else:
            msg.warning(f"Huh? What do you want to use your {tool.name} on?")
            return
        if tool.name.lower() == feature.tool_name.lower():
            msg.success(feature.success_msg)
            tool.uses -= 1
            if feature.unlock:
                feature.unlock.accessible = True
        else:
            print('failed')

    def use(self, name: str, place: Place, target: str):
        for item in self.inventory:
            if item.name.lower() == name.lower():
                break
        else:
            msg.warning(f"Huh, you dig around in your pack and can't find anything like a {name}.")
        if isinstance(item, (Clue)):
            self.read(name)
        elif isinstance(item, Tool):
            self.__use_tool(item, place, target)

    def read(self, name: str):
        for item in self.inventory:
            if isinstance(item, Clue) and item.name.lower() == name.lower():
                msg.heading(f'Clue: "{item.name}"\t{item.form}')
                msg.narrate(item.content)
                msg.heading('end')
                return
        else:
            msg.warning(f"After thumbing through your clues and notes, you can't find a \"{name}\".")

    def wound(self, damage: int):
        self.health -= damage
        msg.danger(f'You are wounded for {damage} ponts.')
        msg.orange(f'Health: {self.health}')
        if self.health <= 0:
            self.lose()

    def lose(self):
        print('You lose, bummer. Finish this method')

    def status(self):
        msg.heading(f"{self.name}'s Status")
        if self.health >= 75:
            msg.success(f'Health: {self.health}')
        elif 30 < self.health <= 75:
            msg.warning(f'Health: {self.health}')
        else: msg.danger(f'Health: {self.health}')
        msg.plain(f'Score: {self.score}')
        msg.plain(f'Items in your inventory: {len(self.inventory)}')
        # plain(f'Strength: {self.strength}')
        msg.heading('end')
    
    def show_inventory(self):
        def sort_key(item):
            if isinstance(item, Consumable):
                return 1
            elif isinstance(item, Tool):
                return 3
            elif isinstance(item, Clue):
                return 5
            else:
                return 7
        sorted_inventory = sorted(self.inventory, key=sort_key)
        msg.heading(f"{self.name}'s Inventory")
        for item in sorted_inventory:
            msg.orange(item)
        msg.heading('end')

    def eat(self, item_name: str):
        for item in self.inventory:
            if item.name.lower() == item_name.lower() and isinstance(item, Consumable):
                self.__consume(item)
                break
        else:
            msg.warning(f"\nYou don't have a consummable named '{item_name}'")
