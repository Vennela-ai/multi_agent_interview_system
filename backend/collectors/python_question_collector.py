import requests
from bs4 import BeautifulSoup
import re


# ==========================================
# SOURCE CONFIGURATION
# ==========================================

SOURCE_URL = "https://www.interviewbit.com/python-interview-questions/"

SOURCE_TITLE = "Python Interview Questions"

SOURCE_TYPE = "InterviewBit"

ROLE_NAME = "Python Developer"


# ==========================================
# DOWNLOAD PAGE
# ==========================================

def get_page():

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/154.0.0.0 "
            "Safari/537.36"
        )
    }

    response = requests.get(
        SOURCE_URL,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.text


# ==========================================
# CLEAN QUESTION TEXT
# ==========================================

def clean_question(text):

    text = text.strip()

    # Remove extra spaces

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # Remove common numbering

    text = re.sub(
        r"^\s*\d+[\.\)\-:]\s*",
        "",
        text
    )

    return text.strip()


# ==========================================
# CHECK WHETHER HEADING LOOKS LIKE QUESTION
# ==========================================

def is_question(text):

    text_lower = text.lower().strip()


    # Ignore very short headings

    if len(text_lower) < 10:
        return False


    # Ignore navigation headings

    ignored = [
        "table of contents",
        "related articles",
        "related interview questions",
        "frequently asked questions",
        "python interview questions",
        "subscribe",
        "share",
        "about us",
        "contact us",
        "follow us",
        "quick links"
    ]


    for word in ignored:

        if text_lower == word:
            return False


    # Question indicators

    indicators = [
        "?",
        "what ",
        "why ",
        "how ",
        "difference between",
        "explain ",
        "define ",
        "which ",
        "when ",
        "where ",
        "can ",
        "is ",
        "are ",
        "does ",
        "do ",
        "write ",
        "list ",
        "tell "
    ]


    for indicator in indicators:

        if text_lower.startswith(indicator):
            return True


    return False


# ==========================================
# EXTRACT QUESTIONS
# ==========================================

def collect_questions():

    html = get_page()

    print(
        "Status: page downloaded successfully"
    )

    print(
        "HTML length:",
        len(html)
    )


    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    questions = []


    # InterviewBit questions are commonly
    # contained in heading elements.

    headings = soup.find_all(
        [
            "h2",
            "h3",
            "h4",
            "h5"
        ]
    )


    print(
        "Headings found:",
        len(headings)
    )


    for heading in headings:

        text = heading.get_text(
            " ",
            strip=True
        )


        text = clean_question(
            text
        )


        if not is_question(text):
            continue


        # Avoid duplicate questions
        # from the same webpage.

        if text.lower() in {
            q.lower()
            for q in questions
        }:
            continue


        questions.append(text)


    print(
        "Candidate questions:",
        len(questions)
    )


    return questions


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    try:

        questions = collect_questions()


        print(
            "\nFirst 20 questions:\n"
        )


        for index, question in enumerate(
            questions[:20],
            start=1
        ):

            print(
                f"{index}. {question}"
            )


        print(
            "\nTotal questions:",
            len(questions)
        )


    except Exception as error:

        print(
            "\nERROR:",
            error
        )