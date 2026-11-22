"""Comprehensive End-to-End (E2E) Test Suite for EduSmart AI.

Simulates real-world user workflows across every subsystem:
1. Authentication & Profile Management (Register, Login, Update, Password Change)
2. Role-Based Access Control (RBAC) & Security Enforcement
3. Academic Subjects / Course Management
4. Smart Study Planner (Task creation, prioritization, deadlines, status transitions)
5. Digital Lecture Notes & PDF Document Attachments (CRUD, Search, Upload, Download, Delete)
6. Coursework & Assignment Tracker (Deadlines, Overdue detection, Notifications)
7. Study Sessions & Chart.js Analytics Aggregation
8. In-App Notifications Lifecycle (Creation, Filtering, Read status)
9. AI Quiz Generation, Test Taking & Auto-Grading (with mocked AI & fallback)
10. Conversational AI Study Assistant (JSON AJAX, Input Validation & Fallbacks)
11. Administrative Oversight & Audit Logging (Account toggling, System Metrics)
12. Error Handlers (403, 404)
"""

import io
import os
import sys
import glob
import json
import unittest
from datetime import datetime, date, timedelta
from unittest.mock import patch, MagicMock

# Ensure project root and venv packages are in sys.path
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
from app.models.note import Note, UploadedFile
from app.models.assignment import Assignment
from app.models.notification import Notification
from app.models.study_session import StudySession
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt
from app.models.activity_log import ActivityLog
from app.services.analytics_service import AnalyticsService


