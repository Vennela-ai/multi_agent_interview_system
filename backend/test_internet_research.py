from agents.internet_researcher import research_interview_questions


result = research_interview_questions(
    role="Python Developer",
    skills=[
        "Python",
        "Flask",
        "SQL",
        "REST API",
        "Git"
    ],
    max_sources=10
)


print("\n================ SOURCES ================\n")

for source in result["sources"]:
    print(source["title"])
    print(source["url"])
    print()


print("\n================ QUESTIONS ================\n")

print(result["questions"])