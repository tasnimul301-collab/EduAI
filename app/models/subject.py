"""Subject Model Module.

Represents academic courses/subjects registered by students.
"""

from datetime import datetime
from app.extensions import db


class Subject(db.Model):
    """Subject/Course entity owned by a specific student."""

    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), nullable=True)
    class_level = db.Column(db.String(50), nullable=True, default="General")
    color_hex = db.Column(db.String(7), default="#4F46E5", nullable=False)  # Hex color for badges & charts
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    tasks = db.relationship("StudyTask", backref="subject", lazy=True, cascade="all, delete-orphan")
    notes = db.relationship("Note", backref="subject", lazy=True, cascade="all, delete-orphan")
    quizzes = db.relationship("Quiz", backref="subject", lazy=True)
    assignments = db.relationship("Assignment", backref="subject", lazy=True, cascade="all, delete-orphan")
    study_sessions = db.relationship("StudySession", backref="subject", lazy=True, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Subject id={self.id} name='{self.name}' code='{self.code}'>"
