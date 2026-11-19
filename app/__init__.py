"""Application Factory Module for EduSmart AI.

Assembles Flask application components, registers Blueprints, binds extensions,
configures context processors, and registers custom error handlers.
"""

import glob
import os
import sys

# Ensure local virtualenv packages are accessible even when running unactivated
_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _candidate in [
    os.path.join(_root_dir, "venv", "Lib", "site-packages"),
    os.path.join(_root_dir, "venv", "lib", "site-packages"),
] + glob.glob(os.path.join(_root_dir, "venv", "lib", "python*", "site-packages")):
    if os.path.isdir(_candidate) and _candidate not in sys.path:
        sys.path.insert(0, _candidate)

from flask import Flask, render_template, session
from config import config_by_name
from app.extensions import db


def create_app(config_name: str = "default") -> Flask:
    """Create and configure the Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Ensure required runtime directories exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Context processors to supply global variables to all Jinja templates
    @app.context_processor
    def inject_global_template_data():
        from app.models.user import User
        from app.models.notification import Notification

        user_id = session.get("user_id")
        current_user = None
        unread_notifications_count = 0

        if user_id:
            current_user = db.session.get(User, user_id)
            if current_user:
                unread_notifications_count = Notification.query.filter_by(
                    user_id=user_id, is_read=False
                ).count()

        return {
            "current_user": current_user,
            "unread_count": unread_notifications_count,
        }

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.planner import planner_bp
    from app.routes.notes import notes_bp
    from app.routes.quiz import quiz_bp
    from app.routes.assistant import assistant_bp
    from app.routes.assignments import assignments_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(planner_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(assistant_bp)
    app.register_blueprint(assignments_bp)
    app.register_blueprint(admin_bp)

    # Error Handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    # Auto-initialize database tables and seed data for production and development
    if config_name != "testing":
        _auto_init_database(app)

    return app


def _auto_init_database(app: Flask):
    """Ensure database tables exist, migrations are applied, and demo data is seeded."""
    with app.app_context():
        try:
            db.create_all()

            # Ensure class_level column exists in quizzes and subjects for SQLite
            from sqlalchemy import text
            for table_name in ["quizzes", "subjects"]:
                try:
                    db.session.execute(text(f"ALTER TABLE {table_name} ADD COLUMN class_level VARCHAR(50) DEFAULT 'General'"))
                    db.session.commit()
                except Exception:
                    db.session.rollback()

            from app.models.user import User
            if not User.query.filter_by(username="admin").first():
                admin = User(
                    username="admin",
                    email="admin@edusmart.ai",
                    full_name="System Administrator",
                    role="admin",
                    bio="EduSmart AI Administrator",
                )
                admin.set_password("admin123")
                db.session.add(admin)

                student = User(
                    username="student",
                    email="student@university.edu",
                    full_name="Alex Johnson",
                    role="student",
                    bio="High School & University Student",
                )
                student.set_password("student123")
                db.session.add(student)
                db.session.commit()

                from app.utils.curriculum import seed_class_quizzes_for_user, seed_class_subjects_for_user
                seed_class_quizzes_for_user(student.id)
                seed_class_subjects_for_user(student.id)
        except Exception as e:
            app.logger.warning(f"Database auto-initialization notice: {e}")


# Expose application instance for WSGI servers running 'gunicorn app:app'
app = create_app(os.getenv("FLASK_ENV", "production"))
