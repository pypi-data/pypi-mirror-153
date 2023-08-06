from typing import Optional

import pyexlatex as pl

from derobertis_cv.models.course import CourseModel


class Syllabus(pl.Template):

    def __init__(self, model: CourseModel):
        self.model = model
        self.add_package(pl.Package('hyperref', modifier_str='hidelinks=true'))
        self.contents = self._get_contents()
        super().__init__()

    def _get_contents(self):
        return [
            self.overview_table,
            self.course_materials_section,
            pl.VSpace(),
            self.general_infomation_section,
            pl.VSpace(),
            self.grading_section,
            pl.VSpace(),
            self.topics_covered_section,
            self.resources_section,
        ]

        
    @property
    def overview_table(self) -> pl.Tabular:
        align = 'C{5.5cm}' * 3
        return pl.Tabular(
            [

                pl.TopRule(),
                pl.TableLineBreak(),
                pl.TableLineBreak(),
                pl.ValuesTable.from_list_of_lists(
                    [
                        [
                            f'{pl.TextSize(2)} {pl.Bold("Instructor")}',
                            f'{pl.TextSize(2)} {pl.Bold("Email")}',
                            f'{pl.TextSize(2)} {pl.Bold("Office Hours")}'
                        ],
                    ]
                ),
                # pl.TextSize(0),
                pl.TableLineBreak(),
                pl.ValuesTable.from_list_of_lists(
                    [
                        [self.model.instructor, self.model.instructor_email, self.model.office_hours],
                    ]
                ),
                pl.TableLineBreak(),
                pl.TableLineBreak(),
                # pl.BottomRule()

            ],
            align=align,
        )

    @property
    def course_materials_section(self) -> pl.Section:
        contents = []
        if self.model.website_url is not None:
            contents.append(
                pl.SubSection(
                    [
                        pl.TextColor(
                            pl.Underline(
                                pl.Hyperlink(self.model.website_url, self.model.website_url)
                            ),
                            'blue'
                        ),
                        pl.UnorderedList([
                            'The course website includes all of the materials for the course, including the '
                            'course schedule, lecture videos, lab exercises, practice problems, and projects.'
                        ])
                    ],
                    title='Course Website'
                )
            )

        if self.model.textbook is not None:
            contents.append(
                pl.SubSection(
                    [
                        self.model.textbook.to_str(),
                        pl.UnorderedList([self.model.textbook.description])
                    ],
                    title='Textbook'
                )
            )

        if self.model.daily_prep is not None:
            contents.append(
                pl.SubSection(
                    [
                        self.model.daily_prep
                    ],
                    title='Prepare for Class'
                )
            )

        return pl.Section(
            contents,
            title='Course Materials'
        )

    @property
    def general_infomation_section(self) -> pl.Section:
        contents = []
        if self.model.long_description is not None:
            contents.append(pl.SubSection(self.model.long_description, title='Description'))

        if self.model.prerequisites is not None:
            prereq_contents = []
            if self.model.prerequisites.courses_description is not None:
                prereq_contents.append(
                    pl.SubSubSection(self.model.prerequisites.courses_description, title='Courses')
                )
            if self.model.prerequisites.technical_skills_description is not None:
                prereq_contents.append(
                    pl.SubSubSection(self.model.prerequisites.technical_skills_description, title='Technical Skills')
                )
            if self.model.prerequisites.technical_skills:
                prereq_contents.append(self.prereq_list)
            if prereq_contents is not None:
                contents.append(pl.SubSection(prereq_contents, title='Prerequisites'))

        if self.model.class_structure_body is not None:
            contents.append(pl.SubSection(self.model.class_structure_body, title='Class Structure'))

        return pl.Section(contents, title='General Information')

    @property
    def prereq_list(self) -> Optional[pl.UnorderedList]:
        if self.model.prerequisites is None or self.model.prerequisites.technical_skills is None:
            return None

        bullet_items = []
        for i, cat in enumerate(self.model.prerequisites.technical_skills):
            if cat.parents:
                continue
            if not cat.children:
                bullet_items.append(cat.title)
            else:
                child_items = [c.title for c in cat.children]
                bullet_items.extend([cat.title, pl.UnorderedList(child_items)])

        if bullet_items:
            return pl.UnorderedList(bullet_items)

        return None

    @property
    def grade_breakdown_table(self) -> Optional[pl.Tabular]:
        if self.model.grading is None or self.model.grading.breakdown is None:
            return None

        align = 'lc'
        return pl.Tabular(
            [

                pl.TopRule(),
                pl.ValuesTable.from_list_of_lists(
                    [
                        [pl.Bold('Item'), pl.Bold('Grade Percentage')]
                    ]
                ),
                pl.MidRule(),
                pl.ValuesTable.from_list_of_lists(
                    [
                        [category, f'{pct:.0%}'] for category, pct in self.model.grading.breakdown.categories.items()
                    ]
                ),
                pl.BottomRule()

            ],
            align=align
        )

    @property
    def grading_scale_table(self) -> Optional[pl.Tabular]:
        if self.model.grading is None or self.model.grading.scale is None:
            return None

        align = 'lc'
        return pl.Tabular(
            [

                pl.TopRule(),
                pl.ValuesTable.from_list_of_lists(
                    [
                        [pl.Bold('Grade'), pl.Bold('Grade Percentage')]
                    ]
                ),
                pl.MidRule(),
                pl.ValuesTable.from_list_of_lists(
                    [
                        [grade, f'{bot} - {top}%'] for grade, (bot, top) in self.model.grading.scale.grade_ranges.items()
                    ]
                ),
                pl.BottomRule()

            ],
            align=align
        )

    @property
    def grading_section(self) -> pl.Section:
        bd_table = self.grade_breakdown_table
        scale_table = self.grading_scale_table

        contents = []
        if bd_table is not None:
            contents.append(pl.SubSection(pl.Center(bd_table), title='Breakdown'))
        if scale_table is not None:
            contents.append(pl.SubSection(pl.Center(scale_table), title='Grading Scale'))
        if self.model.grading is not None and self.model.grading.extra_info is not None:
            contents.append(self.model.grading.extra_info)

        return pl.Section(contents, title='Grades')

    @property
    def topics_covered_section(self) -> pl.Section:

        topic_sections = []
        if self.model.topics is not None:
            for topic in self.model.topics:
                child_topics = list(topic.children)
                if child_topics:
                    topic_contents = pl.UnorderedList([t.title for t in child_topics])
                else:
                    topic_contents = []
                topic_section = pl.SubSection(topic_contents, title=topic.title)
                topic_sections.append(topic_section)

        contents = [
            'Subject to change but in approximate order.',
            *topic_sections
        ]

        return pl.Section(contents, title='Main Topics Covered')

    @property
    def resources_section(self) -> Optional[pl.Section]:
        if self.model.resources is None:
            return None

        sub_sections = [resource.to_pyexlatex_subsection() for resource in self.model.resources]
        out_sections = []
        for i, section in enumerate(sub_sections):
            out_sections.append(section)
            if i != len(sub_sections) - 1:
                out_sections.append(pl.VSpace())
        return pl.Section(sub_sections, title='Resources')
