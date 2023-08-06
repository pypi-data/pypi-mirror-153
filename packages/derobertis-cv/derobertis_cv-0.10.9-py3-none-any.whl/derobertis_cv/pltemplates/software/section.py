from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from derobertis_cv.pltemplates.software.project import SoftwareProject
from copy import deepcopy
import pyexlatex.resume as lr


class SoftwareSection(lr.SpacedSection):

    def __init__(self, contents, compact: bool = False, **kwargs):
        if not isinstance(contents, (list, tuple)):
            contents = [contents]

        contents = deepcopy(contents)  # don't overwrite passed contents

        if compact:
            for content in contents:
                if hasattr(content, 'is_SoftwareProject') and content.is_SoftwareProject:
                    content = cast('SoftwareProject', content)
                    content.compact = True
                    # Refresh output
                    content.contents = content._get_contents()

        super().__init__(contents, **kwargs)