const API_BASE_URL = "http://127.0.0.1:8000";


// =========================================================
// DOM & DISPLAY HELPERS
// =========================================================

function getElement(id) {
    return document.getElementById(id);
}


function storeData(key, data) {

    localStorage.setItem(
        key,
        JSON.stringify(data)
    );
}


function getStoredData(key) {

    const data =
        localStorage.getItem(key);

    if (!data) {
        return null;
    }

    try {

        return JSON.parse(data);

    } catch (error) {

        console.error(
            `Unable to parse stored data for ${key}:`,
            error
        );

        return null;
    }
}


function escapeHTML(value) {

    if (
        value === null ||
        value === undefined
    ) {
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

        return `
            <pre>${escapeHTML(
                JSON.stringify(
                    value,
                    null,
                    2
                )
            )}</pre>
        `;
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


// =========================================================
// DOM READY
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "HirePrep script loaded successfully."
        );


        // =====================================================
        // ANALYZE PAGE
        // =====================================================

        const resumeFile =
            getElement("resumeFile");

        const jdFile =
            getElement("jdFile");

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


        // =====================================================
        // PROCESSING STATUS
        // =====================================================

        function updateProcessing(message) {

            if (processingStatus) {

                processingStatus.textContent =
                    message;
            }

            console.log(message);
        }


        // =====================================================
        // RESUME FILE SELECTION
        // =====================================================

        if (resumeFile) {

            resumeFile.addEventListener(
                "change",
                () => {

                    if (
                        resumeFile.files.length > 0
                    ) {

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


        // =====================================================
        // JD FILE SELECTION
        // =====================================================

        if (jdFile) {

            jdFile.addEventListener(
                "change",
                () => {

                    if (
                        jdFile.files.length > 0
                    ) {

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


        // =====================================================
        // ANALYZE BUTTON
        // =====================================================

        if (analyzeBtn) {

            analyzeBtn.addEventListener(
                "click",
                async () => {

                    console.log(
                        "Analyze button clicked"
                    );


                    // -------------------------------------------------
                    // CHECK RESUME
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


                    // -------------------------------------------------
                    // CHECK JD
                    // -------------------------------------------------

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
                    // CHECK RESUME TYPE
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
                    // CHECK JD TYPE
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


                    if (processing) {

                        processing.style.display =
                            "block";
                    }


                    try {

                        // =============================================
                        // STEP 1 — RESUME
                        // =============================================

                        updateProcessing(
                            "Step 1 of 2: Analyzing your resume..."
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


                        storeData(
                            "resumeAnalysis",
                            resumeAnalysis
                        );


                        // =============================================
                        // STEP 2 — JD
                        // =============================================

                        updateProcessing(
                            "Step 2 of 2: Analyzing the job description..."
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


                        storeData(
                            "jdAnalysis",
                            jdAnalysis
                        );


                        // =============================================
                        // COMPLETE
                        // =============================================

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


        // =====================================================
        // RESUME RESULTS PAGE
        // =====================================================

        if (
            getElement("candidate")
        ) {

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

                // ===============================================
                // CANDIDATE
                // ===============================================

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


                // ===============================================
                // EDUCATION
                // ===============================================

                const education =
                    resumeAnalysis
                        .candidate
                        ?.education ||
                    resumeAnalysis.education ||
                    [];


                const educationElement =
                    getElement("education");


                if (educationElement) {

                    educationElement.innerHTML =
                        displayList(
                            education
                        );
                }


                // ===============================================
                // SKILLS
                // ===============================================

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
                                    skills.programming_languages || []
                                )}

                            </div>

                        </div>


                        <div class="skill-group">

                            <strong>
                                Tools & Technologies
                            </strong>

                            <div class="tag-list">

                                ${createTags(
                                    skills.tools_and_technologies || []
                                )}

                            </div>

                        </div>

                    `;
                }


                // ===============================================
                // PROJECTS
                // ===============================================

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
                                    (
                                        project,
                                        index
                                    ) => {

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
                                                ${escapeHTML(project)}
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


                // ===============================================
                // EXPERIENCE + INTERNSHIPS
                // ===============================================

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
                                    (
                                        item,
                                        index
                                    ) => {

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
                                                ${escapeHTML(item)}
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


                // ===============================================
                // CERTIFICATIONS
                // ===============================================

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
                                            ${escapeHTML(cert)}
                                        </div>
                                    `
                                )
                                .join("");

                    } else {

                        certificationsElement.innerHTML =
                            "Not available";
                    }
                }


                // ===============================================
                // STRENGTHS
                // ===============================================

                const strengths =
                    resumeAnalysis.strengths || [];


                const strengthsElement =
                    getElement("strengths");


                if (strengthsElement) {

                    strengthsElement.innerHTML =
                        createTags(
                            strengths
                        );
                }


                // ===============================================
                // ACHIEVEMENTS
                // ===============================================

                const achievements =
                    resumeAnalysis.achievements || [];


                const achievementsElement =
                    getElement("achievements");


                if (achievementsElement) {

                    achievementsElement.innerHTML =
                        displayList(
                            achievements
                        );
                }
            }
        }


        // =====================================================
        // JD RESULTS PAGE
        // =====================================================

        const jdJobDetails =
            getElement("jdJobDetails");


        if (jdJobDetails) {

            console.log(
                "Loading JD results page..."
            );


            const jdAnalysis =
                getStoredData("jdAnalysis");


            if (!jdAnalysis) {

                alert(
                    "Job description analysis is not available."
                );

                window.location.href =
                    "analyze.html";

            } else {

                const job =
                    jdAnalysis.job || {};


                jdJobDetails.innerHTML = `

                    <div class="detail-row">

                        <strong>
                            Job Title
                        </strong>

                        <span>
                            ${displayValue(
                                job.job_title
                            )}
                        </span>

                    </div>


                    <div class="detail-row">

                        <strong>
                            Company
                        </strong>

                        <span>
                            ${displayValue(
                                job.company
                            )}
                        </span>

                    </div>


                    <div class="detail-row">

                        <strong>
                            Location
                        </strong>

                        <span>
                            ${displayValue(
                                job.location
                            )}
                        </span>

                    </div>


                    <div class="detail-row">

                        <strong>
                            Experience
                        </strong>

                        <span>
                            ${
                                job.experience_required
                                    ? displayValue(
                                        job.experience_required
                                    )
                                    : "Not specified"
                            }
                        </span>

                    </div>

                `;


                const skills =
                    jdAnalysis.skills || {};


                const jdRequiredSkills =
                    getElement("jdRequiredSkills");


                if (jdRequiredSkills) {

                    jdRequiredSkills.innerHTML =
                        createTags(
                            skills.required || []
                        );
                }


                const jdPreferredSkills =
                    getElement("jdPreferredSkills");


                if (jdPreferredSkills) {

                    jdPreferredSkills.innerHTML =
                        createTags(
                            skills.preferred || []
                        );
                }


                const jdLanguages =
                    getElement("jdLanguages");


                if (jdLanguages) {

                    jdLanguages.innerHTML =
                        createTags(
                            skills.programming_languages || []
                        );
                }


                const jdTools =
                    getElement("jdTools");


                if (jdTools) {

                    jdTools.innerHTML =
                        createTags(
                            skills.tools_and_technologies || []
                        );
                }


                const jdEducation =
                    getElement("jdEducation");


                if (jdEducation) {

                    jdEducation.innerHTML =
                        displayList(
                            jdAnalysis.education_requirements || []
                        );
                }


                const jdResponsibilities =
                    getElement("jdResponsibilities");


                if (jdResponsibilities) {

                    jdResponsibilities.innerHTML =
                        displayList(
                            jdAnalysis.responsibilities || []
                        );
                }


                const jdQualifications =
                    getElement("jdQualifications");


                if (jdQualifications) {

                    jdQualifications.innerHTML =
                        displayList(
                            jdAnalysis.qualifications || []
                        );
                }


                const jdCertifications =
                    getElement("jdCertifications");


                if (jdCertifications) {

                    jdCertifications.innerHTML =
                        displayList(
                            jdAnalysis.certifications || []
                        );
                }


                const jdDomain =
                    getElement("jdDomain");


                if (jdDomain) {

                    jdDomain.innerHTML =
                        createTags(
                            jdAnalysis.domain_knowledge || []
                        );
                }


                const jdKeywords =
                    getElement("jdKeywords");


                if (jdKeywords) {

                    jdKeywords.innerHTML =
                        createTags(
                            jdAnalysis.keywords || []
                        );
                }
            }
        }


        // =====================================================
        // GENERATE QUESTIONS
        // =====================================================

        const generateQuestionsBtn =
            getElement("generateQuestionsBtn");


        if (generateQuestionsBtn) {

            generateQuestionsBtn.addEventListener(
                "click",
                async () => {


// =====================================================
// QUESTION SETTINGS PAGE
// =====================================================

const generateQuestionsBtn =
    getElement("generateQuestionsBtn");

if (generateQuestionsBtn) {

    generateQuestionsBtn.addEventListener(
        "click",
        async () => {

            const resumeAnalysis =
                getStoredData("resumeAnalysis");

            const jdAnalysis =
                getStoredData("jdAnalysis");

            const selectedCount =
                document.querySelector(
                    'input[name="questionCount"]:checked'
                );

            const count =
                selectedCount
                    ? parseInt(selectedCount.value)
                    : 5;

            const selectedDifficulty =
                document.querySelector(
                    'input[name="difficulty"]:checked'
                );

            const difficulty =
                selectedDifficulty
                    ? selectedDifficulty.value
                    : "Medium";

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

            const originalButtonText =
                generateQuestionsBtn.innerHTML;

            generateQuestionsBtn.disabled =
                true;

            generateQuestionsBtn.innerHTML = `
                Generating Questions...
                <span>⏳</span>
            `;

            try {

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
                                    jdAnalysis,

                                count:
                                    count,

                                difficulty:
                                    difficulty
                            })
                        }
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

                if (questionData.error) {

                    throw new Error(
                        questionData.error
                    );
                }

                storeData(
                    "questionData",
                    questionData
                );

                storeData(
                    "questionSettings",
                    {
                        count: count,
                        difficulty: difficulty
                    }
                );

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

                generateQuestionsBtn.disabled =
                    false;

                generateQuestionsBtn.innerHTML =
                    originalButtonText;
            }
        }
    );
}


                    // ---------------------------------------------
                    // GET STORED DATA
                    // ---------------------------------------------

                    const resumeAnalysis =
                        getStoredData(
                            "resumeAnalysis"
                        );


                    const jdAnalysis =
                        getStoredData(
                            "jdAnalysis"
                        );


                    // ---------------------------------------------
                    // GET SETTINGS
                    // ---------------------------------------------

                    const questionCount =
                        getElement(
                            "questionCount"
                        );


                    const selectedDifficulty =
                        document.querySelector(
                            'input[name="difficulty"]:checked'
                        );


                    const count =
                        questionCount
                            ? parseInt(
                                questionCount.value
                            )
                            : 10;


                    const difficulty =
                        selectedDifficulty
                            ? selectedDifficulty.value
                            : "Mixed";


                    // ---------------------------------------------
                    // VALIDATION
                    // ---------------------------------------------

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


                    // ---------------------------------------------
                    // DISABLE BUTTON
                    // ---------------------------------------------

                    const originalButtonText =
                        generateQuestionsBtn.innerHTML;


                    generateQuestionsBtn.disabled =
                        true;


                    generateQuestionsBtn.innerHTML = `
                        Generating Questions...
                        <span>⏳</span>
                    `;


                    try {

                        // =========================================
                        // API REQUEST
                        // =========================================

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
                                            jdAnalysis,

                                        count:
                                            count,

                                        difficulty:
                                            difficulty

                                    })
                                }
                            );


                        // =========================================
                        // CHECK RESPONSE
                        // =========================================

                        if (!response.ok) {

                            const errorText =
                                await response.text();

                            throw new Error(
                                `Question generation failed (${response.status}): ${errorText}`
                            );
                        }


                        // =========================================
                        // READ JSON
                        // =========================================

                        const questionData =
                            await response.json();


                        if (
                            questionData.error
                        ) {

                            throw new Error(
                                questionData.error
                            );
                        }


                        console.log(
                            "Generated questions:",
                            questionData
                        );


                        // =========================================
                        // STORE QUESTIONS
                        // =========================================

                        storeData(
                            "questionData",
                            questionData
                        );


                        // =========================================
                        // OPEN QUESTIONS PAGE
                        // =========================================

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


                        generateQuestionsBtn.disabled =
                            false;


                        generateQuestionsBtn.innerHTML =
                            originalButtonText;
                    }
                }
            );
        }


        // =====================================================
        // QUESTIONS PAGE
        // =====================================================

        const questionsContainer =
            getElement(
                "questionsContainer"
            );


        if (questionsContainer) {

            console.log(
                "Loading questions page..."
            );


            const questionData =
                getStoredData(
                    "questionData"
                );


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


                if (
                    Array.isArray(
                        questionData.questions
                    )
                ) {

                    questions =
                        questionData.questions;

                } else if (
                    Array.isArray(
                        questionData
                    )
                ) {

                    questions =
                        questionData;
                }


                console.log(
                    "Questions:",
                    questions
                );


                // ---------------------------------------------
                // QUESTION COUNT DISPLAY
                // ---------------------------------------------

                const questionCountDisplay =
                    getElement(
                        "questionCount"
                    );


                if (
                    questionCountDisplay &&
                    questionCountDisplay.tagName !==
                        "SELECT"
                ) {

                    questionCountDisplay.textContent =
                        questions.length;
                }


                // ---------------------------------------------
                // RENDER QUESTIONS
                // ---------------------------------------------

                function renderQuestions(
                    selectedDifficulty = "All"
                ) {

                    let filteredQuestions =
                        questions;


                    if (
                        selectedDifficulty !==
                        "All"
                    ) {

                        filteredQuestions =
                            questions.filter(
                                question =>
                                    question.difficulty ===
                                    selectedDifficulty
                            );
                    }


                    if (
                        filteredQuestions.length ===
                        0
                    ) {

                        questionsContainer.innerHTML = `

                            <div class="questions-empty">

                                <h3>
                                    No ${escapeHTML(
                                        selectedDifficulty
                                    )} questions available
                                </h3>

                                <p>
                                    Try another difficulty level.
                                </p>

                            </div>

                        `;

                        return;
                    }


                    questionsContainer.innerHTML =
                        filteredQuestions
                            .map(
                                (
                                    item,
                                    index
                                ) => {

                                    const question =
                                        typeof item ===
                                            "object"
                                            ? item.question
                                            : item;


                                    const category =
                                        typeof item ===
                                            "object"
                                            ? item.category
                                            : "";


                                    const difficulty =
                                        typeof item ===
                                            "object"
                                            ? item.difficulty
                                            : "";


                                    const reason =
                                        typeof item ===
                                            "object"
                                            ? item.reason
                                            : "";


                                    const difficultyClass =
                                        String(
                                            difficulty || ""
                                        ).toLowerCase();


                                    return `

                                        <div class="question-card">

                                            <div class="question-card-header">

                                                <span class="question-number">

                                                    Question ${
                                                        index + 1
                                                    }

                                                </span>


                                                ${
                                                    difficulty
                                                        ? `
                                                            <span class="question-difficulty ${difficultyClass}">
                                                                ${escapeHTML(
                                                                    difficulty
                                                                )}
                                                            </span>
                                                        `
                                                        : ""
                                                }

                                            </div>


                                            <h3>

                                                ${escapeHTML(
                                                    question ||
                                                    "Question not available"
                                                )}

                                            </h3>


                                            ${
                                                category
                                                    ? `
                                                        <p class="question-category">

                                                            Category:
                                                            ${escapeHTML(
                                                                category
                                                            )}

                                                        </p>
                                                    `
                                                    : ""
                                            }


                                            ${
                                                reason
                                                    ? `
                                                        <p class="question-reason">

                                                            <strong>
                                                                Why this question:
                                                            </strong>

                                                            ${escapeHTML(
                                                                reason
                                                            )}

                                                        </p>
                                                    `
                                                    : ""
                                            }

                                        </div>

                                    `;
                                }
                            )
                            .join("");
                }


                // ---------------------------------------------
                // FILTER BUTTONS
                // ---------------------------------------------

                const questionFilters =
                    document.querySelectorAll(
                        ".question-filter"
                    );


                questionFilters.forEach(
                    filter => {

                        filter.addEventListener(
                            "click",
                            () => {

                                questionFilters.forEach(
                                    button => {

                                        button.classList.remove(
                                            "active"
                                        );
                                    }
                                );


                                filter.classList.add(
                                    "active"
                                );


                                const difficulty =
                                    filter.dataset.difficulty ||
                                    "All";


                                renderQuestions(
                                    difficulty
                                );
                            }
                        );
                    }
                );


                // ---------------------------------------------
                // INITIAL DISPLAY
                // ---------------------------------------------

                renderQuestions(
                    "All"
                );
            }
        }


        // =====================================================
        // GENERATE JD-TAILORED RESUME
        // =====================================================

        const generateResumeBtn =
            getElement(
                "generateResumeBtn"
            );


        if (generateResumeBtn) {

            generateResumeBtn.addEventListener(
                "click",
                async () => {

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


                    const originalButtonText =
                        generateResumeBtn.innerHTML;


                    generateResumeBtn.disabled =
                        true;


                    generateResumeBtn.innerHTML = `
                        Generating Resume...
                        <span>⏳</span>
                    `;


                    try {

                        const response =
                            await fetch(
                                `${API_BASE_URL}/generate-tailored-resume`,
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


                        if (!response.ok) {

                            const errorText =
                                await response.text();

                            throw new Error(
                                `Resume generation failed (${response.status}): ${errorText}`
                            );
                        }


                        const tailoredResume =
                            await response.json();


                        if (
                            tailoredResume.error
                        ) {

                            throw new Error(
                                tailoredResume.error
                            );
                        }


                        storeData(
                            "tailoredResume",
                            tailoredResume
                        );


                        window.location.href =
                            "tailored-resume.html";


                    } catch (error) {

                        console.error(
                            "Tailored resume generation error:",
                            error
                        );


                        alert(
                            "Unable to generate the tailored resume.\n\n" +
                            error.message +
                            "\n\nPlease make sure the FastAPI backend is running."
                        );


                        generateResumeBtn.disabled =
                            false;


                        generateResumeBtn.innerHTML =
                            originalButtonText;
                    }
                }
            );
        }


        // =====================================================
        // TAILORED RESUME PAGE
        // =====================================================

        const resumeName =
            getElement(
                "resumeName"
            );


        if (resumeName) {

            const tailoredResume =
                getStoredData(
                    "tailoredResume"
                );


            if (!tailoredResume) {

                alert(
                    "Tailored resume data is not available."
                );

                window.location.href =
                    "jd-results.html";

            } else {

                // =============================================
                // CANDIDATE
                // =============================================

                const candidate =
                    tailoredResume.candidate || {};


                resumeName.textContent =
                    displayValue(
                        candidate.name
                    );


                const contactParts = [];


                if (candidate.email) {

                    contactParts.push(
                        candidate.email
                    );
                }


                if (candidate.phone) {

                    contactParts.push(
                        candidate.phone
                    );
                }


                if (candidate.location) {

                    contactParts.push(
                        candidate.location
                    );
                }


                const resumeContact =
                    getElement(
                        "resumeContact"
                    );


                if (resumeContact) {

                    resumeContact.textContent =
                        contactParts.join(
                            " | "
                        );
                }


                // =============================================
                // SUMMARY
                // =============================================

                const resumeSummary =
                    getElement(
                        "resumeSummary"
                    );


                if (resumeSummary) {

                    resumeSummary.textContent =
                        displayValue(
                            tailoredResume.summary
                        );
                }


                // =============================================
                // SKILLS
                // =============================================

                const skills =
                    tailoredResume.skills || {};


                const technical =
                    skills.technical || [];


                const programmingLanguages =
                    skills.programming_languages || [];


                const tools =
                    skills.tools_and_technologies || [];


                const resumeSkills =
                    getElement(
                        "resumeSkills"
                    );


                if (resumeSkills) {

                    resumeSkills.innerHTML = `

                        <div class="resume-skill-group">

                            <strong>
                                Technical Skills
                            </strong>

                            <div class="resume-tags">

                                ${createTags(
                                    technical
                                )}

                            </div>

                        </div>


                        <div class="resume-skill-group">

                            <strong>
                                Programming Languages
                            </strong>

                            <div class="resume-tags">

                                ${createTags(
                                    programmingLanguages
                                )}

                            </div>

                        </div>


                        <div class="resume-skill-group">

                            <strong>
                                Tools & Technologies
                            </strong>

                            <div class="resume-tags">

                                ${createTags(
                                    tools
                                )}

                            </div>

                        </div>

                    `;
                }


                // =============================================
                // EDUCATION
                // =============================================

                const resumeEducation =
                    getElement(
                        "resumeEducation"
                    );


                if (resumeEducation) {

                    const education =
                        tailoredResume.education || [];


                    if (
                        education.length ===
                        0
                    ) {

                        resumeEducation.innerHTML =
                            "<p>No education details available.</p>";

                    } else {

                        resumeEducation.innerHTML =
                            education
                                .map(
                                    item => {

                                        if (
                                            typeof item ===
                                            "string"
                                        ) {

                                            return `

                                                <div class="resume-education-item">

                                                    ${escapeHTML(
                                                        item
                                                    )}

                                                </div>

                                            `;
                                        }


                                        if (
                                            typeof item ===
                                                "object" &&
                                            item !== null
                                        ) {

                                            const degree =
                                                item.degree ||
                                                item.course ||
                                                item.program ||
                                                "";


                                            const institution =
                                                item.institution ||
                                                item.college ||
                                                item.university ||
                                                "";


                                            const duration =
                                                item.duration ||
                                                item.year ||
                                                item.years ||
                                                "";


                                            const grade =
                                                item.cgpa ||
                                                item.gpa ||
                                                item.grade ||
                                                "";


                                            return `

                                                <div class="resume-education-item">

                                                    ${
                                                        degree
                                                            ? `
                                                                <div class="resume-item-title">
                                                                    ${escapeHTML(
                                                                        degree
                                                                    )}
                                                                </div>
                                                            `
                                                            : ""
                                                    }


                                                    ${
                                                        institution
                                                            ? `
                                                                <div class="resume-item-meta">
                                                                    ${escapeHTML(
                                                                        institution
                                                                    )}
                                                                </div>
                                                            `
                                                            : ""
                                                    }


                                                    ${
                                                        duration
                                                            ? `
                                                                <div class="resume-item-meta">
                                                                    ${escapeHTML(
                                                                        duration
                                                                    )}
                                                                </div>
                                                            `
                                                            : ""
                                                    }


                                                    ${
                                                        grade
                                                            ? `
                                                                <div class="resume-item-meta">
                                                                    ${escapeHTML(
                                                                        grade
                                                                    )}
                                                                </div>
                                                            `
                                                            : ""
                                                    }

                                                </div>

                                            `;
                                        }


                                        return "";
                                    }
                                )
                                .join("");
                    }
                }


                // =============================================
                // PROJECTS
                // =============================================

                const resumeProjects =
                    getElement(
                        "resumeProjects"
                    );


                if (resumeProjects) {

                    const projects =
                        tailoredResume.projects || [];


                    if (
                        projects.length ===
                        0
                    ) {

                        resumeProjects.innerHTML =
                            "<p>No projects available.</p>";

                    } else {

                        resumeProjects.innerHTML =
                            projects
                                .map(
                                    project => {

                                        const technologies =
                                            project.technologies || [];


                                        return `

                                            <div class="resume-item">

                                                <div class="resume-item-title">

                                                    ${escapeHTML(
                                                        project.name
                                                    )}

                                                </div>


                                                <div class="resume-item-tech">

                                                    ${createTags(
                                                        technologies
                                                    )}

                                                </div>


                                                <p>

                                                    ${escapeHTML(
                                                        project.description
                                                    )}

                                                </p>

                                            </div>

                                        `;
                                    }
                                )
                                .join("");
                    }
                }


                // =============================================
                // INTERNSHIPS
                // =============================================

                const resumeInternships =
                    getElement(
                        "resumeInternships"
                    );


                if (resumeInternships) {

                    const internships =
                        tailoredResume.internships || [];


                    if (
                        internships.length ===
                        0
                    ) {

                        resumeInternships.innerHTML =
                            "<p>No internships available.</p>";

                    } else {

                        resumeInternships.innerHTML =
                            internships
                                .map(
                                    internship => {

                                        return `

                                            <div class="resume-item">

                                                <div class="resume-item-title">

                                                    ${escapeHTML(
                                                        internship.title
                                                    )}

                                                </div>


                                                <div class="resume-item-meta">

                                                    ${escapeHTML(
                                                        internship.company
                                                    )}

                                                    ·

                                                    ${escapeHTML(
                                                        internship.duration
                                                    )}

                                                </div>


                                                <p>

                                                    ${escapeHTML(
                                                        internship.description
                                                    )}

                                                </p>

                                            </div>

                                        `;
                                    }
                                )
                                .join("");
                    }
                }


                // =============================================
                // CERTIFICATIONS
                // =============================================

                const resumeCertifications =
                    getElement(
                        "resumeCertifications"
                    );


                if (resumeCertifications) {

                    const certifications =
                        tailoredResume.certifications || [];


                    resumeCertifications.innerHTML =
                        displayList(
                            certifications
                        );
                }


                // =============================================
                // ACHIEVEMENTS
                // =============================================

                const resumeAchievements =
                    getElement(
                        "resumeAchievements"
                    );


                if (resumeAchievements) {

                    const achievements =
                        tailoredResume.achievements || [];


                    resumeAchievements.innerHTML =
                        displayList(
                            achievements
                        );
                }
            }
        }


        // =====================================================
        // DOWNLOAD JD-TAILORED RESUME
        // =====================================================

        const downloadResumeBtn =
            getElement(
                "downloadResumeBtn"
            );


        if (downloadResumeBtn) {

            downloadResumeBtn.addEventListener(
                "click",
                async () => {

                    const tailoredResume =
                        getStoredData(
                            "tailoredResume"
                        );


                    if (!tailoredResume) {

                        alert(
                            "Tailored resume data is not available."
                        );

                        return;
                    }


                    const originalButtonText =
                        downloadResumeBtn.innerHTML;


                    downloadResumeBtn.disabled =
                        true;


                    downloadResumeBtn.innerHTML = `
                        Preparing PDF...
                        <span>⏳</span>
                    `;


                    try {

                        const response =
                            await fetch(
                                `${API_BASE_URL}/download-tailored-resume`,
                                {
                                    method: "POST",

                                    headers: {
                                        "Content-Type":
                                            "application/json"
                                    },

                                    body: JSON.stringify({

                                        tailored_resume:
                                            tailoredResume

                                    })
                                }
                            );


                        if (!response.ok) {

                            const errorText =
                                await response.text();

                            throw new Error(
                                `PDF download failed (${response.status}): ${errorText}`
                            );
                        }


                        const blob =
                            await response.blob();


                        const url =
                            window.URL.createObjectURL(
                                blob
                            );


                        const link =
                            document.createElement(
                                "a"
                            );


                        link.href =
                            url;


                        link.download =
                            "JD_Tailored_Resume.pdf";


                        document.body.appendChild(
                            link
                        );


                        link.click();


                        link.remove();


                        window.URL.revokeObjectURL(
                            url
                        );


                    } catch (error) {

                        console.error(
                            "PDF download error:",
                            error
                        );


                        alert(
                            "Unable to download the resume.\n\n" +
                            error.message
                        );


                    } finally {

                        downloadResumeBtn.disabled =
                            false;


                        downloadResumeBtn.innerHTML =
                            originalButtonText;
                    }
                }
            );
        }


        // =====================================================
        // EDIT TAILORED RESUME
        // =====================================================

        const editResumeBtn =
            getElement(
                "editResumeBtn"
            );


        const saveResumeBtn =
            getElement(
                "saveResumeBtn"
            );


        if (
            editResumeBtn &&
            saveResumeBtn
        ) {

            editResumeBtn.addEventListener(
                "click",
                () => {

                    const editableFields = [

                        "resumeName",
                        "resumeContact",
                        "resumeSummary",
                        "resumeSkills",
                        "resumeEducation",
                        "resumeProjects",
                        "resumeInternships",
                        "resumeCertifications",
                        "resumeAchievements"

                    ];


                    editableFields.forEach(
                        id => {

                            const element =
                                getElement(id);


                            if (!element) {
                                return;
                            }


                            element.contentEditable =
                                "true";


                            element.classList.add(
                                "resume-editable"
                            );
                        }
                    );


                    editResumeBtn.style.display =
                        "none";


                    saveResumeBtn.style.display =
                        "inline-flex";
                }
            );


            saveResumeBtn.addEventListener(
                "click",
                () => {

                    const tailoredResume =
                        getStoredData(
                            "tailoredResume"
                        );


                    if (!tailoredResume) {

                        alert(
                            "Tailored resume data is not available."
                        );

                        return;
                    }


                    // =========================================
                    // CANDIDATE
                    // =========================================

                    const candidate =
                        tailoredResume.candidate || {};


                    const nameElement =
                        getElement(
                            "resumeName"
                        );


                    const contactElement =
                        getElement(
                            "resumeContact"
                        );


                    if (nameElement) {

                        candidate.name =
                            nameElement.innerText.trim();
                    }


                    if (contactElement) {

                        const parts =
                            contactElement.innerText
                                .split("|")
                                .map(
                                    item =>
                                        item.trim()
                                )
                                .filter(Boolean);


                        candidate.email =
                            parts[0] || "";


                        candidate.phone =
                            parts[1] || "";


                        candidate.location =
                            parts[2] || "";
                    }


                    tailoredResume.candidate =
                        candidate;


                    // =========================================
                    // SUMMARY
                    // =========================================

                    const summaryElement =
                        getElement(
                            "resumeSummary"
                        );


                    if (summaryElement) {

                        tailoredResume.summary =
                            summaryElement.innerText.trim();
                    }


                    // =========================================
                    // SAVE EDITED HTML
                    // =========================================

                    tailoredResume.editedHTML = {

                        name:
                            nameElement
                                ? nameElement.innerHTML
                                : "",


                        contact:
                            contactElement
                                ? contactElement.innerHTML
                                : "",


                        summary:
                            summaryElement
                                ? summaryElement.innerHTML
                                : "",


                        skills:
                            getElement(
                                "resumeSkills"
                            )?.innerHTML || "",


                        education:
                            getElement(
                                "resumeEducation"
                            )?.innerHTML || "",


                        projects:
                            getElement(
                                "resumeProjects"
                            )?.innerHTML || "",


                        internships:
                            getElement(
                                "resumeInternships"
                            )?.innerHTML || "",


                        certifications:
                            getElement(
                                "resumeCertifications"
                            )?.innerHTML || "",


                        achievements:
                            getElement(
                                "resumeAchievements"
                            )?.innerHTML || ""
                    };


                    storeData(
                        "tailoredResume",
                        tailoredResume
                    );


                    // =========================================
                    // DISABLE EDITING
                    // =========================================

                    const editableFields = [

                        "resumeName",
                        "resumeContact",
                        "resumeSummary",
                        "resumeSkills",
                        "resumeEducation",
                        "resumeProjects",
                        "resumeInternships",
                        "resumeCertifications",
                        "resumeAchievements"

                    ];


                    editableFields.forEach(
                        id => {

                            const element =
                                getElement(id);


                            if (!element) {
                                return;
                            }


                            element.contentEditable =
                                "false";


                            element.classList.remove(
                                "resume-editable"
                            );
                        }
                    );


                    editResumeBtn.style.display =
                        "inline-flex";


                    saveResumeBtn.style.display =
                        "none";


                    alert(
                        "Resume changes saved successfully."
                    );
                }
            );
        }

    }
);
// =====================================================
// QUESTION SETTINGS NAVIGATION
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    const button =
        document.getElementById(
            "goToQuestionSettingsBtn"
        );

    if (!button) {
        console.log(
            "Customize Interview Questions button not found."
        );
        return;
    }

    console.log(
        "Customize Interview Questions button found."
    );

    button.onclick = function () {

        console.log(
            "Customize Interview Questions clicked."
        );

        window.location.href =
            "question-settings.html";
    };

});
async function loadRoles() {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/roles"
        );

        const data = await response.json();

        if (!data.success) {
            throw new Error("Failed to load roles");
        }

        const roleSelect =
            document.getElementById("jobRole");

        roleSelect.innerHTML =
            '<option value="">Select Job Role</option>';

        data.roles.forEach(role => {

            const option =
                document.createElement("option");

            option.value = role.name;
            option.textContent = role.name;

            roleSelect.appendChild(option);
        });

    } catch (error) {

        console.error(
            "Error loading roles:",
            error
        );

        alert(
            "Unable to load job roles. " +
            "Please make sure the backend is running."
        );
    }
}
function updateMoreButton() {

    const button =
        document.getElementById("moreQuestionsBtn");

    if (hasMoreQuestions && nextOffset !== null) {
        button.style.display = "inline-block";
    } else {
        button.style.display = "none";
    }
}
startButton.addEventListener("click", function () {

    const selectedRole =
        roleSelect.value;

    if (!selectedRole) {
        alert("Please select a job role.");
        return;
    }

    window.location.href =
        `questions.html?role=${encodeURIComponent(selectedRole)}`;

});