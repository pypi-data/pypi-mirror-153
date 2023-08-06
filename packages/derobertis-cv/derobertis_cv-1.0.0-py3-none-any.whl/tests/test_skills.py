from derobertis_cv.pldata.skills import CV_EXCLUDE_SKILLS, get_skills


def test_get_skills_does_not_raise_error():
    for skill in get_skills(
        exclude_skills=CV_EXCLUDE_SKILLS, exclude_skill_children=False
    ):
        assert skill.category is not None
        assert skill.level is not None
        # Parent skills are allowed to not have experience
        if skill.parents:
            # TODO: eliminate specific handling for frameworks skill
            if skill.title.casefold() == "frameworks":
                # Frameworks is allowed to violate these conditions, it has specific logic on the
                # nick-derobertis-site to handle this.
                continue
            is_soft_skill = any(
                [parent.title.casefold() == "soft skills" for parent in skill.parents]
            )
            if is_soft_skill:
                # Soft skills don't need tangible experience
                continue
            is_other_skill = any(
                [parent.title.casefold() == "other" for parent in skill.parents]
            )
            if is_other_skill:
                # Other skills don't need tangible experience
                continue
            assert skill.experience is not None
            assert skill.experience.hours is not None
