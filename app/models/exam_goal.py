"""Exam Goal Model Module.

Tracks target exams, countdown deadlines, and target grades (e.g. GPA 5.00 / A+).
"""

from datetime import datetime, date
from app.extensions import db


class ExamGoal(db.Model):
    """Exam milestone with target date and countdown calculation."""

    __tablename__ = "exam_goals"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    title = db.Column(db.String(120), nullable=False)  # e.g. "SSC Board Exam 2027"
    class_level = db.Column(db.String(50), nullable=True, default="General")
    exam_date = db.Column(db.Date, nullable=False)
    target_grade = db.Column(db.String(30), nullable=False, default="GPA 5.00 (A+)")
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def days_remaining(self) -> int:
        """Calculate remaining days until the exam."""
        delta = (self.exam_date - date.today()).days
        return max(0, delta)

    def __repr__(self) -> str:
        return f"<ExamGoal id={self.id} title='{self.title}' date='{self.exam_date}'>"
