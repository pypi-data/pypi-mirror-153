from typing import List, Sequence, Optional

import pyexlatex.resume as lr

from derobertis_cv.models.award import AwardModel
from derobertis_cv.pltemplates.logo import svg_text


def get_awards(
    include_awards: Optional[Sequence[str]] = None,
    order: Optional[Sequence[str]] = None
) -> List[AwardModel]:
    awards = [
        AwardModel(
            'Warrington College of Business Ph.D. Student Teaching Award',
            received='Fall 2016',
            award_parts=['Ph.D. Student Teaching Award', 'University of Florida', 'Warrington College of Business'],
            logo_fa_icon_class_str='fas fa-graduation-cap',
        ),
        AwardModel(
            'Graduate Management Admission Test (GMAT) Score',
            received='2014',
            award_parts=['Graduate Management Admission Test (GMAT)', '780 score', '99.6 percentile'],
            extra_info='780 | 99.6 percentile',
            logo_svg_text=svg_text('gmat-logo.svg'),
        ),
        AwardModel('Warrington Finance Ph.D. Research Grants', received='2014-2019', extra_info=r'\$2000/yr'),
        AwardModel(
            'CFA Global Investment Research Challenge – Global Semi-Finalist',
            received='2013',
            award_parts=['Global Semi-Finalist', 'CFA Challenge', 'CFA Institute'],
            logo_svg_text=svg_text('cfa-logo.svg'),
        ),
        AwardModel(
            'Finance Student of the Year',
            received='2013',
            award_parts=['Finance Student of the Year', 'Virginia Commonwealth University'],
            logo_fa_icon_class_str='fas fa-pencil-alt',
        ),
        AwardModel('Alcoa Foundation Community Scholarship', received='2010-2014', extra_info='full tuition and fees'),
        AwardModel('VCU School of Business Scholarship', received='2010-2014', extra_info=r'\$3000/yr')
    ]

    if include_awards is not None:
        awards = [award for award in awards if award.title in include_awards]

    if order is not None:
        awards.sort(
            key=lambda award: order.index(award.title)  # type: ignore
            if award.title in order else 100000 - awards.index(award)  # type: ignore
        )

    return awards
