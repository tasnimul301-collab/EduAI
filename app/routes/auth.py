"""Authentication Blueprint Routes.

Handles user registration, login, logout, profile management,
password hashing, and session validation.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.user import User
from app.utils.auth import login_required, log_activity, get_current_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register a new student or administrator account."""
    if "user_id" in session:
        user = get_current_user()
        if user:
            return redirect(url_for("dashboard.index"))
        session.clear()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        full_name = request.form.get("full_name", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "student")

        # Basic input validations
        if not username or not email or not password:
            flash("Username, email, and password are required.", "danger")
            return render_template("auth/register.html", username=username, email=email, full_name=full_name)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("auth/register.html", username=username, email=email, full_name=full_name)

        if password != confirm_password:
            flash("Passwords do not match. Please re-enter.", "danger")
            return render_template("auth/register.html", username=username, email=email, full_name=full_name)

        # Check for existing username or email
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            if existing_user.username == username:
                flash("Username is already taken. Please choose another.", "danger")
            else:
                flash("An account with this email already exists.", "danger")
            return render_template("auth/register.html", username=username, email=email, full_name=full_name)

        # Only allow 'admin' or 'student'
        if role not in ["student", "admin"]:
            role = "student"

        # Create and persist new user
        new_user = User(
            username=username,
            email=email,
            full_name=full_name or username.title(),
            role=role,
        )
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        # Seed pre-built curriculum quizzes and subjects for Class 6 to 12
        try:
            from app.utils.curriculum import seed_class_quizzes_for_user, seed_class_subjects_for_user
            seed_class_quizzes_for_user(new_user.id)
            seed_class_subjects_for_user(new_user.id)
        except Exception:
            db.session.rollback()

        log_activity(f"User registered with role: {role}", "Auth", new_user.id)
        flash("Registration successful! You may now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate existing users and initialize session."""
    if "user_id" in session:
        user = get_current_user()
        if user:
            return redirect(url_for("dashboard.index"))
        session.clear()

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")
        next_url = request.args.get("next")

        if not identifier or not password:
            flash("Please provide both identifier and password.", "danger")
            return render_template("auth/login.html", identifier=identifier)

        # Look up by username OR email
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()

        if not user or not user.check_password(password):
            flash("Invalid credentials. Please verify your login details.", "danger")
            return render_template("auth/login.html", identifier=identifier)

        if not user.is_active:
            flash("Your account has been deactivated. Please contact an administrator.", "warning")
            return render_template("auth/login.html")

        # Set session attributes
        session.clear()
        session["user_id"] = user.id
        session["username"] = user.username
        session["full_name"] = user.full_name or user.username
        session["role"] = user.role

        log_activity("User logged in successfully", "Auth", user.id)
        flash(f"Welcome back, {user.full_name}!", "success")

        if next_url and next_url.startswith("/"):
            return redirect(next_url)
        return redirect(url_for("dashboard.index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    """Terminate current user session."""
    user_id = session.get("user_id")
    if user_id:
        log_activity("User logged out", "Auth", user_id)
    session.clear()
    flash("You have been securely logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """View and update profile information and password."""
    user = get_current_user()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "update_info":
            full_name = request.form.get("full_name", "").strip()
            bio = request.form.get("bio", "").strip()

            if full_name:
                user.full_name = full_name
            user.bio = bio

            db.session.commit()
            session["full_name"] = user.full_name
            log_activity("Profile details updated", "Profile", user.id)
            flash("Profile information updated successfully.", "success")

        elif action == "change_password":
            current_password = request.form.get("current_password", "")
            new_password = request.form.get("new_password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not user.check_password(current_password):
                flash("Current password is incorrect.", "danger")
            elif len(new_password) < 6:
                flash("New password must be at least 6 characters.", "danger")
            elif new_password != confirm_password:
                flash("New passwords do not match.", "danger")
            else:
                user.set_password(new_password)
                db.session.commit()
                log_activity("Password changed successfully", "Profile", user.id)
                flash("Password updated successfully.", "success")

        return redirect(url_for("auth.profile"))

    return render_template("auth/profile.html", user=user)
