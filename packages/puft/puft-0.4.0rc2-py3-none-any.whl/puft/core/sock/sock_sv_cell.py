from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass

from puft.core.sv.sv_cell import SvCell

if TYPE_CHECKING:
    from puft.core.sock.sock import Sock


@dataclass
class SockSvCell(SvCell):
    sv_class: type[Sock]
