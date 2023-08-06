from os import PathLike
from typing import Dict, Any, Optional, Union

from converter import Converter

from derobertis_cv.pldata.cover_letters.models import ApplicationComponents

VIDEO_OPTIONS: Dict[str, Dict[str, int]] = {
    '1080p': {
        'width': 1920,
        'height': 1080,
    },
    '720p': {
        'width': 1280,
        'height': 720,
    },
    '480p': {
        'width': 854,
        'height': 480
    },
    '360p': {
        'width': 640,
        'height': 360
    },
    '360p_24fps': {
        'width': 640,
        'height': 360,
        'fps': 24
    },
    '288p': {
        'width': 480,
        'height': 272
    },
    '240p': {
        'width': 426,
        'height': 240
    },
    '240p_24fps': {
        'width': 426,
        'height': 240,
        'fps': 24,
    },
    '216p': {
        'width': 384,
        'height': 216
    },
    '216p_24fps': {
        'width': 384,
        'height': 216,
        'fps': 24,
    },
    '144p': {
        'width': 256,
        'height': 144
    }
}

KNOWN_SIZES_MB: Dict[ApplicationComponents, Dict[str, float]] = {
    ApplicationComponents.JMP_VIDEO: {
        '1080p': 90,
        '720p': 35,
        '480p': 16.6,
        '360p': 10.1,
        '360p_24fps': 9.7,
        '288p': 6.5,
        '240p': 5.7,
        '240p_24fps': 5.5,
        '216p': 5.2,
        '216p_24fps': 5.1,
        '144p': 3.9,
    }
}


def convert_video_format(in_path: Union[str, PathLike], out_path: Union[str, PathLike], file_format: str,
                         audio_options: Optional[Dict[str, Any]] = None,
                         video_options: Optional[Dict[str, Any]] = None):
    conv = Converter()
    audio = {
        'codec': 'aac'
    }
    if audio_options is not None:
        audio.update(audio_options)
    video = {
        'codec': 'h264',
        'width': 1920,
        'height': 1080,
    }
    if video_options is not None:
        video.update(video_options)

    options = {
        'format': file_format,
        'audio': audio,
        'video': video,
    }
    print(f'Converting {in_path} with options {options}')
    convert = conv.convert(str(in_path), str(out_path), options)

    for time_code in convert:
        print(f'\rConverting {in_path} ({time_code:.2f}) ...')


def get_video_options(component: ApplicationComponents, desired_size_mb: int = 10):
    format_sizes = KNOWN_SIZES_MB[component]
    sizes = sorted(list(format_sizes.values()))

    idx = -1
    for size in sizes:
        if size > desired_size_mb:
            bad_idx = sizes.index(size)
            idx = bad_idx - 1
            break

    if idx < 0:
        raise ValueError('no sizes are valid')
    size = sizes[idx]
    format = {value: key for key, value in format_sizes.items()}[size]
    return VIDEO_OPTIONS[format]
