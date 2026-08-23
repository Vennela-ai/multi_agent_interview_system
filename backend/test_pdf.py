from services.pdf_parser import extract_text_from_pdf

file_path = "backend/sample_resume.pdf"

text = extract_text_from_pdf(file_path)

print(text)