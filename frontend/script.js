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
        `<span>✓</span><span>${file.name}</span>`;
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
        `<span>✓</span><span>${file.name}</span>`;
});


/* -----------------------------
   ANALYZE
----------------------------- */

analyzeBtn.addEventListener("click", async () => {

    const resume = resumeFile.files[0];
    const jd = jdFile.files[0];


    if (!resume) {

        status.textContent =
            "Please upload your resume PDF.";

        return;
    }


    if (!jd) {

        status.textContent =
            "Please upload the job description PDF.";

        return;
    }


    if (!resume.name.toLowerCase().endsWith(".pdf")) {

        status.textContent =
            "Resume must be a PDF.";

        return;
    }


    if (!jd.name.toLowerCase().endsWith(".pdf")) {

        status.textContent =
            "Job description must be a PDF.";

        return;
    }


    /*
     * UI loading state
     */

    processing.classList.remove("hidden");

    result.classList.add("hidden");

    status.textContent =
        "Analyzing resume and job description...";


    /*
     * CURRENTLY:
     *
     * Your repository only has the Resume Analyzer
     * connected to this frontend.
     *
     * We will connect the JD Analyzer and
     * Question Generator once their API endpoints
     * are confirmed.
     */


    const formData = new FormData();

    formData.append("file", resume);


    try {

        const response = await fetch(
            "http://127.0.0.1:8000/analyze-resume",
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );
        }


        displayResult(data);


        status.textContent =
            "Resume analysis completed successfully.";

    }

    catch (error) {

        console.error(error);

        status.textContent =
            "Could not connect to Resume Analyzer API.";

    }

    finally {

        processing.classList.add("hidden");

    }

});


/* -----------------------------
   DISPLAY RESULT
----------------------------- */

function displayResult(data) {

    result.classList.remove("hidden");


    document.getElementById("candidate").innerHTML = `

        <div class="card">

            <h3>Candidate</h3>

            <p>
                <strong>Name:</strong>
                ${data.candidate?.name || "Not available"}
            </p>

            <p>
                <strong>Email:</strong>
                ${data.candidate?.email || "Not available"}
            </p>

            <p>
                <strong>CGPA:</strong>
                ${data.candidate?.cgpa || "Not available"}
            </p>

        </div>
    `;


    document.getElementById("skills").innerHTML = `

        <div class="card">

            <h3>Technical Skills</h3>

            ${createList(data.skills?.technical)}

        </div>
    `;


    document.getElementById("projects").innerHTML = `

        <div class="card">

            <h3>Projects</h3>

            ${createList(data.projects)}

        </div>
    `;


    document.getElementById("experience").innerHTML = `

        <div class="card">

            <h3>Internships & Experience</h3>

            ${createList(data.internships)}

        </div>
    `;


    document.getElementById("certifications").innerHTML = `

        <div class="card">

            <h3>Certifications</h3>

            ${createList(data.certifications)}

        </div>
    `;


    document.getElementById("strengths").innerHTML = `

        <div class="card">

            <h3>Strengths</h3>

            ${createList(data.strengths)}

        </div>
    `;


    document.getElementById("skillGaps").innerHTML = `

        <div class="card">

            <h3>Skill Gaps</h3>

            ${createList(data.skill_gaps)}

        </div>
    `;
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
                                ${item.name || item.title || "Project"}
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
                                            Array.isArray(item.technologies)
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
                                        <strong>Role:</strong>
                                        ${item.role}
                                    `
                                    : ""
                            }

                        </li>
                    `;
                }


                return `<li>${item}</li>`;

            }).join("")}

        </ul>
    `;
}