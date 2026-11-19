"""Smart Study Planner Blueprint Routes.

Manages task scheduling, prioritization, deadlines, status transitions,
and daily/weekly study planner views.
"""

from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.task import StudyTask
from app.models.subject import Subject
from app.utils.auth import login_required, log_activity, get_current_user

planner_bp = Blueprint("planner", __name__, url_prefix="/planner")


@planner_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    """List and manage study planner tasks with filtering options."""
    user = get_current_user()

    if request.method == "POST":
        action = request.form.get("action", "create")

        if action == "create":
            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            subject_id = request.form.get("subject_id")
            priority = request.form.get("priority", "medium")
            due_date_str = request.form.get("due_date", "")

            if not title:
                flash("Task title is required.", "danger")
            else:
                due_date = None
                if due_date_str:
                    try:
                        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                    except ValueError:
                        due_date = None

                new_task = StudyTask(
                    user_id=user.id,
                    subject_id=int(subject_id) if subject_id else None,
                    title=title,
                    description=description,
                    priority=priority if priority in ["low", "medium", "high"] else "medium",
                    due_date=due_date,
                    status="pending",
                )
                db.session.add(new_task)
                db.session.commit()
                log_activity(f"Created study task '{title}'", "Planner", user.id)
                flash(f"Task '{title}' scheduled successfully.", "success")

        elif action == "delete":
            task_id = request.form.get("task_id")
            task = StudyTask.query.filter_by(id=task_id, user_id=user.id).first()
            if task:
                title = task.title
                db.session.delete(task)
                db.session.commit()
                log_activity(f"Deleted task '{title}'", "Planner", user.id)
                flash("Task deleted.", "info")

        return redirect(url_for("planner.index"))

    # Filtering logic
    filter_status = request.args.get("status", "all")
    filter_priority = request.args.get("priority", "all")
    filter_timeframe = request.args.get("timeframe", "all")  # 'today', 'week', 'all'

    query = StudyTask.query.filter_by(user_id=user.id)

    if filter_status in ["pending", "in_progress", "completed"]:
        query = query.filter_by(status=filter_status)

    if filter_priority in ["low", "medium", "high"]:
        query = query.filter_by(priority=filter_priority)

    today = date.today()
    if filter_timeframe == "today":
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        query = query.filter(StudyTask.due_date.between(start_of_day, end_of_day))
    elif filter_timeframe == "week":
        end_of_week = datetime.combine(today + timedelta(days=7), datetime.max.time())
        start_of_day = datetime.combine(today, datetime.min.time())
        query = query.filter(StudyTask.due_date.between(start_of_day, end_of_week))

    tasks = query.order_by(StudyTask.due_date.asc().nullslast(), StudyTask.created_at.desc()).all()
    subjects = Subject.query.filter_by(user_id=user.id).all()

    # Progress stats
    total_count = StudyTask.query.filter_by(user_id=user.id).count()
    completed_count = StudyTask.query.filter_by(user_id=user.id, status="completed").count()
    completion_rate = round((completed_count / total_count * 100), 1) if total_count > 0 else 0

    return render_template(
        "planner/index.html",
        user=user,
        tasks=tasks,
        subjects=subjects,
        current_status=filter_status,
        current_priority=filter_priority,
        current_timeframe=filter_timeframe,
        total_count=total_count,
        completed_count=completed_count,
        completion_rate=completion_rate,
    )


@planner_bp.route("/<int:task_id>/toggle", methods=["POST"])
@login_required
def toggle_status(task_id):
    """Toggle a task status between pending and completed."""
    user = get_current_user()
    task = StudyTask.query.filter_by(id=task_id, user_id=user.id).first_or_404()

    new_status = request.form.get("status")
    if new_status in ["pending", "in_progress", "completed"]:
        task.status = new_status
    else:
        task.status = "completed" if task.status != "completed" else "pending"

    db.session.commit()
    log_activity(f"Updated task #{task.id} status to '{task.status}'", "Planner", user.id)
    return redirect(request.referrer or url_for("planner.index"))
