/*chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "autofill" && request.studentData) {
        const data = request.studentData;

        const fields = {
            fullName: document.querySelector('input[name="Name"], input[name="Candidate Name"], input[name="Applicant Name"], input[name="Full Name"], input[name="full_name"], input[id*="name"], input[placeholder*="name"]'),
            email: document.querySelector('input[type="email"], input[name*="Email"], input[name*="Email ID"], input[name*="Contact Email"], input[id*="email"]'),
            phone: document.querySelector('input[type="tel"], input[name*="Phone"], input[name*="Phone No."],input[name*="Phone Number"], input[name*="Contact"], input[name*="Contact No."], input[name*="Contact Number"], input[name*="Telephone"], input[id*="phone"]'),
            address: document.querySelector('input[name*="Address"], input[name*="Home Address,"], input[name*="Full Address,"]. input[name*="Current Address"], input[name*="Mailing Address"], input[name*="Residential Address"], input[id*="address"], textarea[name*="address"]'),
            city: document.querySelector('input[name*="City"], input[name*="Town"] input[id*="city"]'),
            state: document.querySelector('input[name*="State"], input[name*="Region"], input[name*="State Name"], input[id*="state"]'),
            pincode: document.querySelector('input[name*="Pin Code"], input[name*="Postal Code"], input[name*="ZIP"], input[id*="pincode"], input[id*="zip"]'),
            linkedin: document.querySelector('input[name*="LinkedIn"], input[name*="LinkedIn URL"], input[name*="LinkedIn Link"], input[id*="linkedin"]'),
            github: document.querySelector('input[name*="GitHub"], input[name*="GitHub URL"], input[name*="GitHub Link"], input[id*="github"]'),
            portfolio: document.querySelector('input[name*="Portfolio"], input[name*="Website"], input[name*="Personal Website"], input[name*="Online Portfolio"], input[id*="portfolio"]'),
            location: document.querySelector('input[name*="Location"], input[id*="location"]'),
            university: document.querySelector('input[name*="University"], input[name*="College"], input[name*="Institution Name"], input[name*="Name of University"], input[name*="University Name"], input[id*="university"]'),
            course: document.querySelector('input[name*="Course"], input[name*="Course Name"], input[name*="Degree"], input[name*="Degree Name"], input[id*="university"]'),
            fieldOfStudy: document.querySelector('input[name*="Field of Study"], input[name*="Major"], input[name*="Specialization"], input[name*="Subject"], input[id*="field"]'),
            graduationYear: document.querySelector('input[name*="Graduation Year"], input[name*="Completion Year"], input[id*="grad_year"]'),
            cgpa: document.querySelector('input[name*="CGPA"], input[name*="GPA"], input[name*="Grade"], input[name*="Academic Score"], input[id*="cgpa"]'),
            certifications: document.querySelector('textarea[name*="Certifications"], textarea[name*="Certificates"], textarea[id*="certifications"]'),
            technicalSkills: document.querySelector('textarea[name*="Technical Skills"], textarea[name*="Skills"], textarea[id*="technical_skills"]'),
            softSkills: document.querySelector('textarea[name*="Soft Skills"], textarea[id*="soft_skills"]'),
            preferredProfiles: document.querySelector('textarea[name*="Preferred Profiles"], textarea[name*="Preferred Roles"], textarea[name*="Desired Roles"], textarea[name*="Positions"], textarea[name*="Preferred Positions"], textarea[name*="Desired Positions"], textarea[id*="preferred_profiles"]'),
            preferredLocationsIndia: document.querySelector('textarea[name*="Preferred Locations in India"], textarea[name*="Preferred Locations"], textarea[name*="Desired Locations"], textarea[name*="Work Locations"], textarea[id*="preferred_locations_india"]'),
            preferredLocationsAbroad: document.querySelector('textarea[name*="Preferred Locations Outside India"], textarea[name*="Preferred Locations"], textarea[name*="Desired Locations"], textarea[name*="Work Locations"], textarea[id*="preferred_locations_abroad"]'),
            projects: document.querySelector('textarea[name="Projects"], textarea[name="Past Work"] textarea[name="projects"], textarea[id*="projects"]')
        };

        // Autofill fields
        if (fields.fullName) fields.fullName.value = data.full_name || "";
        if (fields.email) fields.email.value = data.email || "";
        if (fields.phone) fields.phone.value = data.phone || "";
        if (fields.address) fields.address.value = data.address || "";
        if (fields.city) fields.city.value = data.city || "";
        if (fields.state) fields.state.value = data.state || "";
        if (fields.pincode) fields.pincode.value = data.pincode || "";
        if (fields.linkedin) fields.linkedin.value = data.linkedin || "";
        if (fields.github) fields.github.value = data.github || "";
        if (fields.portfolio) fields.portfolio.value = data.portfolio || "";
        if (fields.location) fields.location.value = data.location || "";
        if (fields.university) fields.university.value = data.university || "";
        if (fields.course) fields.course.value = data.course || "";
        if (fields.fieldOfStudy) fields.fieldOfStudy.value = data.field_of_study || "";
        if (fields.graduationYear) fields.graduationYear.value = data.graduation_year || "";
        if (fields.cgpa) fields.cgpa.value = data.cgpa || "";
        if (fields.certifications) fields.certifications.value = data.certifications || "";
        if (fields.technicalSkills) fields.technicalSkills.value = data.technical_skills || "";
        if (fields.softSkills) fields.softSkills.value = data.soft_skills || "";
        if (fields.preferredProfiles) fields.preferredProfiles.value = data.preferred_profiles || "";
        if (fields.preferredLocationsIndia) fields.preferredLocationsIndia.value = data.preferred_locations_india || "";
        if (fields.preferredLocationsAbroad) fields.preferredLocationsAbroad.value = data.preferred_locations_abroad || "";
        if (fields.projects) fields.projects.value = data.projects || "";

        console.log("✅ Autofilled the form successfully!");

        // ✅ Send a response back to popup.js
        sendResponse({ success: true });
    }
});
*/
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "autofill" && request.studentData) {
        const data = request.studentData;

        const fields = {
            fullName: document.querySelector('input[name="Full Name"], input[name="full_name"], input[id*="name"]'),
            email: document.querySelector('input[type="email"], input[name*="email" i], input[id*="email" i]'),
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

