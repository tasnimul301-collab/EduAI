"""Dashboard Blueprint Routes.

Handles landing page routing, student dashboard overview,
course/subject management, study session logging, and notifications.
"""

import os
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    session,
    jsonify,
    send_from_directory,
    current_app,
)
from app.extensions import db
from app.models.subject import Subject
from app.models.notification import Notification
from app.models.study_session import StudySession
from app.services.analytics_service import AnalyticsService
from app.utils.auth import login_required, log_activity, get_current_user
from app.utils.curriculum import seed_class_subjects_for_user

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/favicon.ico")
def favicon():
    """Serve the platform favicon."""
    return send_from_directory(
        os.path.join(current_app.root_path, "static"),
        "favicon.svg",
        mimetype="image/svg+xml",
    )


@dashboard_bp.route("/")
def index():
    """Landing page for visitors; redirects authenticated users to their dashboard."""
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard"))
    return render_template("landing.html")


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    """Primary student dashboard displaying KPIs, deadlines, streaks, and Chart.js analytics."""
    user = get_current_user()
    user.update_streak()
    db.session.commit()

    from app.models.exam_goal import ExamGoal
    exam_goal = ExamGoal.query.filter_by(user_id=user.id).order_by(ExamGoal.exam_date.asc()).first()
    metrics = AnalyticsService.get_student_dashboard_metrics(user.id)
    subjects = Subject.query.filter_by(user_id=user.id).all()

    return render_template(
        "dashboard/index.html",
        user=user,
        metrics=metrics,
        subjects=subjects,
        exam_goal=exam_goal,
    )


@dashboard_bp.route("/leaderboard")
@login_required
def leaderboard():
    """Display real-time student leaderboard, points, and achievement rankings."""
    user = get_current_user()
    user.update_streak()
    db.session.commit()

    from app.models.user import User
    top_students = (
        User.query.filter_by(role="student")
        .order_by(User.total_points.desc(), User.streak_count.desc())
        .limit(25)
        .all()
    )

    return render_template(
        "dashboard/leaderboard.html",
        user=user,
        top_students=top_students,
    )


@dashboard_bp.route("/subjects", methods=["GET", "POST"])
@login_required
def subjects():
    """Manage academic courses and subjects."""
    user = get_current_user()
    # Ensure Class 6 through Class 12 curriculum subjects are seeded for the student
    seed_class_subjects_for_user(user.id)

    if request.method == "POST":
        action = request.form.get("action", "create")

        if action == "create":
            name = request.form.get("name", "").strip()
            code = request.form.get("code", "").strip().upper()
            class_level = request.form.get("class_level", "General").strip()
            color_hex = request.form.get("color_hex", "#4F46E5").strip()

            if not name:
                flash("Subject name is required.", "danger")
            else:
                new_subject = Subject(
                    user_id=user.id,
                    name=name,
                    code=code or None,
                    class_level=class_level,
                    color_hex=color_hex,
                )
                db.session.add(new_subject)
                db.session.commit()
                log_activity(f"Created subject '{name}'", "Subjects", user.id)
                flash(f"Subject '{name}' created successfully.", "success")

        elif action == "delete":
            subject_id = request.form.get("subject_id")
            subject = Subject.query.filter_by(id=subject_id, user_id=user.id).first()
            if subject:
                name = subject.name
                db.session.delete(subject)
                db.session.commit()
                log_activity(f"Deleted subject '{name}'", "Subjects", user.id)
                flash(f"Subject '{name}' deleted.", "info")

        return redirect(url_for("dashboard.subjects"))

    all_subjects = Subject.query.filter_by(user_id=user.id).order_by(Subject.name.asc()).all()
    return render_template("dashboard/subjects.html", user=user, subjects=all_subjects)


@dashboard_bp.route("/study-session/log", methods=["POST"])
@login_required
def log_study_session():
    """Log a completed study session to update study hours immediately."""
    user = get_current_user()
    subject_id = request.form.get("subject_id")
    duration = request.form.get("duration_minutes", 30)
    notes = request.form.get("notes", "").strip()

    try:
        duration_int = int(duration)
        if duration_int <= 0:
            duration_int = 30
    except ValueError:
        duration_int = 30

    session_log = StudySession(
        user_id=user.id,
        subject_id=int(subject_id) if subject_id and str(subject_id).isdigit() else None,
        duration_minutes=duration_int,
        notes=notes,
    )
    db.session.add(session_log)
    db.session.commit()

    log_activity(f"Logged {duration_int} mins study session", "Analytics", user.id)
    flash(f"Logged {duration_int} minutes of study time!", "success")
    return redirect(request.referrer or url_for("dashboard.dashboard"))


@dashboard_bp.route("/notifications")
@login_required
def notifications():
    """List student in-app notifications."""
    user = get_current_user()
    user_notifications = (
        Notification.query.filter_by(user_id=user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return render_template(
        "dashboard/notifications.html",
        user=user,
        notifications=user_notifications,
    )


@dashboard_bp.route("/notifications/<int:notification_id>/read", methods=["POST"])
@login_required
def mark_notification_read(notification_id):
    """Mark a notification as read."""
    user = get_current_user()
    notif = Notification.query.filter_by(id=notification_id, user_id=user.id).first_or_404()
    notif.mark_as_read()
    db.session.commit()
    return redirect(url_for("dashboard.notifications"))
