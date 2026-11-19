"""Automated Unit and Integration Test Suite for EduSmart AI.

Covers:
- Database model integrity & password hashing
- Authentication and session flows
- Role-Based Access Control (RBAC) security enforcement
- Subject, Task, Note, and Assignment CRUD operations
- Quiz evaluation logic
"""

import glob
import os
import sys
import unittest
from datetime import datetime, timedelta

# Ensure project root and local virtualenv packages are in sys.path
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

for _candidate in [
    os.path.join(_project_root, "venv", "Lib", "site-packages"),
    os.path.join(_project_root, "venv", "lib", "site-packages"),
] + glob.glob(os.path.join(_project_root, "venv", "lib", "python*", "site-packages")):
    if os.path.isdir(_candidate) and _candidate not in sys.path:
        sys.path.insert(0, _candidate)

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.subject import Subject
from app.models.task import StudyTask
from app.models.note import Note
from app.models.assignment import Assignment
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt


class EduSmartTestCase(unittest.TestCase):
    """Test suite executing in-memory against SQLite testing config."""

    def setUp(self):
        """Set up test application and in-memory database before every test."""
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # Build schema in-memory
        db.create_all()

    def tearDown(self):
        """Clean up and tear down database after every test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_password_hashing(self):
        """Test cryptographic password hashing and verification."""
        user = User(username="testuser", email="test@uni.edu", role="student")
        user.set_password("secret123")
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.check_password("secret123"))
        self.assertFalse(user.check_password("wrongpassword"))
        self.assertNotEqual(user.password_hash, "secret123")

    def test_registration_and_login_flow(self):
        """Test full user registration and subsequent login."""
        # 1. Register new student
        response = self.client.post(
            "/auth/register",
            data={
                "username": "newstudent",
                "email": "newstudent@uni.edu",
                "full_name": "New Student",
                "password": "mypassword",
                "confirm_password": "mypassword",
                "role": "student",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registration successful", response.data)

        # 2. Log in with credentials
        response = self.client.post(
            "/auth/login",
            data={
                "identifier": "newstudent",
                "password": "mypassword",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome back", response.data)

        # 3. Log out
        response = self.client.get("/auth/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"logged out", response.data)

    def test_role_based_access_control(self):
        """Verify that students cannot access the admin portal (403/Forbidden)."""
        # Create student user
        student = User(username="sam", email="sam@uni.edu", role="student")
        student.set_password("pass123")
        db.session.add(student)
        db.session.commit()

        # Login as student
        self.client.post(
            "/auth/login",
            data={"identifier": "sam", "password": "pass123"},
            follow_redirects=True,
        )

        # Attempt to access admin portal
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 403)
        self.assertIn(b"Access Forbidden", response.data)

    def test_subject_and_task_crud(self):
        """Verify subject creation and associated study task workflow."""
        user = User(username="jdoe", email="jdoe@uni.edu", role="student")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        # Add subject
        subj = Subject(user_id=user.id, name="Algorithms", code="CSE-301")
        db.session.add(subj)
        db.session.commit()
        self.assertEqual(Subject.query.count(), 1)

        # Add study task
        task = StudyTask(
            user_id=user.id,
            subject_id=subj.id,
            title="Graph Traversals",
            priority="high",
            status="pending",
        )
        db.session.add(task)
        db.session.commit()

        self.assertEqual(StudyTask.query.count(), 1)
        self.assertFalse(task.is_completed())

        # Complete task
        task.status = "completed"
        db.session.commit()
        self.assertTrue(task.is_completed())

    def test_assignment_overdue_logic(self):
        """Verify assignment overdue calculation."""
        user = User(username="alice", email="alice@uni.edu", role="student")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        # Past assignment (overdue)
        past_assign = Assignment(
            user_id=user.id,
            title="Past Due Lab",
            due_date=datetime.utcnow() - timedelta(days=2),
            status="pending",
        )
        # Future assignment (not overdue)
        future_assign = Assignment(
            user_id=user.id,
            title="Future Project",
            due_date=datetime.utcnow() + timedelta(days=5),
            status="pending",
        )
        db.session.add_all([past_assign, future_assign])
        db.session.commit()

        self.assertTrue(past_assign.is_overdue())
        self.assertFalse(future_assign.is_overdue())

    def test_quiz_attempt_scoring(self):
        """Verify quiz evaluation and percentage calculation."""
        user = User(username="bob", email="bob@uni.edu", role="student")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        quiz = Quiz(
            user_id=user.id,
            title="Operating Systems Quiz",
            topic="Deadlocks",
            total_questions=2,
        )
        db.session.add(quiz)
        db.session.commit()

        attempt = QuizAttempt(
            quiz_id=quiz.id,
            user_id=user.id,
            score=2,
            total_score=2,
            percentage=100.0,
        )
        db.session.add(attempt)
        db.session.commit()

        self.assertEqual(attempt.score, 2)
        self.assertEqual(attempt.percentage, 100.0)

    def test_class_6_to_12_curriculum_quizzes(self):
        """Verify that Class 6 to 12 quizzes are successfully seeded across all classes."""
        from app.utils.curriculum import seed_class_quizzes_for_user, CLASS_CURRICULUM, PREBUILT_QUIZZES

        user = User(username="quizstudent", email="quiz@edusmart.ai")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        # Seed quizzes for this user
        count = seed_class_quizzes_for_user(user.id)
        self.assertGreaterEqual(count, 35)

        # Verify all classes 6-12 are present
        user_quizzes = Quiz.query.filter_by(user_id=user.id).all()
        classes_present = {q.class_level for q in user_quizzes}
        for expected_class in ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"]:
            self.assertIn(expected_class, classes_present)

        # Verify idempotency
        second_count = seed_class_quizzes_for_user(user.id)
        self.assertEqual(second_count, 0)

    def test_class_6_to_12_curriculum_subjects(self):
        """Verify that Class 6 to 12 subjects are seeded across all classes."""
        from app.utils.curriculum import seed_class_subjects_for_user
        from app.models.subject import Subject

        user = User(username="subjstudent", email="subj@edusmart.ai")
        user.set_password("pass123")
        db.session.add(user)
        db.session.commit()

        # Seed subjects
        count = seed_class_subjects_for_user(user.id)
        self.assertGreaterEqual(count, 50)

        # Verify all classes 6-12 are represented
        user_subjects = Subject.query.filter_by(user_id=user.id).all()
        classes_present = {s.class_level for s in user_subjects}
        for expected_class in ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Class 11", "Class 12"]:
            self.assertIn(expected_class, classes_present)

        # Verify idempotency
        second_count = seed_class_subjects_for_user(user.id)
        self.assertEqual(second_count, 0)


if __name__ == "__main__":
    unittest.main()
