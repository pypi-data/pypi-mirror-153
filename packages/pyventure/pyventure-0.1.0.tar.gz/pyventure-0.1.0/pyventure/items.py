from dataclasses import dataclass

@dataclass
class Consumable:
    name: str
    risk: int
    value: int
    description: str
    on_use: str
    total: int
    def __repr__(self) -> str:
        return f'Consumable: {self.name}\n\tTotal: {self.total}\tValue: {self.value}\tRisk: {self.risk}\n\tDescription: {self.description}'


@dataclass
class Tool:
    name: str
    risk: int
    uses: int
    description: str
    total: int
    def __repr__(self):
        return f'Tool: {self.name}\n\tTotal: {self.total}\t Uses left: {self.uses}\tRisk: {self.risk}\n\tDescription: {self.description}'


@dataclass
class Clue:
    name: str
    form: str # note, scroll, book, etc.
    content: str
    def __repr__(self):
        return f'Clue: {self.name}\tForm: {self.form}'
