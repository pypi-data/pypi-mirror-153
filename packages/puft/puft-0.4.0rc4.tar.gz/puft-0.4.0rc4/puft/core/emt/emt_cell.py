from dataclasses import dataclass

from puft.core.cell.cell import Cell

from .emt import Emt


@dataclass
class EmtCell(Cell):
    emt_class: type[Emt]