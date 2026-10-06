import sys
import os
import re
import requests
from bs4 import BeautifulSoup

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from database import SessionLocal
from models import Role, Question, RoleQuestion, QuestionSource


SOURCE_URL = (
    "https://www.geeksforgeeks.org/"
    "advance-java/introduction-to-advanced-java-interview-questions/"
)

SOURCE_TITLE = (
    "Advanced Java Interview Questions - GeeksforGeeks"
)

ROLE_NAME = "Java Developer"


def fetch_page(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def collect_questions(url):

    html = fetch_page(url)

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    questions = []

    for heading in soup.find_all(
        ["h2", "h3", "h4", "h5"]
    ):

        text = heading.get_text(
            " ",
            strip=True
        )

        if not text:
            continue

        cleaned = re.sub(
            r"^\s*\d+\.\s*",
            "",
            text
        ).strip()

        lower = cleaned.lower()

        if (
            lower.startswith("what ")
            or lower.startswith("why ")
            or lower.startswith("how ")
            or lower.startswith("which ")
            or lower.startswith("when ")
            or lower.startswith("where ")
            or lower.startswith("can ")
            or lower.startswith("is ")
            or lower.startswith("are ")
            or lower.startswith("difference ")
            or lower.startswith("explain ")
            or lower.startswith("define ")
        ):
            questions.append(cleaned)

    return list(
        dict.fromkeys(questions)
    )


def save_questions(questions):

    db = SessionLocal()

    try:

        role = (
            db.query(Role)
            .filter(
                Role.normalized_name
                == ROLE_NAME.lower()
            )
            .first()
        )

        if not role:
            print(
                f"❌ Role not found: {ROLE_NAME}"
            )
            return

        added = 0
        linked = 0
        source_added = 0

        for question_text in questions:

            question = (
                db.query(Question)
                .filter(
                    Question.question_text
                    == question_text
                )
                .first()
            )

            # Create question if it doesn't exist
            if not question:

                question = Question(
                    question_text=question_text,
                    category="Java",
                    frequency_score=1,
                    relevance_score=1,
                    verified=True
                )

                db.add(question)
                db.flush()

                added += 1

            # Connect question with Java Developer
            role_question = (
                db.query(RoleQuestion)
                .filter(
                    RoleQuestion.role_id == role.id,
                    RoleQuestion.question_id
                    == question.id
                )
                .first()
            )

            if not role_question:

                db.add(
                    RoleQuestion(
                        role_id=role.id,
                        question_id=question.id
                    )
                )

                linked += 1

            # Add GFG source evidence
            source_exists = (
                db.query(QuestionSource)
                .filter(
                    QuestionSource.question_id
                    == question.id,
                    QuestionSource.source_url
                    == SOURCE_URL
                )
                .first()
            )

            if not source_exists:

                db.add(
                    QuestionSource(
                        question_id=question.id,
                        source_type="web",
                        source_url=SOURCE_URL,
                        source_title=SOURCE_TITLE
                    )
                )

                source_added += 1

        db.commit()

        print()
        print("✅ GFG questions saved successfully")
        print(
            f"Questions collected: {len(questions)}"
        )
        print(
            f"New questions added: {added}"
        )
        print(
            f"New role links: {linked}"
        )
        print(
            f"New source records: {source_added}"
        )

    except Exception as e:

        db.rollback()

        print()
        print("❌ Database error:")
        print(e)

    finally:

        db.close()


if __name__ == "__main__":

    print(
        "🌐 Collecting and saving GFG questions..."
    )

    try:

        questions = collect_questions(
            SOURCE_URL
        )

        save_questions(questions)

    except Exception as e:

        print()
        print("❌ Collector error:")
        print(e)