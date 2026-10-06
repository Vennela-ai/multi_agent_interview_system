import json
from tavily import TavilyClient
from services.llm_service import ask_llm
import os


# ============================================
# PROJECT AGENT
# ============================================

def generate_project_queries(role, skills):

    skill_text = ", ".join(skills)

    return [
        f"{role} industry level projects using {skill_text}",
        f"{role} advanced real world project ideas using {skill_text}",
        f"{role} production level project architecture {skill_text}",
        f"{role} advanced project tutorial {skill_text} YouTube",
        f"{role} real world project implementation {skill_text}"
    ]


def search_project_sources(role, skills, max_results=10):

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in .env")

    client = TavilyClient(api_key=api_key)

    queries = generate_project_queries(
        role,
        skills
    )

    sources = []

    for query in queries:

        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results
        )

        for result in response.get("results", []):

            sources.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", "")
            })

    # Remove duplicate URLs
    unique_sources = []
    seen_urls = set()

    for source in sources:

        url = source.get("url")

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)
        unique_sources.append(source)

    return unique_sources


def generate_project_recommendation(
    role,
    resume_analysis,
    jd_analysis,
    sources
):

    prompt = f"""
You are a Project Recommendation Agent in a
multi-agent career preparation system.

Your task is to recommend a project for a candidate
based on their resume and target job description.

IMPORTANT:
- Recommend a NEW project that the candidate can build.
- Do NOT claim that the candidate has already completed it.
- Do NOT add the project to their experience as completed work.
- The project may have industry-level / 3+ years complexity.
- "3+ years complexity" refers ONLY to project complexity.
- It does NOT mean the candidate has 3+ years of experience.
- Use only technologies relevant to the role and JD.
- Use the internet research sources provided below.
- Include useful website and YouTube sources when available.
- Do not invent URLs.

========================
TARGET ROLE
========================
{role}

========================
RESUME
========================
{json.dumps(resume_analysis, indent=2)}

========================
JOB DESCRIPTION
========================
{json.dumps(jd_analysis, indent=2)}

========================
INTERNET SOURCES
========================
{json.dumps(sources, indent=2)}

========================
REQUIREMENTS
========================

Recommend exactly 1 project.

The project must:

1. Be strongly relevant to the target role.
2. Address missing or important JD skills where possible.
3. Have realistic industry-level complexity.
4. Be suitable for a student to implement.
5. Clearly explain what the project does.
6. Explain why it is relevant to the target job.
7. List recommended technologies.
8. Provide useful source links.
9. Never claim that the candidate already completed this project.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "projects": [
        {{
            "title": "",
            "role": "",
            "experience_level": "Industry-level / 3+ years complexity",
            "technologies": [],
            "summary": "",
            "why_relevant": [],
            "sources": [
                {{
                    "type": "website",
                    "title": "",
                    "url": ""
                }}
            ]
        }}
    ]
}}
"""

    response = ask_llm(prompt)

    response = response.strip()

    if response.startswith("```json"):
        response = response[7:]

    if response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    return json.loads(response)


def recommend_project(
    role,
    resume_analysis,
    jd_analysis
):

    # -----------------------------------------
    # Extract JD skills
    # -----------------------------------------

    jd_skills = jd_analysis.get(
        "skills",
        {}
    )

    skills = []

    for key in [
        "required",
        "preferred",
        "programming_languages",
        "tools_and_technologies"
    ]:

        for skill in jd_skills.get(key, []):

            if skill and skill not in skills:
                skills.append(skill)

    # -----------------------------------------
    # Internet Research
    # -----------------------------------------

    sources = search_project_sources(
        role=role,
        skills=skills,
        max_results=5
    )

    # -----------------------------------------
    # Generate Project Recommendation
    # -----------------------------------------

    result = generate_project_recommendation(
        role=role,
        resume_analysis=resume_analysis,
        jd_analysis=jd_analysis,
        sources=sources
    )

    return result