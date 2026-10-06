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
from database import SessionLocal
from services.question_service import get_questions_by_role
from models import Role, Question, RoleQuestion, QuestionSource
from services.question_retriever import (
    retrieve_questions_for_role,
    update_role_question_relevance,
    retrieve_questions_by_skills
)
from agents.question_generator import (
    generate_personalized_questions as generate_questions_agent
)
from agents.mapping_agent import calculate_mapping
from agents.project_agent import recommend_project
from agents.interview_preparation_agent import (
    generate_500_questions,
    generate_question_batch
)

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
# RESUME-JD MAPPING
# ===============================

@app.post("/calculate-mapping")
def calculate_mapping_api(data: dict):

    resume_analysis = data.get("resume_analysis")
    jd_analysis = data.get("jd_analysis")

    if not resume_analysis:
        return {
            "success": False,
            "error": "Resume analysis is missing."
        }

    if not jd_analysis:
        return {
            "success": False,
            "error": "Job description analysis is missing."
        }

    try:

        result = calculate_mapping(
            resume_analysis,
            jd_analysis
        )

        return {
            "success": True,
            **result
        }

    except Exception as e:

        print(
            "Mapping error:",
            e
        )

        return {
            "success": False,
            "error": str(e)
        }
# ===============================
# RESUME-JD PROCESSING
# ===============================

@app.post("/process-resume-jd")
def process_resume_jd(data: dict):

    resume_analysis = data.get(
        "resume_analysis"
    )

    jd_analysis = data.get(
        "jd_analysis"
    )

    if not resume_analysis:
        return {
            "success": False,
            "error": "Resume analysis is missing."
        }

    if not jd_analysis:
        return {
            "success": False,
            "error": "Job description analysis is missing."
        }

    try:

        # -----------------------------------------
        # STEP 1 — Calculate Mapping
        # -----------------------------------------

        mapping_result = calculate_mapping(
            resume_analysis,
            jd_analysis
        )

        match_percentage = mapping_result.get(
            "match_percentage",
            0
        )

        # -----------------------------------------
        # STEP 2 — Decide Resume Action
        # -----------------------------------------

        if match_percentage >= 85:

            return {
                "success": True,
                "match_percentage": match_percentage,
                "mapping": mapping_result,
                "resume_action": "keep_current_resume",
                "message": "Resume match is 85% or higher. Current resume can be used.",
                "tailored_resume": None
            }

        # -----------------------------------------
        # STEP 3 — Generate Tailored Resume
        # -----------------------------------------

        tailored_resume = generate_tailored_resume(
            resume_analysis,
            jd_analysis
        )

        return {
            "success": True,
            "match_percentage": match_percentage,
            "mapping": mapping_result,
            "resume_action": "generate_tailored_resume",
            "message": "Resume match is below 85%. Tailored resume generated.",
            "tailored_resume": tailored_resume
        }

    except Exception as e:

        print(
            "Resume-JD processing error:",
            e
        )

        return {
            "success": False,
            "error": str(e)
        }
# ============================================
# PROJECT RECOMMENDATION
# ============================================

