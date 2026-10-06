import json
from services.llm_service import ask_llm


def generate_personalized_questions(
    resume_analysis,
    jd_analysis,
    retrieved_questions
):
    """
    Generate personalized interview questions using:

    1. Resume analysis
    2. Job description analysis
    3. Retrieved interview questions
    """

    prompt = f"""
You are a Question Generator Agent in a
multi-agent AI interview system.

Your task is to generate personalized interview
questions for a candidate based on their resume,
the job description, and retrieved interview
questions.

========================
RESUME ANALYSIS
========================

{json.dumps(resume_analysis, indent=2)}

========================
JOB DESCRIPTION ANALYSIS
========================

{json.dumps(jd_analysis, indent=2)}

========================
RETRIEVED QUESTIONS
========================

{json.dumps(retrieved_questions, indent=2)}

========================
REQUIREMENTS
========================

Generate exactly 10 interview questions.

Follow these rules:

1. Questions must be relevant to the candidate's
   resume and the job description.

2. Use the retrieved questions as a knowledge source.

3. Do not copy all retrieved questions blindly.
   Adapt them when necessary.

4. Do not invent skills, projects, internships,
   certifications, or experience.

5. Give higher priority to skills that appear in
   both the resume and job description.

6. Include technical questions relevant to the
   required skills.

7. Include questions related to the candidate's
   projects or internships when those are present.

8. Include a small number of behavioral questions
   where appropriate.

9. Questions should have different difficulty levels.

10. Return ONLY valid JSON.

Use exactly this format:

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
"""

    response = ask_llm(prompt)

    try:
        return json.loads(response)

    except json.JSONDecodeError:

        return {
            "error": "Invalid JSON returned by AI",
            "raw_response": response
        }