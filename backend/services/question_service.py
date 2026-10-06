from sqlalchemy.orm import Session

from models import Question, Role, RoleQuestion
from services.question_retriever import retrieve_questions_for_role


BATCH_SIZE = 100
MAX_QUESTIONS = 500


def get_questions_by_role(
    db: Session,
    role_name: str,
    offset: int = 0
):
    """
    Generic interview-question service.

    Works for every configured role.

    First request:
        offset=0   -> 1-100

    Second request:
        offset=100 -> 101-200

    Third request:
        offset=200 -> 201-300

    Maximum:
        500 questions

    Interview questions are collected from public sources.
    No AI-generated interview questions are used.
    """

    if offset < 0:
        offset = 0

    if offset >= MAX_QUESTIONS:
        return {
            "success": True,
            "role": role_name,
            "offset": offset,
            "batch_size": BATCH_SIZE,
            "available_questions": 0,
            "returned_questions": 0,
            "next_offset": None,
            "has_more": False,
            "questions": []
        }

    normalized_role = role_name.strip().lower()

    role = (
        db.query(Role)
        .filter(
            Role.normalized_name == normalized_role
        )
        .first()
    )

    if not role:
        return {
            "success": False,
            "message": f"Role not found: {role_name}",
            "role": role_name,
            "offset": offset,
            "batch_size": BATCH_SIZE,
            "available_questions": 0,
            "returned_questions": 0,
            "next_offset": None,
            "has_more": False,
            "questions": []
        }

    # --------------------------------------------------
    # Count questions currently available for this role
    # --------------------------------------------------

    def get_total_questions():
        return (
            db.query(Question)
            .join(
                RoleQuestion,
                Question.id == RoleQuestion.question_id
            )
            .filter(
                RoleQuestion.role_id == role.id,
                Question.verified == True
            )
            .count()
        )

    total_available = get_total_questions()

    # --------------------------------------------------
    # Make sure enough questions exist for requested batch
    # --------------------------------------------------

    required_questions = min(
        offset + BATCH_SIZE,
        MAX_QUESTIONS
    )

    if total_available < required_questions:

        try:

            retrieve_questions_for_role(
                db=db,
                role_name=role.name,
                required_count=required_questions
            )

            db.commit()

        except Exception as e:

            db.rollback()

            return {
                "success": False,
                "message": (
                    f"Question retrieval failed: {str(e)}"
                ),
                "role": role.name,
                "offset": offset,
                "batch_size": BATCH_SIZE,
                "available_questions": total_available,
                "returned_questions": 0,
                "next_offset": None,
                "has_more": False,
                "questions": []
            }

        total_available = get_total_questions()

    # --------------------------------------------------
    # Never expose more than 500
    # --------------------------------------------------

    usable_total = min(
        total_available,
        MAX_QUESTIONS
    )

    # --------------------------------------------------
    # Fetch requested batch
    # --------------------------------------------------

    query = (
        db.query(Question)
        .join(
            RoleQuestion,
            Question.id == RoleQuestion.question_id
        )
        .filter(
            RoleQuestion.role_id == role.id,
            Question.verified == True
        )
        .order_by(
            Question.frequency_score.desc(),
            Question.relevance_score.desc(),
            Question.id.asc()
        )
    )

    questions = (
        query
        .offset(offset)
        .limit(BATCH_SIZE)
        .all()
    )

    next_offset = offset + len(questions)
    has_more = next_offset < usable_total
    return {
        "success": True,
        "role": role.name,
        "offset": offset,
        "batch_size": BATCH_SIZE,
        "available_questions": usable_total,
        "returned_questions": len(questions),
        "next_offset": (
            next_offset
            if has_more
            else None
        ),
        "has_more": has_more,
        "questions": [
            {
                "id": question.id,
                "question": question.question_text,
                "category": question.category
            }
            for question in questions
        ]
    }