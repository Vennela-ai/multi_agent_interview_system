from database import SessionLocal
from models import Role, Question, RoleQuestion, QuestionSource


JAVA_QUESTIONS = [
    {
        "question": "Why is Java a platform-independent language?",
        "category": "Java Fundamentals",
        "source_url": "https://www.interviewbit.com/java-interview-questions/",
        "source_title": "Java Interview Questions",
    },
    {
        "question": "Why is Java not a pure object-oriented language?",
        "category": "Java Fundamentals",
        "source_url": "https://www.interviewbit.com/java-interview-questions/",
        "source_title": "Java Interview Questions",
    },
    {
        "question": "What is data encapsulation in Java?",
        "category": "OOP",
        "source_url": "https://www.interviewbit.com/java-interview-questions/",
        "source_title": "Java Interview Questions",
    },
    {
        "question": "Why are strings immutable in Java?",
        "category": "Strings",
        "source_url": "https://www.interviewbit.com/java-interview-questions/",
        "source_title": "Java Interview Questions",
    },
    {
        "question": "What is the difference between String, StringBuffer and StringBuilder?",
        "category": "Strings",
        "source_url": "https://www.interviewbit.com/java-interview-questions/",
        "source_title": "Java Interview Questions",
    },
    {
        "question": "What is a singleton class in Java?",
        "category": "OOP",
        "source_url": "https://www.interviewbit.com/java-interview-questions/",
        "source_title": "Java Interview Questions",
    },
    {
        "question": "What is the difference between HashMap and Hashtable in Java?",
        "category": "Collections",
        "source_url": "https://www.interviewbit.com/java-interview-questions/",
        "source_title": "Java Interview Questions",
    },
    {
        "question": "What is the difference between >> and >>> operators in Java?",
        "category": "Java Fundamentals",
        "source_url": "https://www.interviewbit.com/java-interview-questions/",
        "source_title": "Java Interview Questions",
    },
    {
        "question": "What are lambda expressions in Java?",
        "category": "Java 8",
        "source_url": "https://www.interviewbit.com/java-8-interview-questions/",
        "source_title": "Java 8 Interview Questions",
    },
    {
        "question": "What are Java Streams?",
        "category": "Java 8",
        "source_url": "https://www.interviewbit.com/java-8-interview-questions/",
        "source_title": "Java 8 Interview Questions",
    },
]


db = SessionLocal()

try:
    role = (
        db.query(Role)
        .filter(Role.normalized_name == "java developer")
        .first()
    )

    if not role:
        print("❌ Java Developer role not found.")
        raise SystemExit

    for item in JAVA_QUESTIONS:

        question = (
            db.query(Question)
            .filter(
                Question.question_text == item["question"]
            )
            .first()
        )

        if not question:
            question = Question(
                question_text=item["question"],
                category=item["category"],
                frequency_score=1,
                relevance_score=1,
                verified=True
            )

            db.add(question)
            db.flush()

        role_question = (
            db.query(RoleQuestion)
            .filter(
                RoleQuestion.role_id == role.id,
                RoleQuestion.question_id == question.id
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

        source_exists = (
            db.query(QuestionSource)
            .filter(
                QuestionSource.question_id == question.id,
                QuestionSource.source_url == item["source_url"]
            )
            .first()
        )

        if not source_exists:
            db.add(
                QuestionSource(
                    question_id=question.id,
                    source_type="web",
                    source_url=item["source_url"],
                    source_title=item["source_title"]
                )
            )

    db.commit()

    print("✅ Java questions added successfully.")

except Exception as e:
    db.rollback()
    print("❌ Error:")
    print(e)

finally:
    db.close()