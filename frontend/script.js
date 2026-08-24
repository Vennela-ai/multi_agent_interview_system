const fileInput = document.getElementById("resumeFile");
const analyzeBtn = document.getElementById("analyzeBtn");
const status = document.getElementById("status");
const result = document.getElementById("result");

analyzeBtn.addEventListener("click", async () => {

    const file = fileInput.files[0];

    if (!file) {
        status.textContent = "Please select a PDF resume.";
        return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {
        status.textContent = "Please upload a PDF file.";
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    status.textContent = "Analyzing resume...";

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
            throw new Error(data.error || "Something went wrong.");
        }

        displayResult(data);

        status.textContent = "Resume analyzed successfully!";

    } catch (error) {

        console.error(error);

        status.textContent =
            "Could not connect to Resume Analyzer API.";

    }
});


function displayResult(data) {

    result.classList.remove("hidden");

    document.getElementById("candidate").innerHTML = `
        <div class="card">
            <h3>Candidate</h3>
            <p><strong>Name:</strong> ${data.candidate?.name || "Not available"}</p>
            <p><strong>Email:</strong> ${data.candidate?.email || "Not available"}</p>
            <p><strong>CGPA:</strong> ${data.candidate?.cgpa || "Not available"}</p>
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
                            <strong>${item.name || item.title || "Project"}</strong>
                            ${item.description
                                ? `<br>${item.description}`
                                : ""}
                            ${item.technologies
                                ? `<br><strong>Technologies:</strong> ${Array.isArray(item.technologies)
                                    ? item.technologies.join(", ")
                                    : item.technologies}`
                                : ""}
                            ${item.role
                                ? `<br><strong>Role:</strong> ${item.role}`
                                : ""}
                        </li>
                    `;
                }

                return `<li>${item}</li>`;

            }).join("")}
        </ul>
    `;
}