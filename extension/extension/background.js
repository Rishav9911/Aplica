chrome.runtime.onInstalled.addListener(() => {
    console.log("Job Auto-Fill Extension Installed!");
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "fetchStudentData") {
        console.log("📩 Fetch request received for email:", request.email);

        fetch(`http://localhost:5001/get_student_data?email=${encodeURIComponent(request.email)}`)
            .then(response => response.json())
            .then(data => {
                console.log("📡 API Response:", data);

                if (data && Object.keys(data).length > 0) {
                    console.log("Success: Sending student data to popup.js:", data);
                    sendResponse({ success: true, data });
                } else {
                    console.error("Failure: No student data found!");
                    sendResponse({ success: false, error: "No student data found!" });
                }
            })
            .catch(error => {
                console.error("Failure: API fetch error:", error);
                sendResponse({ success: false, error: "API request failed" });
            });

        console.log("Message listener returning true to keep response channel open...");
        return true;  
    }
});