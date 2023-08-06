from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from puft.core.sv.sv_cell import SvCell

if TYPE_CHECKING:
    from puft.core.app.puft import Puft
    from puft.tools.hints import CLIModeEnumUnion


@dataclass
class PuftSvCell(SvCell):
    """Injection cell with app itself which is required in any build."""
    sv_class: type[Puft]
    mode_enum: CLIModeEnumUnion
    host: str
    port: int
    ctx_processor_func: Callable | None = None
    each_request_func: Callable | None = None
    first_request_func: Callable | None = None