import json

from backend.services.llm_service import ask_llm


def generate_questions(resume_analysis, jd_analysis):

    prompt = f"""
You are a Question Generator Agent in a multi-agent AI interview system.

Generate interview questions based ONLY on the candidate's resume analysis
and the job description analysis.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "questions": [
        {{
            "question": "",
            "category": "",
            "difficulty": "",
            "reason": ""
        }}
    ]
}}

Rules:
- Do not invent candidate experience.
- Questions must be relevant to the resume and job description.
- Include technical questions.
- Include project-based questions where appropriate.
- Include questions related to the job requirements.
- Keep questions clear and interview-ready.
- Return JSON only.
- Generate 10 questions.

Resume Analysis:
{json.dumps(resume_analysis)}

Job Description Analysis:
{json.dumps(jd_analysis)}
"""

    response = ask_llm(prompt)

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by AI",
            "raw_response": response
        }