@app.post("/recommend-project")
def recommend_project_api(data: dict):

    resume_analysis = data.get(
        "resume_analysis"
    )

    jd_analysis = data.get(
        "jd_analysis"
    )

    if not resume_analysis:
        return {
            "success": False,
            "error": "Resume analysis is missing."
        }

    if not jd_analysis:
        return {
            "success": False,
            "error": "Job description analysis is missing."
        }

    try:

        role = (
            jd_analysis
            .get("job", {})
            .get("job_title", "Software Developer")
        )

        result = recommend_project(
            role=role,
            resume_analysis=resume_analysis,
            jd_analysis=jd_analysis
        )

        return {
            "success": True,
            "project_recommendation": result
        }

    except Exception as e:

        print(
            "Project recommendation error:",
            e
        )

        return {
            "success": False,
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
@app.get("/questions")
def get_questions(
    role: str,
    offset: int = 0
):

    db = SessionLocal()

    try:
        return get_questions_by_role(
            db=db,
            role_name=role,
            offset=offset
        )

    finally:
        db.close()
@app.post("/generate-personalized-questions")
def generate_personalized_questions(
    resume_analysis: dict,
    jd_analysis: dict
):

    db = SessionLocal()

    try:

        # -----------------------------------------
        # Extract resume skills
        # -----------------------------------------

        resume_skills = []

        resume_skill_data = resume_analysis.get(
            "skills",
            {}
        )

        resume_skills.extend(
            resume_skill_data.get(
                "technical",
                []
            )
        )

        resume_skills.extend(
            resume_skill_data.get(
                "programming_languages",
                []
            )
        )

        resume_skills.extend(
            resume_skill_data.get(
                "tools_and_technologies",
                []
            )
        )

        # -----------------------------------------
        # Extract JD skills
        # -----------------------------------------

        jd_skills = []

        jd_skill_data = jd_analysis.get(
            "skills",
            {}
        )

        jd_skills.extend(
            jd_skill_data.get(
                "required",
                []
            )
        )

        jd_skills.extend(
            jd_skill_data.get(
                "preferred",
                []
            )
        )

        jd_skills.extend(
            jd_skill_data.get(
                "programming_languages",
                []
            )
        )

        jd_skills.extend(
            jd_skill_data.get(
                "tools_and_technologies",
                []
            )
        )

        # -----------------------------------------
        # Find matching skills
        # -----------------------------------------

        resume_skill_map = {
            str(skill).strip().lower(): skill
            for skill in resume_skills
            if skill
        }

        jd_skill_map = {
            str(skill).strip().lower(): skill
            for skill in jd_skills
            if skill
        }

        matching_skills = []

        for skill in resume_skill_map:

            if skill in jd_skill_map:
                matching_skills.append(
                    resume_skill_map[skill]
                )

        # -----------------------------------------
        # If no exact match, use JD skills
        # -----------------------------------------

        retrieval_skills = matching_skills

        if not retrieval_skills:
            retrieval_skills = jd_skills

        # -----------------------------------------
        # Retrieve relevant questions
        # -----------------------------------------

        retrieved_questions = retrieve_questions_by_skills(
            db=db,
            skills=retrieval_skills,
            limit=20
        )

        # -----------------------------------------
        # Generate personalized questions
        # -----------------------------------------

        generated_questions = generate_questions_agent(
            resume_analysis=resume_analysis,
            jd_analysis=jd_analysis,
            retrieved_questions=retrieved_questions
        )

        # -----------------------------------------
        # Return final result
        # -----------------------------------------

        return {
            "success": True,

            "resume_skills": resume_skills,

            "jd_skills": jd_skills,

            "matching_skills": matching_skills,

            "retrieval_skills": retrieval_skills,

            "retrieved_question_count": len(
                retrieved_questions
            ),

            "retrieved_questions": retrieved_questions,

            "generated_questions": generated_questions
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

    finally:
        db.close()
@app.post("/update-relevance")
def update_relevance(role: str):

    db = SessionLocal()

    try:

        return update_role_question_relevance(
            db=db,
            role_name=role
        )

    finally:

        db.close()
@app.post("/populate-all-roles")
def populate_all_roles():

    db = SessionLocal()

    try:

        roles = (
            db.query(Role)
            .order_by(Role.id.asc())
            .all()
        )

        results = []

        for role in roles:

            print(f"\n{'=' * 60}")
            print(f"PROCESSING ROLE: {role.name}")
            print(f"{'=' * 60}")

            try:

                result = retrieve_questions_for_role(
                    db=db,
                    role_name=role.name,
                    required_count=100
                )

                results.append({
                    "role": role.name,
                    "success": result.get(
                        "success", False
                    ),
                    "added_questions": result.get(
                        "added_questions", 0
                    ),
                    "total_questions": result.get(
                        "total_questions", 0
                    )
                })

                print(
                    f"COMPLETED: {role.name} | "
                    f"Total: {result.get('total_questions', 0)}"
                )

            except Exception as e:

                db.rollback()

                print(
                    f"FAILED: {role.name} | {str(e)}"
                )

                results.append({
                    "role": role.name,
                    "success": False,
                    "added_questions": 0,
                    "total_questions": 0,
                    "error": str(e)
                })

                continue

        successful_roles = sum(
            1
            for result in results
            if result["success"]
        )

        failed_roles = len(results) - successful_roles

        return {
            "success": True,
            "message": "All roles processed.",
            "total_roles": len(roles),
            "successful_roles": successful_roles,
            "failed_roles": failed_roles,
            "results": results
        }

    finally:

        db.close()
@app.get("/roles")
def get_roles():

    db = SessionLocal()

    try:

        roles = (
            db.query(Role)
            .order_by(Role.name.asc())
            .all()
        )

        return {
            "success": True,
            "roles": [
                {
                    "id": role.id,
                    "name": role.name
                }
                for role in roles
            ]
        }

    finally:

        db.close()
@app.post("/update-all-relevance")
def update_all_relevance():

    db = SessionLocal()

    try:

        roles = (
            db.query(Role)
            .order_by(Role.id.asc())
            .all()
        )

        results = []

        for role in roles:

            try:

                result = update_role_question_relevance(
                    db=db,
                    role_name=role.name
                )

                results.append(result)

            except Exception as e:

                db.rollback()

                results.append({
                    "success": False,
                    "role": role.name,
                    "updated_questions": 0,
                    "error": str(e)
                })

        successful_roles = sum(
            1
            for result in results
            if result.get("success")
        )

        failed_roles = len(results) - successful_roles

        return {
            "success": True,
            "message": "Relevance updated for all roles.",
            "total_roles": len(roles),
            "successful_roles": successful_roles,
            "failed_roles": failed_roles,
            "results": results
        }

    finally:

        db.close()
# ============================================
# INTERVIEW PREPARATION
# ============================================

@app.post("/generate-interview-preparation")
def generate_interview_preparation_api(data: dict):

    resume_analysis = data.get(
        "resume_analysis"
    )

    jd_analysis = data.get(
        "jd_analysis"
    )

    research_result = data.get(
        "research_result"
    )

    if not resume_analysis:
        return {
            "success": False,
            "error": "Resume analysis is missing."
        }

    if not jd_analysis:
        return {
            "success": False,
            "error": "Job description analysis is missing."
        }

    if not research_result:
        return {
            "success": False,
            "error": "Internet research result is missing."
        }

    try:

        role = (
            jd_analysis
            .get("job", {})
            .get(
                "job_title",
                "Software Developer"
            )
        )

        result = generate_interview_questions(
            role=role,
            resume_analysis=resume_analysis,
            jd_analysis=jd_analysis,
            research_result=research_result,
            max_questions=500
        )

        return {
            "success": True,
            "interview_preparation": result
        }

    except Exception as e:

        print(
            "Interview preparation error:",
            e
        )

        return {
            "success": False,
            "error": str(e)
        }
def get_or_create_role(db, role_name):
    normalized_name = role_name.strip().lower()

    role = (
        db.query(Role)
        .filter(Role.normalized_name == normalized_name)
        .first()
    )

    if not role:
        role = Role(
            name=role_name.strip(),
            normalized_name=normalized_name
        )

        db.add(role)
        db.commit()
        db.refresh(role)

    return role


def save_interview_questions(
    db,
    role_name,
    questions
):
    role = get_or_create_role(
        db,
        role_name
    )

    saved_count = 0

    for item in questions:

        question_text = str(
            item.get("question", "")
        ).strip()

        if not question_text:
            continue

        # Check whether question already exists
        question = (
            db.query(Question)
            .filter(
                Question.question_text == question_text
            )
            .first()
        )

        if not question:

            question = Question(
                question_text=question_text,
                category=item.get(
                    "category",
                    "General"
                ),
                verified=True
            )

            db.add(question)
            db.flush()

        # Check role-question relationship
        existing_relation = (
            db.query(RoleQuestion)
            .filter(
                RoleQuestion.role_id == role.id,
                RoleQuestion.question_id == question.id
            )
            .first()
        )

        if not existing_relation:

            db.add(
                RoleQuestion(
                    role_id=role.id,
                    question_id=question.id
                )
            )

        # Save source
        source = item.get(
            "source",
            {}
        )

        source_name = source.get(
            "name",
            "Generated"
        )

        source_url = source.get(
            "url",
            ""
        )

        if source_url:

            existing_source = (
                db.query(QuestionSource)
                .filter(
                    QuestionSource.question_id == question.id,
                    QuestionSource.source_url == source_url
                )
                .first()
            )

            if not existing_source:

                db.add(
                    QuestionSource(
                        question_id=question.id,
                        source_type="internet",
                        source_url=source_url,
                        source_title=source_name
                    )
                )

        saved_count += 1

    db.commit()

    return saved_count
@app.post("/generate-500-interview-questions")
def generate_500_interview_questions_api(data: dict):

    resume_analysis = data.get(
        "resume_analysis",
        {}
    )

    jd_analysis = data.get(
        "jd_analysis",
        {}
    )

    research_result = data.get(
        "research_result",
        {}
    )

    if not resume_analysis:
        return {
            "success": False,
            "error": "Resume analysis is missing."
        }

    if not jd_analysis:
        return {
            "success": False,
            "error": "Job description analysis is missing."
        }

    db = SessionLocal()

    try:

        role = (
            jd_analysis
            .get("job", {})
            .get(
                "job_title",
                "Software Developer"
            )
        )

        role_db = get_or_create_role(
            db,
            role
        )

        # Get already stored questions
        existing_count = (
            db.query(RoleQuestion)
            .filter(
                RoleQuestion.role_id == role_db.id
            )
            .count()
        )

        # Generate only the first 10 if needed
        if existing_count < 10:

            questions = generate_question_batch(
                role=role,
                resume_analysis=resume_analysis,
                jd_analysis=jd_analysis,
                research_result=research_result,
                existing_questions=[],
                batch_size=10
            )

            save_interview_questions(
                db=db,
                role_name=role,
                questions=questions
            )

        # Retrieve first 10
        role_questions = (
            db.query(RoleQuestion)
            .filter(
                RoleQuestion.role_id == role_db.id
            )
            .order_by(
                RoleQuestion.question_id.asc()
            )
            .limit(10)
            .all()
        )

        questions_response = []

        for rq in role_questions:

            question = rq.question

            source = (
                db.query(QuestionSource)
                .filter(
                    QuestionSource.question_id == question.id
                )
                .first()
            )

            questions_response.append({
                "id": question.id,
                "question": question.question_text,
                "category": question.category,
                "source": {
                    "name": (
                        source.source_title
                        if source
                        else "Generated"
                    ),
                    "url": (
                        source.source_url
                        if source
                        else ""
                    )
                }
            })

        return {
            "success": True,
            "role": role,
            "page": 1,
            "limit": 10,
            "total_available": existing_count,
            "has_more": True,
            "questions": questions_response
        }

    except Exception as e:

        db.rollback()

        print(
            "Interview question generation error:",
            e
        )

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        db.close()
@app.post("/get-more-interview-questions")
def get_more_interview_questions(data: dict):

    role = data.get(
        "role",
        "Software Developer"
    )

    resume_analysis = data.get(
        "resume_analysis",
        {}
    )

    jd_analysis = data.get(
        "jd_analysis",
        {}
    )

    research_result = data.get(
        "research_result",
        {}
    )

    page = int(
        data.get(
            "page",
            1
        )
    )

    limit = 10

    if page < 1:
        page = 1

    db = SessionLocal()

    try:

        role_db = get_or_create_role(
            db,
            role
        )

        start = (page - 1) * limit
        required_count = start + limit

        # Maximum 500 questions
        if required_count > 500:
            required_count = 500

        # Current number stored
        current_count = (
            db.query(RoleQuestion)
            .filter(
                RoleQuestion.role_id == role_db.id
            )
            .count()
        )

        # Generate more only when required
        while (
            current_count < required_count
            and current_count < 500
        ):

            existing_questions = (
                db.query(Question.question_text)
                .join(
                    RoleQuestion,
                    RoleQuestion.question_id == Question.id
                )
                .filter(
                    RoleQuestion.role_id == role_db.id
                )
                .all()
            )

            existing_questions = [
                item[0]
                for item in existing_questions
            ]

            questions_needed = min(
                10,
                500 - current_count
            )

            new_questions = generate_question_batch(
                role=role,
                resume_analysis=resume_analysis,
                jd_analysis=jd_analysis,
                research_result=research_result,
                existing_questions=existing_questions,
                batch_size=questions_needed
            )

            if not new_questions:
                break

            save_interview_questions(
                db=db,
                role_name=role,
                questions=new_questions
            )

            new_count = (
                db.query(RoleQuestion)
                .filter(
                    RoleQuestion.role_id == role_db.id
                )
                .count()
            )

            # Prevent infinite loop
            if new_count <= current_count:
                break

            current_count = new_count

        # Retrieve requested page
        role_questions = (
            db.query(RoleQuestion)
            .filter(
                RoleQuestion.role_id == role_db.id
            )
            .order_by(
                RoleQuestion.question_id.asc()
            )
            .offset(start)
            .limit(limit)
            .all()
        )

        questions_response = []

        for rq in role_questions:

            question = rq.question

            source = (
                db.query(QuestionSource)
                .filter(
                    QuestionSource.question_id == question.id
                )
                .first()
            )

            questions_response.append({
                "id": question.id,
                "question": question.question_text,
                "category": question.category,
                "source": {
                    "name": (
                        source.source_title
                        if source
                        else "Generated"
                    ),
                    "url": (
                        source.source_url
                        if source
                        else ""
                    )
                }
            })

        total_questions = (
            db.query(RoleQuestion)
            .filter(
                RoleQuestion.role_id == role_db.id
            )
            .count()
        )

        return {
            "success": True,
            "role": role,
            "page": page,
            "limit": limit,
            "total_questions": min(
                total_questions,
                500
            ),
            "has_more": (
                start + len(questions_response)
                < min(total_questions, 500)
            ),
            "questions": questions_response
        }

    except Exception as e:

        db.rollback()

        print(
            "Get More Questions Error:",
            e
        )

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        db.close()