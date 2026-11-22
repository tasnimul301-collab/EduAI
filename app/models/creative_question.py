"""Creative Question (CQ / সৃজনশীল প্রশ্ন) Model Module.

Defines schemas for Board-style and NCTB-aligned Creative Questions
with a stimulus (উদ্দীপক), 4-part questions (ক, খ, গ, ঘ), and model answers.
"""

from datetime import datetime
from app.extensions import db


class CreativeQuestion(db.Model):
    """Creative Question container holding stimulus, 4 sub-questions, and solutions."""

    __tablename__ = "creative_questions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    class_level = db.Column(db.String(50), nullable=False, default="Class 10")
    subject_name = db.Column(db.String(100), nullable=False)
    chapter_topic = db.Column(db.String(150), nullable=False)

    stimulus = db.Column(db.Text, nullable=False)  # উদ্দীপক

    question_a = db.Column(db.Text, nullable=False)  # ক: জ্ঞানমূলক (১ নম্বর)
    answer_a = db.Column(db.Text, nullable=False)

    question_b = db.Column(db.Text, nullable=False)  # খ: অনুধাবনমূলক (২ নম্বর)
    answer_b = db.Column(db.Text, nullable=False)

    question_c = db.Column(db.Text, nullable=False)  # গ: প্রয়োগমূলক (৩ নম্বর)
    answer_c = db.Column(db.Text, nullable=False)

    question_d = db.Column(db.Text, nullable=False)  # ঘ: উচ্চতর দক্ষতামূলক (৪ নম্বর)
    answer_d = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<CreativeQuestion id={self.id} class='{self.class_level}' subject='{self.subject_name}'>"
