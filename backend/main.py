from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import tempfile
import os

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

from agents.resume_generator import generate_tailored_resume
from services.pdf_parser import extract_text_from_pdf
from services.document_parser import extract_text_from_document
from agents.resume_analyser import analyze_resume
from agents.jd_analyser import analyze_job_description
from agents.question_generator import generate_questions

app = FastAPI(
    title="Multi-Agent Interview System",
    description="Multi-Agent Resume, Job Description and Interview Question Generation System",
    version="0.1.0"
)


# ===============================
# CORS
# ===============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5501"
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
       "message": "Multi-Agent Interview System is running"
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

# ===============================
# QUESTION GENERATOR
# ===============================

@app.post("/generate-questions")
async def generate_questions_api(data: dict):

    resume_analysis = data.get("resume_analysis")
    jd_analysis = data.get("jd_analysis")

    if not resume_analysis:
        return {"error": "Resume analysis is required."}

    if not jd_analysis:
        return {"error": "Job description analysis is required."}

    try:
        result = generate_questions(
            resume_analysis,
            jd_analysis
        )
        return result

    except Exception as e:
        print("Question generation error:", e)
        return {"error": str(e)}
@app.post("/generate-tailored-resume")
async def generate_tailored_resume_api(data: dict):

    resume_analysis = data.get("resume_analysis")
    jd_analysis = data.get("jd_analysis")

    if not resume_analysis:
        return {
            "error": "Resume analysis is missing."
        }

    if not jd_analysis:
        return {
            "error": "Job description analysis is missing."
        }

    try:

        result = generate_tailored_resume(
            resume_analysis,
            jd_analysis
        )

        return result

    except Exception as e:

        print("Tailored resume generation error:", e)

        return {
            "error": str(e)
        }
# ===============================
# DOWNLOAD TAILORED RESUME AS PDF
# ===============================

@app.post("/download-tailored-resume")
async def download_tailored_resume(data: dict):

    resume = data.get("tailored_resume")

    if not resume:
        return {
            "error": "Tailored resume data is missing."
        }

    try:

        # Create temporary PDF file
        pdf_path = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ).name

        # Page size
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=45,
            leftMargin=45,
            topMargin=40,
            bottomMargin=40
        )

        # Styles
        styles = getSampleStyleSheet()

        name_style = ParagraphStyle(
            "ResumeName",
            parent=styles["Title"],
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            spaceAfter=8
        )

        contact_style = ParagraphStyle(
            "Contact",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            alignment=TA_CENTER,
            textColor=colors.grey,
            spaceAfter=18
        )

        heading_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=11,
            leading=14,
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontSize=9,
            leading=13,
            spaceAfter=6
        )

        # PDF content
        story = []

        # --------------------------------
        # Candidate
        # --------------------------------

        candidate = resume.get(
            "candidate",
            {}
        )

        name = candidate.get(
            "name",
            "Candidate"
        )

        email = candidate.get(
            "email",
            ""
        )

        phone = candidate.get(
            "phone",
            ""
        )

        location = candidate.get(
            "location",
            ""
        )

        story.append(
            Paragraph(
                str(name),
                name_style
            )
        )

        contact_parts = [
            value
            for value in [
                email,
                phone,
                location
            ]
            if value
        ]

        if contact_parts:

            story.append(
                Paragraph(
                    " | ".join(
                        map(str, contact_parts)
                    ),
                    contact_style
                )
            )

        # --------------------------------
        # Professional Summary
        # --------------------------------

        summary = resume.get(
            "summary",
            ""
        )

        if summary:

            story.append(
                Paragraph(
                    "PROFESSIONAL SUMMARY",
                    heading_style
                )
            )

            story.append(
                Paragraph(
                    str(summary),
                    body_style
                )
            )

        # --------------------------------
        # Skills
        # --------------------------------

        skills = resume.get(
            "skills",
            {}
        )

        story.append(
            Paragraph(
                "SKILLS",
                heading_style
            )
        )

        skill_groups = [
            (
                "Technical Skills",
                skills.get(
                    "technical",
                    []
                )
            ),
            (
                "Programming Languages",
                skills.get(
                    "programming_languages",
                    []
                )
            ),
            (
                "Tools & Technologies",
                skills.get(
                    "tools_and_technologies",
                    []
                )
            )
        ]

        for label, items in skill_groups:

            if items:

                story.append(
                    Paragraph(
                        f"<b>{label}:</b> "
                        + ", ".join(
                            map(str, items)
                        ),
                        body_style
                    )
                )

        # --------------------------------
        # Education
        # --------------------------------

        education = resume.get(
            "education",
            []
        )

        if education:

            story.append(
                Paragraph(
                    "EDUCATION",
                    heading_style
                )
            )

            for item in education:

                story.append(
                    Paragraph(
                        f"• {str(item)}",
                        body_style
                    )
                )

        # --------------------------------
        # Projects
        # --------------------------------

        projects = resume.get(
            "projects",
            []
        )

        if projects:

            story.append(
                Paragraph(
                    "PROJECTS",
                    heading_style
                )
            )

            for project in projects:

                project_name = project.get(
                    "name",
                    ""
                )

                technologies = project.get(
                    "technologies",
                    []
                )

                description = project.get(
                    "description",
                    ""
                )

                story.append(
                    Paragraph(
                        f"<b>{project_name}</b>",
                        body_style
                    )
                )

                if technologies:

                    story.append(
                        Paragraph(
                            "Technologies: "
                            + ", ".join(
                                map(
                                    str,
                                    technologies
                                )
                            ),
                            body_style
                        )
                    )

                if description:

                    story.append(
                        Paragraph(
                            str(description),
                            body_style
                        )
                    )

        # --------------------------------
        # Internships
        # --------------------------------

        internships = resume.get(
            "internships",
            []
        )

        if internships:

            story.append(
                Paragraph(
                    "INTERNSHIPS",
                    heading_style
                )
            )

            for internship in internships:

                title = internship.get(
                    "title",
                    ""
                )

                company = internship.get(
                    "company",
                    ""
                )

                duration = internship.get(
                    "duration",
                    ""
                )

                description = internship.get(
                    "description",
                    ""
                )

                story.append(
                    Paragraph(
                        f"<b>{title}</b>",
                        body_style
                    )
                )

                meta = " | ".join(
                    value
                    for value in [
                        str(company),
                        str(duration)
                    ]
                    if value
                )

                if meta:

                    story.append(
                        Paragraph(
                            meta,
                            body_style
                        )
                    )

                if description:

                    story.append(
                        Paragraph(
                            str(description),
                            body_style
                        )
                    )

        # --------------------------------
        # Certifications
        # --------------------------------

        certifications = resume.get(
            "certifications",
            []
        )

        if certifications:

            story.append(
                Paragraph(
                    "CERTIFICATIONS",
                    heading_style
                )
            )

            for certification in certifications:

                story.append(
                    Paragraph(
                        f"• {str(certification)}",
                        body_style
                    )
                )

        # --------------------------------
        # Achievements
        # --------------------------------

        achievements = resume.get(
            "achievements",
            []
        )

        if achievements:

            story.append(
                Paragraph(
                    "ACHIEVEMENTS",
                    heading_style
                )
            )

            for achievement in achievements:

                story.append(
                    Paragraph(
                        f"• {str(achievement)}",
                        body_style
                    )
                )

        # Build PDF
        doc.build(story)

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename="JD_Tailored_Resume.pdf"
        )

    except Exception as e:

        print(
            "PDF generation error:",
            e
        )

        return {
            "error": str(e)
        }


