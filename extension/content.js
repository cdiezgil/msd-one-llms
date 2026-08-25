// extension/content.js
// Mock logic to send data to our local server
setInterval(() => {
    chrome.runtime.sendMessage({
        type: 'update_llm',
        data: {
            llm: 'claude',
            h5: Math.random() * 100, // mock data
            weekly: 50,
            monthly: 20
        }
    });
}, 5000);
