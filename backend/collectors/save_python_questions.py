import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from database import SessionLocal
from models import (
    Role,
    Question,
    RoleQuestion,
    QuestionSource
)

from python_question_collector import (
    collect_questions,
    SOURCE_URL,
    SOURCE_TYPE,
    SOURCE_TITLE
)

# ==========================================
# DATABASE SESSION
# ==========================================

db = SessionLocal()


try:

    # ==========================================
    # GET PYTHON DEVELOPER ROLE
    # ==========================================

    role = (
        db.query(Role)
        .filter(
            Role.normalized_name == "python developer"
        )
        .first()
    )


    if not role:

        print(
            "ERROR: Python Developer role not found."
        )

        raise SystemExit


    print(
        f"Role found: {role.name}"
    )


    # ==========================================
    # COLLECT QUESTIONS
    # ==========================================

    questions = collect_questions()


    print(
        f"Questions collected: {len(questions)}"
    )


    new_questions = 0
    existing_questions = 0
    new_role_links = 0
    new_sources = 0


    # ==========================================
    # SAVE QUESTIONS
    # ==========================================

    for question_text in questions:


        # --------------------------------------
        # CHECK WHETHER QUESTION ALREADY EXISTS
        # --------------------------------------

        question = (
            db.query(Question)
            .filter(
                Question.question_text
                == question_text
            )
            .first()
        )


        # --------------------------------------
        # CREATE QUESTION IF NEW
        # --------------------------------------

        if not question:

            question = Question(
                question_text=question_text,
                category="Python",
                frequency_score=1,
                relevance_score=1,
                verified=True
            )

            db.add(question)

            db.flush()

            new_questions += 1

        else:

            existing_questions += 1


        # --------------------------------------
        # LINK QUESTION TO PYTHON DEVELOPER
        # --------------------------------------

        role_link = (
            db.query(RoleQuestion)
            .filter(
                RoleQuestion.role_id == role.id,
                RoleQuestion.question_id == question.id
            )
            .first()
        )


        if not role_link:

            role_link = RoleQuestion(
                role_id=role.id,
                question_id=question.id
            )

            db.add(role_link)

            new_role_links += 1


        # --------------------------------------
        # CHECK SOURCE
        # --------------------------------------

        source = (
            db.query(QuestionSource)
            .filter(
                QuestionSource.question_id
                == question.id,
                QuestionSource.source_url
                == SOURCE_URL
            )
            .first()
        )


        if not source:

            source = QuestionSource(
                question_id=question.id,
                source_type=SOURCE_TYPE,
                source_url=SOURCE_URL,
                source_title=SOURCE_TITLE
            )

            db.add(source)

            new_sources += 1


    # ==========================================
    # SAVE CHANGES
    # ==========================================

    db.commit()


    # ==========================================
    # FINAL RESULT
    # ==========================================

    print("\n==========================================")

    print("Python question import completed.")

    print("==========================================")

    print(
        f"New questions: {new_questions}"
    )

    print(
        f"Existing questions: {existing_questions}"
    )

    print(
        f"New role links: {new_role_links}"
    )

    print(
        f"New source records: {new_sources}"
    )

    print("==========================================")


finally:

    db.close()