// ===============================
// API BASE URL
// ===============================

const API_BASE_URL = "http://127.0.0.1:8000";


// ===============================
// RESUME ANALYZER
// ===============================

const fileInput = document.getElementById("resumeFile");
const analyzeBtn = document.getElementById("analyzeBtn");
const status = document.getElementById("status");
const result = document.getElementById("result");


if (analyzeBtn) {

    analyzeBtn.addEventListener("click", async () => {

        const file = fileInput ? fileInput.files[0] : null;

        // Check file
        if (!file) {
            status.textContent = "Please select a PDF resume.";
            return;
        }

        // Check PDF
        if (!file.name.toLowerCase().endsWith(".pdf")) {
            status.textContent = "Please upload a PDF file.";
            return;
        }

        // Create FormData
        const formData = new FormData();
        formData.append("file", file);

        status.textContent = "Analyzing resume...";

        try {

            const response = await fetch(
                `${API_BASE_URL}/analyze-resume`,
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            console.log("Resume API response:", data);

            if (!response.ok) {
                throw new Error(
                    data.detail ||
                    data.error ||
                    "Resume analysis failed."
                );
            }

            if (data.error) {
                throw new Error(data.error);
            }

            displayResult(data);

            status.textContent =
                "Resume analyzed successfully!";

        } catch (error) {

            console.error(
                "Resume analyzer error:",
                error
            );

            status.textContent =
                "Could not connect to Resume Analyzer API: " +
                error.message;
        }
    });
}


// ===============================
// DISPLAY RESUME RESULT
// ===============================

function displayResult(data) {

    if (result) {
        result.classList.remove("hidden");
    }

    // ===============================
    // CANDIDATE
    // ===============================

    const candidateElement =
        document.getElementById("candidate");

    if (candidateElement) {

        const candidate =
            data.candidate || {};

        candidateElement.innerHTML = `
            <div class="card">

                <h3>Candidate</h3>

                <p>
                    <strong>Name:</strong>
                    ${candidate.name || "Not available"}
                </p>

                <p>
                    <strong>Email:</strong>
                    ${candidate.email || "Not available"}
                </p>

                <p>
                    <strong>CGPA:</strong>
                    ${candidate.cgpa || "Not available"}
                </p>

            </div>
        `;
    }


    // ===============================
    // TECHNICAL SKILLS
    // ===============================

    const skillsElement =
        document.getElementById("skills");

    if (skillsElement) {

        skillsElement.innerHTML = `
            <div class="card">

                <h3>Technical Skills</h3>

                ${createList(
                    data.skills?.technical
                )}

            </div>
        `;
    }


    // ===============================
    // PROJECTS
    // ===============================

    const projectsElement =
        document.getElementById("projects");

    if (projectsElement) {

        projectsElement.innerHTML = `
            <div class="card">

                <h3>Projects</h3>

                ${createList(
                    data.projects
                )}

            </div>
        `;
    }


    // ===============================
    // EXPERIENCE
    // ===============================

    const experienceElement =
        document.getElementById("experience");

    if (experienceElement) {

        experienceElement.innerHTML = `
            <div class="card">

                <h3>Internships & Experience</h3>

                ${createList(
                    data.internships
                )}

            </div>
        `;
    }


    // ===============================
    // CERTIFICATIONS
    // ===============================

    const certificationsElement =
        document.getElementById("certifications");

    if (certificationsElement) {

        certificationsElement.innerHTML = `
            <div class="card">

                <h3>Certifications</h3>

                ${createList(
                    data.certifications
                )}

            </div>
        `;
    }


    // ===============================
    // STRENGTHS
    // ===============================

    const strengthsElement =
        document.getElementById("strengths");

    if (strengthsElement) {

        strengthsElement.innerHTML = `
            <div class="card">

                <h3>Strengths</h3>

                ${createList(
                    data.strengths
                )}

            </div>
        `;
    }


    // ===============================
    // SKILL GAPS
    // ===============================

    const skillGapsElement =
        document.getElementById("skillGaps");

    if (skillGapsElement) {

        skillGapsElement.innerHTML = `
            <div class="card">

                <h3>Skill Gaps</h3>

                ${createList(
                    data.skill_gaps
                )}

            </div>
        `;
    }
}


// ===============================
// CREATE LIST
// ===============================

function createList(items) {

    if (!items) {
        return "<p>Not available</p>";
    }


    // If backend sends a string

    if (typeof items === "string") {

        return `
            <ul>
                <li>${items}</li>
            </ul>
        `;
    }


    // If backend sends empty array

    if (!Array.isArray(items) || items.length === 0) {

        return "<p>Not available</p>";
    }


    return `
        <ul>

            ${items.map(item => {

                // Object

                if (
                    typeof item === "object" &&
                    item !== null
                ) {

                    return `
                        <li>

                            <strong>
                                ${
                                    item.name ||
                                    item.title ||
                                    item.role ||
                                    "Item"
                                }
                            </strong>

                            ${
                                item.description
                                    ? `<br>${item.description}`
                                    : ""
                            }

                            ${
                                item.technologies
                                    ? `
                                        <br>

                                        <strong>
                                            Technologies:
                                        </strong>

                                        ${
                                            Array.isArray(
                                                item.technologies
                                            )
                                                ? item.technologies.join(", ")
                                                : item.technologies
                                        }
                                    `
                                    : ""
                            }

                            ${
                                item.role
                                    ? `
                                        <br>

                                        <strong>
                                            Role:
                                        </strong>

                                        ${item.role}
                                    `
                                    : ""
                            }

                        </li>
                    `;
                }


                // Normal string

                return `
                    <li>${item}</li>
                `;

            }).join("")}

        </ul>
    `;
}


// ===============================
// JOB DESCRIPTION ANALYZER
// ===============================

const jobDescriptionFile =
    document.getElementById("jobDescriptionFile");

const jobDescriptionInput =
    document.getElementById("jobDescription");

const analyzeJobBtn =
    document.getElementById("analyzeJobBtn");

const jobStatus =
    document.getElementById("jobStatus");

const jobResult =
    document.getElementById("jobResult");


// ===============================
// ANALYZE JOB DESCRIPTION
// ===============================

if (analyzeJobBtn) {

    analyzeJobBtn.addEventListener(
        "click",
        async () => {

            // Get selected JD file

            const file =
                jobDescriptionFile
                    ? jobDescriptionFile.files[0]
                    : null;


            // Get pasted JD

            const jobDescription =
                jobDescriptionInput
                    ? jobDescriptionInput.value.trim()
                    : "";


            // ===============================
            // OPTION 1: JD FILE UPLOAD
            // ===============================

            if (file) {

                const allowedExtensions = [
                    ".txt",
                    ".pdf",
                    ".docx"
                ];

                const fileName =
                    file.name.toLowerCase();

                const isAllowed =
                    allowedExtensions.some(
                        extension =>
                            fileName.endsWith(extension)
                    );


                if (!isAllowed) {

                    jobStatus.textContent =
                        "Please choose a TXT, PDF, or DOCX file.";

                    return;
                }


                jobStatus.textContent =
                    "Uploading and analyzing JD file...";


                try {

                    // Create FormData

                    const formData =
                        new FormData();

                    formData.append(
                        "file",
                        file
                    );


                    // Send JD file to backend

                    const response =
                        await fetch(
                            `${API_BASE_URL}/analyze-job-description-file`,
                            {
                                method: "POST",
                                body: formData
                            }
                        );


                    const data =
                        await response.json();


                    console.log(
                        "JD File API response:",
                        data
                    );


                    if (!response.ok) {

                        throw new Error(
                            data.detail ||
                            data.error ||
                            "JD file analysis failed."
                        );
                    }


                    if (data.error) {

                        throw new Error(
                            data.error
                        );
                    }


                    // Display result

                    displayJobResult(data);


                    jobStatus.textContent =
                        "Job description file analyzed successfully!";


                } catch (error) {

                    console.error(
                        "JD file analyzer error:",
                        error
                    );

                    jobStatus.textContent =
                        "Could not analyze the JD file: " +
                        error.message;
                }


                return;
            }


            // ===============================
            // OPTION 2: PASTE JD
            // ===============================

            if (jobDescription) {

                jobStatus.textContent =
                    "Analyzing job description...";


                try {

                    const response =
                        await fetch(
                            `${API_BASE_URL}/analyze-job-description`,
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({
                                    job_description:
                                        jobDescription
                                })
                            }
                        );


                    const data =
                        await response.json();


                    console.log(
                        "JD Text API response:",
                        data
                    );


                    if (!response.ok) {

                        throw new Error(
                            data.detail ||
                            data.error ||
                            "Job description analysis failed."
                        );
                    }


                    if (data.error) {

                        throw new Error(
                            data.error
                        );
                    }


                    // Display result

                    displayJobResult(data);


                    jobStatus.textContent =
                        "Job description analyzed successfully!";


                } catch (error) {

                    console.error(
                        "JD text analyzer error:",
                        error
                    );

                    jobStatus.textContent =
                        "Could not connect to Job Description Analyzer API: " +
                        error.message;
                }


                return;
            }


            // ===============================
            // NOTHING ENTERED
            // ===============================

            jobStatus.textContent =
                "Please paste a job description or choose a file.";
        }
    );
}


