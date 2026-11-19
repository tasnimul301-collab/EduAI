"""Study Task Model Module.

Represents actionable study tasks and schedules within the Smart Study Planner.
Supports priorities, deadlines, and lifecycle statuses.
"""

from datetime import datetime
from app.extensions import db


class StudyTask(db.Model):
    """Study task scheduled by a student."""

    __tablename__ = "study_tasks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True, index=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(10), default="medium", nullable=False)  # 'low', 'medium', 'high'
    status = db.Column(db.String(20), default="pending", nullable=False)    # 'pending', 'in_progress', 'completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def is_completed(self) -> bool:
        """Helper to quickly check task completion status."""
        return self.status == "completed"

    def __repr__(self) -> str:
        return f"<StudyTask id={self.id} title='{self.title}' status='{self.status}'>"
