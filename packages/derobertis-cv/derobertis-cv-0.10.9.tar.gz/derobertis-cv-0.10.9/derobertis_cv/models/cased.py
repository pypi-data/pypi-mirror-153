from typing import Optional, Sequence, List, Set, Callable


class CasedModel:
    title: str
    flexible_case: bool = True
    case_lower_func: Callable[[str], str] = lambda x: x.lower()
    case_title_func: Callable[[str], str] = lambda x: x.title()
    case_capitalize_func: Callable[[str], str] = lambda x: x.capitalize()

    def __post_init__(self):
        super().__init__()

    def to_title_case_str(self) -> str:
        if not self.flexible_case:
            return self.title
        return self.case_title_func(self.title)  # type: ignore

    def to_lower_case_str(self) -> str:
        if not self.flexible_case:
            return self.title
        return self.case_lower_func(self.title)  # type: ignore

    def to_capitalized_str(self) -> str:
        if not self.flexible_case:
            return self.title
        return self.case_capitalize_func(self.title)  # type: ignore


def first_word_untouched_rest_title(s: str) -> str:
    parts = s.split()
    return f'{parts[0]} {" ".join([part.title() for part in parts[1:]])}'


def first_word_untouched_rest_lower(s: str) -> str:
    parts = s.split()
    return f'{parts[0]} {" ".join([part.lower() for part in parts[1:]])}'


def first_word_untouched_rest_capitalized(s: str) -> str:
    parts = s.split()
    return f'{parts[0]} {" ".join([part.capitalize() for part in parts[1:]])}'