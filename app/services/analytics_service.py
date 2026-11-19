"""Analytics Service Module.

Computes academic metrics, study hour aggregations, task completion velocities,
and prepares datasets formatted for Chart.js visual graphs.
"""

from datetime import datetime, timedelta, date
from sqlalchemy import func
from app.extensions import db
from app.models.subject import Subject
from app.models.task import StudyTask
from app.models.assignment import Assignment
from app.models.quiz import QuizAttempt
from app.models.study_session import StudySession
from app.models.activity_log import ActivityLog


class AnalyticsService:
    """Service class delivering calculated statistics for student and admin dashboards."""

    @staticmethod
    def get_student_dashboard_metrics(user_id: int) -> dict:
        """Aggregate high-level overview metrics for the student dashboard."""
        # 1. Total Subjects
        total_subjects = Subject.query.filter_by(user_id=user_id).count()

        # 2. Pending Assignments
        pending_assignments = Assignment.query.filter_by(
            user_id=user_id, status="pending"
        ).count()

        # 3. Tasks Metrics
        total_tasks = StudyTask.query.filter_by(user_id=user_id).count()
        completed_tasks = StudyTask.query.filter_by(
            user_id=user_id, status="completed"
        ).count()

        # 4. Total Study Hours
        total_minutes = (
            db.session.query(func.coalesce(func.sum(StudySession.duration_minutes), 0))
            .filter(StudySession.user_id == user_id)
            .scalar()
        )
        study_hours = round(total_minutes / 60.0, 1)

        # 5. Average Quiz Score
        avg_score = (
            db.session.query(func.coalesce(func.avg(QuizAttempt.percentage), 0))
            .filter(QuizAttempt.user_id == user_id)
            .scalar()
        )
        avg_quiz_score = round(float(avg_score), 1)

        # 6. Upcoming Deadlines (Assignments due in future)
        now = datetime.utcnow()
        upcoming_assignments = (
            Assignment.query.filter(
                Assignment.user_id == user_id,
                Assignment.status == "pending",
                Assignment.due_date >= now,
            )
            .order_by(Assignment.due_date.asc())
            .limit(5)
            .all()
        )

        # 7. Recent Activity Logs
        recent_activities = (
            ActivityLog.query.filter_by(user_id=user_id)
            .order_by(ActivityLog.timestamp.desc())
            .limit(5)
            .all()
        )

        # 8. Weekly Study Hours (Last 7 days)
        today = date.today()
        seven_days_ago = today - timedelta(days=6)
        daily_sessions = (
            db.session.query(
                StudySession.session_date,
                func.sum(StudySession.duration_minutes).label("total_mins"),
            )
            .filter(
                StudySession.user_id == user_id,
                StudySession.session_date >= seven_days_ago,
            )
            .group_by(StudySession.session_date)
            .all()
        )

        # Map to 7 distinct days
        day_map = {row.session_date: round(row.total_mins / 60.0, 2) for row in daily_sessions}
        weekly_labels = []
        weekly_hours = []
        for i in range(7):
            d = seven_days_ago + timedelta(days=i)
            weekly_labels.append(d.strftime("%a (%b %d)"))
            weekly_hours.append(day_map.get(d, 0.0))

        # 9. Subject-wise Study Distribution
        subject_sessions = (
            db.session.query(
                Subject.name,
                func.coalesce(func.sum(StudySession.duration_minutes), 0).label("minutes"),
            )
            .join(StudySession, Subject.id == StudySession.subject_id)
            .filter(Subject.user_id == user_id)
            .group_by(Subject.name)
            .all()
        )
        subject_labels = [row.name for row in subject_sessions]
        subject_hours = [round(row.minutes / 60.0, 1) for row in subject_sessions]

        # 10. Recent Quiz Scores Trend (last 6 attempts)
        recent_quizzes = (
            QuizAttempt.query.filter_by(user_id=user_id)
            .order_by(QuizAttempt.completed_at.desc())
            .limit(6)
            .all()
        )
        recent_quizzes.reverse()  # Chronological order
        quiz_trend_labels = [q.quiz.title[:15] + "..." if len(q.quiz.title) > 15 else q.quiz.title for q in recent_quizzes]
        quiz_trend_scores = [q.percentage for q in recent_quizzes]

        return {
            "total_subjects": total_subjects,
            "pending_assignments": pending_assignments,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "study_hours": study_hours,
            "avg_quiz_score": avg_quiz_score,
            "upcoming_assignments": upcoming_assignments,
            "recent_activities": recent_activities,
            "charts": {
                "weekly_labels": weekly_labels,
                "weekly_hours": weekly_hours,
                "subject_labels": subject_labels,
                "subject_hours": subject_hours,
                "quiz_trend_labels": quiz_trend_labels,
                "quiz_trend_scores": quiz_trend_scores,
            },
        }

    @staticmethod
    def get_admin_metrics() -> dict:
        """Aggregate institutional metrics for the Administrator dashboard."""
        from app.models.user import User
        from app.models.quiz import Quiz
        from app.models.note import Note

        total_users = User.query.count()
        student_count = User.query.filter_by(role="student").count()
        admin_count = User.query.filter_by(role="admin").count()
        active_users = User.query.filter_by(is_active=True).count()

        total_quizzes = Quiz.query.count()
        total_notes = Note.query.count()
        total_attempts = QuizAttempt.query.count()

        recent_logs = (
            ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(15).all()
        )

        all_users = User.query.order_by(User.created_at.desc()).all()

        return {
            "total_users": total_users,
            "student_count": student_count,
            "admin_count": admin_count,
            "active_users": active_users,
            "total_quizzes": total_quizzes,
            "total_notes": total_notes,
            "total_attempts": total_attempts,
            "recent_logs": recent_logs,
            "all_users": all_users,
        }
