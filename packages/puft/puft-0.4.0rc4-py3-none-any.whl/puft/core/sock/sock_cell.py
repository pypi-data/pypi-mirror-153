from dataclasses import dataclass
from typing import Callable

from puft.core.cell.cell import Cell
from .sock import Sock
from .default_sock_error_handler import default_sock_error_handler


@dataclass
class SockCell(Cell):
    namespace: str
    handler_class: type[Sock]
    error_handler: Callable = default_sock_error_handler
