import base64
import os
import pathlib
from typing import Optional

from derobertis_cv.plbuild.paths import IMAGES_PATH


class HasLogo:
    logo_url: Optional[str] = None
    logo_svg_text: Optional[str] = None
    logo_base64: Optional[str] = None
    logo_fa_icon_class_str: Optional[str] = None

    @property
    def logo_src(self) -> Optional[str]:
        if self.logo_url is not None:
            return self.logo_url
        if self.logo_base64 is not None:
            return self.logo_base64
        return None


def image_base64(file_name: str) -> str:
    _, file_extension = os.path.splitext(file_name)
    file_extension = file_extension[:1]  # remove . at beginning
    image_type = file_extension.lower()

    file_path = os.path.join(IMAGES_PATH, file_name)
    with open(file_path, 'rb') as f:
        contents = f.read()
    b64 = base64.b64encode(contents).decode('utf8')
    src = f"data:image/{image_type};base64,{b64}"
    return src


def svg_text(file_name: str) -> str:
    file_path = os.path.join(IMAGES_PATH, file_name)
    contents = pathlib.Path(file_path).read_text()
    content_idx = contents.find('<svg')
    return contents[content_idx:]
