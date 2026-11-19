"""Study Session Model Module.

Tracks study duration (in minutes), session dates, and reflection notes
per subject. Directly powers the daily and weekly Chart.js analytics.
"""

from datetime import datetime, date
from app.extensions import db


class StudySession(db.Model):
    """Study session log recorded by a student."""

    __tablename__ = "study_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True, index=True)

    duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    session_date = db.Column(db.Date, default=date.today, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def duration_hours(self) -> float:
        """Helper to get duration in fractional hours."""
        return round(self.duration_minutes / 60.0, 1)

    def __repr__(self) -> str:
        return f"<StudySession id={self.id} date='{self.session_date}' minutes={self.duration_minutes}>"