// ===============================
// DISPLAY JOB RESULT
// ===============================

function displayJobResult(data) {

    if (jobResult) {
        jobResult.classList.remove("hidden");
    }


    const job =
        data.job || {};

    const skills =
        data.skills || {};


    // ===============================
    // JOB DETAILS
    // ===============================

    const jobDetails =
        document.getElementById("jobDetails");

    if (jobDetails) {

        jobDetails.innerHTML = `
            <div class="card">

                <h3>Job Details</h3>

                <p>
                    <strong>Job Title:</strong>
                    ${
                        job.job_title ||
                        "Not available"
                    }
                </p>

                <p>
                    <strong>Company:</strong>
                    ${
                        job.company ||
                        "Not available"
                    }
                </p>

                <p>
                    <strong>Location:</strong>
                    ${
                        job.location ||
                        "Not available"
                    }
                </p>

                <p>
                    <strong>
                        Experience Required:
                    </strong>

                    ${
                        job.experience_required ||
                        "Not available"
                    }
                </p>

            </div>
        `;
    }


    // ===============================
    // JOB SKILLS
    // ===============================

    const jobSkills =
        document.getElementById("jobSkills");

    if (jobSkills) {

        jobSkills.innerHTML = `
            <div class="card">

                <h3>Required Skills</h3>

                ${createList(
                    skills.required
                )}


                <h3>Preferred Skills</h3>

                ${createList(
                    skills.preferred
                )}


                <h3>Programming Languages</h3>

                ${createList(
                    skills.programming_languages
                )}


                <h3>Tools & Technologies</h3>

                ${createList(
                    skills.tools_and_technologies
                )}

            </div>
        `;
    }


    // ===============================
    // RESPONSIBILITIES
    // ===============================

    const jobResponsibilities =
        document.getElementById(
            "jobResponsibilities"
        );

    if (jobResponsibilities) {

        jobResponsibilities.innerHTML = `
            <div class="card">

                <h3>Responsibilities</h3>

                ${createList(
                    data.responsibilities
                )}

            </div>
        `;
    }


    // ===============================
    // KEYWORDS
    // ===============================

    const jobKeywords =
        document.getElementById(
            "jobKeywords"
        );

    if (jobKeywords) {

        jobKeywords.innerHTML = `
            <div class="card">

                <h3>Keywords</h3>

                ${createList(
                    data.keywords
                )}

            </div>
        `;
    }
}