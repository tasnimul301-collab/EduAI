"""Assignment Model Module.

Manages student academic coursework assignments, submission statuses,
priority levels, and deadline alerting.
"""

from datetime import datetime
from app.extensions import db


class Assignment(db.Model):
    """Academic Assignment entity created and tracked by a student."""

    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True, index=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(10), default="medium", nullable=False)  # 'low', 'medium', 'high'
    status = db.Column(db.String(20), default="pending", nullable=False)   # 'pending', 'submitted'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def is_overdue(self) -> bool:
        """Check whether the assignment is overdue (past deadline and not submitted)."""
        if self.status == "submitted":
            return False
        return datetime.utcnow() > self.due_date

    def days_remaining(self) -> int:
        """Calculate days remaining until submission deadline."""
        delta = self.due_date - datetime.utcnow()
        return max(0, delta.days)

    def __repr__(self) -> str:
        return f"<Assignment id={self.id} title='{self.title}' status='{self.status}'>"
