import os
import shutil
from os import PathLike
from pathlib import Path
from typing import Union

from derobertis_cv.plbuild.paths import SPECIFIC_APPLICATIONS_OUT_PATH, APPLICATIONS_OUT_PATH


def copy_application_folder(
    abbreviation: str,
    src: Union[str, PathLike] = APPLICATIONS_OUT_PATH,
    dst: Union[str, PathLike] = SPECIFIC_APPLICATIONS_OUT_PATH
):
    full_src = Path(src) / abbreviation
    full_dst = Path(dst) / abbreviation
    print(f'Copying {full_src} to {full_dst}')
    if os.path.exists(full_dst):
        shutil.rmtree(full_dst)
    shutil.copytree(full_src, full_dst)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('name', help="Abbreviation of cover letter to push to specific applications")
    args = parser.parse_args()

    copy_application_folder(args.name)
