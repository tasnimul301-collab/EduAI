"""User Model Module.

Represents registered students and system administrators.
Enforces password hashing, role-based authorization, and
relationships to all student-owned academic entities.
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    """User entity representing students and administrators."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")  # 'student' or 'admin'
    full_name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Gamification, Points & Streaks
    streak_count = db.Column(db.Integer, default=1, nullable=False)
    last_active_date = db.Column(db.Date, nullable=True)
    total_points = db.Column(db.Integer, default=50, nullable=False)
    badges = db.Column(db.Text, default='["Novice Scholar"]', nullable=False)

    # Relationships to user-owned entities (cascading deletes for data hygiene)
    subjects = db.relationship("Subject", backref="user", lazy=True, cascade="all, delete-orphan")
    tasks = db.relationship("StudyTask", backref="user", lazy=True, cascade="all, delete-orphan")
    notes = db.relationship("Note", backref="user", lazy=True, cascade="all, delete-orphan")
    quizzes = db.relationship("Quiz", backref="user", lazy=True, cascade="all, delete-orphan")
    quiz_attempts = db.relationship("QuizAttempt", backref="user", lazy=True, cascade="all, delete-orphan")
    assignments = db.relationship("Assignment", backref="user", lazy=True, cascade="all, delete-orphan")
    notifications = db.relationship("Notification", backref="user", lazy=True, cascade="all, delete-orphan")
    study_sessions = db.relationship("StudySession", backref="user", lazy=True, cascade="all, delete-orphan")
    activity_logs = db.relationship("ActivityLog", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        """Securely hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify the plain-text password against the stored cryptographic hash."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        """Check whether the current user has administrative privileges."""
        return self.role == "admin"

    def get_badges_list(self) -> list:
        """Return list of earned achievement badges."""
        import json
        try:
            return json.loads(self.badges) if self.badges else ["Novice Scholar"]
        except Exception:
            return ["Novice Scholar"]

    def add_badge(self, badge_name: str) -> bool:
        """Award a new badge if not already unlocked."""
        import json
        b_list = self.get_badges_list()
        if badge_name not in b_list:
            b_list.append(badge_name)
            self.badges = json.dumps(b_list)
            return True
        return False

    def update_streak(self) -> int:
        """Update daily study streak calculation and award bonus points."""
        from datetime import date, timedelta
        today = date.today()
        if not self.last_active_date:
            self.streak_count = 1
            self.last_active_date = today
        elif self.last_active_date == today:
            pass  # Already active today
        elif self.last_active_date == today - timedelta(days=1):
            self.streak_count += 1
            self.last_active_date = today
            self.total_points += 15  # Daily streak bonus!
        else:
            self.streak_count = 1
            self.last_active_date = today
        return self.streak_count

    def __repr__(self) -> str:
        return f"<User id={self.id} username='{self.username}' role='{self.role}'>"
