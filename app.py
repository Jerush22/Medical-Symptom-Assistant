
from flask import Flask, render_template, request
from datetime import datetime
from pathlib import Path
import ollama
import re

app = Flask(__name__)

# Project folders
BASE_DIR = Path(__file__).resolve().parent
REPORT_FOLDER = BASE_DIR / "reports"
REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

# Local AI model
MODEL_NAME = "llama3.2:1b"


def clean_ai_response(text):
    """Clean Markdown symbols and improve plain-text formatting."""

    text = text.strip()

    # Remove accidental escape characters before Markdown symbols
    text = re.sub(r"\\([*#_])", r"\1", text)

    # Convert Markdown headings to plain text headings
    text = re.sub(r"(?m)^\s*#{1,6}\s*", "", text)

    # Convert bold and italic markers to readable plain text
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("*", "")
    text = text.replace("_", "")

    # Clean up bullet points and excess blank lines
    text = re.sub(r"(?m)^\s*[-+]\s+", "• ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    # Collect submitted information
    age = request.form.get("age", "").strip()
    sex = request.form.get("sex", "").strip()
    symptoms = request.form.get("symptoms", "").strip()
    duration = request.form.get("duration", "").strip()
    severity = request.form.get("severity", "").strip()
    history = request.form.get("history", "").strip()
    medications = request.form.get("medications", "").strip()
    allergies = request.form.get("allergies", "").strip()

    # Validate required fields
    if not age or not symptoms or not duration or not severity:
        return (
            "Please provide age, symptoms, duration, and severity. "
            '<a href="/">Return to home</a>.',
            400,
        )

    # Basic warning for some potentially urgent symptoms.
    # This keyword check cannot detect every emergency.
    urgent_terms = [
        "chest pain",
        "difficulty breathing",
        "can't breathe",
        "cannot breathe",
        "shortness of breath",
        "unconscious",
        "stroke",
        "face drooping",
        "severe allergic reaction",
    ]

    urgent = any(term in symptoms.lower() for term in urgent_terms)

    # Prompt for general educational information
    prompt = f"""
Provide general educational information about the reported symptoms.
Do not diagnose, prescribe, or claim certainty.

Patient information:
Age: {age}
Sex: {sex or "Not provided"}
Symptoms: {symptoms}
Duration: {duration}
Reported severity: {severity}
Medical history: {history or "Not provided"}
Current medications: {medications or "Not provided"}
Known allergies: {allergies or "Not provided"}

Use these four headings:
1. Summary of Reported Symptoms
2. General Possible Explanations (Not a Diagnosis)
3. Questions a Healthcare Professional May Ask
4. Safe Next Steps

Use plain text. Do not use Markdown bold markers, asterisks,
or hash symbols for headings. Use short paragraphs and simple
bullet points. Do not recommend starting, stopping, or changing
medication. Mention uncertainty and the need for professional
medical assessment.
"""

    # Generate AI response using local Ollama
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You provide cautious, general medical education. "
                        "Never present guesses as a diagnosis. "
                        "Use clear plain text and simple bullet points. "
                        "Do not prescribe medicine."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            options={"temperature": 0.2},
        )

        analysis = clean_ai_response(
            response["message"]["content"]
        )

    except Exception:
        app.logger.exception("Ollama analysis failed.")
        analysis = (
            "AI analysis is currently unavailable.\n\n"
            "Check that Ollama is running and the model "
            f"'{MODEL_NAME}' is installed, then try again."
        )

    # Display a safety notice
    if urgent:
        safety_message = (
            "Some reported symptoms may require immediate medical "
            "attention. Contact your local emergency service or seek "
            "emergency care now. Do not wait for an AI response."
        )
    else:
        safety_message = (
            "Seek prompt medical attention if symptoms are severe, "
            "worsening, or concerning. For emergencies, contact your "
            "local emergency service. This automated check cannot "
            "determine whether a situation is safe."
        )

    # Create a unique report filename
    current_time = datetime.now()
    filename = current_time.strftime(
        "report_%Y%m%d_%H%M%S_%f.txt"
    )

    # Prepare the report content
    report = f"""
AI-POWERED MEDICAL SYMPTOM ASSISTANT
===================================

Report Date: {current_time.strftime("%Y-%m-%d %H:%M:%S")}

PATIENT INFORMATION
-------------------
Age: {age}
Sex: {sex or "Not provided"}

REPORTED SYMPTOMS
-----------------
Symptoms: {symptoms}
Duration: {duration}
Severity: {severity}

MEDICAL HISTORY
---------------
{history or "Not provided"}

CURRENT MEDICATIONS
-------------------
{medications or "Not provided"}

KNOWN ALLERGIES
---------------
{allergies or "Not provided"}

AI-GENERATED GENERAL INFORMATION
--------------------------------
{analysis}

MEDICAL SAFETY NOTICE
---------------------
{safety_message}

DISCLAIMER
----------
AI-generated information may be incomplete or incorrect.
It is not a diagnosis or a substitute for professional medical care.
Do not use this report alone to make medical decisions.
"""

    # Save the report
    try:
        report_path = REPORT_FOLDER / filename
        report_path.write_text(report, encoding="utf-8")

    except OSError:
        app.logger.exception("Could not save the report.")
        return "Unable to save the report. Please try again.", 500

    # Display the result page
    return render_template(
        "result.html",
        report_name=filename,
        analysis=analysis,
        safety_message=safety_message,
        urgent=urgent,
    )


@app.errorhandler(404)
def page_not_found(error):
    return (
        '<h1>Page Not Found</h1>'
        '<p><a href="/">Return to MediAssist AI</a></p>',
        404,
    )


if __name__ == "__main__":
    app.run(debug=True)
