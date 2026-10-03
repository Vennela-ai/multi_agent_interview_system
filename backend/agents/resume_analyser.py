import json
from services.llm_service import ask_llm


def analyze_resume(resume_text):

    prompt = f"""
You are a Resume Analyzer Agent in a multi-agent AI interview system.

Analyze the student's resume and extract accurate information.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "candidate": {{
        "name": "",
        "email": "",
        "phone": "",
        "education": [],
        "cgpa": ""
    }},
    "skills": {{
        "technical": [],
        "programming_languages": [],
        "tools_and_technologies": []
    }},
    "experience": [],
    "projects": [],
    "internships": [],
    "certifications": [],
    "achievements": [],
    "strengths": [],
    "skill_gaps": []
}}

Rules:
- Do not invent information.
- If information is not present, use an empty string or empty list.
- Keep project names and technologies accurate.
- Extract only information actually present in the resume.
- Return JSON only. Do not add explanations.

Resume:

{resume_text}
"""

    response = ask_llm(prompt)

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by AI",
            "raw_response": response
        }