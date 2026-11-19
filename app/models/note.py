"""Digital Notes and Uploaded Files Models Module.

Manages rich lecture notes and uploaded PDF documents.
Enforces ownership validation and categorical organization.
"""

from datetime import datetime
from app.extensions import db


class Note(db.Model):
    """Digital Note entity created by a student."""

    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True, index=True)

    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="Lecture", nullable=False)  # 'Lecture', 'Revision', 'Formula', 'General'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationship to uploaded files linked with this note
    files = db.relationship("UploadedFile", backref="note", lazy=True, cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Note id={self.id} title='{self.title}' category='{self.category}'>"


class UploadedFile(db.Model):
    """Uploaded PDF or study material document."""

    __tablename__ = "uploaded_files"

    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"), nullable=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def size_in_kb(self) -> float:
        """Helper to get file size formatted in kilobytes."""
        return round(self.file_size / 1024, 2)

    def size_in_mb(self) -> float:
        """Helper to get file size formatted in megabytes."""
        return round(self.file_size / (1024 * 1024), 2)

    def __repr__(self) -> str:
        return f"<UploadedFile id={self.id} filename='{self.filename}'>"
