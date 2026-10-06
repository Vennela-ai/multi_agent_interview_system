import sys
import os
import re
import requests
from bs4 import BeautifulSoup

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


SOURCE_URL = (
    "https://www.geeksforgeeks.org/"
    "advance-java/introduction-to-advanced-java-interview-questions/"
)

SOURCE_TITLE = "Advanced Java Interview Questions - GeeksforGeeks"


def fetch_page(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/154.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    print("Status:", response.status_code)
    print("Final URL:", response.url)

    response.raise_for_status()

    return response.text


def collect_questions(url):

    html = fetch_page(url)

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    questions = []

    for heading in soup.find_all(
        ["h2", "h3", "h4", "h5"]
    ):

        text = heading.get_text(
            " ",
            strip=True
        )

        if not text:
            continue

        # Remove numbering such as:
        # "1. What is Java?"
        cleaned = re.sub(
            r"^\s*\d+\.\s*",
            "",
            text
        ).strip()

        lower = cleaned.lower()

        if (
            lower.startswith("what ")
            or lower.startswith("why ")
            or lower.startswith("how ")
            or lower.startswith("which ")
            or lower.startswith("when ")
            or lower.startswith("where ")
            or lower.startswith("can ")
            or lower.startswith("is ")
            or lower.startswith("are ")
            or lower.startswith("difference ")
            or lower.startswith("explain ")
            or lower.startswith("define ")
        ):
            questions.append(cleaned)

    # Remove duplicates
    questions = list(
        dict.fromkeys(questions)
    )

    return questions


if __name__ == "__main__":

    print(
        "🌐 Collecting Java questions from GeeksforGeeks..."
    )

    try:

        questions = collect_questions(
            SOURCE_URL
        )

        print()
        print(
            f"Found {len(questions)} candidate questions."
        )

        print()
        print("First 20 questions:")

        for i, question in enumerate(
            questions[:20],
            start=1
        ):
            print(
                f"{i}. {question}"
            )

    except Exception as e:

        print()
        print("❌ Collector error:")
        print(e)