// extension/background.js
console.log("Service worker registered.");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'update_llm') {
        fetch('http://localhost:5000/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(message.data)
        }).catch(console.error);
    }
});
