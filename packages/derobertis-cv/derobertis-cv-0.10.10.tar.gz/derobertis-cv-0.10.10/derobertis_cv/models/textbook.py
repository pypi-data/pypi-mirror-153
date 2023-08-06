from dataclasses import dataclass
from typing import Optional


@dataclass
class TextbookModel:
    title: str
    author: str
    required: bool = True
    publisher_details: Optional[str] = None
    description: Optional[str] = None

    def to_str(self) -> str:
        base_str = f'{self.author}, "{self.title}'
        if self.publisher_details:
            end_str = f'," {self.publisher_details}.'
        else:
            end_str = '."'
        return base_str + end_str