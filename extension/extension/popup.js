console.log("Popup.js loaded successfully!"); 

document.addEventListener("DOMContentLoaded", function () {
    const autofillButton = document.getElementById("autofillButton");
    const emailInput = document.getElementById("emailInput");

    autofillButton.addEventListener("click", function () {
        const userEmail = emailInput.value.trim();

        if (!userEmail) {
            alert("Please enter your email before autofilling!");
            return;
        }

        console.log("Sending request for email:", userEmail);

        chrome.runtime.sendMessage({ action: "fetchStudentData", email: userEmail }, function (response) {
            if (chrome.runtime.lastError) {
                console.error("Failure: Message passing error:", chrome.runtime.lastError.message);
                alert("Failure: Error communicating with background script: " + chrome.runtime.lastError.message);
                return;
            }

            console.log("Received response from background.js:", response);

            if (response && response.success) {
                console.log("Success: Data received from MongoDB:", response.data);

                chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                    if (tabs.length === 0) {
                        console.error("Failure: No active tab found!");
                        return;
                    }

                    const tabId = tabs[0].id;

                    chrome.scripting.executeScript(
                        {
                            target: { tabId: tabId },
                            files: ["content.js"]
                        },
                        () => {
                            console.log("Content script injected!");

                            setTimeout(() => {
                                chrome.tabs.sendMessage(tabId, { action: "autofill", studentData: response.data }, (res) => {
                                    if (chrome.runtime.lastError) {
                                        console.error("Failure: Error sending data to content.js:", chrome.runtime.lastError.message);
                                    } else {
                                        console.log("Success: Sent student data to content.js:", res);
                                    }
                                });
                            }, 500); 
                        }
                    );
                });

            } else {
                console.error("Failure: No student data found in popup.js.");
                alert("Failure: No student data found for this email!");
            }
        });
    });
});
