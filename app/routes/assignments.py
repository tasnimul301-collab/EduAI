"""Assignment Management Blueprint Routes.

Handles academic assignments, submission tracking, deadline calculation,
priority tagging, and reminder alerts.
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.assignment import Assignment
from app.models.subject import Subject
from app.models.notification import Notification
from app.utils.auth import login_required, log_activity, get_current_user

assignments_bp = Blueprint("assignments", __name__, url_prefix="/assignments")


@assignments_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    """List and filter academic assignments; handle creation of new assignments."""
    user = get_current_user()

    if request.method == "POST":
        action = request.form.get("action", "create")

        if action == "create":
            if user.role != "admin":
                flash("Only administrators have permission to add new coursework assignments.", "danger")
                return redirect(url_for("assignments.index"))

            title = request.form.get("title", "").strip()
            description = request.form.get("description", "").strip()
            subject_id = request.form.get("subject_id")
            priority = request.form.get("priority", "medium")
            due_date_str = request.form.get("due_date", "")

            if not title or not due_date_str:
                flash("Assignment title and due date are required.", "danger")
            else:
                try:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M")
                except ValueError:
                    try:
                        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                    except ValueError:
                        due_date = datetime.utcnow()

                new_assignment = Assignment(
                    user_id=user.id,
                    subject_id=int(subject_id) if subject_id and subject_id.isdigit() else None,
                    title=title,
                    description=description,
                    priority=priority if priority in ["low", "medium", "high"] else "medium",
                    due_date=due_date,
                    status="pending",
                )
                db.session.add(new_assignment)

                # Add automatic deadline notification reminder for all students
                from app.models.user import User
                all_students = User.query.filter_by(role="student").all()
                for st in all_students:
                    reminder = Notification(
                        user_id=st.id,
                        title=f"New Assignment: {title}",
                        message=f"Due on {due_date.strftime('%b %d, %Y at %I:%M %p')}. Stay on schedule!",
                        type="deadline",
                    )
                    db.session.add(reminder)

                # Also add for admin
                reminder_admin = Notification(
                    user_id=user.id,
                    title=f"New Assignment: {title}",
                    message=f"Due on {due_date.strftime('%b %d, %Y at %I:%M %p')}.",
                    type="deadline",
                )
                db.session.add(reminder_admin)

                db.session.commit()
                log_activity(f"Created assignment '{title}'", "Assignments", user.id)
                flash("Assignment added successfully!", "success")

        elif action == "delete":
            if user.role != "admin":
                flash("Only administrators have permission to delete assignments.", "danger")
                return redirect(url_for("assignments.index"))

            assignment_id = request.form.get("assignment_id")
            assignment = Assignment.query.filter_by(id=assignment_id).first()
            if assignment:
                title = assignment.title
                db.session.delete(assignment)
                db.session.commit()
                log_activity(f"Deleted assignment '{title}'", "Assignments", user.id)
                flash(f"Assignment '{title}' deleted.", "info")

        return redirect(url_for("assignments.index"))

    filter_status = request.args.get("status", "all")
    if user.role == "admin":
        query = Assignment.query
    else:
        from app.models.user import User
        admin_ids = [u.id for u in User.query.filter_by(role="admin").all()]
        query = Assignment.query.filter((Assignment.user_id == user.id) | (Assignment.user_id.in_(admin_ids)))

    if filter_status == "pending":
        query = query.filter_by(status="pending")
    elif filter_status == "submitted":
        query = query.filter_by(status="submitted")
    elif filter_status == "overdue":
        query = query.filter(Assignment.status == "pending", Assignment.due_date < datetime.utcnow())

    assignments = query.order_by(Assignment.due_date.asc()).all()
    subjects = Subject.query.filter_by(user_id=user.id).all() if user.role != "admin" else Subject.query.all()

    return render_template(
        "assignments/index.html",
        user=user,
        assignments=assignments,
        subjects=subjects,
        current_filter=filter_status,
    )


@assignments_bp.route("/<int:assignment_id>/toggle", methods=["POST"])
@login_required
def toggle_status(assignment_id):
    """Toggle an assignment status between pending and submitted."""
    user = get_current_user()
    assignment = Assignment.query.filter_by(id=assignment_id).first_or_404()

    if assignment.status == "submitted":
        assignment.status = "pending"
    else:
        assignment.status = "submitted"

    db.session.commit()
    log_activity(f"Updated assignment #{assignment.id} status to '{assignment.status}'", "Assignments", user.id)
    flash(f"Assignment marked as {assignment.status}.", "success")
    return redirect(request.referrer or url_for("assignments.index"))
