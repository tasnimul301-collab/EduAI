"""Assignment Submission Model Module.

Represents student-submitted coursework files (Word .docx/.doc, PDF),
submission timestamps, instructor notes, and grading status.
"""

from datetime import datetime
from app.extensions import db


class AssignmentSubmission(db.Model):
    """Entity representing a student's submission for an assignment."""

    __tablename__ = "assignment_submissions"

    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    file_path = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)  # 'pdf', 'docx', 'doc'
    file_size = db.Column(db.Integer, nullable=True)  # in bytes
    submission_notes = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    assignment = db.relationship(
        "Assignment",
        backref=db.backref("submissions", lazy=True, cascade="all, delete-orphan"),
    )
    student = db.relationship(
        "User",
        backref=db.backref("assignment_submissions", lazy=True, cascade="all, delete-orphan"),
    )

    def is_word_doc(self) -> bool:
        """Check whether file is a Microsoft Word document."""
        return self.file_type.lower() in ["docx", "doc"]

    def is_pdf(self) -> bool:
        """Check whether file is a PDF document."""
        return self.file_type.lower() == "pdf"

    def format_size(self) -> str:
        """Format bytes into readable KB or MB."""
        if not self.file_size:
            return "Unknown size"
        if self.file_size < 1024 * 1024:
            return f"{round(self.file_size / 1024, 1)} KB"
        return f"{round(self.file_size / (1024 * 1024), 2)} MB"

    def __repr__(self) -> str:
        return f"<AssignmentSubmission id={self.id} assignment_id={self.assignment_id} user_id={self.user_id} file='{self.original_filename}'>"
