from dataclasses import dataclass
from warepy import snakefy


@dataclass
class Cell:
    @classmethod
    def _get_formatted_name(cls, base_name: str = 'Cell') -> str:
        return snakefy(cls.__name__.replace(base_name, ''))

    def get_json(self) -> dict:
        return {
            self._get_formatted_name(): self.__dict__
        }
