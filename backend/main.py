from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

from backend.services.pdf_parser import extract_text_from_pdf
from backend.services.document_parser import extract_text_from_document
from backend.agents.resume_analyser import analyze_resume
from backend.agents.jd_analyser import analyze_job_description


app = FastAPI(
    title="Multi-Agent Interview System",
    description="Resume and Job Description Analyser API",
    version="0.1.0"
)


# ===============================
# CORS
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8080",
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===============================
# HOME
# ===============================

@app.get("/")
def home():
    return {
        "message": "Resume Analyser Agent is running"
    }


# ===============================
# RESUME ANALYZER
# ===============================

@app.post("/analyze-resume")
async def analyze_resume_api(file: UploadFile = File(...)):

    # Check file type
    if not file.filename:
        return {
            "error": "No file selected."
        }

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported."
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

        if not resume_text or not resume_text.strip():
            return {
                "error": "Could not extract text from the resume."
            }

        # Analyze resume using AI agent
        result = analyze_resume(resume_text)

        return result

    except Exception as e:

        print("Resume analysis error:", e)

        return {
            "error": str(e)
        }

    finally:

        # Delete temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# ===============================
# JOB DESCRIPTION FILE ANALYZER
# ===============================

@app.post("/analyze-job-description-file")
async def analyze_job_description_file(
    file: UploadFile = File(...)
):

    if not file.filename:
        return {
            "error": "No file selected."
        }

    allowed_extensions = {
        ".txt",
        ".pdf",
        ".docx"
    }

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in allowed_extensions:
        return {
            "error": "Only TXT, PDF, and DOCX files are supported."
        }

    file_content = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=extension
    ) as temp_file:

        temp_file.write(file_content)
        temp_file_path = temp_file.name

    try:

        job_description = extract_text_from_document(
            temp_file_path
        )

        if not job_description or not job_description.strip():
            return {
                "error": "Could not extract text from the file."
            }

        result = analyze_job_description(
            job_description
        )

        return result

    except Exception as e:

        print("Job description file analysis error:", e)

        return {
            "error": str(e)
        }

    finally:

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# ===============================
# PASTED JOB DESCRIPTION ANALYZER
# ===============================

@app.post("/analyze-job-description")
async def analyze_job_description_api(data: dict):

    job_description = data.get(
        "job_description",
        ""
    ).strip()

    if not job_description:

        return {
            "error": "Job description cannot be empty."
        }

    try:

        # Analyze pasted job description
        result = analyze_job_description(
            job_description
        )

        return result

    except Exception as e:

        print("Job description analysis error:", e)

        return {
            "error": str(e)
        }