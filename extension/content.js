// extension/content.js
// Mock logic to send data to our local server
setInterval(() => {
    fetch('http://localhost:5000/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            llm: 'claude',
            h5: Math.random() * 100, // mock data
            weekly: 50,
            monthly: 20
        })
    }).catch(console.error);
}, 5000);
