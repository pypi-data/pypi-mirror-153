from typing import Callable
from dataclasses import dataclass

from puft.core.cell.cell import Cell

from .error import Error


@dataclass
class ErrorCell(Cell):
    error_class: type[Error]
    handler_function: Callable