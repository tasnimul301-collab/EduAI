"""Authentication and Authorization Utilities.

Provides decorators and helper functions for session management,
role-based access control (RBAC), and activity logging.
"""

from functools import wraps
from flask import session, redirect, url_for, flash, request, abort
from app.extensions import db
from app.models.user import User
from app.models.activity_log import ActivityLog


def get_current_user() -> User | None:
    """Retrieve the currently authenticated User instance from the database session."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(User, user_id)


def login_required(f):
    """Decorator to protect routes requiring an active student or admin session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        user = get_current_user()
        if not user:
            session.clear()
            flash("Your session has expired. Please log in again.", "info")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to restrict access strictly to users with the 'admin' role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in with administrator privileges.", "warning")
            return redirect(url_for("auth.login"))
        user = get_current_user()
        if not user:
            session.clear()
            flash("Your session has expired. Please log in again.", "info")
            return redirect(url_for("auth.login"))
        if user.role != "admin":
            flash("Access denied: Administrator privileges required.", "danger")
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def log_activity(action: str, module: str, user_id: int | None = None) -> None:
    """Helper to record user and system actions in the audit log."""
    try:
        active_user_id = user_id or session.get("user_id")
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        log_entry = ActivityLog(
            user_id=active_user_id,
            action=action,
            module=module,
            ip_address=client_ip,
        )
        db.session.add(log_entry)
        db.session.commit()
    except Exception:
        # Prevent logging errors from crashing core operations
        db.session.rollback()
