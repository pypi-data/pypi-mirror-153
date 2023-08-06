from typing import Union, Sequence

import pyexlatex as pl
from pyexlatex.typing import PyexlatexItems

partial_circle_def = pl.Raw(
r"""
\tikzset{%
    pics/partialcircle/.style args={#1/#2/#3/#4}{code={%
        \ifstrequal{#2}{0}{%
            \node[circle,minimum width=1.35mm,draw=#4,fill=#1] {};
        }{%
            \tkzDefPoint(0,0){O}
            \tkzDrawSector[R,fill=#1,draw=#4](O,1.35mm)(90,90-#2)
            \tkzDrawSector[R,fill=#3,draw=#4](O,1.35mm)(90-#2,90-360)
    }
    }},
}
"""
)

GRAY_DARK = 130
GRAY_LIGHT = 220


class PartialCircle(pl.Template):

    def __init__(self, fill: float = 0.5, bg_color: Union[str, pl.TextColor] = 'white',
                 fg_color: Union[str, pl.TextColor] = 'black', line_color: Union[str, pl.TextColor] = 'black'):
        self.fill = fill
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.line_color = line_color
        self.init_data()
        self.add_package('etoolbox')
        self.add_package('tkz-euclide')
        self.data.packages.extend([
            # pl.Raw(r'\usetkzobj{all}'),  # required in overleaf but not with newer version of tkz-euclide
            partial_circle_def
        ])
        self.contents = self._get_contents()
        super().__init__()

    def _validate_contents(self):
        if self.fill < 0 or self.fill > 1:
            raise ValueError(f'fill must be between 0 and 1, got {self.fill}')
        super()._validate_contents()

    @property
    def _circle_fill(self) -> int:
        full = 360
        return int(full * self.fill)

    def _get_contents(self) -> PyexlatexItems:
        if self.fill == 1:
            fill_def = str(self.fg_color) + '/0//' + str(self.line_color)
        else:
            fill_def = (
                str(self.bg_color) +
                '/' +
                str(self._circle_fill) +
                '/' +
                str(self.fg_color) +
                '/' +
                str(self.line_color)
            )

        return [
            pl.TextSize(-3),
            r'\tikz[baseline=-0.9ex]\pic{partialcircle=' + fill_def + '};',
            pl.TextSize(0),
        ]


class SkillDot(PartialCircle):

    def __init__(self, level: int, max_level: int = 5, color_level: int = 1,
                 color_choices: Sequence[Union[str, pl.TextColor]] = ('black',)):
        fill = (level - 1) * 1 / (max_level - 1)
        try:
            color = color_choices[color_level - 1]
        except IndexError:
            raise ValueError(
                'Must pass a 1-based index for color_level which is valid for the length of color_choices'
            )
        super().__init__(fill, fg_color=color, line_color=color)


class GrayscaleSkillDot(SkillDot):

    def __init__(self, level: int, max_level: int = 5, color_level: int = 3):
        gray_dark = GRAY_DARK
        gray_light = GRAY_LIGHT
        gray_dark_def = pl.RGB(gray_dark, gray_dark, gray_dark, color_name=f'gray{gray_dark}')
        gray_light_def = pl.RGB(gray_light, gray_light, gray_light, color_name=f'gray{gray_light}')
        self.init_data()
        self.add_package('xcolor')
        self.data.packages.extend([gray_dark_def, gray_light_def])
        colors = (f'gray{gray_light}', f'gray{gray_dark}', 'black')
        super().__init__(level, max_level=max_level, color_level=color_level, color_choices=colors)
