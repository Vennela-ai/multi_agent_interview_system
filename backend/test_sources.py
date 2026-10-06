from services.question_retriever import (
    SOURCE_REGISTRY,
    fetch_page,
    extract_questions_from_html
)


print()
print("SOURCE EXTRACTION TEST")
print("=" * 100)


total_sources = 0
working_sources = 0
failed_sources = 0
total_questions = 0


for topic, sources in SOURCE_REGISTRY.items():

    print()
    print(f"TOPIC: {topic}")
    print("-" * 100)

    for source in sources:

        total_sources += 1

        try:

            html = fetch_page(
                source["url"]
            )

            questions = extract_questions_from_html(
                html
            )

            count = len(questions)

            print(
                f"OK   | "
                f"{source['source_type']:<18} | "
                f"{count:>4} questions | "
                f"{source['url']}"
            )

            working_sources += 1
            total_questions += count

        except Exception as e:

            print(
                f"FAIL | "
                f"{source['source_type']:<18} | "
                f"{source['url']}"
            )

            print(
                f"       ERROR: {str(e)}"
            )

            failed_sources += 1


print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)

print(
    "TOTAL SOURCES :",
    total_sources
)

print(
    "WORKING       :",
    working_sources
)

print(
    "FAILED        :",
    failed_sources
)

print(
    "RAW QUESTIONS :",
    total_questions
)

print("=" * 100)