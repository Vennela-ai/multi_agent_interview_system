# ============================================
# MAPPING AGENT
# ============================================

def normalize_skill(skill):
    return str(skill).strip().lower()


def get_resume_skills(resume_analysis):

    skills = resume_analysis.get(
        "skills",
        {}
    )

    result = []

    for key in [
        "technical",
        "programming_languages",
        "tools_and_technologies"
    ]:

        result.extend(
            skills.get(key, [])
        )

    return {
        normalize_skill(skill)
        for skill in result
        if skill
    }


def get_jd_skills(jd_analysis):

    skills = jd_analysis.get(
        "skills",
        {}
    )

    required = skills.get(
        "required",
        []
    )

    preferred = skills.get(
        "preferred",
        []
    )

    programming_languages = skills.get(
        "programming_languages",
        []
    )

    tools = skills.get(
        "tools_and_technologies",
        []
    )

    return {
        "required": {
            normalize_skill(skill)
            for skill in required
            if skill
        },

        "preferred": {
            normalize_skill(skill)
            for skill in preferred
            if skill
        },

        "programming_languages": {
            normalize_skill(skill)
            for skill in programming_languages
            if skill
        },

        "tools_and_technologies": {
            normalize_skill(skill)
            for skill in tools
            if skill
        }
    }


def calculate_mapping(
    resume_analysis,
    jd_analysis
):

    resume_skills = get_resume_skills(
        resume_analysis
    )

    jd_skills = get_jd_skills(
        jd_analysis
    )

    # --------------------------------------------
    # Combine required JD skills
    # --------------------------------------------

    required_skills = (
        jd_skills["required"]
        | jd_skills["programming_languages"]
        | jd_skills["tools_and_technologies"]
    )

    preferred_skills = jd_skills[
        "preferred"
    ]

    # --------------------------------------------
    # Required skill matching
    # --------------------------------------------

    matched_required = (
        resume_skills
        & required_skills
    )

    missing_required = (
        required_skills
        - resume_skills
    )

    # --------------------------------------------
    # Preferred skill matching
    # --------------------------------------------

    matched_preferred = (
        resume_skills
        & preferred_skills
    )

    # --------------------------------------------
    # Calculate percentage
    # --------------------------------------------

    if required_skills:

        required_percentage = (
            len(matched_required)
            / len(required_skills)
        ) * 80

    else:

        required_percentage = 80

    if preferred_skills:

        preferred_percentage = (
            len(matched_preferred)
            / len(preferred_skills)
        ) * 20

    else:

        preferred_percentage = 20

    match_percentage = (
        required_percentage
        + preferred_percentage
    )

    match_percentage = round(
        match_percentage,
        2
    )

    # --------------------------------------------
    # Decision
    # --------------------------------------------

    tailored_resume_required = (
        match_percentage < 85
    )

    return {

        "match_percentage":
            match_percentage,

        "matched_required_skills":
            sorted(matched_required),

        "missing_required_skills":
            sorted(missing_required),

        "matched_preferred_skills":
            sorted(matched_preferred),

        "tailored_resume_required":
            tailored_resume_required,

        "decision":
            (
                "Generate Tailored Resume"
                if tailored_resume_required
                else
                "Keep Current Resume"
            )
    }