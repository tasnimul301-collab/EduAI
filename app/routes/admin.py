"""Admin Dashboard Blueprint Routes.

Provides administrative controls, system-wide metrics, student account management,
and security audit monitoring.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.user import User
from app.services.analytics_service import AnalyticsService
from app.utils.auth import admin_required, log_activity, get_current_user

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_required
def index():
    """Administrative dashboard displaying institutional statistics and audit logs."""
    user = get_current_user()
    metrics = AnalyticsService.get_admin_metrics()
    return render_template(
        "admin/index.html",
        user=user,
        metrics=metrics,
    )


@admin_bp.route("/users/<int:user_id>/toggle-status", methods=["POST"])
@admin_required
def toggle_user_status(user_id):
    """Activate or deactivate a student account."""
    admin_user = get_current_user()
    target_user = User.query.get_or_404(user_id)

    if target_user.id == admin_user.id:
        flash("You cannot deactivate your own administrative account.", "danger")
        return redirect(url_for("admin.index"))

    target_user.is_active = not target_user.is_active
    db.session.commit()

    status_str = "activated" if target_user.is_active else "deactivated"
    log_activity(
        f"Admin {admin_user.username} {status_str} user #{target_user.id} ({target_user.username})",
        "Admin",
        admin_user.id,
    )
    flash(f"User account '{target_user.username}' has been {status_str}.", "info")
    return redirect(url_for("admin.index"))
