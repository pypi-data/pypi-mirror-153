from dataclasses import dataclass, field
from typing import Sequence, Optional, Set

from weakreflist import WeakList


class NestedModel:
    parents: Optional[Sequence['NestedModel']]
    children: WeakList

    def __init__(self):
        if self.parents is not None:
            for parent in self.parents:
                parent.children.append(self)

    def get_nested_children(self) -> Set['NestedModel']:
        all_children = set()
        child: 'NestedModel'
        for child in self.children:
            all_children.add(child)
            all_children.update(child.get_nested_children())
        return all_children