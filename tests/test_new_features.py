"""Unit & Integration tests for the 10 new EduSmart AI features.

Covers:
- AI Flashcards & Mastery Tracking
- Creative Questions (CQ) & Model Answers
- AI Note Summarizer Endpoint
- Gamification (Streaks, Points, Badges)
- Academic Leaderboard
- Pomodoro / Exam Goal Countdown
- Quiz Completion Certificate
"""

import unittest
from datetime import date, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.flashcard import FlashcardDeck, Flashcard
from app.models.creative_question import CreativeQuestion
from app.models.exam_goal import ExamGoal
from app.models.note import Note
from app.models.quiz import Quiz, QuizAttempt, QuizQuestion


class TestNewFeatures(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Seed test student
        self.user = User(
            username="testscholar",
            email="scholar@test.com",
            full_name="Test Scholar",
            role="student",
            total_points=50,
            streak_count=3,
        )
        self.user.set_password("pass123")
        db.session.add(self.user)
        db.session.commit()

        self.client = self.app.test_client()
        with self.client.session_transaction() as sess:
            sess["user_id"] = self.user.id
            sess["role"] = self.user.role
            sess["username"] = self.user.username

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_gamification_streaks_and_badges(self):
        """Test daily streak increment, points, and badge unlocking."""
        user = User.query.get(self.user.id)
        self.assertEqual(user.streak_count, 3)
        self.assertEqual(user.total_points, 50)

        # Award points and add badge
        user.total_points += 25
        user.add_badge("Quiz Master")
        user.add_badge("Fast Learner")
        db.session.commit()

        badges = user.get_badges_list()
        self.assertIn("Novice Scholar", badges)
        self.assertIn("Quiz Master", badges)
        self.assertIn("Fast Learner", badges)
        self.assertEqual(len(badges), 3)
        self.assertEqual(user.total_points, 75)

    def test_leaderboard_route(self):
        """Test the leaderboard page renders top scholars and rankings."""
        res = self.client.get("/leaderboard")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Academic Leaderboard", res.data)
        self.assertIn(b"Test Scholar", res.data)
        self.assertIn(b"50", res.data)

    def test_flashcards_deck_and_study_flow(self):
        """Test flashcard deck creation, viewing, and mastery toggle."""
        deck = FlashcardDeck(
            user_id=self.user.id,
            title="Physics Formulas",
            topic="Motion and Force",
            class_level="Class 10",
        )
        db.session.add(deck)
        db.session.commit()

        card = Flashcard(
            deck_id=deck.id,
            front_question="What is Newton's Second Law?",
            back_answer="F = m * a",
        )
        db.session.add(card)
        db.session.commit()

        # Check index
        res = self.client.get("/flashcards/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Physics Formulas", res.data)

        # Check study view
        res = self.client.get(f"/flashcards/deck/{deck.id}")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"What is Newton", res.data)

        # Toggle card mastery
        toggle_res = self.client.post(f"/flashcards/card/{card.id}/toggle")
        self.assertEqual(toggle_res.status_code, 200)
        data = toggle_res.get_json()
        self.assertTrue(data["is_mastered"])

    def test_creative_question_view(self):
        """Test Creative Question viewing with model answers."""
        cq = CreativeQuestion(
            user_id=self.user.id,
            class_level="Class 10",
            subject_name="Chemistry",
            chapter_topic="Periodic Table",
            stimulus="Element A has atomic number 11 and Element B has atomic number 17.",
            question_a="What is an octet rule?",
            answer_a="Atoms combine to form 8 valence electrons.",
            question_b="Explain ionic bonding.",
            answer_b="Electrostatic attraction between cations and anions.",
            question_c="Draw the bonding of AB.",
            answer_c="Na+ and Cl- transfer 1 electron.",
            question_d="Analyze conductivity.",
            answer_d="Conducts electricity in molten or aqueous state.",
        )
        db.session.add(cq)
        db.session.commit()

        res = self.client.get(f"/cq/view/{cq.id}")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Periodic Table", res.data)
        self.assertIn(b"What is an octet rule?", res.data)
        self.assertIn(b"Element A has atomic number 11", res.data)

    def test_exam_goal_countdown(self):
        """Test exam goal countdown logic and planner integration."""
        target_date = date.today() + timedelta(days=45)
        goal = ExamGoal(
            user_id=self.user.id,
            title="SSC Board Exam 2027",
            class_level="Class 10",
            exam_date=target_date,
            target_grade="GPA 5.00 (A+)",
        )
        db.session.add(goal)
        db.session.commit()

        self.assertEqual(goal.days_remaining(), 45)

        # Check planner view
        res = self.client.get("/planner/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"SSC Board Exam 2027", res.data)
        self.assertIn(b"Pomodoro Focus Timer", res.data)

    def test_note_summarize_endpoint(self):
        """Test AI note summarizer endpoint."""
        note = Note(
            user_id=self.user.id,
            title="Operating Systems Memory Management",
            content="Virtual memory allows executing processes that are not completely in physical RAM through paging and swapping algorithms.",
            category="Lecture",
        )
        db.session.add(note)
        db.session.commit()

        res = self.client.post(f"/notes/{note.id}/summarize")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("summary", data)

    def test_quiz_certificate_generation(self):
        """Test official quiz completion certificate route."""
        quiz = Quiz(
            title="General Science Diagnostic",
            topic="Diagnostic Test",
            class_level="Class 10",
            user_id=self.user.id,
        )
        db.session.add(quiz)
        db.session.commit()

        attempt = QuizAttempt(
            quiz_id=quiz.id,
            user_id=self.user.id,
            score=9,
            total_score=10,
            percentage=90.0,
        )
        db.session.add(attempt)
        db.session.commit()

        res = self.client.get(f"/quiz/certificate/{attempt.id}")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Certificate of Academic Achievement", res.data)
        self.assertIn(b"Test Scholar", res.data)
        self.assertIn(b"General Science Diagnostic", res.data)
        self.assertIn(b"90.0%", res.data)

    def test_student_cannot_add_cq_or_assignment_or_quiz(self):
        """Verify that students cannot generate CQ, add assignments, or generate quizzes."""
        # 1. Student attempting to generate CQ
        cq_res = self.client.post(
            "/cq/generate",
            data={"class_level": "Class 10", "curriculum_subject": "Physics", "topic": "Motion"},
            follow_redirects=True,
        )
        self.assertIn(b"Only administrators have permission to generate or add new Creative Questions", cq_res.data)

        # 2. Student attempting to add assignment
        assign_res = self.client.post(
            "/assignments/",
            data={"action": "create", "title": "Illegal Homework", "due_date": "2027-01-01"},
            follow_redirects=True,
        )
        self.assertIn(b"Only administrators have permission to add new coursework assignments", assign_res.data)

        # 3. Student attempting to generate quiz
        quiz_res = self.client.post(
            "/quiz/generate",
            data={"topic": "Unauthorized Quiz", "difficulty": "easy", "count": "5"},
            follow_redirects=True,
        )
        self.assertIn(b"Only administrators have permission to generate or add new quizzes", quiz_res.data)

    def test_class_5_quizzes_present(self):
        """Test that Class 5 quizzes are seeded and displayed in quiz catalog."""
        res = self.client.get("/quiz/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Class 5", res.data)
        self.assertIn(b"Primary Science", res.data)


if __name__ == "__main__":
    unittest.main()
