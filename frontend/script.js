const API_BASE_URL = "http://127.0.0.1:8000";

const resumeFile = document.getElementById("resumeFile");
const jdFile = document.getElementById("jdFile");

const analyzeBtn = document.getElementById("analyzeBtn");

const status = document.getElementById("status");
const result = document.getElementById("result");
const processing = document.getElementById("processing");

const resumeSelected = document.getElementById("resumeSelected");
const jdSelected = document.getElementById("jdSelected");


/* -----------------------------
   FILE SELECTION
----------------------------- */

resumeFile.addEventListener("change", () => {

    const file = resumeFile.files[0];

    if (!file) {
        resumeSelected.innerHTML =
            "<span>○</span><span>No file selected</span>";
        return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {
        resumeSelected.innerHTML =
            "<span>✕</span><span>Please select a PDF file</span>";

        resumeFile.value = "";
        return;
    }

    resumeSelected.innerHTML =
        `<span>✓</span><span>${escapeHtml(file.name)}</span>`;
});


jdFile.addEventListener("change", () => {

    const file = jdFile.files[0];

    if (!file) {
        jdSelected.innerHTML =
            "<span>○</span><span>No file selected</span>";
        return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {
        jdSelected.innerHTML =
            "<span>✕</span><span>Please select a PDF file</span>";

        jdFile.value = "";
        return;
    }

    jdSelected.innerHTML =
        `<span>✓</span><span>${escapeHtml(file.name)}</span>`;
});


/* -----------------------------
   ANALYZE EVERYTHING
----------------------------- */

analyzeBtn.addEventListener("click", async () => {

    const resume = resumeFile.files[0];
    const jd = jdFile.files[0];

    if (!resume) {
        status.textContent = "Please upload your resume PDF.";
        return;
    }

    if (!jd) {
        status.textContent = "Please upload the job description PDF.";
        return;
    }

    if (!resume.name.toLowerCase().endsWith(".pdf")) {
        status.textContent = "Resume must be a PDF.";
        return;
    }

    if (!jd.name.toLowerCase().endsWith(".pdf")) {
        status.textContent = "Job description must be a PDF.";
        return;
    }


    /* -----------------------------
       START PROCESSING
    ----------------------------- */

    analyzeBtn.disabled = true;

    processing.classList.remove("hidden");
    result.classList.add("hidden");

    status.textContent =
        "AI agents are analyzing your resume and job description...";


    try {

        /* -----------------------------
           STEP 1: RESUME ANALYSIS
        ----------------------------- */

        status.textContent =
            "Step 1/3: Analyzing your resume...";

        const resumeFormData = new FormData();
        resumeFormData.append("file", resume);

        const resumeResponse = await fetch(
            `${API_BASE_URL}/analyze-resume`,
            {
                method: "POST",
                body: resumeFormData
            }
        );

        const resumeData = await resumeResponse.json();

        if (!resumeResponse.ok || resumeData.error) {
            throw new Error(
                resumeData.error ||
                "Resume analysis failed."
            );
        }


        /* -----------------------------
           STEP 2: JOB DESCRIPTION
        ----------------------------- */

        status.textContent =
            "Step 2/3: Analyzing the job description...";

        const jdFormData = new FormData();
        jdFormData.append("file", jd);

        const jdResponse = await fetch(
            `${API_BASE_URL}/analyze-job-description-file`,
            {
                method: "POST",
                body: jdFormData
            }
        );

        const jdData = await jdResponse.json();

        if (!jdResponse.ok || jdData.error) {
            throw new Error(
                jdData.error ||
                "Job description analysis failed."
            );
        }


        /* -----------------------------
           STEP 3: QUESTION GENERATION
        ----------------------------- */

        status.textContent =
            "Step 3/3: Generating personalized interview questions...";

        const questionResponse = await fetch(
            `${API_BASE_URL}/generate-questions`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    resume_analysis: resumeData,
                    jd_analysis: jdData
                })
            }
        );

        const questionData = await questionResponse.json();

        if (!questionResponse.ok || questionData.error) {
            throw new Error(
                questionData.error ||
                "Question generation failed."
            );
        }


        /* -----------------------------
           DISPLAY RESULTS
        ----------------------------- */

        displayResult(
            resumeData,
            jdData,
            questionData
        );

        status.textContent =
            "Analysis complete! Your personalized interview questions are ready.";

    }

    catch (error) {

        console.error("Interview preparation error:", error);

        status.textContent =
            error.message ||
            "Something went wrong while analyzing your files.";

    }

    finally {

        processing.classList.add("hidden");
        analyzeBtn.disabled = false;

    }

});


/* -----------------------------
   DISPLAY RESULTS
----------------------------- */

