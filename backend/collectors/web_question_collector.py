import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import re
import requests
from bs4 import BeautifulSoup

from database import SessionLocal
from models import Role, Question, RoleQuestion, QuestionSource


SOURCE_URL = "https://www.interviewbit.com/java-interview-questions/"
SOURCE_TITLE = "Java Interview Questions"
ROLE_NAME = "Java Developer"


def fetch_page(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
        allow_redirects=True
    )

    print("Requested URL:", url)
    print("Final URL:", response.url)
    print("Status:", response.status_code)

    response.raise_for_status()

    return response.text


def collect_questions(url):

    html = fetch_page(url)

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    questions = []

    headings = soup.find_all(
        ["h2", "h3", "h4", "h5"]
    )

    for heading in headings:

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

        ignored = [
            "download interview guide pdf",
            "download pdf",
            "learn via our video courses",
            "java interview questions",
            "java interview questions for freshers",
            "java intermediate interview questions",
            "java advanced interview questions"
        ]

        if lower in ignored:
            continue

        if (
            cleaned.endswith("?")
            or lower.startswith("why ")
            or lower.startswith("what ")
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
            or lower.startswith("comment ")
            or lower.startswith("identify ")
        ):
            questions.append(cleaned)

    questions = list(
        dict.fromkeys(questions)
    )

    return questions


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
        sources_added = 0

        for question_text in questions:

            question = (
                db.query(Question)
                .filter(
                    Question.question_text
                    == question_text
                )
                .first()
            )

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

                sources_added += 1

        db.commit()

        print()
        print("✅ Collection completed")
        print(
            f"Questions found: {len(questions)}"
        )
        print(
            f"New questions added: {added}"
        )
        print(
            f"New role links: {linked}"
        )
        print(
            f"New sources added: {sources_added}"
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
        "🌐 Collecting Java interview questions..."
    )

    try:

        questions = collect_questions(
            SOURCE_URL
        )

        print()
        print(
            f"Found {len(questions)} candidate questions."
        )

        print()
        print("First 20 questions:")

        for i, question in enumerate(
            questions[:20],
            start=1
        ):
            print(
                f"{i}. {question}"
            )

        save_questions(questions)

    except Exception as e:

        print()
        print("❌ Collector error:")
        print(e)