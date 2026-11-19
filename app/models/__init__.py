"""Models package initialization.

Imports all SQLAlchemy models so that Flask-SQLAlchemy can register them
with the metadata and build the database schema.
"""

from app.models.user import User
from app.models.subject import Subject
from app.models.task import StudyTask
from app.models.note import Note, UploadedFile
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt
from app.models.assignment import Assignment
from app.models.notification import Notification
from app.models.study_session import StudySession
from app.models.activity_log import ActivityLog

__all__ = [
    "User",
    "Subject",
    "StudyTask",
    "Note",
    "UploadedFile",
    "Quiz",
    "QuizQuestion",
    "QuizAttempt",
    "Assignment",
    "Notification",
    "StudySession",
    "ActivityLog",
]
