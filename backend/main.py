from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from backend.services.pdf_parser import extract_text_from_pdf
from backend.agents.resume_analyser import analyze_resume
from backend.agents.jd_analyser import analyze_job_description

app = FastAPI(
    title="Multi-Agent Interview System",
    description="Resume Analyser Agent API"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.post("/analyze-job-description")
async def analyze_job_description_api(data: dict):
    job_description = data.get("job_description", "")

    if not job_description.strip():
        return {
            "error": "Job description is required"
        }

    result = analyze_job_description(job_description)

    return result