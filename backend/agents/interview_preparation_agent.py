import json
from services.llm_service import ask_llm


def clean_json_response(response):
    response = response.strip()

    if response.startswith("```json"):
        response = response[7:]

    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    return response.strip()


def generate_question_batch(
    role,
    resume_analysis,
    jd_analysis,
    research_result,
    existing_questions,
    batch_size=10
):
    prompt = f"""
Generate exactly {batch_size} unique interview questions for the role:

{role}

Candidate skills:
{json.dumps(resume_analysis.get("skills", {}))}

Job requirements:
{json.dumps(jd_analysis.get("skills", {}))}

Research information:
{json.dumps(research_result)}

Existing questions that MUST NOT be repeated:
{json.dumps(existing_questions[-100:])}

Requirements:

1. Generate exactly {batch_size} questions.
2. Questions must be relevant to the role.
3. Use the candidate skills and job requirements.
4. Mix technical, coding, conceptual and practical questions.
5. Do NOT include difficulty.
6. Do NOT include answers.
7. Do NOT repeat existing questions.
8. Do not invent candidate experience.
9. Return ONLY valid JSON.

Use exactly this format:

{{
    "questions": [
        {{
            "question": "Question text",
            "category": "Python",
            "source": {{
                "name": "Generated",
                "url": ""
            }}
        }}
    ]
}}
"""

    print(f"Generating {batch_size} questions...")

    response = ask_llm(prompt)

    print("Groq response received.")

    response = clean_json_response(response)

    result = json.loads(response)

    questions = result.get("questions", [])

    return questions


def generate_500_questions(
    role,
    resume_analysis,
    jd_analysis,
    research_result
):
    """
    Generate up to 500 questions.

    Questions are generated in batches of 10.
    """

    all_questions = []
    seen_questions = set()

    batch_size = 10
    max_questions = 500

    while len(all_questions) < max_questions:

        remaining = max_questions - len(all_questions)

        current_batch_size = min(batch_size, remaining)

        existing_questions = [
            item["question"]
            for item in all_questions
        ]

        questions = generate_question_batch(
            role=role,
            resume_analysis=resume_analysis,
            jd_analysis=jd_analysis,
            research_result=research_result,
            existing_questions=existing_questions,
            batch_size=current_batch_size
        )

        if not questions:
            print("No questions returned.")
            break

        new_questions = 0

        for item in questions:

            question_text = str(
                item.get("question", "")
            ).strip()

            if not question_text:
                continue

            normalized = question_text.lower()

            if normalized in seen_questions:
                continue

            seen_questions.add(normalized)

            all_questions.append({
                "question": question_text,
                "category": item.get(
                    "category",
                    "General"
                ),
                "source": {
                    "name": item.get(
                        "source",
                        {}
                    ).get(
                        "name",
                        "Generated"
                    ),
                    "url": item.get(
                        "source",
                        {}
                    ).get(
                        "url",
                        ""
                    )
                }
            })

            new_questions += 1

            if len(all_questions) >= max_questions:
                break

        print(
            f"Total unique questions: "
            f"{len(all_questions)}"
        )

        if new_questions == 0:
            print(
                "No new unique questions generated."
            )
            break

    return {
        "role": role,
        "question_count": len(all_questions),
        "questions": all_questions
    }