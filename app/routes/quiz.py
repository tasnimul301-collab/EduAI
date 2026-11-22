"""AI Quiz Generator Blueprint Routes.

Handles quiz generation via Gemini AI, interactive test taking,
automated answer verification, scoring, and performance tracking.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.extensions import db
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt
from app.models.subject import Subject
from app.services.ai_service import AIService
from app.utils.auth import login_required, log_activity, get_current_user
from app.utils.curriculum import CLASS_CURRICULUM, seed_class_quizzes_for_user

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")


@quiz_bp.route("/")
@login_required
def index():
    """List quizzes across Class 5-12, randomized on refresh so students encounter fresh quizzes."""
    user = get_current_user()
    from sqlalchemy.sql.expression import func
    # Ensure Class 5 to Class 12 curriculum quizzes are pre-seeded for this user
    seed_class_quizzes_for_user(user.id)

    # Order by random so each refresh dynamically surfaces fresh quizzes across all classes
    quizzes = Quiz.query.order_by(func.random()).all()
    attempts = (
        QuizAttempt.query.filter_by(user_id=user.id)
        .order_by(QuizAttempt.completed_at.desc())
        .limit(10)
        .all()
    )
    subjects = Subject.query.filter_by(user_id=user.id).all()

    return render_template(
        "quiz/index.html",
        user=user,
        quizzes=quizzes,
        attempts=attempts,
        subjects=subjects,
        curriculum=CLASS_CURRICULUM,
        ai_configured=AIService.is_configured(),
    )


@quiz_bp.route("/generate", methods=["POST"])
@login_required
def generate():
    """Trigger AI generation of a new multiple-choice quiz (Admin only)."""
    user = get_current_user()

    if user.role != "admin":
        flash("Only administrators have permission to generate or add new quizzes.", "danger")
        return redirect(url_for("quiz.index"))

    class_level = request.form.get("class_level", "Class 10").strip()
    curriculum_subject = request.form.get("curriculum_subject", "").strip()
    subject_id = request.form.get("subject_id")
    topic = request.form.get("topic", "").strip()
    difficulty = request.form.get("difficulty", "medium")
    count_str = request.form.get("count", "5")

    try:
        count = int(count_str)
        count = max(3, min(count, 10))  # Bound between 3 and 10
    except ValueError:
        count = 5

    if not topic:
        flash("Please specify a topic or chapter for the quiz.", "warning")
        return redirect(url_for("quiz.index"))

    subject_name = curriculum_subject or "General Academic"
    if not curriculum_subject and subject_id and subject_id.isdigit():
        subj = Subject.query.filter_by(id=int(subject_id), user_id=user.id).first()
        if subj:
            subject_name = subj.name

    # Call AI Service with class level and curriculum subject
    result = AIService.generate_quiz_questions(
        subject_name=subject_name,
        topic=topic,
        difficulty=difficulty,
        count=count,
        class_level=class_level,
    )

    if not result["success"]:
        flash(f"Quiz Generation Notice: {result['error']}", "danger")
        return redirect(url_for("quiz.index"))

    # Save Quiz to DB
    quiz_title = f"[{class_level}] {subject_name}: {topic}"
    new_quiz = Quiz(
        user_id=user.id,
        subject_id=int(subject_id) if subject_id and subject_id.isdigit() else None,
        title=quiz_title,
        topic=topic,
        class_level=class_level,
        difficulty=difficulty,
        total_questions=len(result["questions"]),
    )
    db.session.add(new_quiz)
    db.session.flush()

    for q_data in result["questions"]:
        question = QuizQuestion(
            quiz_id=new_quiz.id,
            question_text=q_data["question"],
            option_a=q_data["options"]["A"],
            option_b=q_data["options"]["B"],
            option_c=q_data["options"]["C"],
            option_d=q_data["options"]["D"],
            correct_option=q_data["correct"],
            explanation=q_data.get("explanation", ""),
        )
        db.session.add(question)

    db.session.commit()
    log_activity(f"Generated quiz '{new_quiz.title}'", "Quiz", user.id)
    if result.get("is_fallback"):
        flash(f"Generated '{new_quiz.title}' with {len(result['questions'])} questions via Offline Academic Bank (add GEMINI_API_KEY in .env for dynamic AI).", "info")
    else:
        flash(f"Successfully generated '{new_quiz.title}' with {len(result['questions'])} questions via Google Gemini!", "success")
    return redirect(url_for("quiz.take", quiz_id=new_quiz.id))


@quiz_bp.route("/create-manual", methods=["POST"])
@login_required
def create_manual():
    """Manually create a new quiz with custom questions (Admin only)."""
    user = get_current_user()
    if user.role != "admin":
        flash("Only administrators have permission to create quizzes.", "danger")
        return redirect(url_for("quiz.index"))

    title = request.form.get("title", "").strip()
    class_level = request.form.get("class_level", "Class 10").strip()
    subject_name = request.form.get("subject_name", "General Science").strip()
    topic = request.form.get("topic", "").strip() or title
    difficulty = request.form.get("difficulty", "medium").strip()

    if not title:
        flash("Quiz title is required.", "warning")
        return redirect(url_for("quiz.index"))

    # Extract questions dynamically from form
    questions_data = []
    idx = 1
    while True:
        q_text = request.form.get(f"q_text_{idx}", "").strip()
        if not q_text:
            break
        opt_a = request.form.get(f"opt_a_{idx}", "").strip()
        opt_b = request.form.get(f"opt_b_{idx}", "").strip()
        opt_c = request.form.get(f"opt_c_{idx}", "").strip()
        opt_d = request.form.get(f"opt_d_{idx}", "").strip()
        correct = request.form.get(f"correct_{idx}", "A").strip().upper()
        explanation = request.form.get(f"explanation_{idx}", "").strip()

        if opt_a and opt_b and opt_c and opt_d:
            questions_data.append({
                "question": q_text,
                "opt_a": opt_a,
                "opt_b": opt_b,
                "opt_c": opt_c,
                "opt_d": opt_d,
                "correct": correct if correct in ["A", "B", "C", "D"] else "A",
                "explanation": explanation,
            })
        idx += 1

    if not questions_data:
        flash("Please provide at least 1 complete question with 4 options.", "danger")
        return redirect(url_for("quiz.index"))

    quiz_title = f"[{class_level}] {subject_name}: {title}"
    new_quiz = Quiz(
        user_id=user.id,
        title=quiz_title,
        topic=topic,
        class_level=class_level,
        difficulty=difficulty,
        total_questions=len(questions_data),
    )
    db.session.add(new_quiz)
    db.session.flush()

    for qd in questions_data:
        q = QuizQuestion(
            quiz_id=new_quiz.id,
            question_text=qd["question"],
            option_a=qd["opt_a"],
            option_b=qd["opt_b"],
            option_c=qd["opt_c"],
            option_d=qd["opt_d"],
            correct_option=qd["correct"],
            explanation=qd["explanation"],
        )
        db.session.add(q)

    db.session.commit()
    log_activity(f"Manually created quiz '{new_quiz.title}'", "Quiz", user.id)
    flash(f"Quiz '{new_quiz.title}' with {len(questions_data)} questions created successfully!", "success")
    return redirect(url_for("quiz.index"))


@quiz_bp.route("/delete/<int:quiz_id>", methods=["POST"])
@login_required
def delete_quiz(quiz_id):
    """Delete a quiz (Admin only)."""
    user = get_current_user()
    if user.role != "admin":
        flash("Only administrators have permission to delete quizzes.", "danger")
        return redirect(url_for("quiz.index"))

    quiz = Quiz.query.filter_by(id=quiz_id).first_or_404()
    title = quiz.title
    db.session.delete(quiz)
    db.session.commit()
    flash(f"Quiz '{title}' has been deleted.", "info")
    return redirect(url_for("quiz.index"))


@quiz_bp.route("/take/<int:quiz_id>")
@login_required
def take(quiz_id):
    """Interactive quiz-taking interface."""
    user = get_current_user()
    quiz = Quiz.query.filter_by(id=quiz_id).first_or_404()
    return render_template("quiz/take.html", user=user, quiz=quiz)


@quiz_bp.route("/submit/<int:quiz_id>", methods=["POST"])
@login_required
def submit(quiz_id):
    """Evaluate submitted quiz answers and store attempt results."""
    user = get_current_user()
    quiz = Quiz.query.filter_by(id=quiz_id).first_or_404()

    score = 0
    total = len(quiz.questions)
    results = []

    for question in quiz.questions:
        user_answer = request.form.get(f"question_{question.id}", "").upper()
        is_correct = user_answer == question.correct_option
        if is_correct:
            score += 1

        results.append({
            "question": question,
            "user_answer": user_answer,
            "is_correct": is_correct,
            "correct_option": question.correct_option,
            "explanation": question.explanation,
        })

    percentage = round((score / total * 100), 1) if total > 0 else 0

    attempt = QuizAttempt(
        quiz_id=quiz.id,
        user_id=user.id,
        score=score,
        total_score=total,
        percentage=percentage,
    )
    db.session.add(attempt)

    # Award Gamification points & streaks
    earned_pts = score * 10 + (25 if percentage >= 80 else 10)
    user.total_points += earned_pts
    user.update_streak()
    if percentage >= 80:
        user.add_badge("Quiz Master")
    if percentage == 100:
        user.add_badge("Perfectionist")

    db.session.commit()

    log_activity(f"Completed quiz '{quiz.title}' with score {score}/{total}", "Quiz", user.id)

    return render_template(
        "quiz/result.html",
        user=user,
        quiz=quiz,
        attempt=attempt,
        score=score,
        total=total,
        percentage=percentage,
        results=results,
    )


@quiz_bp.route("/certificate/<int:attempt_id>")
@login_required
def certificate(attempt_id):
    """Render official completion certificate suitable for saving / printing."""
    user = get_current_user()
    attempt = QuizAttempt.query.filter_by(id=attempt_id, user_id=user.id).first_or_404()
    return render_template("quiz/certificate.html", user=user, attempt=attempt, quiz=attempt.quiz)
