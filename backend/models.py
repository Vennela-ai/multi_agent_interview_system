from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    normalized_name = Column(String(150), nullable=False, unique=True)
    created_at = Column(DateTime)

    questions = relationship(
        "RoleQuestion",
        back_populates="role",
        cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False, unique=True)
    category = Column(String(100))
    frequency_score = Column(Numeric(10, 2), default=0)
    relevance_score = Column(Numeric(10, 2), default=0)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    roles = relationship(
        "RoleQuestion",
        back_populates="question",
        cascade="all, delete-orphan"
    )

    sources = relationship(
        "QuestionSource",
        back_populates="question",
        cascade="all, delete-orphan"
    )


class RoleQuestion(Base):
    __tablename__ = "role_questions"

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        primary_key=True
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        primary_key=True
    )

    role = relationship(
        "Role",
        back_populates="questions"
    )

    question = relationship(
        "Question",
        back_populates="roles"
    )


class QuestionSource(Base):
    __tablename__ = "question_sources"

    id = Column(Integer, primary_key=True)

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )

    source_type = Column(String(50), nullable=False)
    source_url = Column(Text, nullable=False)
    source_title = Column(Text)
    source_id = Column(String(255))
    published_at = Column(DateTime)
    collected_at = Column(DateTime)

    question = relationship(
        "Question",
        back_populates="sources"
    )