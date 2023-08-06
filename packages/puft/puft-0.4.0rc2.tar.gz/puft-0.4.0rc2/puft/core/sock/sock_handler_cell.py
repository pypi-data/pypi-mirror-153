from dataclasses import dataclass
from typing import Callable

from puft.core.cell.cell import Cell
from .sock_handler import SockHandler
from .default_sock_error_handler import default_sock_error_handler


@dataclass
class SockHandlerCell(Cell):
    namespace: str
    handler_class: type[SockHandler]
    error_handler: Callable = default_sock_error_handler
