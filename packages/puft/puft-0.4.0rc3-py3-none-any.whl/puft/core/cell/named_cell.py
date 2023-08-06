from dataclasses import dataclass
from typing import Sequence, TypeVar

from puft.core.cell.cell import Cell


# Set TypeVar upper bound to class defined afterwards.
# https://stackoverflow.com/a/67662276
AnyNamedCell = TypeVar("AnyNamedCell", bound="NamedCell")


@dataclass
class NamedCell(Cell):
    name: str

    @staticmethod
    def find_by_name(name: str, cells: Sequence[AnyNamedCell]) -> AnyNamedCell:
        """Traverse through given list of cells and return first one with
        specified name.
        
        Raise:
            ValueError: 
                No cell with given name found.
        """
        for cell in cells:
            if cell.name == name:
                return cell
        raise ValueError(
            "No cell with given name {} found.", name)

    @staticmethod
    def map_to_name(cells: list[AnyNamedCell]) -> dict[str, AnyNamedCell]:
        """Traverse through given cells names and return dict with these cells
        as values and their names as keys."""
        cells_by_name: dict[str, AnyNamedCell] = {}
        for cell in cells:
            cells_by_name[cell.name] = cell
        return cells_by_name