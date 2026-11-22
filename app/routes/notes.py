"""Digital Notes and Document Manager Blueprint Routes.

Handles creating, editing, categorizing, searching notes,
uploading PDF attachments, and secure document serving.
"""

import os
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
    send_from_directory,
    abort,
)
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models.note import Note, UploadedFile
from app.models.subject import Subject
from app.utils.auth import login_required, log_activity, get_current_user

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


def allowed_file(filename: str) -> bool:
    """Check if uploaded file has an allowed extension (.pdf)."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


@notes_bp.route("/")
@login_required
def index():
    """List notes with search, subject filter, and category filter."""
    user = get_current_user()
    search_query = request.args.get("q", "").strip()
    category_filter = request.args.get("category", "all")
    subject_filter = request.args.get("subject_id", "all")

    # All students and administrators can view all notes created by administrators/instructors
    query = Note.query

    if search_query:
        query = query.filter(
            (Note.title.ilike(f"%{search_query}%"))
            | (Note.content.ilike(f"%{search_query}%"))
        )

    if category_filter in ["Lecture", "Revision", "Formula", "General"]:
        query = query.filter_by(category=category_filter)

    if subject_filter.isdigit():
        query = query.filter_by(subject_id=int(subject_filter))

    notes = query.order_by(Note.updated_at.desc()).all()
    subjects = Subject.query.order_by(Subject.name.asc()).all()

    return render_template(
        "notes/index.html",
        user=user,
        notes=notes,
        subjects=subjects,
        search_query=search_query,
        category_filter=category_filter,
        subject_filter=subject_filter,
    )


@notes_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a new digital study note with optional PDF attachment (Admin only)."""
    user = get_current_user()
    if user.role != "admin":
        flash("Only administrators have permission to create and upload study notes.", "danger")
        return redirect(url_for("notes.index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        subject_id = request.form.get("subject_id")
        category = request.form.get("category", "Lecture")
        pdf_file = request.files.get("pdf_file")

        if not title or not content:
            flash("Note title and content are required.", "danger")
            subjects = Subject.query.order_by(Subject.name.asc()).all()
            return render_template("notes/create.html", subjects=subjects, title=title, content=content)

        new_note = Note(
            user_id=user.id,
            subject_id=int(subject_id) if subject_id and subject_id.isdigit() else None,
            title=title,
            content=content,
            category=category if category in ["Lecture", "Revision", "Formula", "General"] else "Lecture",
        )
        db.session.add(new_note)
        db.session.flush()  # Generates note id

        # Handle optional PDF file upload
        if pdf_file and pdf_file.filename:
            if not allowed_file(pdf_file.filename):
                flash("Only PDF (.pdf) documents are permitted.", "warning")
            else:
                original_filename = secure_filename(pdf_file.filename)
                unique_filename = f"user_{user.id}_note_{new_note.id}_{original_filename}"
                save_dir = current_app.config["UPLOAD_FOLDER"]
                os.makedirs(save_dir, exist_ok=True)
                save_path = os.path.join(save_dir, unique_filename)

                pdf_file.save(save_path)
                file_size = os.path.getsize(save_path)

                uploaded = UploadedFile(
                    note_id=new_note.id,
                    user_id=user.id,
                    filename=original_filename,
                    file_path=unique_filename,
                    file_size=file_size,
                )
                db.session.add(uploaded)

        db.session.commit()
        log_activity(f"Created note '{title}'", "Notes", user.id)
        flash("Note created successfully!", "success")
        return redirect(url_for("notes.view", note_id=new_note.id))

    subjects = Subject.query.order_by(Subject.name.asc()).all()
    return render_template("notes/create.html", subjects=subjects)


@notes_bp.route("/<int:note_id>")
@login_required
def view(note_id):
    """View a single note and its attachments (Students and Admins)."""
    user = get_current_user()
    note = Note.query.filter_by(id=note_id).first_or_404()
    return render_template("notes/view.html", user=user, note=note)


@notes_bp.route("/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit(note_id):
    """Edit an existing note (Admin only)."""
    user = get_current_user()
    if user.role != "admin":
        flash("Only administrators have permission to edit study notes.", "danger")
        return redirect(url_for("notes.view", note_id=note_id))

    note = Note.query.filter_by(id=note_id).first_or_404()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        subject_id = request.form.get("subject_id")
        category = request.form.get("category", "Lecture")

        if not title or not content:
            flash("Title and content cannot be blank.", "danger")
        else:
            note.title = title
            note.content = content
            note.subject_id = int(subject_id) if subject_id and subject_id.isdigit() else None
            note.category = category
            db.session.commit()
            log_activity(f"Edited note #{note.id}", "Notes", user.id)
            flash("Note updated successfully.", "success")
            return redirect(url_for("notes.view", note_id=note.id))

    subjects = Subject.query.order_by(Subject.name.asc()).all()
    return render_template("notes/edit.html", user=user, note=note, subjects=subjects)


@notes_bp.route("/<int:note_id>/delete", methods=["POST"])
@login_required
def delete(note_id):
    """Delete a note and any attached files (Admin only)."""
    user = get_current_user()
    if user.role != "admin":
        flash("Only administrators have permission to delete study notes.", "danger")
        return redirect(url_for("notes.index"))

    note = Note.query.filter_by(id=note_id).first_or_404()
    title = note.title

    # Remove attached files from disk
    for file_record in note.files:
        try:
            full_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file_record.file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        except OSError:
            pass

    db.session.delete(note)
    db.session.commit()
    log_activity(f"Deleted note '{title}'", "Notes", user.id)
    flash("Note deleted successfully.", "info")
    return redirect(url_for("notes.index"))


@notes_bp.route("/download/<int:file_id>")
@login_required
def download_file(file_id):
    """Download or view an uploaded PDF securely (Students and Admins)."""
    user = get_current_user()
    file_record = UploadedFile.query.filter_by(id=file_id).first_or_404()
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        file_record.file_path,
        as_attachment=True,
        download_name=file_record.filename,
    )


@notes_bp.route("/<int:note_id>/summarize", methods=["POST"])
@login_required
def summarize(note_id):
    """Summarize note with AI and return high-yield exam takeaways."""
    from flask import jsonify
    from app.services.ai_service import AIService
    user = get_current_user()
    note = Note.query.filter_by(id=note_id).first_or_404()

    result = AIService.summarize_note(note.title, note.content)
    if result.get("success"):
        user.total_points += 10
        user.add_badge("Smart Note Taker")
        db.session.commit()
    return jsonify(result)
