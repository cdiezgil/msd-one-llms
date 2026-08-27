// extension/background.js
console.log("Service worker registered.");

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    if (message.type === 'update_llm') {
        const response = await fetch("http://127.0.0.1:5001/update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(message.data)
        }).catch(console.error);
    }
});
