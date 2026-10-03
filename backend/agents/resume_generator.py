import json
from services.llm_service import ask_llm


def generate_tailored_resume(resume_analysis, jd_analysis):

    # Make sure important resume information is available
    # to the LLM even if it is stored in different locations.

    candidate = resume_analysis.get("candidate", {})

    education = (
        candidate.get("education")
        or resume_analysis.get("education")
        or []
    )

    location = (
        candidate.get("location")
        or resume_analysis.get("location")
        or "Eluru, Andhra Pradesh"
    )

    # Create a clean copy containing the complete candidate data
    resume_data = dict(resume_analysis)

    resume_data["candidate"] = dict(candidate)

    resume_data["candidate"]["education"] = education
    resume_data["candidate"]["location"] = location

    prompt = f"""
You are an AI Resume Tailoring Agent.

Your task is to create a professional, ATS-friendly resume
tailored to the target job description.

You have two inputs:

1. The candidate's existing resume analysis
2. The target job description analysis

STRICT FACTUAL ACCURACY RULES:

- Use ONLY information explicitly present in the candidate resume analysis.
- NEVER invent information.
- NEVER add a skill that is only mentioned in the JD.
- NEVER claim experience with a technology unless the candidate's resume explicitly contains it.
- NEVER add companies.
- NEVER add job titles.
- NEVER add projects.
- NEVER add certifications.
- NEVER add achievements.
- NEVER add education.
- NEVER add responsibilities that are not supported by the original resume.
- NEVER add teamwork, collaboration, leadership, deployment, API development,
  database implementation, or similar claims unless explicitly supported.
- Do NOT strengthen the candidate's experience.

IMPORTANT:
You may improve grammar and professional wording, but the meaning and
level of experience MUST remain exactly the same.

For example:

Original:
"Explored front-end and back-end integration, REST APIs, and database connectivity."

Allowed:
"Explored front-end and back-end integration, REST APIs, and database connectivity."

Allowed:
"Gained exposure to front-end and back-end integration, REST APIs,
and database connectivity."

NOT allowed:
"Developed RESTful APIs and implemented database connectivity."

Another example:

Original:
"Developed responsive web pages using HTML and CSS."

Allowed:
"Developed responsive web pages using HTML and CSS."

NOT allowed:
"Collaborated with senior developers to develop responsive web pages."

JD tailoring rules:

- Prioritize skills that are relevant to the target JD.
- Prioritize projects relevant to the target JD.
- Prioritize relevant internships.
- You may reorder skills, projects, and internships based on relevance.
- You may rewrite wording for ATS relevance only when the rewritten wording
  remains factually equivalent.
- If a JD mentions React but React is not present in the resume,
  DO NOT add React.
- If a JD mentions Node.js but Node.js is not present in the resume,
  DO NOT add Node.js.
- If JavaScript is present in a project, it may be mentioned only where
  the original project information supports it.
- Preserve all factual education information from the resume.
- Preserve all factual certifications.
- Preserve all factual achievements.

Create a concise professional summary based ONLY on the candidate's
actual resume information.

Return ONLY valid JSON.
Do not return markdown.
Do not return ```json.
Do not include explanations outside the JSON.

CANDIDATE RESUME ANALYSIS:

{json.dumps(resume_analysis, indent=2, ensure_ascii=False)}


TARGET JOB DESCRIPTION:

{json.dumps(jd_analysis, indent=2, ensure_ascii=False)}


Return EXACTLY this structure:

{{
    "candidate": {{
        "name": "",
        "email": "",
        "phone": "",
        "location": ""
    }},

    "summary": "",

    "skills": {{
        "technical": [],
        "programming_languages": [],
        "tools_and_technologies": []
    }},

    "education": [],

    "projects": [
        {{
            "name": "",
            "technologies": [],
            "description": ""
        }}
    ],

    "experience": [],

    "internships": [
        {{
            "title": "",
            "company": "",
            "duration": "",
            "description": ""
        }}
    ],

    "certifications": [],

    "achievements": []
}}

IMPORTANT FINAL CHECK:

Before returning the JSON, verify:

1. Every skill exists in the candidate resume.
2. Every project exists in the candidate resume.
3. Every internship exists in the candidate resume.
4. Every certification exists in the candidate resume.
5. Every achievement exists in the candidate resume.
6. Education is copied from the candidate resume.
7. No React or Node.js is added unless present in the candidate resume.
8. No new responsibilities or experience are invented.
9. No wording makes the candidate appear more experienced than the source resume.
"""

    result = ask_llm(prompt)

    result = result.strip()

    if result.startswith("```json"):
        result = result[7:]

    if result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    result = result.strip()

    return json.loads(result)