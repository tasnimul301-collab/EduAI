"""Assignment Management Blueprint Routes.

Handles academic assignments, Word (.docx, .doc) & PDF (.pdf) student submissions,
deadline calculation, priority tagging, and instructor review.
"""

import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app,
    send_from_directory,
)
from app.extensions import db
from app.models.assignment import Assignment
from app.models.assignment_submission import AssignmentSubmission
from app.models.subject import Subject
from app.models.notification import Notification
from app.utils.auth import login_required, log_activity, get_current_user

assignments_bp = Blueprint("assignments", __name__, url_prefix="/assignments")

ALLOWED_ASSIGNMENT_EXTENSIONS = {"pdf", "docx", "doc"}


def allowed_assignment_file(filename: str) -> bool:
    """Verify that uploaded coursework file is a valid Word document or PDF."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_ASSIGNMENT_EXTENSIONS


@assignments_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    """List and filter academic assignments; handle creation and deletion by admin."""
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

                db.session.commit()
                log_activity(f"Created assignment '{title}'", "Assignments", user.id)
                flash(f"Assignment '{title}' added successfully!", "success")

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

    all_assignments = query.order_by(Assignment.due_date.asc()).all()

    # Build mapping of current student's submissions
    student_submissions = {}
    if user.role != "admin":
        subs = AssignmentSubmission.query.filter_by(user_id=user.id).all()
        student_submissions = {s.assignment_id: s for s in subs}

    filtered_assignments = []
    for a in all_assignments:
        user_sub = student_submissions.get(a.id)
        is_submitted = (user_sub is not None) or (a.status == "submitted" and user.role != "admin")
        is_overdue = (not is_submitted) and (datetime.utcnow() > a.due_date)

        # Attach computed metadata for Jinja templates
        a.user_submission = user_sub
        a.user_is_submitted = is_submitted
        a.user_is_overdue = is_overdue

        if filter_status == "pending" and not is_submitted:
            filtered_assignments.append(a)
        elif filter_status == "submitted" and is_submitted:
            filtered_assignments.append(a)
        elif filter_status == "overdue" and is_overdue:
            filtered_assignments.append(a)
        elif filter_status == "all":
            filtered_assignments.append(a)

    subjects = Subject.query.filter_by(user_id=user.id).all() if user.role != "admin" else Subject.query.all()

    return render_template(
        "assignments/index.html",
        user=user,
        assignments=filtered_assignments,
        subjects=subjects,
        current_filter=filter_status,
    )


@assignments_bp.route("/<int:assignment_id>/submit", methods=["POST"])
@login_required
def submit_file(assignment_id):
    """Handle student coursework submission with Word (.docx, .doc) or PDF (.pdf) file."""
    user = get_current_user()
    if user.role == "admin":
        flash("Administrators do not need to submit coursework.", "info")
        return redirect(url_for("assignments.index"))

    assignment = Assignment.query.filter_by(id=assignment_id).first_or_404()
    file = request.files.get("submission_file")
    notes = request.form.get("submission_notes", "").strip()

    if not file or not file.filename:
        flash("Please choose a Word (.docx, .doc) or PDF (.pdf) file to submit.", "warning")
        return redirect(url_for("assignments.index"))

    if not allowed_assignment_file(file.filename):
        flash("Invalid file format! Only Word (.docx, .doc) and PDF (.pdf) files are supported.", "danger")
        return redirect(url_for("assignments.index"))

    # Secure filename and directory setup
    original_filename = secure_filename(file.filename)
    ext = original_filename.rsplit(".", 1)[1].lower() if "." in original_filename else "pdf"
    unique_filename = f"user_{user.id}_assign_{assignment.id}_{int(datetime.utcnow().timestamp())}_{original_filename}"

    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "assignments")
    os.makedirs(upload_dir, exist_ok=True)
    full_save_path = os.path.join(upload_dir, unique_filename)
    file.save(full_save_path)
    file_size = os.path.getsize(full_save_path)

    # Upsert submission record
    existing_sub = AssignmentSubmission.query.filter_by(
        assignment_id=assignment.id, user_id=user.id
    ).first()

    if existing_sub:
        existing_sub.file_path = unique_filename
        existing_sub.original_filename = original_filename
        existing_sub.file_type = ext
        existing_sub.file_size = file_size
        existing_sub.submission_notes = notes
        existing_sub.submitted_at = datetime.utcnow()
    else:
        new_sub = AssignmentSubmission(
            assignment_id=assignment.id,
            user_id=user.id,
            file_path=unique_filename,
            original_filename=original_filename,
            file_type=ext,
            file_size=file_size,
            submission_notes=notes,
        )
        db.session.add(new_sub)
        user.total_points += 20
        user.add_badge("Assignment Pro")

    assignment.status = "submitted"
    db.session.commit()

    log_activity(f"Submitted coursework file '{original_filename}' for '{assignment.title}'", "Assignments", user.id)
    flash(f"Coursework submitted successfully! (Attached: {original_filename})", "success")
    return redirect(url_for("assignments.index"))


@assignments_bp.route("/download/<int:submission_id>")
@login_required
def download_submission(submission_id):
    """Download submitted coursework file for reviewing student or administrator."""
    user = get_current_user()
    submission = AssignmentSubmission.query.filter_by(id=submission_id).first_or_404()

    # Security check: User must be either the owner student or an admin
    if user.role != "admin" and submission.user_id != user.id:
        flash("You do not have permission to download this coursework file.", "danger")
        return redirect(url_for("assignments.index"))

    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "assignments")
    return send_from_directory(
        upload_dir,
        submission.file_path,
        as_attachment=True,
        download_name=submission.original_filename,
    )


@assignments_bp.route("/<int:assignment_id>/unsubmit", methods=["POST"])
@login_required
def unsubmit(assignment_id):
    """Allow student to withdraw a submission to replace or edit the file."""
    user = get_current_user()
    assignment = Assignment.query.filter_by(id=assignment_id).first_or_404()
    submission = AssignmentSubmission.query.filter_by(
        assignment_id=assignment.id, user_id=user.id
    ).first()

    if submission:
        db.session.delete(submission)
        assignment.status = "pending"
        db.session.commit()
        log_activity(f"Unsubmitted coursework for '{assignment.title}'", "Assignments", user.id)
        flash("Assignment unsubmitted. You can now upload a revised file.", "info")

    return redirect(url_for("assignments.index"))


@assignments_bp.route("/<int:assignment_id>/toggle", methods=["POST"])
@login_required
def toggle_status(assignment_id):
    """Quick toggle an assignment status between pending and submitted."""
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
