import re
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from models import (
    Role,
    Question,
    RoleQuestion,
    QuestionSource
)


# ---------------------------------------------------------
# SOURCE REGISTRY
# ---------------------------------------------------------

SOURCE_REGISTRY = {

    # =========================================================
    # PROGRAMMING LANGUAGES
    # =========================================================

    "python": [
        {
            "url": "https://www.interviewbit.com/python-interview-questions/",
            "title": "Python Interview Questions",
            "source_type": "InterviewBit"
        },
        {
            "url": "https://www.geeksforgeeks.org/python/python-interview-questions/",
            "title": "Python Interview Questions",
            "source_type": "GeeksforGeeks"
        },
        {
            "url": "https://www.edureka.co/blog/interview-questions/python-interview-questions",
            "title": "Python Interview Questions",
            "source_type": "Edureka"
        }
    ],

    "java": [
        {
            "url": "https://www.interviewbit.com/java-interview-questions/",
            "title": "Java Interview Questions",
            "source_type": "InterviewBit"
        },
        {
            "url": "https://www.geeksforgeeks.org/java/java-interview-questions/",
            "title": "Java Interview Questions",
            "source_type": "GeeksforGeeks"
        },
        {
            "url": "https://www.edureka.co/blog/interview-questions/java-interview-questions/",
            "title": "Java Interview Questions",
            "source_type": "Edureka"
        }
    ],

    "c": [
        {
            "url": "https://www.geeksforgeeks.org/c/c-interview-questions/",
            "title": "C Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    "javascript": [
        {
            "url": "https://www.interviewbit.com/javascript-interview-questions/",
            "title": "JavaScript Interview Questions",
            "source_type": "InterviewBit"
        },
        {
            "url": "https://www.geeksforgeeks.org/javascript/javascript-interview-questions/",
            "title": "JavaScript Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    "html": [
        {
            "url": "https://www.interviewbit.com/html-interview-questions/",
            "title": "HTML Interview Questions",
            "source_type": "InterviewBit"
        },
        {
            "url": "https://www.geeksforgeeks.org/html/html-interview-questions/",
            "title": "HTML Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    "css": [
        {
            "url": "https://www.geeksforgeeks.org/css/css-interview-questions/",
            "title": "CSS Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    # =========================================================
    # WEB DEVELOPMENT
    # =========================================================

    "react": [
        {
            "url": "https://www.geeksforgeeks.org/reactjs/react-interview-questions/",
            "title": "React Interview Questions",
            "source_type": "GeeksforGeeks"
        },
        {
            "url": "https://www.edureka.co/blog/interview-questions/react-interview-questions/amp/",
            "title": "React Interview Questions",
            "source_type": "Edureka"
        }
    ],

    "angular": [
        {
            "url": "https://www.interviewbit.com/angular-interview-questions/",
            "title": "Angular Interview Questions",
            "source_type": "InterviewBit"
        },
        {
            "url": "https://www.edureka.co/blog/interview-questions/top-angularjs-interview-questions/",
            "title": "Angular Interview Questions",
            "source_type": "Edureka"
        }
    ],

    "nodejs": [
        {
            "url": "https://www.geeksforgeeks.org/node-js/node-interview-questions-and-answers/",
            "title": "Node.js Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    # =========================================================
    # CORE COMPUTER SCIENCE
    # =========================================================

    "data structures": [
        {
            "url": "https://www.interviewbit.com/data-structure-interview-questions/",
            "title": "Data Structure Interview Questions",
            "source_type": "InterviewBit"
        }
    ],

    "algorithms": [],

    "oop": [
        {
            "url": "https://www.geeksforgeeks.org/oops/oops-interview-questions/",
            "title": "OOP Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    "os": [
        {
            "url": "https://www.geeksforgeeks.org/operating-systems/operating-systems-interview-questions/",
            "title": "Operating Systems Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    "dbms": [
        {
            "url": "https://www.geeksforgeeks.org/dbms/commonly-asked-dbms-interview-questions/",
            "title": "DBMS Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    "sql": [
        {
            "url": "https://www.geeksforgeeks.org/sql/sql-interview-questions/",
            "title": "SQL Interview Questions",
            "source_type": "GeeksforGeeks"
        },
        {
            "url": "https://www.edureka.co/blog/interview-questions/sql-interview-questions",
            "title": "SQL Interview Questions",
            "source_type": "Edureka"
        }
    ],

    "networking": [
        {
            "url": "https://www.interviewbit.com/networking-interview-questions/",
            "title": "Computer Networking Interview Questions",
            "source_type": "InterviewBit"
        }
    ],

    "system design": [],

    "software engineering": [
        {
            "url": "https://www.geeksforgeeks.org/software-engineering/software-engineering-interview-questions-and-answers/",
            "title": "Software Engineering Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    # =========================================================
    # DATA / AI / ML
    # =========================================================

    "data science": [
        {
            "url": "https://www.interviewbit.com/data-science-interview-questions/",
            "title": "Data Science Interview Questions",
            "source_type": "InterviewBit"
        },
        {
            "url": "https://www.geeksforgeeks.org/data-science/data-science-interview-questions-and-answers/",
            "title": "Data Science Interview Questions",
            "source_type": "GeeksforGeeks"
        },
        {
            "url": "https://www.edureka.co/blog/interview-questions/data-science-interview-questions/",
            "title": "Data Science Interview Questions",
            "source_type": "Edureka"
        }
    ],

    "data analyst": [],

    "machine learning": [
        {
            "url": "https://www.geeksforgeeks.org/machine-learning/machine-learning-interview-questions/",
            "title": "Machine Learning Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    "ai": [
        {
            "url": "https://www.geeksforgeeks.org/artificial-intelligence/artificial-intelligenceai-interview-questions-and-answers/",
            "title": "Artificial Intelligence Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    # =========================================================
    # CLOUD / DEVOPS
    # =========================================================

    "aws": [
        {
            "url": "https://www.geeksforgeeks.org/aws/aws-interview-questions/",
            "title": "AWS Interview Questions",
            "source_type": "GeeksforGeeks"
        },
        {
            "url": "https://www.edureka.co/blog/interview-questions/aws-interview-questions/",
            "title": "AWS Interview Questions",
            "source_type": "Edureka"
        }
    ],

    "cloud": [
        {
            "url": "https://www.interviewbit.com/cloud-computing-interview-questions/",
            "title": "Cloud Computing Interview Questions",
            "source_type": "InterviewBit"
        }
    ],

    "linux": [
        {
            "url": "https://www.interviewbit.com/linux-interview-questions/",
            "title": "Linux Interview Questions",
            "source_type": "InterviewBit"
        }
    ],

    "devops": [
        {
            "url": "https://www.geeksforgeeks.org/devops/devops-interview-questions/",
            "title": "DevOps Interview Questions",
            "source_type": "GeeksforGeeks"
        },
        {
            "url": "https://www.edureka.co/blog/interview-questions/top-devops-interview-questions-2016/amp/",
            "title": "DevOps Interview Questions",
            "source_type": "Edureka"
        }
    ],

    # =========================================================
    # TESTING
    # =========================================================

    "testing": [
        {
            "url": "https://www.geeksforgeeks.org/software-testing/software-testing-interview-questions/",
            "title": "Software Testing Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ],

    "selenium": [
        {
            "url": "https://www.geeksforgeeks.org/software-testing/selenium-interview-questions/",
            "title": "Selenium Interview Questions",
            "source_type": "GeeksforGeeks"
        }
    ]
}
# ---------------------------------------------------------
# ROLE → TOPIC MAPPING
# ---------------------------------------------------------

ROLE_TOPICS = {

    "python developer": [
        "python",
        "data structures",
        "sql"
    ],

    "java developer": [
        "java",
        "data structures",
        "sql"
    ],

    "software engineer": [
        "data structures",
        "sql",
        "java",
        "python",
        "system design"
    ],

    "software developer": [
        "data structures",
        "sql",
        "java",
        "python"
    ],

    "backend developer": [
        "python",
        "java",
        "sql",
        "data structures",
        "system design"
    ],

    "python backend developer": [
        "python",
        "sql",
        "data structures",
        "system design"
    ],

    "java backend developer": [
        "java",
        "sql",
        "data structures",
        "system design"
    ],

    "full stack developer": [
        "javascript",
        "html",
        "python",
        "java",
        "sql"
    ],

    "frontend developer": [
        "javascript",
        "html",
        "data structures"
    ],

    "ui developer": [
        "javascript",
        "html"
    ],

    "react developer": [
        "javascript",
        "html"
    ],

    "angular developer": [
        "angular",
        "javascript",
        "html"
    ],

    "data analyst": [
        "sql",
        "python",
        "data science"
    ],

    "data scientist": [
        "python",
        "sql",
        "data science",
        "data structures"
    ],

    "data engineer": [
        "python",
        "sql",
        "data structures",
        "system design"
    ],

    "ai engineer": [
        "python",
        "data science",
        "data structures"
    ],

    "machine learning engineer": [
        "python",
        "data science",
        "data structures"
    ],

    "ai/ml engineer": [
        "python",
        "data science",
        "data structures"
    ],

    "generative ai engineer": [
        "python",
        "data science",
        "system design"
    ],

    "network engineer": [
        "networking",
        "data structures"
    ],

    "network administrator": [
        "networking"
    ],

    "c developer": [
        "c",
        "data structures"
    ]
}


# ---------------------------------------------------------
# QUESTION NORMALIZATION
# ---------------------------------------------------------

def normalize_question(text):
    text = text.strip()

    # Remove source numbering such as:
    # Q1. Question
    # Q44. Question
    # 1. Question
    # 44) Question
    # 12: Question
    text = re.sub(
        r"^\s*(?:Q\s*)?\d+\s*[\.\):\-]\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(r"\s+", " ", text)

    text = text.rstrip(" .:-")

    return text.lower().strip()
def is_question_heading(text):

    if not text:
        return False

    text = text.strip()

    if len(text) < 15:
        return False

    if len(text) > 300:
        return False

    lower_text = text.lower()

    ignored = [
        "table of contents",
        "related articles",
        "related topics",
        "about interviewbit",
        "subscribe",
        "comments",
        "conclusion",
        "introduction",
        "references",
        "top companies",
        "popular courses",
        "read more",
        "frequently asked questions"
    ]

    if lower_text in ignored:
        return False

    question_words = [
        "what ",
        "why ",
        "how ",
        "which ",
        "when ",
        "where ",
        "explain ",
        "difference ",
        "compare ",
        "define ",
        "describe ",
        "can ",
        "is ",
        "are ",
        "does ",
        "do ",
        "will ",
        "have ",
        "has "
    ]

    if text.endswith("?"):
        return True

    for word in question_words:

        if lower_text.startswith(word):
            return True

    return False


# ---------------------------------------------------------
# FETCH WEB PAGE
# ---------------------------------------------------------

def fetch_page(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/154.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    return response.text


# ---------------------------------------------------------
# EXTRACT QUESTIONS
# ---------------------------------------------------------

# ---------------------------------------------------------
# SEARCH ENGINE SOURCE DISCOVERY
# ---------------------------------------------------------

def discover_sources_for_role(role_name, max_results=40):
    """
    Discover public interview-question pages for a role.

    This does NOT generate questions.
    It only finds publicly accessible webpages that may contain
    real interview questions.
    """

    role = role_name.strip()

    search_queries = [
        f'"{role}" interview questions',
        f'"{role}" technical interview questions',
        f'"{role}" interview questions and answers',
        f'"{role}" coding interview questions',
        f'"{role}" programming interview questions',
        f'"{role}" fresher interview questions',
        f'"{role}" experienced interview questions',
        f'"{role}" frequently asked interview questions',
    ]

    # Important public technical/interview domains.
    # Search is not restricted to these domains; they simply
    # receive additional targeted searches.
    domains = [
        "geeksforgeeks.org",
        "interviewbit.com",
        "indeed.com",
        "coursera.org",
        "datacamp.com",
        "simplilearn.com",
        "javatpoint.com",
        "scaler.com",
        "intellipaat.com",
        "edureka.co",
        "greatlearning.in",
        "hackerrank.com",
        "leetcode.com",
        "interviewquery.com",
        "turing.com",
        "talent.com",
        "upgrad.com",
        "naukri.com",
    ]

    discovered = []
    seen_urls = set()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/154.0 Safari/537.36"
        )
    }

    def add_result(url, title):
        if not url:
            return

        url = url.strip()

        if not url.startswith("http"):
            return

        # Remove tracking fragments
        url = url.split("#")[0]

        if url in seen_urls:
            return

        seen_urls.add(url)

        discovered.append({
            "url": url,
            "title": title or f"{role} Interview Questions",
            "source_type": (
                url.split("/")[2]
                .replace("www.", "")
                .split(".")[0]
                .title()
            )
        })

    # -----------------------------------------------------
    # General web searches
    # -----------------------------------------------------

    for query in search_queries:

        if len(discovered) >= max_results:
            break

        try:

            search_url = (
                "https://html.duckduckgo.com/html/?q="
                + requests.utils.quote(query)
            )

            response = requests.get(
                search_url,
                headers=headers,
                timeout=20
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            for result in soup.select(".result"):

                link = result.select_one(".result__a")

                if not link:
                    continue

                href = link.get("href")

                title = link.get_text(
                    " ",
                    strip=True
                )

                if not href:
                    continue

                # DuckDuckGo may return redirect URLs.
                if "uddg=" in href:

                    from urllib.parse import urlparse, parse_qs

                    parsed = urlparse(href)

                    params = parse_qs(
                        parsed.query
                    )

                    if "uddg" in params:
                        href = params["uddg"][0]

                add_result(
                    href,
                    title
                )

                if len(discovered) >= max_results:
                    break

        except Exception as e:

            print(
                f"SEARCH SKIP | {query} | {e}"
            )

    # -----------------------------------------------------
    # Targeted domain searches
    # -----------------------------------------------------

    for domain in domains:

        if len(discovered) >= max_results:
            break

        domain_queries = [
            f'site:{domain} "{role}" interview questions',
            f'site:{domain} "{role}" technical interview',
        ]

        for query in domain_queries:

            if len(discovered) >= max_results:
                break

            try:

                search_url = (
                    "https://html.duckduckgo.com/html/?q="
                    + requests.utils.quote(query)
                )

                response = requests.get(
                    search_url,
                    headers=headers,
                    timeout=20
                )

                response.raise_for_status()

                soup = BeautifulSoup(
                    response.text,
                    "html.parser"
                )

                for result in soup.select(".result"):

                    link = result.select_one(
                        ".result__a"
                    )

                    if not link:
                        continue

                    href = link.get("href")

                    title = link.get_text(
                        " ",
                        strip=True
                    )

                    if not href:
                        continue

                    if "uddg=" in href:

                        from urllib.parse import (
                            urlparse,
                            parse_qs
                        )

                        parsed = urlparse(href)

                        params = parse_qs(
                            parsed.query
                        )

                        if "uddg" in params:
                            href = params["uddg"][0]

                    add_result(
                        href,
                        title
                    )

                    if len(discovered) >= max_results:
                        break

            except Exception as e:

                print(
                    f"DOMAIN SEARCH SKIP | "
                    f"{domain} | {e}"
                )

    print(
        f"DISCOVERY | {role} | "
        f"{len(discovered)} candidate sources"
    )

    return discovered


# ---------------------------------------------------------
# EXTRACT QUESTIONS
# ---------------------------------------------------------

def extract_questions_from_html(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    questions = []
    seen = set()

    # -----------------------------------------------------
    # 1. Heading-based questions
    # -----------------------------------------------------

    for heading in soup.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6"]
    ):

        text = heading.get_text(
            " ",
            strip=True
        )

        if not is_question_heading(text):
            continue

        text = re.sub(
            r"^\s*(?:Q\s*)?\d+\s*[\.\):\-]\s*",
            "",
            text,
            flags=re.IGNORECASE
        ).strip()

        normalized = normalize_question(text)

        if not normalized:
            continue

        if normalized in seen:
            continue

        seen.add(normalized)

        questions.append(text)

    # -----------------------------------------------------
    # 2. Numbered-list questions
    # -----------------------------------------------------

    for item in soup.find_all("li"):

        text = item.get_text(
            " ",
            strip=True
        )

        if not is_question_heading(text):
            continue

        text = re.sub(
            r"^\s*(?:Q\s*)?\d+\s*[\.\):\-]\s*",
            "",
            text,
            flags=re.IGNORECASE
        ).strip()

        normalized = normalize_question(text)

        if not normalized:
            continue

        if normalized in seen:
            continue

        seen.add(normalized)

        questions.append(text)

    # -----------------------------------------------------
    # 3. Paragraph questions
    # -----------------------------------------------------

    for paragraph in soup.find_all("p"):

        text = paragraph.get_text(
            " ",
            strip=True
        )

        if not is_question_heading(text):
            continue

        normalized = normalize_question(text)

        if not normalized:
            continue

        if normalized in seen:
            continue

        seen.add(normalized)

        questions.append(text)

    return questions


# ---------------------------------------------------------
# GET SOURCES FOR ROLE
# ---------------------------------------------------------

def get_sources_for_role(role_name):

    """
    Returns configured sources PLUS dynamically discovered
    public interview-question sources.
    """

    sources = []

    # -----------------------------------------------------
    # Existing configured sources
    # -----------------------------------------------------

    topics = infer_topics_for_role(
        role_name
    )

    for topic in topics:

        for source in SOURCE_REGISTRY.get(
            topic,
            []
        ):

            if source not in sources:
                sources.append(source)

    # -----------------------------------------------------
    # Dynamically discover additional sources
    # -----------------------------------------------------

    discovered_sources = discover_sources_for_role(
        role_name,
        max_results=40
    )

    for source in discovered_sources:

        if not any(
            existing["url"] == source["url"]
            for existing in sources
        ):
            sources.append(source)

    print(
        f"SOURCES | {role_name} | "
        f"{len(sources)} total sources"
    )

    return sources
def calculate_question_relevance(role_name, question_source_url):
    """
    Calculates relevance of a question for a role
    based on the technical topics associated with that role.

    No AI is used.
    """

    role_topics = set(
        infer_topics_for_role(role_name)
    )

    matched_topics = set()

    for topic, sources in SOURCE_REGISTRY.items():

        for source in sources:

            if source.get("url") == question_source_url:
                matched_topics.add(topic)

    if not matched_topics:
        return 1

    matching_topics = role_topics.intersection(
        matched_topics
    )

    if not matching_topics:
        return 1

    return len(matching_topics)
def update_role_question_relevance(db, role_name):
    """
    Recalculate relevance scores for all questions
    already associated with a role.
    """

    role = (
        db.query(Role)
        .filter(
            Role.normalized_name == role_name.strip().lower()
        )
        .first()
    )

    if not role:
        return {
            "success": False,
            "message": f"Role not found: {role_name}"
        }

    role_questions = (
        db.query(RoleQuestion)
        .filter(
            RoleQuestion.role_id == role.id
        )
        .all()
    )

    updated = 0

    for role_question in role_questions:

        question = (
            db.query(Question)
            .filter(
                Question.id == role_question.question_id
            )
            .first()
        )

        if not question:
            continue

        source = (
            db.query(QuestionSource)
            .filter(
                QuestionSource.question_id == question.id
            )
            .order_by(
                QuestionSource.id.asc()
            )
            .first()
        )

        if not source:
            question.relevance_score = 1
            continue

        question.relevance_score = calculate_question_relevance(
            role_name,
            source.source_url
        )

        updated += 1

    db.commit()

    return {
        "success": True,
        "role": role.name,
        "updated_questions": updated
    }
def retrieve_questions_for_role(db, role_name, required_count):
    role = (
        db.query(Role)
        .filter(Role.normalized_name == role_name.strip().lower())
        .first()
    )

    if not role:
        return 0

    sources = get_sources_for_role(role_name)

    existing_role_questions = (
        db.query(RoleQuestion.question_id)
        .filter(RoleQuestion.role_id == role.id)
        .all()
    )

    existing_ids = {row[0] for row in existing_role_questions}

    existing_questions = db.query(Question).all()

    normalized_question_map = {}

    for question in existing_questions:
        normalized = normalize_question(question.question_text)

        if normalized:
            normalized_question_map[normalized] = question

    current_total = len(existing_ids)

    if current_total >= required_count:
        return 0

    added_questions = 0
    processed_urls = set()

    for source in sources:

        if current_total >= required_count:
            break

        source_url = source.get("url")
        source_type = source.get("source_type", "Web")

        if not source_url:
            continue

        if source_url in processed_urls:
            continue

        processed_urls.add(source_url)

        try:
            response = requests.get(
                source_url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 Chrome/131.0 Safari/537.36"
                    )
                },
                timeout=15
            )

            if response.status_code != 200:
                continue

            questions_found = extract_questions_from_html(
                response.text
            )

        except Exception:
            continue

        for question_text in questions_found:

            if current_total >= required_count:
                break

            normalized = normalize_question(question_text)

            if not normalized:
                continue

            question = normalized_question_map.get(normalized)

            if question is None:

                question = Question(
                    question_text=question_text.strip(),
                    category=source_type,
                    frequency_score=1,
                    relevance_score=calculate_question_relevance(
                        role_name,
                        source_url
                    ),
                    verified=True
                )

                db.add(question)
                db.flush()

                normalized_question_map[normalized] = question

            if question.id not in existing_ids:

                role_question = RoleQuestion(
                    role_id=role.id,
                    question_id=question.id
                )

                db.add(role_question)

                existing_ids.add(question.id)
                current_total += 1
                added_questions += 1

            existing_source = (
                db.query(QuestionSource)
                .filter(
                    QuestionSource.question_id == question.id,
                    QuestionSource.source_url == source_url
                )
                .first()
            )

            if not existing_source:

                source_record = QuestionSource(
                    question_id=question.id,
                    source_type=source_type,
                    source_url=source_url,
                    source_title=source.get("title")
                )

                db.add(source_record)

    db.commit()

    return added_questions
def retrieve_questions_by_skills(
    db,
    skills,
    limit=20
):
    """
    Retrieve verified interview questions related to
    the supplied skills.

    Example:
        skills = ["Python", "SQL", "Flask"]
    """

    if not skills:
        return []

    # Normalize skills
    normalized_skills = []

    for skill in skills:
        if not skill:
            continue

        skill = str(skill).strip().lower()

        if skill and skill not in normalized_skills:
            normalized_skills.append(skill)

    if not normalized_skills:
        return []

    # Get all verified questions
    questions = (
        db.query(Question)
        .filter(
            Question.verified == True
        )
        .all()
    )

    matched_questions = []

    for question in questions:

        question_text = (
            question.question_text or ""
        ).lower()

        category = (
            question.category or ""
        ).lower()

        matched = False

        for skill in normalized_skills:

            if skill in question_text:
                matched = True
                break

            if skill in category:
                matched = True
                break

        if matched:
            matched_questions.append(question)

        if len(matched_questions) >= limit:
            break

    return [
        {
            "id": question.id,
            "question": question.question_text,
            "category": question.category
        }
        for question in matched_questions
    ]