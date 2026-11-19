"""AI Quiz Models Module.

Defines schemas for AI-generated Multiple-Choice Question (MCQ) quizzes,
individual questions, options, correct answers, and student attempt histories.
"""

from datetime import datetime
from app.extensions import db


class Quiz(db.Model):
    """Quiz container holding metadata and a list of questions."""

    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True, index=True)

    title = db.Column(db.String(150), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    class_level = db.Column(db.String(50), nullable=True, default="General")
    difficulty = db.Column(db.String(20), default="medium", nullable=False)  # 'easy', 'medium', 'hard'
    total_questions = db.Column(db.Integer, default=5, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    questions = db.relationship(
        "QuizQuestion", backref="quiz", lazy=True, cascade="all, delete-orphan"
    )
    attempts = db.relationship(
        "QuizAttempt", backref="quiz", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Quiz id={self.id} title='{self.title}' topic='{self.topic}'>"


class QuizQuestion(db.Model):
    """Individual MCQ question belonging to a specific quiz."""

    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False, index=True)

    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    explanation = db.Column(db.Text, nullable=True)

    def get_options_dict(self) -> dict:
        """Helper to get a dictionary of available options."""
        return {
            "A": self.option_a,
            "B": self.option_b,
            "C": self.option_c,
            "D": self.option_d,
        }

    def __repr__(self) -> str:
        return f"<QuizQuestion id={self.id} quiz_id={self.quiz_id} correct='{self.correct_option}'>"


class QuizAttempt(db.Model):
    """Record of a student taking and completing a quiz."""

    __tablename__ = "quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    score = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<QuizAttempt id={self.id} score={self.score}/{self.total_score} ({self.percentage}%)>"
