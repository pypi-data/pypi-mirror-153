from typing import Optional, Sequence, Union, Any, List
import pyexlatex as pl
import pyexlatex.resume as lr

from derobertis_cv.models.course import CourseModel


class AcademicEmployment(lr.Employment):

    def __init__(self, contents, company_name: str, employed_dates: str, job_title: str, location: str,
                 courses_taught: Optional[Sequence[CourseModel]] = None,
                 extra_contents: Optional[Any] = None):
        if extra_contents is None:
            extra_contents = []

        if courses_taught is not None:
            # TODO [#2]: don't use raw, use latex objects
            taught_bullet_contents = []
            for course in courses_taught:
                from pyexlatex.logic.builder import _build
                # Put each part of course taught on left and right side
                course_contents = [
                    course.name_score_description,
                    pl.Raw(r'\itemsep -0.5em \vspace{-0.5em}'),
                ]
                bullet_contents: List[Union[list, str]] = []
                if course.website_url:
                    bullet_contents.append(['Course Website:', pl.Hyperlink(
                        course.website_url,
                        pl.Bold(
                            pl.TextColor(course.website_url, color=pl.RGB(50, 82, 209, color_name="darkblue"))
                        ),
                    )])
                    bullet_contents.append(pl.Raw(r'\itemsep -0.3em \vspace{-0.3em}'))
                bullet_contents.append('Semesters: ' + course.periods_taught_str)
                course_contents.append(pl.UnorderedList(bullet_contents))
                course_item_str = _build(course_contents)
                taught_bullet_contents.append(course_item_str)
                taught_bullet_contents.append(pl.Raw(r'\itemsep -0.3em \vspace{-0.3em}'))
            del taught_bullet_contents[-1]  # remove spacing after last item
            taught_contents = [
                '',
                pl.Bold('Courses taught:'),
                pl.Raw(r'\itemsep -0.5em \vspace{-0.5em}'),
                pl.UnorderedList(taught_bullet_contents)
            ]
            extra_contents[:0] = taught_contents

        super().__init__(
            contents,
            company_name=company_name,
            employed_dates=employed_dates,
            job_title=job_title,
            location=location,
            extra_contents=extra_contents
        )