function displayResult(
    resumeData,
    jdData,
    questionData
) {

    result.classList.remove("hidden");


    /* -----------------------------
       CANDIDATE
    ----------------------------- */

    document.getElementById("candidate").innerHTML = `

        <div class="card">

            <h3>Candidate</h3>

            <p>
                <strong>Name:</strong>
                ${escapeHtml(
                    resumeData.candidate?.name ||
                    "Not available"
                )}
            </p>

            <p>
                <strong>Email:</strong>
                ${escapeHtml(
                    resumeData.candidate?.email ||
                    "Not available"
                )}
            </p>

            <p>
                <strong>CGPA:</strong>
                ${escapeHtml(
                    resumeData.candidate?.cgpa ||
                    "Not available"
                )}
            </p>

        </div>
    `;


    /* -----------------------------
       SKILLS
    ----------------------------- */

    document.getElementById("skills").innerHTML = `

        <div class="card">

            <h3>Technical Skills</h3>

            ${createList(
                resumeData.skills?.technical
            )}

        </div>
    `;


    /* -----------------------------
       PROJECTS
    ----------------------------- */

    document.getElementById("projects").innerHTML = `

        <div class="card">

            <h3>Projects</h3>

            ${createList(
                resumeData.projects
            )}

        </div>
    `;


    /* -----------------------------
       EXPERIENCE
    ----------------------------- */

    document.getElementById("experience").innerHTML = `

        <div class="card">

            <h3>Internships & Experience</h3>

            ${createList(
                resumeData.internships?.length
                    ? resumeData.internships
                    : resumeData.experience
            )}

        </div>
    `;


    /* -----------------------------
       CERTIFICATIONS
    ----------------------------- */

    document.getElementById("certifications").innerHTML = `

        <div class="card">

            <h3>Certifications</h3>

            ${createList(
                resumeData.certifications
            )}

        </div>
    `;


    /* -----------------------------
       STRENGTHS
    ----------------------------- */

    document.getElementById("strengths").innerHTML = `

        <div class="card">

            <h3>Strengths</h3>

            ${createList(
                resumeData.strengths
            )}

        </div>
    `;


    /* -----------------------------
       SKILL GAPS
    ----------------------------- */

    document.getElementById("skillGaps").innerHTML = `

        <div class="card">

            <h3>Skill Gaps</h3>

            ${createList(
                resumeData.skill_gaps
            )}

        </div>
    `;


    /* -----------------------------
       QUESTIONS
    ----------------------------- */

    displayQuestions(questionData.questions);


    /* -----------------------------
       JOB INFORMATION
    ----------------------------- */

    displayJobInformation(jdData);
}


/* -----------------------------
   DISPLAY QUESTIONS
----------------------------- */

function displayQuestions(questions) {

    if (!questions || questions.length === 0) {
        return;
    }


    const questionContainer = document.createElement("div");

    questionContainer.id = "questions";

    questionContainer.className = "questions-section";


    questionContainer.innerHTML = `

        <div class="section-label">
            PERSONALIZED INTERVIEW
        </div>

        <h2>Interview Questions</h2>

        <div class="questions-list">

            ${questions.map((item, index) => `

                <div class="question-card">

                    <div class="question-number">
                        ${index + 1}
                    </div>

                    <div class="question-content">

                        <h3>
                            ${escapeHtml(
                                item.question ||
                                "Question unavailable"
                            )}
                        </h3>

                        <div class="question-meta">

                            <span>
                                ${escapeHtml(
                                    item.category ||
                                    "General"
                                )}
                            </span>

                            <span>
                                ${escapeHtml(
                                    item.difficulty ||
                                    "Medium"
                                )}
                            </span>

                        </div>

                        ${
                            item.reason
                                ? `
                                    <p class="question-reason">
                                        <strong>Why this question:</strong>
                                        ${escapeHtml(item.reason)}
                                    </p>
                                `
                                : ""
                        }

                    </div>

                </div>

            `).join("")}

        </div>
    `;


    result.appendChild(questionContainer);
}


/* -----------------------------
   DISPLAY JOB INFORMATION
----------------------------- */

function displayJobInformation(jdData) {

    if (!jdData || !jdData.job) {
        return;
    }


    const existingJob =
        document.getElementById("jobInformation");

    if (existingJob) {
        existingJob.remove();
    }


    const jobContainer = document.createElement("div");

    jobContainer.id = "jobInformation";

    jobContainer.className = "job-information";


    jobContainer.innerHTML = `

        <div class="card">

            <h3>Job Information</h3>

            <p>
                <strong>Role:</strong>
                ${escapeHtml(
                    jdData.job.job_title ||
                    "Not available"
                )}
            </p>

            <p>
                <strong>Company:</strong>
                ${escapeHtml(
                    jdData.job.company ||
                    "Not available"
                )}
            </p>

            <p>
                <strong>Location:</strong>
                ${escapeHtml(
                    jdData.job.location ||
                    "Not available"
                )}
            </p>

            <p>
                <strong>Experience:</strong>
                ${escapeHtml(
                    jdData.job.experience_required ||
                    "Not available"
                )}
            </p>

        </div>
    `;


    result.insertBefore(
        jobContainer,
        result.firstChild
    );
}


/* -----------------------------
   CREATE LIST
----------------------------- */

function createList(items) {

    if (!items || items.length === 0) {
        return "<p>Not available</p>";
    }


    return `

        <ul>

            ${items.map(item => {

                if (typeof item === "object") {

                    return `

                        <li>

                            <strong>
                                ${escapeHtml(
                                    item.name ||
                                    item.title ||
                                    "Item"
                                )}
                            </strong>

                            ${
                                item.description
                                    ? `<br>${escapeHtml(item.description)}`
                                    : ""
                            }

                            ${
                                item.technologies
                                    ? `
                                        <br>
                                        <strong>
                                            Technologies:
                                        </strong>

                                        ${escapeHtml(
                                            Array.isArray(item.technologies)
                                                ? item.technologies.join(", ")
                                                : item.technologies
                                        )}
                                    `
                                    : ""
                            }

                            ${
                                item.role
                                    ? `
                                        <br>
                                        <strong>Role:</strong>
                                        ${escapeHtml(item.role)}
                                    `
                                    : ""
                            }

                        </li>
                    `;
                }


                return `<li>${escapeHtml(item)}</li>`;

            }).join("")}

        </ul>
    `;
}


/* -----------------------------
   HTML ESCAPING
----------------------------- */

function escapeHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}