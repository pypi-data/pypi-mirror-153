from dataclasses import dataclass

from puft.core.cell.named_cell import NamedCell
from puft.core.sv.sv import Sv


@dataclass
class SvCell(NamedCell):
    sv_class: type[Sv]
