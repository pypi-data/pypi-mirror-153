from time import sleep
import re

from rich.console import Console


console = Console(color_system='256')

HELP = '''
Gameplay works by typing a command and a target.

The following commands are valid:
"take", "investigate", "use", "read", "go", "eat", "quit",
"save", "exit", "quit".

Make sure to include a target, for example:
"take book", "investigate nest", "read leather book", "go right".

The "use" command requires a tool [italic]and[/italic] a target,
for example: "[u]use key [/u] on [u]door lock[/u]"

Type "status" to see your character info and "hint"
to receive a help message if there is one.

Type "backpack" or "inventory" to list out all of your items.
'''.strip()

class Message:

    def __init__(self) -> None:
        self.text_scroll_delay = 0.01

    def danger(self, text: str):
        console.print(text, style='bold red')

    def warning(self, text: str):
        console.print(text, style='bold yellow')

    def narrate(self, text: str):
        console.print(text, style='italic')

    def dialogue(self, text: str):
        console.print(text, style='italic cyan')

    def success(self, text: str):
        console.print(text, style='bold green')

    def orange(self, text: str):
        console.print(text, style='orange1')

    def plain(self, text: str):
        console.print(text)

    def heading(self, text: str, color: str = 'magenta'):
        print()
        console.rule(f'[bold magenta]{text}', style=f'bold {color}')
        print()

    def scroll_text(self, text: list | str, style: str):
        print()
        if not isinstance(text, list):
            text: str = text.splitlines()
        spinner = console.status('', spinner='toggle2', spinner_style=style, speed=1.0, refresh_per_second=25)
        spinner.start()
        for line in text:
            words = []
            for word in line.split():
                characters = []
                for character in re.sub(r'\[[^\]]+\]', '', word): #strip out markup when rendering single characters
                    characters.append(character)
                    spinner.update(f'\t[{style}]{" ".join(words)} {"".join(characters)}')
                    sleep(self.text_scroll_delay)
                words.append(word)
            console.print(f'\t{line}', style=style)

        spinner.stop()
        print()

    def scroll_danger(self, text):
        self.self.scroll_text(text, 'bold red')

    def scroll_warning(self, text):
        self.scroll_text(text, 'bold yellow')

    def scroll_narrate(self, text):
        self.scroll_text(text, 'italic')

    def scroll_dialogue(self, text):
        self.scroll_text(text, 'italic cyan')

    def scroll_success(self, text):
        self.scroll_text(text, 'bold green')

    def scroll_orange(self, text):
        self.scroll_text(text, 'orange1')

    def scroll_plain(self, text):
        self.scroll_text(self, text, 'white on black')

    def scroll_danger(self, text):
        self.scroll_text(text, 'bold red')


    def help_text(self):
        console.rule('[bold]Help')
        self.plain(HELP)
        console.rule('[bold]End of Help')

msg = Message()
