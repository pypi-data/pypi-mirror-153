import pyexlatex as pl
import pyexlatex.table as lt
import pyexlatex.presentation as lp
import pyexlatex.graphics as lg
import pyexlatex.layouts as ll
import pyexlatex.resume as lr
from pyexlatex.models.page.number import PageReference

from derobertis_cv import plbuild
from derobertis_cv.plbuild.paths import images_path
from derobertis_cv.pldata.constants.contact import CONTACT_LINES, NAME

AUTHORS = ['Nick DeRobertis']

DOCUMENT_CLASS = pl.Document
OUTPUT_LOCATION = plbuild.paths.DOCUMENTS_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = None

title = 'Teaching Statement'


def get_content():
    return [
"""
The common theme across my courses is a focus on preparing students for introductory finance positions related 
to the course. I try to 
emphasize basic financial and analytic concepts and practical technical skills without cluttering the class with 
specific institutional details. 

Having been through an undergraduate and master's degree in finance prior to the Ph.D., and also having worked in an analyst role, 
I understand that such institutional details will only be useful to those that work in the particular related area, 
while the foundational concepts and technical skills are applicable across a variety of roles. 
This is why I slowly and deliberately build 
from the simplest concepts to more advanced concepts and practical applications. 

I am currently teaching Financial Modeling, but even when I taught Debt and Money Markets, the assignments were 
modeling projects. I believe that finance students should not graduate without understanding basic financial modeling
and a competency in Excel or Python.

Through my experience in teaching and tutoring, I believe there are three main learning types: 
auditory, visual, and kinesthetic, and I try to cater to all three. 

For the auditory learners, I try to use many examples and analogies when speaking about the material. 
The point on the slide gets the main idea across, but I elaborate substantially on each point verbally. 
If it is a live lecture, I also call on students for questions throughout. 

For the visual learners, it starts with the point on the slide. I use a dim and reveal animation on all 
my slides so it's always clear which point I am talking about, and it's easy for the visual learner to 
link what he or she sees on the slide to what I am discussing. Further, I use graphics and graphs 
on the slides as well as the white board, and work problems out in front of students to aid visual learners. 

While some are primarily kinesthetic learners, I believe that this kind of learning in particular is 
important for everyone to participate in. This is why multiple times during each lecture, 
I have in-class questions that I have the students work on. Directly after giving them the auditory and 
visual portion of the learning, students must learn by doing. It is often only after attempting the 
relevant problems that most students have questions about the material. The in-class questions are turned 
in at the end of class for completion, and this serves as a small attendance grade. In addition to catering 
to kinesthetic learners and encouraging students to attend class, I believe that these questions increase 
motivation to learn and help students pay attention by breaking up the lecture.

While some learn best in a lecture situation or by going through material on their own, others require 
one-on-one attention. This is why I am always encouraging my students to come to office hours and 
reach out by email with any questions. I am always happy to help and encourage students to come 
for more help when they need it. Perhaps some students may be intimidated by one-on-one attention, 
but I try to be as approachable as possible. One way I do this is by learning all of my students' names. 
Another is by sharing small personal aspects of my life to promote a less formal atmosphere. 

Some students learn better individually while others learn best in a group. That is why I use a mixture 
of individual and group work my courses.  

I try to teach to differing levels of understanding as well. In every course, some students will feel that 
the material is too slow or simple, while others will feel that it is too fast or complicated. To combat this, 
I build slowly at first and try to emphasize the main ideas repeatedly. The points on the slide represent what 
I would consider an average level of understanding of the material. Then for the fast learners, I speak about 
additional detail on the topics while making it clear that the expanded detail is not covered on the exams 
or projects. 
Often this has started class discussions or some particularly interested students will ask 
me after class for more detail. Further, I also include bonus problems on projects that require outside 
research for the more advanced students.

Overall, I believe that the structure of my course motivates and prepares students for introductory finance
positions regardless of the particular learning style of the student. 
""".strip()
    ]

DOCUMENT_CLASS_KWARGS = dict(
    remove_section_numbering=True,
    title=title,
    page_modifier_str='margin=1in',
    font_size=12,
    apply_page_style_to_section_starts=True,
    custom_footers=[
        pl.LeftFooter(NAME),
        pl.CenterFooter(title),
        pl.RightFooter(
            ['Page', pl.ThisPageNumber(), '\\', 'of', PageReference('LastPage')]
        ),
        pl.FooterLine()
    ]
)
OUTPUT_NAME = title

