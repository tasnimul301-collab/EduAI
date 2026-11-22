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
    """List student quizzes and past attempt history."""
    user = get_current_user()
    # Ensure Class 6 to Class 12 curriculum quizzes are pre-seeded for this user
    seed_class_quizzes_for_user(user.id)

    quizzes = Quiz.query.filter_by(user_id=user.id).order_by(Quiz.created_at.desc()).all()
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
    """Trigger AI generation of a new multiple-choice quiz."""
    user = get_current_user()

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


@quiz_bp.route("/take/<int:quiz_id>")
@login_required
def take(quiz_id):
    """Interactive quiz-taking interface."""
    user = get_current_user()
    quiz = Quiz.query.filter_by(id=quiz_id, user_id=user.id).first_or_404()
    return render_template("quiz/take.html", user=user, quiz=quiz)


@quiz_bp.route("/submit/<int:quiz_id>", methods=["POST"])
@login_required
def submit(quiz_id):
    """Evaluate submitted quiz answers and store attempt results."""
    user = get_current_user()
    quiz = Quiz.query.filter_by(id=quiz_id, user_id=user.id).first_or_404()

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
