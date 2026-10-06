from database import SessionLocal
from models import Role


ROLES = [
    "Software Engineer",
    "Software Developer",
    "Application Developer",

    "Frontend Developer",
    "UI Developer",
    "React Developer",
    "Angular Developer",
    "Vue Developer",

    "Backend Developer",
    "Node.js Developer",
    "Java Backend Developer",
    "Python Backend Developer",
    ".NET Developer",

    "Full Stack Developer",
    "MERN Developer",
    "MEAN Developer",
    "Java Full Stack Developer",

    "Android Developer",
    "iOS Developer",
    "Flutter Developer",
    "React Native Developer",

    "AI Engineer",
    "Machine Learning Engineer",
    "AI/ML Engineer",
    "Generative AI Engineer",

    "Data Analyst",
    "Data Scientist",
    "Data Engineer",
    "BI Developer",

    "Cloud Engineer",
    "AWS Engineer",
    "Azure Engineer",
    "DevOps Engineer",
    "Site Reliability Engineer",

    "QA Engineer",
    "Test Engineer",
    "Automation Tester",
    "SDET",

    "Cybersecurity Analyst",
    "Security Engineer",
    "SOC Analyst",
    "Ethical Hacker",

    "Database Developer",
    "Database Administrator",
    "SQL Developer",

    "Network Engineer",
    "Network Administrator",

    "Embedded Engineer",
    "Embedded Software Engineer",
    "Firmware Engineer",

    "SAP Developer",
    "Salesforce Developer",
    "ServiceNow Developer",

    "Business Analyst",
    "Product Analyst",
    "Product Manager",

    "UI/UX Designer",
    "UX Designer",
    "Product Designer",

    "Technical Support Engineer",
    "Application Support Engineer",

    "Systems Engineer",
    "Integration Engineer",
    "Solutions Engineer"
]


db = SessionLocal()

try:
    for role_name in ROLES:

        normalized_name = role_name.lower().strip()

        existing_role = (
            db.query(Role)
            .filter(
                Role.normalized_name == normalized_name
            )
            .first()
        )

        if not existing_role:
            role = Role(
                name=role_name,
                normalized_name=normalized_name
            )

            db.add(role)

    db.commit()

    print(f"✅ {len(ROLES)} roles processed successfully.")

except Exception as e:

    db.rollback()

    print("❌ Error while inserting roles:")
    print(e)

finally:
    db.close()