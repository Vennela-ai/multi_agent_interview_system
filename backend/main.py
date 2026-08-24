from fastapi import FastAPI, UploadFile, File
import tempfile
import os
from backend.services.pdf_parser import extract_text_from_pdf
from backend.agents.resume_analyser import analyze_resume

app = FastAPI(
    title="Multi-Agent Interview System",
    description="Resume Analyser Agent API"
)


@app.get("/")
def home():
    return {
        "message": "Resume Analyser Agent is running"
    }


@app.post("/analyze-resume")
async def analyze_resume_api(file: UploadFile = File(...)):

    # Check file type
    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported"
        }

    # Read uploaded file
    file_content = await file.read()

    # Create temporary PDF
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(file_content)
        temp_file_path = temp_file.name

    try:
        # Extract resume text
        resume_text = extract_text_from_pdf(temp_file_path)

        # Analyze resume using AI agent
        result = analyze_resume(resume_text)

        return result

    finally:
        # Delete temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)