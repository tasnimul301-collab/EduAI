"""Activity Log Model Module.

Records platform actions, module operations, timestamps, and IP addresses
for institutional security, auditing, and admin activity monitoring.
"""

from datetime import datetime
from app.extensions import db


class ActivityLog(db.Model):
    """Audit trail logging critical events across the platform."""

    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)

    action = db.Column(db.String(100), nullable=False)
    module = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<ActivityLog id={self.id} action='{self.action}' module='{self.module}'>"
