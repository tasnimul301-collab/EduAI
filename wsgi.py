"""WSGI Entry Point for EduSmart AI.

Used by production WSGI application servers (e.g., Gunicorn on Render, Railway, or Heroku).
"""

import os
from app import create_app
from app.extensions import db
from app.models.user import User

# Create Flask application configured for production
app = create_app(os.getenv("FLASK_ENV", "production"))

# Ensure database tables exist and initial demo data is seeded on startup
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        print("🌱 Initializing production database with initial demo accounts...")
        # 1. Create Admin
        admin = User(
            username="admin",
            email="admin@edusmart.ai",
            full_name="System Administrator",
            role="admin",
            bio="EduSmart AI Administrator",
        )
        admin.set_password("admin123")
        db.session.add(admin)

        # 2. Create Student
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

        # 3. Seed Class 6-12 Quizzes and Subjects
        from app.utils.curriculum import seed_class_quizzes_for_user, seed_class_subjects_for_user
        seed_class_quizzes_for_user(student.id)
        seed_class_subjects_for_user(student.id)
        print("✅ Production database initialized successfully!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
