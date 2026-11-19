"""Application Entry Point.

Initializes the EduSmart AI application, seeds initial demo data
if the database is brand new, and launches the development web server.
"""

import glob
import os
import sys

# Ensure local virtualenv packages are accessible even when running unactivated
_script_dir = os.path.dirname(os.path.abspath(__file__))
for _candidate in [
    os.path.join(_script_dir, "venv", "Lib", "site-packages"),
    os.path.join(_script_dir, "venv", "lib", "site-packages"),
] + glob.glob(os.path.join(_script_dir, "venv", "lib", "python*", "site-packages")):
    if os.path.isdir(_candidate) and _candidate not in sys.path:
        sys.path.insert(0, _candidate)

from datetime import datetime, date, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.subject import Subject
from app.models.task import StudyTask
from app.models.note import Note
from app.models.assignment import Assignment
from app.models.notification import Notification
from app.models.study_session import StudySession
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt

app = create_app(os.getenv("FLASK_ENV", "development"))


def seed_database():
    """Seed initial demo data if the database has not been initialized yet."""
    with app.app_context():
        db.create_all()

        # Check if an admin already exists
        if not User.query.filter_by(username="admin").first():
            print("🌱 Initializing EduSmart AI database with demo records...")

            # 1. Create Administrator Account
            admin = User(
                username="admin",
                email="admin@edusmart.ai",
                full_name="System Administrator",
                role="admin",
                bio="EduSmart AI Capstone Administrator",
            )
            admin.set_password("admin123")
            db.session.add(admin)

            # 2. Create Demo Student Account
            student = User(
                username="student",
                email="student@university.edu",
                full_name="Alex Johnson",
                role="student",
                bio="3rd Year Computer Science & Engineering Undergraduate",
            )
            student.set_password("student123")
            db.session.add(student)
            db.session.flush()

            # 3. Create Sample Subjects
            subj_algo = Subject(
                user_id=student.id,
                name="Algorithms & Complexity",
                code="CSE-301",
                color_hex="#4F46E5",
            )
            subj_db = Subject(
                user_id=student.id,
                name="Database Management Systems",
                code="CSE-303",
                color_hex="#0EA5E9",
            )
            subj_ai = Subject(
                user_id=student.id,
                name="Artificial Intelligence",
                code="CSE-305",
                color_hex="#10B981",
            )
            db.session.add_all([subj_algo, subj_db, subj_ai])
            db.session.flush()

            # 4. Create Sample Tasks
            task1 = StudyTask(
                user_id=student.id,
                subject_id=subj_algo.id,
                title="Review Dijkstra and Bellman-Ford algorithms",
                description="Solve 3 graph shortest-path problems from textbook chapter 24.",
                priority="high",
                status="completed",
                due_date=datetime.utcnow() - timedelta(days=1),
            )
            task2 = StudyTask(
                user_id=student.id,
                subject_id=subj_db.id,
                title="Practice B+ Tree indexing exercises",
                description="Draw tree node splits after 5 key insertions.",
                priority="medium",
                status="in_progress",
                due_date=datetime.utcnow() + timedelta(days=2),
            )
            task3 = StudyTask(
                user_id=student.id,
                subject_id=subj_ai.id,
                title="Read A* Search heuristic admissibility proof",
                description="Understand theorem on optimal path guarantees.",
                priority="high",
                status="pending",
                due_date=datetime.utcnow() + timedelta(days=4),
            )
            db.session.add_all([task1, task2, task3])

            # 5. Create Sample Notes
            note1 = Note(
                user_id=student.id,
                subject_id=subj_algo.id,
                title="Asymptotic Notation Reference",
                category="Formula",
                content=(
                    "Big-O: Upper bound on growth rate.\n"
                    "Big-Omega: Lower bound on growth rate.\n"
                    "Big-Theta: Tight bound (both upper and lower).\n\n"
                    "Master Theorem recurrence forms:\n"
                    "T(n) = aT(n/b) + f(n)"
                ),
            )
            note2 = Note(
                user_id=student.id,
                subject_id=subj_db.id,
                title="ACID Properties in Relational Databases",
                category="Lecture",
                content=(
                    "1. Atomicity: All or nothing execution.\n"
                    "2. Consistency: Database state remains valid.\n"
                    "3. Isolation: Concurrent transactions do not interfere.\n"
                    "4. Durability: Committed updates persist permanently on disk."
                ),
            )
            db.session.add_all([note1, note2])

            # 6. Create Sample Assignments
            assign1 = Assignment(
                user_id=student.id,
                subject_id=subj_algo.id,
                title="Dynamic Programming Problem Set 3",
                description="Implement 0/1 Knapsack and Matrix Chain Multiplication in Python.",
                priority="high",
                due_date=datetime.utcnow() + timedelta(days=3),
                status="pending",
            )
            assign2 = Assignment(
                user_id=student.id,
                subject_id=subj_db.id,
                title="Schema Normalization Report",
                description="Normalize bookstore schema from 1NF through BCNF.",
                priority="medium",
                due_date=datetime.utcnow() + timedelta(days=7),
                status="pending",
            )
            db.session.add_all([assign1, assign2])

            # 7. Create Sample Study Sessions for Chart.js
            today = date.today()
            session1 = StudySession(
                user_id=student.id,
                subject_id=subj_algo.id,
                duration_minutes=90,
                session_date=today - timedelta(days=3),
                notes="Graph search algorithms review.",
            )
            session2 = StudySession(
                user_id=student.id,
                subject_id=subj_db.id,
                duration_minutes=60,
                session_date=today - timedelta(days=2),
                notes="SQL joins and relational algebra practice.",
            )
            session3 = StudySession(
                user_id=student.id,
                subject_id=subj_ai.id,
                duration_minutes=120,
                session_date=today - timedelta(days=1),
                notes="State space formulation and depth-first search.",
            )
            session4 = StudySession(
                user_id=student.id,
                subject_id=subj_algo.id,
                duration_minutes=75,
                session_date=today,
                notes="Divide and conquer recurrence solving.",
            )
            db.session.add_all([session1, session2, session3, session4])

            # 8. Create Sample Quiz and Attempt
            sample_quiz = Quiz(
                user_id=student.id,
                subject_id=subj_db.id,
                title="Database Normalization Basics",
                topic="Relational Normal Forms",
                difficulty="medium",
                total_questions=3,
            )
            db.session.add(sample_quiz)
            db.session.flush()

            q1 = QuizQuestion(
                quiz_id=sample_quiz.id,
                question_text="Which normal form removes partial functional dependencies?",
                option_a="First Normal Form (1NF)",
                option_b="Second Normal Form (2NF)",
                option_c="Third Normal Form (3NF)",
                option_d="Boyce-Codd Normal Form (BCNF)",
                correct_option="B",
                explanation="2NF requires that all non-prime attributes are fully functionally dependent on the primary key.",
            )
            q2 = QuizQuestion(
                quiz_id=sample_quiz.id,
                question_text="Which SQL clause is used to filter aggregated group results?",
                option_a="WHERE",
                option_b="ORDER BY",
                option_c="HAVING",
                option_d="GROUP BY",
                correct_option="C",
                explanation="HAVING filters groups created by GROUP BY, while WHERE filters individual rows.",
            )
            q3 = QuizQuestion(
                quiz_id=sample_quiz.id,
                question_text="What does the 'I' represent in ACID properties?",
                option_a="Integrity",
                option_b="Indexing",
                option_c="Isolation",
                option_d="Iteration",
                correct_option="C",
                explanation="Isolation ensures that concurrent transactions occur without mutual interference.",
            )
            db.session.add_all([q1, q2, q3])

            attempt = QuizAttempt(
                quiz_id=sample_quiz.id,
                user_id=student.id,
                score=3,
                total_score=3,
                percentage=100.0,
                completed_at=datetime.utcnow() - timedelta(days=1),
            )
            db.session.add(attempt)

            # Seed pre-built curriculum quizzes and subjects for Class 6 to 12
            from app.utils.curriculum import seed_class_quizzes_for_user, seed_class_subjects_for_user
            seed_class_quizzes_for_user(student.id)
            seed_class_subjects_for_user(student.id)

            # 9. Create Welcome Notification
            welcome_notif = Notification(
                user_id=student.id,
                title="Welcome to EduSmart AI!",
                message="Your intelligent academic workspace is ready. Start by reviewing your study schedule or asking the AI Assistant a question.",
                type="system",
            )
            db.session.add(welcome_notif)

            db.session.commit()
            print("✅ Demo data successfully seeded!")
            print("   Admin: username='admin', password='admin123'")
            print("   Student: username='student', password='student123'")


# Seed initial data on startup
seed_database()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    print("\n" + "=" * 60)
    print("🚀 EduSmart AI Web Server is starting...")
    print(f"👉 Open your browser at: http://{host}:{port}")
    print("🔑 Demo Accounts:")
    print("   Student:  username='student' | password='student123'")
    print("   Admin:    username='admin'   | password='admin123'")
    print("=" * 60 + "\n")
    # Run server
    app.run(host=host, port=port, debug=False)
