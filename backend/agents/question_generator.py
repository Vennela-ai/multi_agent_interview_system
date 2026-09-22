import json

from backend.services.llm_service import ask_llm


def generate_questions(resume_analysis, jd_analysis):

    prompt = f"""
You are a Question Generator Agent in a multi-agent AI interview system.

Your task is to generate interview questions using ONLY:
1. The candidate's resume analysis
2. The job description analysis

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
- Generate exactly 10 questions.
- Do not invent information about the candidate.
- Questions must be based on the candidate's actual resume information.
- Questions must also relate to the job description.
- Include technical questions.
- Include project-based questions.
- Include questions about the candidate's skills.
- Include questions related to required job skills.
- Use these difficulty levels only: Easy, Medium, Hard.
- Keep questions clear and suitable for an interview.
- Return JSON only.
- Do not add markdown.
- Do not add explanations outside the JSON.

Resume Analysis:
{json.dumps(resume_analysis, indent=2)}

Job Description Analysis:
{json.dumps(jd_analysis, indent=2)}
"""

    response = ask_llm(prompt)

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by AI",
            "raw_response": response
        }