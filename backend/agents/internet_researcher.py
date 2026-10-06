import os
import json
from dotenv import load_dotenv
from tavily import TavilyClient

from services.llm_service import ask_llm


load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env")


tavily_client = TavilyClient(
    api_key=TAVILY_API_KEY
)


# =========================================================
# GENERATE SEARCH QUERIES
# =========================================================

def generate_search_queries(role, skills):

    skill_text = ", ".join(skills)

    return [
        f"{role} interview questions",
        f"{role} technical interview questions",
        f"{role} coding interview questions",
        f"{role} scenario based interview questions",
        f"{role} interview preparation {skill_text}",
        f"{role} important interview topics {skill_text}"
    ]


# =========================================================
# SEARCH WEB
# =========================================================

def search_web(query, max_results=5):

    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_answer=False
    )

    return response.get("results", [])


# =========================================================
# EXTRACT QUESTIONS FROM SOURCES
# =========================================================

def extract_questions_from_sources(
    role,
    skills,
    sources
):

    research_text = ""

    for index, source in enumerate(
        sources,
        start=1
    ):

        content = source.get(
            "content",
            ""
        )

        content = content[:6000]

        research_text += f"""
SOURCE {index}

TITLE:
{source.get("title", "")}

URL:
{source.get("url", "")}

CONTENT:
{content}

==================================================
"""


    prompt = f"""
You are an Internet Research Agent for an AI
interview preparation system.

TARGET ROLE:
{role}

TARGET SKILLS:
{json.dumps(skills)}

Extract interview questions from the provided
web research.

RULES:

1. Only create questions supported by the research.
2. Questions must be relevant to the target role.
3. Include technical questions.
4. Include coding questions when available.
5. Include scenario-based questions when available.
6. Remove duplicate questions.
7. Do not invent candidate experience.
8. Preserve the original source for every question.
9. Return ONLY valid JSON.
10. Do not use markdown.
11. Do not add explanations.

Return exactly:

{{
    "questions": [
        {{
            "question": "question text",
            "category": "category",
            "difficulty": "Easy/Medium/Hard",
            "source": {{
                "name": "website name",
                "url": "source url"
            }}
        }}
    ]
}}

WEB RESEARCH:

{research_text}
"""


    try:

        response = ask_llm(prompt)

        print(
            "\n========== GROQ RESPONSE ==========\n"
        )

        print(response)

        response = response.strip()


        # -------------------------------------------------
        # REMOVE MARKDOWN CODE FENCES
        # -------------------------------------------------

        if response.startswith("```"):

            response = response.replace(
                "```json",
                ""
            )

            response = response.replace(
                "```",
                ""
            )

            response = response.strip()


        # -------------------------------------------------
        # NORMAL JSON PARSING
        # -------------------------------------------------

        try:

            parsed = json.loads(response)

            return parsed.get(
                "questions",
                []
            )


        except json.JSONDecodeError:

            print(
                "\nJSON parsing failed."
            )

            print(
                "Trying JSON recovery..."
            )


            # -------------------------------------------------
            # JSON RECOVERY
            # -------------------------------------------------

            start = response.find("{")

            end = response.rfind("}")


            if start != -1 and end != -1:

                cleaned_response = response[
                    start:end + 1
                ]


                try:

                    parsed = json.loads(
                        cleaned_response
                    )

                    return parsed.get(
                        "questions",
                        []
                    )


                except json.JSONDecodeError as recovery_error:

                    print(
                        "\nJSON recovery failed:"
                    )

                    print(
                        recovery_error
                    )


            return []


    except Exception as e:

        print(
            "\nQuestion extraction failed:"
        )

        print(e)

        return []


# =========================================================
# MAIN INTERNET RESEARCH AGENT
# =========================================================

def research_interview_questions(
    role,
    skills,
    max_sources=30
):

    queries = generate_search_queries(
        role,
        skills
    )


    discovered_sources = []

    seen_urls = set()


    # =====================================================
    # STEP 1 — DYNAMIC WEB SEARCH
    # =====================================================

    for query in queries:

        print(
            f"\nSearching: {query}"
        )


        try:

            results = search_web(
                query,
                max_results=5
            )


            for result in results:

                url = result.get(
                    "url",
                    ""
                ).strip()


                if not url:
                    continue


                if url in seen_urls:
                    continue


                seen_urls.add(url)


                discovered_sources.append({

                    "title": result.get(
                        "title",
                        ""
                    ),

                    "url": url,

                    "content": result.get(
                        "content",
                        ""
                    ),

                    "score": result.get(
                        "score",
                        0
                    )
                })


                if len(discovered_sources) >= max_sources:

                    break


        except Exception as e:

            print(
                f"Search failed for '{query}': {e}"
            )


        if len(discovered_sources) >= max_sources:

            break


    print(
        f"\nTotal unique sources discovered: "
        f"{len(discovered_sources)}"
    )


    # =====================================================
    # STEP 2 — PROCESS SOURCES IN BATCHES
    # =====================================================

    all_questions = []

    batch_size = 3


    for i in range(
        0,
        len(discovered_sources),
        batch_size
    ):

        batch = discovered_sources[
            i:i + batch_size
        ]


        print(
            f"\nProcessing sources "
            f"{i + 1} - "
            f"{i + len(batch)}"
        )


        questions = extract_questions_from_sources(
            role,
            skills,
            batch
        )


        all_questions.extend(
            questions
        )


    # =====================================================
    # STEP 3 — REMOVE DUPLICATES
    # =====================================================

    unique_questions = []

    seen_questions = set()


    for item in all_questions:

        if not isinstance(
            item,
            dict
        ):
            continue


        question = item.get(
            "question",
            ""
        ).strip()


        if not question:
            continue


        normalized = (
            question
            .lower()
            .replace("?", "")
            .strip()
        )


        if normalized in seen_questions:

            continue


        seen_questions.add(
            normalized
        )


        unique_questions.append(
            item
        )


    # =====================================================
    # STEP 4 — FINAL RESULT
    # =====================================================

    return {

        "role": role,

        "sources": [

            {
                "title": source["title"],
                "url": source["url"]
            }

            for source in discovered_sources

        ],

        "question_count":
            len(unique_questions),

        "questions":
            unique_questions
    }