chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "autofill" && request.studentData) {
        const data = request.studentData;

        const fields = {
            fullName: document.querySelector('input[name="Full Name"], input[name="full_name"], input[id*="name"]'),
            email: document.querySelector('input[type="email"], input[name*="Email"], input[id*="email"]'),
            phone: document.querySelector('input[type="tel"], input[name*="Phone"], input[id*="phone"]')
        };

        if (fields.fullName) fields.fullName.value = data.full_name || "";
        if (fields.email) fields.email.value = data.email || "";
        if (fields.phone) fields.phone.value = data.phone || "";

        console.log("✅ Autofilled the form successfully!");

        // ✅ Send a response back to popup.js
        sendResponse({ success: true });
    }
});

/*chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "autofill" && request.studentData) {
        const data = request.studentData;

        // Define mappings for form fields with different possible names
        const fields = {
            fullName: document.querySelector('input[name="Full Name"], input[name="full_name"], input[id*="name"]'),
            email: document.querySelector('input[type="email"], input[name*="Email"], input[id*="email"]'),
            phone: document.querySelector('input[type="tel"], input[name*="Phone"], input[id*="phone"], input[name*="contact"], input[id*="contact"]'),
            linkedin: document.querySelector('input[name*="linkedin"], input[id*="linkedin"]'),
            github: document.querySelector('input[name*="github"], input[id*="github"]'),
            portfolio: document.querySelector('input[name*="portfolio"], input[id*="portfolio"], input[name*="website"], input[id*="website"]'),
            location: document.querySelector('input[name*="location"], input[id*="location"], input[name*="city"], input[id*="city"]'),
            highest_degree: document.querySelector('input[name*="degree"], input[id*="degree"], input[name*="education"], input[id*="education"]'),
            university: document.querySelector('input[name*="university"], input[id*="university"], input[name*="college"], input[id*="college"]'),
            graduation_year: document.querySelector('input[name*="grad_year"], input[id*="grad_year"], input[name*="graduation"], input[id*="graduation"]'),
            cgpa: document.querySelector('input[name*="cgpa"], input[id*="cgpa"], input[name*="gpa"], input[id*="gpa"]'),
            field_of_study: document.querySelector('input[name*="field"], input[id*="field"], input[name*="major"], input[id*="major"]'),
            certifications: document.querySelector('textarea[name*="certifications"], textarea[id*="certifications"], input[name*="certifications"], input[id*="certifications"]'),
            work_experience: document.querySelector('textarea[name*="experience"], textarea[id*="experience"], input[name*="experience"], input[id*="experience"]'),
            technical_skills: document.querySelector('textarea[name*="technical_skills"], textarea[id*="technical_skills"], input[name*="technical_skills"], input[id*="technical_skills"]'),
            soft_skills: document.querySelector('textarea[name*="soft_skills"], textarea[id*="soft_skills"], input[name*="soft_skills"], input[id*="soft_skills"]'),
            projects: document.querySelector('textarea[name*="projects"], textarea[id*="projects"], input[name*="projects"], input[id*="projects"]'),
            internships: document.querySelector('textarea[name*="internships"], textarea[id*="internships"], input[name*="internships"], input[id*="internships"]')
        };

        // Autofill fields if found
        Object.keys(fields).forEach((key) => {
            if (fields[key]) {
                if (Array.isArray(data[key])) {
                    fields[key].value = data[key].join(", "); // Convert array to comma-separated string
                } else {
                    fields[key].value = data[key] || "";
                }
            } else {
                console.warn(`⚠️ No form field found for: ${key}`);
            }
        });

        console.log("✅ Autofilled the form successfully!");

        // ✅ Send a response back to popup.js
        sendResponse({ success: true });
    }
});
*/
