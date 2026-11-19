"""AI Study Assistant Blueprint Routes.

Powers conversational academic question answering, step-by-step
topic explanations, study resource recommendations, and summary generation.
"""

from flask import Blueprint, render_template, request, jsonify, session
from app.services.ai_service import AIService
from app.utils.auth import login_required, log_activity, get_current_user

assistant_bp = Blueprint("assistant", __name__, url_prefix="/assistant")


@assistant_bp.route("/")
@login_required
def index():
    """Render the AI Study Assistant chat interface."""
    user = get_current_user()
    return render_template(
        "assistant/index.html",
        user=user,
        ai_configured=AIService.is_configured(),
    )


@assistant_bp.route("/ask", methods=["POST"])
@login_required
def ask():
    """Endpoint for conversational AI study inquiries (JSON/AJAX)."""
    user = get_current_user()
    data = request.get_json(silent=True) or {}
    query = data.get("message", "").strip()

    if not query:
        return jsonify({"success": False, "response": "Please enter an academic question."}), 400

    # Call AI service
    result = AIService.ask_study_assistant(prompt=query)

    if result["success"]:
        log_activity(f"AI Query: '{query[:30]}...'", "Assistant", user.id)

    return jsonify(result)
