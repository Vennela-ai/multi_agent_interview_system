from services.pdf_parser import extract_text_from_pdf
from agents.resume_analyser import analyze_resume


# Resume PDF path
resume_path = "backend/sample_resume.pdf"

# Step 1: Extract text from PDF
resume_text = extract_text_from_pdf(resume_path)

print("\n========== RESUME TEXT ==========\n")
print(resume_text)

# Step 2: Analyze resume using AI
result = analyze_resume(resume_text)

print("\n========== RESUME ANALYSIS ==========\n")
print(result)