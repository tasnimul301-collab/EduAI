"""Notification Model Module.

Stores in-app alert notifications for assignment deadlines,
study schedule reminders, and administrative announcements.
"""

from datetime import datetime
from app.extensions import db


class Notification(db.Model):
    """In-app alert notification addressed to a specific user."""

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default="system", nullable=False)  # 'deadline', 'reminder', 'system'
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def mark_as_read(self) -> None:
        """Mark this notification as read."""
        self.is_read = True

    def __repr__(self) -> str:
        return f"<Notification id={self.id} title='{self.title}' is_read={self.is_read}>"
