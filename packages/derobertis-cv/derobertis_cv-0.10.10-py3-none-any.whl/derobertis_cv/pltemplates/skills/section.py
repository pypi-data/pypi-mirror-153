from typing import Sequence, List, Dict, Optional
from collections import defaultdict

import math
import pyexlatex as pl
from pyexlatex.typing import PyexlatexItem

from derobertis_cv.models.skill import SkillModel
from derobertis_cv.pltemplates.skills.skill import PyexlatexSkill


class SkillsSection(pl.Section):
    def __init__(self, skills: Sequence[SkillModel], skills_per_row: int = 4,
                 section_order: Optional[Sequence[str]] = None, font_scale: Optional[float] = None,
                 exclude_sections: Optional[Sequence[str]] = None,
                 reassign_sections: Optional[Dict[str, str]] = None, adjust_space_after_section: float = -0.15):
        self.skills = skills
        self.font_scale = font_scale
        self.adjust_space_after_section = adjust_space_after_section

        skill_items: Dict[str, List[SkillModel]] = defaultdict(lambda: [])
        for skill in self.skills:
            if reassign_sections is not None and skill.to_lower_case_str() in reassign_sections:
                category = reassign_sections[skill.to_lower_case_str()]
            else:
                category = skill.category.to_title_case_str()
            if exclude_sections is not None and category in exclude_sections:
                continue
            skill_items[category].append(skill)

        category_names = list(skill_items.keys())
        orig_category_names = category_names.copy()

        if section_order:
            so = list(section_order)

            def _skill_sort_key(skill_name: str) -> int:
                key = orig_category_names.index(skill_name)
                if skill_name in so:
                    key -= 1000 * so.index(skill_name)
                return key
            category_names.sort(key=_skill_sort_key, reverse=True)

        content: List[PyexlatexItem] = []
        if font_scale is not None:
            font_str = (
                    r'\setmainfont{Latin Modern Roman}[Scale =' +
                    str(font_scale) +
                    ',Ligatures = {Common, TeX}]'
            )
            font_resize = pl.Raw(font_str)
            content.append(font_resize)

        content.extend([PyexlatexSkill.legend, ''])
        for category_skill_name in category_names:
            cat_skills = skill_items[category_skill_name]
            valid_skills = [skill for skill in cat_skills if not skill.to_title_case_str() in category_names]
            if not valid_skills:
                continue
            content.extend([pl.Bold(category_skill_name), ""])
            if self.adjust_space_after_section:
                content.append(pl.VSpace(self.adjust_space_after_section))
            num_rows = math.ceil(len(valid_skills) / skills_per_row)
            table_data: List[List[PyexlatexItem]] = [[] for _ in range(num_rows)]
            for i in range(num_rows * skills_per_row):
                col_idx = i % num_rows
                try:
                    skill = valid_skills[i]
                except IndexError:
                    table_data[col_idx].append('')
                else:
                    table_data[col_idx].append(PyexlatexSkill(skill.to_title_case_str(), skill.experience_level))

            vt = pl.ValuesTable.from_list_of_lists(table_data)
            total_width_cm = 17
            width_per_col = total_width_cm / skills_per_row
            align = f"L{{{width_per_col}cm}}" * skills_per_row
            table = pl.Tabular([vt], align=align)
            content.append(table)

            content.append("")
        content = content[:-1]  # remove last spacer

        super().__init__(content, title="Skills")
