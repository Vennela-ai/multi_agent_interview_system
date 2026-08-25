import json
from backend.services.llm_service import ask_llm


def analyze_job_description(job_description):
    prompt = f"""
You are a Job Description Analyzer Agent in a multi-agent AI interview system.

Analyze the given job description and extract accurate information.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "job": {{
        "job_title": "",
        "company": "",
        "location": "",
        "experience_required": ""
    }},
    "skills": {{
        "required": [],
        "preferred": [],
        "programming_languages": [],
        "tools_and_technologies": []
    }},
    "education_requirements": [],
    "responsibilities": [],
    "qualifications": [],
    "certifications": [],
    "domain_knowledge": [],
    "keywords": []
}}

Rules:
- Do not invent information.
- If information is not present, use an empty string or empty list.
- Keep skill and technology names accurate.
- Clearly distinguish required skills from preferred skills.
- Extract only information actually present in the job description.
- Do not add explanations.
- Return JSON only.

Job Description:
{job_description}
"""

    response = ask_llm(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by AI",
            "raw_response": response
        }