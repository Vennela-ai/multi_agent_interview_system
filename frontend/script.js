const API_BASE_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {

    // =========================================================
    // COMMON HELPERS
    // =========================================================

    function storeData(key, data) {
        localStorage.setItem(key, JSON.stringify(data));
    }

    function getStoredData(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (error) {
            console.error("LocalStorage error:", error);
            return null;
        }
    }

    function escapeHTML(value) {
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

    function displayValue(value) {
        if (
            value === null ||
            value === undefined ||
            value === ""
        ) {
            return "Not available";
        }

        if (typeof value === "object") {
            return `<pre>${escapeHTML(
                JSON.stringify(value, null, 2)
            )}</pre>`;
        }

        return escapeHTML(value);
    }

    function displayList(value) {

        if (!value) {
            return "Not available";
        }

        if (!Array.isArray(value)) {
            return displayValue(value);
        }

        if (value.length === 0) {
            return "Not available";
        }

        return value
            .map(item => {

                if (
                    typeof item === "object" &&
                    item !== null
                ) {
                    return `
                        <div class="result-list-item">
                            ${escapeHTML(
                                item.name ||
                                item.title ||
                                item.role ||
                                JSON.stringify(item)
                            )}
                        </div>
                    `;
                }

                return `
                    <div class="result-list-item">
                        ${escapeHTML(item)}
                    </div>
                `;
            })
            .join("");
    }

    function createTags(items) {

        if (
            !Array.isArray(items) ||
            items.length === 0
        ) {
            return `
                <span class="empty-value">
                    Not available
                </span>
            `;
        }

        return items
            .map(item => `
                <span class="tag">
                    ${escapeHTML(item)}
                </span>
            `)
            .join("");
    }

    function getElement(id) {
        return document.getElementById(id);
    }


    // =========================================================
    // ANALYZE PAGE
    // =========================================================

    const resumeFile = getElement("resumeFile");
    const jdFile = getElement("jdFile");

    const resumeFileName =
        getElement("resumeFileName");

    const jdFileName =
        getElement("jdFileName");

    const analyzeBtn =
        getElement("analyzeBtn");

    const processing =
        getElement("processing");

    const processingStatus =
        getElement("processingStatus");


    // =========================================================
    // RESUME FILE SELECTION
    // =========================================================

    if (resumeFile) {

        resumeFile.addEventListener(
            "change",
            () => {

                if (resumeFile.files.length > 0) {

                    const file =
                        resumeFile.files[0];

                    if (resumeFileName) {
                        resumeFileName.textContent =
                            file.name;
                    }

                } else {

                    if (resumeFileName) {
                        resumeFileName.textContent =
                            "No file selected";
                    }
                }
            }
        );
    }


    // =========================================================
    // JD FILE SELECTION
    // =========================================================

    if (jdFile) {

        jdFile.addEventListener(
            "change",
            () => {

                if (jdFile.files.length > 0) {

                    const file =
                        jdFile.files[0];

                    if (jdFileName) {
                        jdFileName.textContent =
                            file.name;
                    }

                } else {

                    if (jdFileName) {
                        jdFileName.textContent =
                            "No file selected";
                    }
                }
            }
        );
    }


    // =========================================================
    // ANALYZE BUTTON
    // =========================================================

    if (analyzeBtn) {

        analyzeBtn.addEventListener(
            "click",
            async () => {

                console.log(
                    "Analyze button clicked"
                );


                // -------------------------------------------------
                // CHECK FILES
                // -------------------------------------------------

                if (
                    !resumeFile ||
                    !resumeFile.files.length
                ) {

                    alert(
                        "Please select your Resume PDF."
                    );

                    return;
                }

                if (
                    !jdFile ||
                    !jdFile.files.length
                ) {

                    alert(
                        "Please select the Job Description PDF."
                    );

                    return;
                }


                const resume =
                    resumeFile.files[0];

                const jd =
                    jdFile.files[0];


                // -------------------------------------------------
                // CHECK RESUME PDF
                // -------------------------------------------------

                if (
                    resume.type !==
                        "application/pdf" &&
                    !resume.name
                        .toLowerCase()
                        .endsWith(".pdf")
                ) {

                    alert(
                        "Resume must be a PDF file."
                    );

                    return;
                }


                // -------------------------------------------------
                // CHECK JD PDF
                // -------------------------------------------------

                if (
                    jd.type !==
                        "application/pdf" &&
                    !jd.name
                        .toLowerCase()
                        .endsWith(".pdf")
                ) {

                    alert(
                        "Job Description must be a PDF file."
                    );

                    return;
                }


                // -------------------------------------------------
                // DISABLE BUTTON
                // -------------------------------------------------

                analyzeBtn.disabled = true;

                const originalButtonText =
                    analyzeBtn.innerHTML;

                analyzeBtn.innerHTML = `
                    Analyzing...
                    <span>⏳</span>
                `;


                // -------------------------------------------------
                // SHOW PROCESSING
                // -------------------------------------------------

                if (processing) {
                    processing.style.display =
                        "block";
                }


                try {

                    // =================================================
                    // STEP 1 - RESUME ANALYSIS
                    // =================================================

                    updateProcessing(
                        "Step 1 of 2: Analyzing your resume..."
                    );

                    console.log(
                        "Sending resume to backend..."
                    );


                    const resumeFormData =
                        new FormData();

                    resumeFormData.append(
                        "file",
                        resume
                    );


                    const resumeResponse =
                        await fetch(
                            `${API_BASE_URL}/analyze-resume`,
                            {
                                method: "POST",
                                body: resumeFormData
                            }
                        );


                    console.log(
                        "Resume response:",
                        resumeResponse.status
                    );


                    if (!resumeResponse.ok) {

                        const errorText =
                            await resumeResponse.text();

                        throw new Error(
                            `Resume analysis failed (${resumeResponse.status}): ${errorText}`
                        );
                    }


                    const resumeAnalysis =
                        await resumeResponse.json();


                    console.log(
                        "Resume analysis:",
                        resumeAnalysis
                    );


                    // Save resume analysis
                    storeData(
                        "resumeAnalysis",
                        resumeAnalysis
                    );


                    // =================================================
                    // STEP 2 - JD ANALYSIS
                    // =================================================

                    updateProcessing(
                        "Step 2 of 2: Analyzing the job description..."
                    );

                    console.log(
                        "Sending JD to backend..."
                    );


                    const jdFormData =
                        new FormData();

                    jdFormData.append(
                        "file",
                        jd
                    );


                    const jdResponse =
                        await fetch(
                            `${API_BASE_URL}/analyze-job-description-file`,
                            {
                                method: "POST",
                                body: jdFormData
                            }
                        );


                    console.log(
                        "JD response:",
                        jdResponse.status
                    );


                    if (!jdResponse.ok) {

                        const errorText =
                            await jdResponse.text();

                        throw new Error(
                            `Job description analysis failed (${jdResponse.status}): ${errorText}`
                        );
                    }


                    const jdAnalysis =
                        await jdResponse.json();


                    console.log(
                        "JD analysis:",
                        jdAnalysis
                    );


                    // Save JD analysis
                    storeData(
                        "jdAnalysis",
                        jdAnalysis
                    );


                    // =================================================
                    // COMPLETE
                    // =================================================

                    updateProcessing(
                        "Analysis complete! Opening resume analysis..."
                    );


                    setTimeout(
                        () => {

                            window.location.href =
                                "resume-results.html";

                        },
                        700
                    );

                } catch (error) {

                    console.error(
                        "Analysis error:",
                        error
                    );


                    alert(
                        "Something went wrong.\n\n" +
                        error.message +
                        "\n\nPlease make sure the FastAPI backend is running."
                    );


                    // Restore button
                    analyzeBtn.disabled =
                        false;

                    analyzeBtn.innerHTML =
                        originalButtonText;


                    if (processing) {
                        processing.style.display =
                            "none";
                    }
                }
            }
        );
    }


    // =========================================================
    // PROCESSING STATUS
    // =========================================================

    function updateProcessing(message) {

        if (processingStatus) {

            processingStatus.textContent =
                message;
        }

        console.log(message);
    }


    // =========================================================
    // RESUME RESULTS PAGE
    // =========================================================

    if (getElement("candidate")) {

        console.log(
            "Loading resume results page..."
        );


        const resumeAnalysis =
            getStoredData("resumeAnalysis");


        if (!resumeAnalysis) {

            console.warn(
                "No resume analysis found."
            );

        } else {

            // =================================================
            // CANDIDATE
            // =================================================

            const candidate =
                resumeAnalysis.candidate || {};


            const candidateElement =
                getElement("candidate");


            if (candidateElement) {

                candidateElement.innerHTML = `

                    <strong>
                        ${escapeHTML(
                            candidate.name ||
                            "Not available"
                        )}
                    </strong>

                    ${
                        candidate.email
                            ? `<br>${escapeHTML(
                                candidate.email
                            )}`
                            : ""
                    }

                    ${
                        candidate.phone
                            ? `<br>${escapeHTML(
                                candidate.phone
                            )}`
                            : ""
                    }

                    ${
                        candidate.cgpa
                            ? `<br>CGPA: ${escapeHTML(
                                candidate.cgpa
                            )}`
                            : ""
                    }
                `;
            }


            // =================================================
            // EDUCATION
            // =================================================

            const education =
                resumeAnalysis.candidate?.education ||
                resumeAnalysis.education ||
                [];


            const educationElement =
                getElement("education");


            if (educationElement) {

                educationElement.innerHTML =
                    displayList(education);
            }


            // =================================================
            // SKILLS
            // =================================================

            const skills =
                resumeAnalysis.skills || {};


            const skillsElement =
                getElement("skills");


            if (skillsElement) {

                skillsElement.innerHTML = `

                    <div class="skill-group">

                        <strong>
                            Technical Skills
                        </strong>

                        <div class="tag-list">

                            ${createTags(
                                skills.technical || []
                            )}

                        </div>

                    </div>


                    <div class="skill-group">

                        <strong>
                            Programming Languages
                        </strong>

                        <div class="tag-list">

                            ${createTags(
                                skills.programming_languages ||
                                []
                            )}

                        </div>

                    </div>


                    <div class="skill-group">

                        <strong>
                            Tools & Technologies
                        </strong>

                        <div class="tag-list">

                            ${createTags(
                                skills.tools_and_technologies ||
                                []
                            )}

                        </div>

                    </div>
                `;
            }


            // =================================================
            // PROJECTS
            // =================================================

            const projects =
                resumeAnalysis.projects || [];


            const projectsElement =
                getElement("projects");


            if (projectsElement) {

                if (
                    Array.isArray(projects) &&
                    projects.length > 0
                ) {

                    projectsElement.innerHTML =
                        projects
                            .map(
                                (project, index) => {

                                    if (
                                        project &&
                                        typeof project ===
                                            "object"
                                    ) {

                                        return `

                                            <div class="result-list-item">

                                                <strong>
                                                    ${escapeHTML(
                                                        project.name ||
                                                        `Project ${index + 1}`
                                                    )}
                                                </strong>


                                                ${
                                                    Array.isArray(
                                                        project.technologies
                                                    )
                                                        ? `
                                                            <div class="result-list-subtext">

                                                                <strong>
                                                                    Technologies:
                                                                </strong>

                                                                ${escapeHTML(
                                                                    project
                                                                        .technologies
                                                                        .join(", ")
                                                                )}

                                                            </div>
                                                        `
                                                        : ""
                                                }

                                            </div>
                                        `;
                                    }


                                    return `

                                        <div class="result-list-item">

                                            ${escapeHTML(
                                                project
                                            )}

                                        </div>
                                    `;
                                }
                            )
                            .join("");

                } else {

                    projectsElement.innerHTML =
                        "Not available";
                }
            }


            // =================================================
            // EXPERIENCE + INTERNSHIPS
            // =================================================

            const experience =
                Array.isArray(
                    resumeAnalysis.experience
                )
                    ? resumeAnalysis.experience
                    : [];


            const internships =
                Array.isArray(
                    resumeAnalysis.internships
                )
                    ? resumeAnalysis.internships
                    : [];


            const allExperience = [
                ...experience,
                ...internships
            ];


            const experienceElement =
                getElement("experience");


            if (experienceElement) {

                if (
                    allExperience.length > 0
                ) {

                    experienceElement.innerHTML =
                        allExperience
                            .map(
                                (item, index) => {

                                    if (
                                        item &&
                                        typeof item ===
                                            "object"
                                    ) {

                                        return `

                                            <div class="result-list-item">

                                                <strong>
                                                    ${escapeHTML(
                                                        item.title ||
                                                        item.role ||
                                                        `Experience ${index + 1}`
                                                    )}
                                                </strong>


                                                ${
                                                    item.company
                                                        ? `
                                                            <div class="result-list-subtext">
                                                                ${escapeHTML(
                                                                    item.company
                                                                )}
                                                            </div>
                                                        `
                                                        : ""
                                                }


                                                ${
                                                    item.duration
                                                        ? `
                                                            <div class="result-list-subtext">
                                                                ${escapeHTML(
                                                                    item.duration
                                                                )}
                                                            </div>
                                                        `
                                                        : ""
                                                }


                                                ${
                                                    item.description
                                                        ? `
                                                            <p class="result-list-description">
                                                                ${escapeHTML(
                                                                    item.description
                                                                )}
                                                            </p>
                                                        `
                                                        : ""
                                                }

                                            </div>
                                        `;
                                    }


                                    return `

                                        <div class="result-list-item">

                                            ${escapeHTML(
                                                item
                                            )}

                                        </div>
                                    `;
                                }
                            )
                            .join("");

                } else {

                    experienceElement.innerHTML =
                        "Not available";
                }
            }


            // =================================================
            // CERTIFICATIONS
            // =================================================

            const certifications =
                resumeAnalysis.certifications ||
                [];


            const certificationsElement =
                getElement("certifications");


            if (certificationsElement) {

                if (
                    Array.isArray(
                        certifications
                    ) &&
                    certifications.length > 0
                ) {

                    certificationsElement.innerHTML =
                        certifications
                            .map(
                                cert => `

                                    <div class="result-list-item">

                                        ${escapeHTML(
                                            cert
                                        )}

                                    </div>
                                `
                            )
                            .join("");

                } else {

                    certificationsElement.innerHTML =
                        "Not available";
                }
            }


            // =================================================
            // STRENGTHS
            // =================================================

            const strengths =
                resumeAnalysis.strengths || [];


            const strengthsElement =
                getElement("strengths");


            if (strengthsElement) {

                strengthsElement.innerHTML =
                    createTags(strengths);
            }


            // =================================================
            // ACHIEVEMENTS
            // =================================================

            const achievements =
                resumeAnalysis.achievements || [];


            const achievementsElement =
                getElement("achievements");


            if (achievementsElement) {

                achievementsElement.innerHTML =
                    displayList(achievements);
            }
        }
    }


    // =========================================================
    // JD RESULTS PAGE
    // =========================================================

    if (getElement("jdJobDetails")) {

        console.log(
            "Loading JD results page..."
        );


        const jdAnalysis =
            getStoredData("jdAnalysis");


        if (!jdAnalysis) {

            console.warn(
                "No JD analysis found."
            );

        } else {

            // =================================================
            // HELPER FOR JD DATA
            // =================================================

            function findJDValue(...keys) {

                for (const key of keys) {

                    if (
                        jdAnalysis[key] !== undefined &&
                        jdAnalysis[key] !== null &&
                        jdAnalysis[key] !== ""
                    ) {

                        return jdAnalysis[key];
                    }
                }

                return null;
            }


            // =================================================
            // JOB DETAILS
            // =================================================

            const jdJobDetails =
                getElement("jdJobDetails");


            if (jdJobDetails) {

                const value =
                    findJDValue(
                        "job_details",
                        "jobDetails",
                        "job",
                        "role",
                        "position"
                    );


                jdJobDetails.innerHTML =
                    displayValue(value);
            }


            // =================================================
            // REQUIRED SKILLS
            // =================================================

            const jdRequiredSkills =
                getElement("jdRequiredSkills");


            if (jdRequiredSkills) {

                const value =
                    findJDValue(
                        "required_skills",
                        "requiredSkills",
                        "skills",
                        "technical_skills"
                    );


                jdRequiredSkills.innerHTML =
                    displayList(value);
            }


            // =================================================
            // PREFERRED SKILLS
            // =================================================

            const jdPreferredSkills =
                getElement("jdPreferredSkills");


            if (jdPreferredSkills) {

                const value =
                    findJDValue(
                        "preferred_skills",
                        "preferredSkills",
                        "preferred_qualifications"
                    );


                jdPreferredSkills.innerHTML =
                    displayList(value);
            }


            // =================================================
            // PROGRAMMING LANGUAGES
            // =================================================

            const jdLanguages =
                getElement("jdLanguages");


            if (jdLanguages) {

                const value =
                    findJDValue(
                        "languages",
                        "programming_languages",
                        "programmingLanguages"
                    );


                jdLanguages.innerHTML =
                    displayList(value);
            }


            // =================================================
            // TOOLS & TECHNOLOGIES
            // =================================================

            const jdTools =
                getElement("jdTools");


            if (jdTools) {

                const value =
                    findJDValue(
                        "tools_and_technologies",
                        "toolsAndTechnologies",
                        "tools",
                        "technologies"
                    );


                jdTools.innerHTML =
                    displayList(value);
            }


            // =================================================
            // EDUCATION
            // =================================================

            const jdEducation =
                getElement("jdEducation");


            if (jdEducation) {

                const value =
                    findJDValue(
                        "education",
                        "educational_qualification",
                        "educationalQualification"
                    );


                jdEducation.innerHTML =
                    displayList(value);
            }


            // =================================================
            // RESPONSIBILITIES
            // =================================================

            const jdResponsibilities =
                getElement("jdResponsibilities");


            if (jdResponsibilities) {

                const value =
                    findJDValue(
                        "responsibilities",
                        "job_responsibilities",
                        "jobResponsibilities"
                    );


                jdResponsibilities.innerHTML =
                    displayList(value);
            }


            // =================================================
            // QUALIFICATIONS
            // =================================================

            const jdQualifications =
                getElement("jdQualifications");


            if (jdQualifications) {

                const value =
                    findJDValue(
                        "qualifications",
                        "requirements",
                        "minimum_qualifications",
                        "minimumQualifications"
                    );


                jdQualifications.innerHTML =
                    displayList(value);
            }


            // =================================================
            // DOMAIN
            // =================================================

            const jdDomain =
                getElement("jdDomain");


            if (jdDomain) {

                const value =
                    findJDValue(
                        "domain",
                        "industry",
                        "job_domain"
                    );


                jdDomain.innerHTML =
                    displayValue(value);
            }


            // =================================================
            // KEYWORDS
            // =================================================

            const jdKeywords =
                getElement("jdKeywords");


            if (jdKeywords) {

                const value =
                    findJDValue(
                        "keywords",
                        "key_words",
                        "keyWords"
                    );


                jdKeywords.innerHTML =
                    displayList(value);
            }
        }
    }


    // =========================================================
    // GENERATE QUESTIONS BUTTON
    // =========================================================

    const generateQuestionsBtn =
        getElement("generateQuestionsBtn");


    if (generateQuestionsBtn) {

        generateQuestionsBtn.addEventListener(
            "click",
            async () => {

                console.log(
                    "Generate Questions button clicked"
                );


                // -------------------------------------------------
                // GET STORED ANALYSIS
                // -------------------------------------------------

                const resumeAnalysis =
                    getStoredData(
                        "resumeAnalysis"
                    );


                const jdAnalysis =
                    getStoredData(
                        "jdAnalysis"
                    );


                if (!resumeAnalysis) {

                    alert(
                        "Resume analysis is not available."
                    );

                    return;
                }


                if (!jdAnalysis) {

                    alert(
                        "Job description analysis is not available."
                    );

                    return;
                }


                // -------------------------------------------------
                // DISABLE BUTTON
                // -------------------------------------------------

                const originalButtonText =
                    generateQuestionsBtn.innerHTML;


                generateQuestionsBtn.disabled =
                    true;


                generateQuestionsBtn.innerHTML = `
                    Generating Questions...
                    <span>⏳</span>
                `;


                try {

                    console.log(
                        "Sending resume + JD to question generator..."
                    );


                    // =================================================
                    // GENERATE QUESTIONS API
                    // =================================================

                    const response =
                        await fetch(
                            `${API_BASE_URL}/generate-questions`,
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({

                                    resume_analysis:
                                        resumeAnalysis,

                                    jd_analysis:
                                        jdAnalysis

                                })
                            }
                        );


                    console.log(
                        "Question response:",
                        response.status
                    );


                    if (!response.ok) {

                        const errorText =
                            await response.text();

                        throw new Error(
                            `Question generation failed (${response.status}): ${errorText}`
                        );
                    }


                    const questionData =
                        await response.json();


                    console.log(
                        "Question data:",
                        questionData
                    );


                    if (questionData.error) {

                        throw new Error(
                            questionData.error
                        );
                    }


                    // -------------------------------------------------
                    // STORE QUESTIONS
                    // -------------------------------------------------

                    storeData(
                        "questionData",
                        questionData
                    );


                    // -------------------------------------------------
                    // GO TO QUESTIONS PAGE
                    // -------------------------------------------------

                    window.location.href =
                        "questions.html";


                } catch (error) {

                    console.error(
                        "Question generation error:",
                        error
                    );


                    alert(
                        "Unable to generate interview questions.\n\n" +
                        error.message +
                        "\n\nPlease make sure the FastAPI backend is running."
                    );


                    // Restore button
                    generateQuestionsBtn.disabled =
                        false;


                    generateQuestionsBtn.innerHTML =
                        originalButtonText;
                }
            }
        );
    }


    // =========================================================
    // QUESTIONS PAGE
    // =========================================================

    const questionsContainer =
        getElement("questionsContainer");


    if (questionsContainer) {

        console.log(
            "Loading questions page..."
        );


        const questionData =
            getStoredData("questionData");


        if (!questionData) {

            questionsContainer.innerHTML = `

                <div class="questions-empty">

                    <h3>
                        No questions available
                    </h3>

                    <p>
                        Please analyze your resume and
                        job description first.
                    </p>

                </div>

            `;

        } else {

            let questions = [];


            // Backend normally returns:
            // { questions: [...] }

            if (
                questionData &&
                Array.isArray(
                    questionData.questions
                )
            ) {

                questions =
                    questionData.questions;

            }

            // Also support direct array
            else if (
                Array.isArray(questionData)
            ) {

                questions =
                    questionData;
            }


            console.log(
                "Questions:",
                questions
            );


            const questionCount =
                getElement("questionCount");


            if (questionCount) {

                questionCount.textContent =
                    questions.length;
            }


            if (questions.length === 0) {

                questionsContainer.innerHTML = `

                    <div class="questions-empty">

                        <h3>
                            No questions generated
                        </h3>

                        <p>
                            The question generator did not
                            return any questions.
                        </p>

                    </div>

                `;

            } else {

                questionsContainer.innerHTML =
                    questions
                        .map(
                            (item, index) => {

                                const question =
                                    typeof item === "object"
                                        ? item.question
                                        : item;


                                const category =
                                    typeof item === "object"
                                        ? item.category
                                        : "";


                                const difficulty =
                                    typeof item === "object"
                                        ? item.difficulty
                                        : "";


                                const reason =
                                    typeof item === "object"
                                        ? item.reason
                                        : "";


                                return `

                                    <div class="question-card">

                                        <div class="question-card-header">

                                            <span class="question-index">

                                                ${String(
                                                    index + 1
                                                ).padStart(
                                                    2,
                                                    "0"
                                                )}

                                            </span>


                                            <div class="question-meta">

                                                ${
                                                    category
                                                        ? `
                                                            <span>
                                                                ${escapeHTML(
                                                                    category
                                                                )}
                                                            </span>
                                                        `
                                                        : ""
                                                }


                                                ${
                                                    difficulty
                                                        ? `
                                                            <span>
                                                                ${escapeHTML(
                                                                    difficulty
                                                                )}
                                                            </span>
                                                        `
                                                        : ""
                                                }

                                            </div>

                                        </div>


                                        <div class="question-text">

                                            ${escapeHTML(
                                                question ||
                                                "Question not available"
                                            )}

                                        </div>


                                        ${
                                            reason
                                                ? `
                                                    <div class="question-reason">

                                                        <strong>
                                                            Why this question:
                                                        </strong>

                                                        ${escapeHTML(
                                                            reason
                                                        )}

                                                    </div>
                                                `
                                                : ""
                                        }

                                    </div>

                                `;
                            }
                        )
                        .join("");
            }
        }
    }


    // =========================================================
    // FINAL LOG
    // =========================================================

    console.log(
        "HirePrep script loaded successfully."
    );

});