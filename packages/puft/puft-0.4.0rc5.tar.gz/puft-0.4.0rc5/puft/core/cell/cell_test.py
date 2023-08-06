from dataclasses import dataclass
from puft.core.test.test import Test
from puft.core.cell.cell import Cell


class TestCell(Test):
    def test_get_json(self):
        @dataclass
        class ChildCell(Cell):
            a: int
            b: str
            c: bool

        cell: ChildCell = ChildCell(1, 'hello', True)
        json: dict = cell.get_json()
        
        cell_json: dict = json['child']
        a: int = cell_json['a']
        b: int = cell_json['b']
        c: int = cell_json['c']
        assert a == 1
        assert b == 'hello'
        assert c == True

    def test_get_json_redefine_name(self):
        @dataclass
        class ChildModelCell(Cell):
            a: int
            b: str
            c: bool

            @classmethod
            def _get_formatted_name(cls, base_name: str = 'ModelCell') -> str:
                return super()._get_formatted_name(base_name)

        cell: ChildModelCell = ChildModelCell(1, 'hello', True)
        json: dict = cell.get_json()
        
        cell_json: dict = json['child']
        a: int = cell_json['a']
        b: int = cell_json['b']
        c: int = cell_json['c']
        assert a == 1
        assert b == 'hello'
        assert c == True
        