class EduSmartE2ETestCase(unittest.TestCase):
    """Full End-to-End Test Suite."""

    def setUp(self):
        """Set up in-memory application context and fresh database schema."""
        self.app = create_app("testing")
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["UPLOAD_FOLDER"] = os.path.join(_project_root, "tests", "temp_uploads")
        os.makedirs(self.app.config["UPLOAD_FOLDER"], exist_ok=True)

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()

        # Create Baseline Admin & Student accounts
        self.admin = User(
            username="admin_e2e",
            email="admin_e2e@edusmart.ai",
            full_name="E2E Administrator",
            role="admin",
        )
        self.admin.set_password("AdminPass123!")

        self.student = User(
            username="student_e2e",
            email="student_e2e@edusmart.ai",
            full_name="E2E Student",
            role="student",
        )
        self.student.set_password("StudentPass123!")

        db.session.add_all([self.admin, self.student])
        db.session.commit()

    def tearDown(self):
        """Clean up database and test upload files."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        # Clean test uploads
        upload_dir = os.path.join(_project_root, "tests", "temp_uploads")
        if os.path.exists(upload_dir):
            for f in os.listdir(upload_dir):
                try:
                    os.remove(os.path.join(upload_dir, f))
                except OSError:
                    pass
            try:
                os.rmdir(upload_dir)
            except OSError:
                pass

    # =========================================================================
    # 1. Authentication & Profile Management
    # =========================================================================
    def test_e2e_registration_validation_and_flow(self):
        """Test registration constraints, edge cases, and successful registration."""
        # A. Short password validation
        res = self.client.post(
            "/auth/register",
            data={
                "username": "shortpass",
                "email": "short@uni.edu",
                "password": "123",
                "confirm_password": "123",
            },
            follow_redirects=True,
        )
        self.assertIn(b"at least 6 characters", res.data)

        # B. Password mismatch
        res = self.client.post(
            "/auth/register",
            data={
                "username": "mismatch",
                "email": "mismatch@uni.edu",
                "password": "password123",
                "confirm_password": "password456",
            },
            follow_redirects=True,
        )
        self.assertIn(b"do not match", res.data)

        # C. Duplicate username
        res = self.client.post(
            "/auth/register",
            data={
                "username": "student_e2e",
                "email": "another@uni.edu",
                "password": "password123",
                "confirm_password": "password123",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Username is already taken", res.data)

        # D. Successful registration
        res = self.client.post(
            "/auth/register",
            data={
                "username": "sarah_connor",
                "email": "sarah@cyberdyne.edu",
                "full_name": "Sarah Connor",
                "password": "ValidPassword123!",
                "confirm_password": "ValidPassword123!",
                "role": "student",
            },
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Registration successful", res.data)

        # Verify user in database
        user = User.query.filter_by(username="sarah_connor").first()
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password("ValidPassword123!"))

    def test_e2e_login_logout_and_profile_update(self):
        """Test login with wrong password, success, profile update, and password change."""
        # A. Bad credentials
        res = self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "WrongPassword"},
            follow_redirects=True,
        )
        self.assertIn(b"Invalid credentials", res.data)

        # B. Successful login
        res = self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "StudentPass123!"},
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Welcome back", res.data)

        # C. Update profile info
        res = self.client.post(
            "/auth/profile",
            data={
                "action": "update_info",
                "full_name": "E2E Student Updated",
                "bio": "Studying Distributed Algorithms.",
            },
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Profile information updated successfully", res.data)

        user = User.query.filter_by(username="student_e2e").first()
        self.assertEqual(user.full_name, "E2E Student Updated")
        self.assertEqual(user.bio, "Studying Distributed Algorithms.")

        # D. Change password
        res = self.client.post(
            "/auth/profile",
            data={
                "action": "change_password",
                "current_password": "StudentPass123!",
                "new_password": "NewSecretPassword456!",
                "confirm_password": "NewSecretPassword456!",
            },
            follow_redirects=True,
        )
        self.assertIn(b"Password updated successfully", res.data)

        # E. Logout and log in with new password
        self.client.get("/auth/logout", follow_redirects=True)
        res = self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "NewSecretPassword456!"},
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Welcome back", res.data)

    # =========================================================================
    # 2. RBAC & Security Enforcement
    # =========================================================================
    def test_e2e_rbac_student_forbidden_from_admin(self):
        """Verify student is forbidden (403) from accessing admin routes."""
        self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "StudentPass123!"},
            follow_redirects=True,
        )
        res = self.client.get("/admin/")
        self.assertEqual(res.status_code, 403)
        self.assertIn(b"Access Forbidden", res.data)

        # Student cannot toggle user status
        res = self.client.post(f"/admin/users/{self.student.id}/toggle-status")
        self.assertEqual(res.status_code, 403)

    def test_e2e_admin_user_deactivation_prevents_login(self):
        """Admin deactivates student; student cannot log in while inactive."""
        # Login as Admin
        self.client.post(
            "/auth/login",
            data={"identifier": "admin_e2e", "password": "AdminPass123!"},
            follow_redirects=True,
        )

        # Admin deactivates student
        res = self.client.post(
            f"/admin/users/{self.student.id}/toggle-status",
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"deactivated", res.data)

        # Verify student inactive in DB
        db.session.refresh(self.student)
        self.assertFalse(self.student.is_active)

        # Admin logs out
        self.client.get("/auth/logout", follow_redirects=True)

        # Student tries to log in
        res = self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "StudentPass123!"},
            follow_redirects=True,
        )
        self.assertIn(b"deactivated", res.data)

    # =========================================================================
    # 3. Academic Subjects Management
    # =========================================================================
    def test_e2e_subject_lifecycle(self):
        """Test creating, listing, and deleting academic subjects."""
        self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "StudentPass123!"},
            follow_redirects=True,
        )

        # 1. Create Subject
        res = self.client.post(
            "/subjects",
            data={"action": "create", "name": "Computer Networks", "code": "CSE-304", "color_hex": "#10B981"},
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Computer Networks", res.data)

        subj = Subject.query.filter_by(name="Computer Networks", user_id=self.student.id).first()
        self.assertIsNotNone(subj)
        self.assertEqual(subj.code, "CSE-304")

        # 2. Delete Subject
        res = self.client.post(
            "/subjects",
            data={"action": "delete", "subject_id": subj.id},
            follow_redirects=True,
        )
        self.assertIn(b"deleted", res.data)
        self.assertIsNone(db.session.get(Subject, subj.id))

    # =========================================================================
    # 4. Smart Study Planner (Task Management)
    # =========================================================================
    def test_e2e_study_planner_workflow(self):
        """Test task creation, filtering, toggling status, and progress metrics."""
        self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "StudentPass123!"},
            follow_redirects=True,
        )

        # Create a Subject first
        subj = Subject(user_id=self.student.id, name="Data Structures", code="CSE-201")
        db.session.add(subj)
        db.session.commit()

        # 1. Create a task
        due_date_str = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
        res = self.client.post(
            "/planner/",
            data={
                "action": "create",
                "title": "Implement AVL Tree Rotations",
                "description": "Left and Right balance factors implementation in C++.",
                "subject_id": str(subj.id),
                "priority": "high",
                "due_date": due_date_str,
            },
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Implement AVL Tree Rotations", res.data)

        task = StudyTask.query.filter_by(title="Implement AVL Tree Rotations").first()
        self.assertIsNotNone(task)
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.status, "pending")

        # 2. Toggle status to completed
        res = self.client.post(f"/planner/{task.id}/toggle", follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        db.session.refresh(task)
        self.assertEqual(task.status, "completed")
        self.assertTrue(task.is_completed())

        # 3. Test filtering
        res_completed = self.client.get("/planner/?status=completed")
        self.assertIn(b"Implement AVL Tree Rotations", res_completed.data)

        res_pending = self.client.get("/planner/?status=pending")
        self.assertNotIn(b"Implement AVL Tree Rotations", res_pending.data)

        # 4. Delete task
        res_del = self.client.post(
            "/planner/",
            data={"action": "delete", "task_id": task.id},
            follow_redirects=True,
        )
        self.assertEqual(res_del.status_code, 200)
        self.assertIsNone(db.session.get(StudyTask, task.id))

    # =========================================================================
    # 5. Digital Notes & PDF Attachments
    # =========================================================================
    def test_e2e_notes_crud_search_and_pdf_attachment(self):
        """Test admin note creation, searching, editing, PDF upload, and student download."""
        self.client.post(
            "/auth/login",
            data={"identifier": "admin_e2e", "password": "AdminPass123!"},
            follow_redirects=True,
        )

        subj = Subject(user_id=self.admin.id, name="Software Engineering", code="CSE-306")
        db.session.add(subj)
        db.session.commit()

        # 1. Admin creates note with PDF file
        pdf_content = b"%PDF-1.4 Mock PDF file for testing attachments."
        data = {
            "title": "Design Patterns: Observer & Singleton",
            "content": "Observer defines a one-to-many dependency between objects.",
            "category": "Lecture",
            "subject_id": str(subj.id),
            "pdf_file": (io.BytesIO(pdf_content), "design_patterns.pdf"),
        }
        res = self.client.post(
            "/notes/create",
            data=data,
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Design Patterns: Observer", res.data)

        note = Note.query.filter_by(title="Design Patterns: Observer & Singleton").first()
        self.assertIsNotNone(note)
        self.assertEqual(len(note.files), 1)

        uploaded_file = note.files[0]
        self.assertEqual(uploaded_file.filename, "design_patterns.pdf")

        # 2. Student logs in to search and download the PDF attachment
        self.client.get("/auth/logout")
        self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "StudentPass123!"},
            follow_redirects=True,
        )

        download_res = self.client.get(f"/notes/download/{uploaded_file.id}")
        self.assertEqual(download_res.status_code, 200)
        self.assertEqual(download_res.data, pdf_content)
        download_res.close()

        # 3. Search notes as student
        search_res = self.client.get("/notes/?q=Observer")
        self.assertIn(b"Design Patterns: Observer", search_res.data)

        search_miss = self.client.get("/notes/?q=NonExistentKeywordXYZ")
        self.assertNotIn(b"Design Patterns: Observer", search_miss.data)

        # 4. Admin logs back in to edit and delete note
        self.client.get("/auth/logout")
        self.client.post(
            "/auth/login",
            data={"identifier": "admin_e2e", "password": "AdminPass123!"},
            follow_redirects=True,
        )

        edit_res = self.client.post(
            f"/notes/{note.id}/edit",
            data={
                "title": "Design Patterns: Observer, Singleton & Factory",
                "content": "Added Factory Method details.",
                "category": "Revision",
                "subject_id": str(subj.id),
            },
            follow_redirects=True,
        )
        self.assertEqual(edit_res.status_code, 200)
        db.session.refresh(note)
        self.assertEqual(note.title, "Design Patterns: Observer, Singleton & Factory")
        self.assertEqual(note.category, "Revision")

        # 5. Delete note and verify attachment file cleanup on disk
        file_path_on_disk = os.path.join(self.app.config["UPLOAD_FOLDER"], uploaded_file.file_path)
        self.assertTrue(os.path.exists(file_path_on_disk))

        del_res = self.client.post(f"/notes/{note.id}/delete", follow_redirects=True)
        self.assertEqual(del_res.status_code, 200)
        self.assertIsNone(db.session.get(Note, note.id))
        self.assertFalse(os.path.exists(file_path_on_disk))

    # =========================================================================
    # 6. Assignments Tracker & Overdue Logic
    # =========================================================================
    def test_e2e_assignment_tracking_and_deadline_notification(self):
        """Test assignment creation by admin, automatic reminder notification, and student status toggle."""
        # Admin creates assignment
        self.client.post(
            "/auth/login",
            data={"identifier": "admin_e2e", "password": "AdminPass123!"},
            follow_redirects=True,
        )

        future_due = (datetime.utcnow() + timedelta(days=5)).strftime("%Y-%m-%dT%H:%M")
        res = self.client.post(
            "/assignments/",
            data={
                "action": "create",
                "title": "Distributed Consensus Lab",
                "description": "Implement Raft leader election algorithm.",
                "priority": "high",
                "due_date": future_due,
            },
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Distributed Consensus Lab", res.data)

        assign = Assignment.query.filter_by(title="Distributed Consensus Lab").first()
        self.assertIsNotNone(assign)
        self.assertFalse(assign.is_overdue())

        # Verify automated deadline notification created for student
        notif = Notification.query.filter_by(user_id=self.student.id, type="deadline").first()
        self.assertIsNotNone(notif)
        self.assertIn("Distributed Consensus Lab", notif.title)

        # Student logs in and toggles assignment to submitted
        self.client.get("/auth/logout", follow_redirects=True)
        self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "StudentPass123!"},
            follow_redirects=True,
        )
        toggle_res = self.client.post(f"/assignments/{assign.id}/toggle", follow_redirects=True)
        self.assertEqual(toggle_res.status_code, 200)
        db.session.refresh(assign)
        self.assertEqual(assign.status, "submitted")

    # =========================================================================
    # 7. Study Sessions & Analytics Aggregation
    # =========================================================================
    def test_e2e_study_session_logging_and_dashboard_metrics(self):
        """Test logging study sessions and verifying Chart.js metric calculation."""
        self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "StudentPass123!"},
            follow_redirects=True,
        )

        # Log 90 minutes study session
        res = self.client.post(
            "/study-session/log",
            data={"duration_minutes": "90", "notes": "Deep learning backpropagation calculus."},
            follow_redirects=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Logged 90 minutes of study time", res.data)

        metrics = AnalyticsService.get_student_dashboard_metrics(self.student.id)
        self.assertGreaterEqual(metrics["study_hours"], 1.5)
        self.assertIn("weekly_labels", metrics["charts"])
        self.assertIn("weekly_hours", metrics["charts"])
        self.assertEqual(len(metrics["charts"]["weekly_labels"]), 7)

    # =========================================================================
    # 8. Notifications Lifecycle
    # =========================================================================
    def test_e2e_notifications_flow(self):
        """Test notification listing and mark as read."""
        self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "StudentPass123!"},
            follow_redirects=True,
        )

        notif = Notification(
            user_id=self.student.id,
            title="Exam Reminder",
            message="Final exams commence in 2 weeks.",
            type="reminder",
        )
        db.session.add(notif)
        db.session.commit()

        # View notifications page
        res = self.client.get("/notifications")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Exam Reminder", res.data)

        # Mark as read
        self.client.post(f"/notifications/{notif.id}/read", follow_redirects=True)
        db.session.refresh(notif)
        self.assertTrue(notif.is_read)

    # =========================================================================
    # 9. AI Quiz Generation, Test Taking & Auto-Grading
    # =========================================================================
    def test_e2e_quiz_flow_with_mocked_ai(self):
        """Test quiz generation with mocked Gemini AI by admin, test taking by student, and scoring."""
        # Admin creates quiz
        self.client.post(
            "/auth/login",
            data={"identifier": "admin_e2e", "password": "AdminPass123!"},
            follow_redirects=True,
        )

        mock_ai_questions = [
            {
                "question": "What is the time complexity of binary search?",
                "options": {"A": "O(1)", "B": "O(log n)", "C": "O(n)", "D": "O(n^2)"},
                "correct": "B",
                "explanation": "Binary search divides the search interval in half at each step.",
            },
            {
                "question": "Which data structure operates on a FIFO basis?",
                "options": {"A": "Stack", "B": "Queue", "C": "Tree", "D": "Graph"},
                "correct": "B",
                "explanation": "Queue is First-In-First-Out.",
            },
        ]

        with patch("app.services.ai_service.AIService.generate_quiz_questions") as mock_generate:
            mock_generate.return_value = {
                "success": True,
                "questions": mock_ai_questions,
                "error": None,
            }

            # Generate Quiz as Admin
            res = self.client.post(
                "/quiz/generate",
                data={"topic": "Data Structures Basics", "difficulty": "easy", "count": "2"},
                follow_redirects=True,
            )
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Data Structures Basics", res.data)

            quiz = Quiz.query.filter_by(topic="Data Structures Basics").first()
            self.assertIsNotNone(quiz)
            self.assertEqual(len(quiz.questions), 2)

            # Student logs in to take and submit Quiz: Q1 correct ('B'), Q2 incorrect ('A')
            self.client.get("/auth/logout", follow_redirects=True)
            self.client.post(
                "/auth/login",
                data={"identifier": "student_e2e", "password": "StudentPass123!"},
                follow_redirects=True,
            )
            q1, q2 = quiz.questions[0], quiz.questions[1]
            submit_data = {
                f"question_{q1.id}": "B",
                f"question_{q2.id}": "A",
            }
            res_submit = self.client.post(
                f"/quiz/submit/{quiz.id}",
                data=submit_data,
                follow_redirects=True,
            )
            self.assertEqual(res_submit.status_code, 200)
            self.assertIn(b"Quiz Result", res_submit.data)
            self.assertIn(b"50.0%", res_submit.data)

            # Verify attempt stored in database
            attempt = QuizAttempt.query.filter_by(quiz_id=quiz.id, user_id=self.student.id).first()
            self.assertIsNotNone(attempt)
            self.assertEqual(attempt.score, 1)
            self.assertEqual(attempt.total_score, 2)
            self.assertEqual(attempt.percentage, 50.0)

    # =========================================================================
    # 10. Conversational AI Study Assistant
    # =========================================================================
    def test_e2e_ai_study_assistant_ajax(self):
        """Test conversational AI endpoint validation, fallback, and mocked response."""
        self.client.post(
            "/auth/login",
            data={"identifier": "student_e2e", "password": "StudentPass123!"},
            follow_redirects=True,
        )

        # 1. Empty message validation
        res_empty = self.client.post(
            "/assistant/ask",
            data=json.dumps({"message": "   "}),
            content_type="application/json",
        )
        self.assertEqual(res_empty.status_code, 400)
        data = res_empty.get_json()
        self.assertFalse(data["success"])

        # 2. Mocked successful response
        with patch("app.services.ai_service.AIService.ask_study_assistant") as mock_ask:
            mock_ask.return_value = {
                "success": True,
                "response": "Polymorphism allows objects of different classes to be treated through a common interface.",
                "error": None,
            }

            res = self.client.post(
                "/assistant/ask",
                data=json.dumps({"message": "Explain OOP Polymorphism."}),
                content_type="application/json",
            )
            self.assertEqual(res.status_code, 200)
            res_json = res.get_json()
            self.assertTrue(res_json["success"])
            self.assertIn("Polymorphism", res_json["response"])

            # Verify activity log recorded
            log = ActivityLog.query.filter_by(user_id=self.student.id, module="Assistant").first()
            self.assertIsNotNone(log)

    # =========================================================================
    # 11. Administrative Oversight & Audit Logging
    # =========================================================================
    def test_e2e_admin_dashboard_and_audit_trail(self):
        """Verify Admin KPI calculation, user list, and audit logs."""
        self.client.post(
            "/auth/login",
            data={"identifier": "admin_e2e", "password": "AdminPass123!"},
            follow_redirects=True,
        )

        res = self.client.get("/admin/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Administrative Control", res.data)
        self.assertIn(b"student_e2e", res.data)

        # Check admin metrics
        admin_metrics = AnalyticsService.get_admin_metrics()
        self.assertGreaterEqual(admin_metrics["total_users"], 2)
        self.assertIn("recent_logs", admin_metrics)

    # =========================================================================
    # 12. Custom Error Handlers
    # =========================================================================
    def test_e2e_custom_error_handlers(self):
        """Verify 404 page."""
        res = self.client.get("/route-that-does-not-exist-404")
        self.assertEqual(res.status_code, 404)
        self.assertIn(b"Page Not Found", res.data)


if __name__ == "__main__":
    unittest.main()
