// extension/content.js

function extractRegex(text, regex, defaultValue = 0) {
    const match = text.match(regex);
    if (match && match[1]) {
        return parseFloat(match[1].replace(',', '.'));
    }
    return defaultValue;
}

function scrapeData() {
    const text = document.body.innerText;
    const hostname = window.location.hostname;
    
    let llm = '';
    let h5 = 0;
    let weekly = 0;
    let monthly = 0;

    if (hostname.includes('z.ai')) {
        llm = 'z.ai';
        // z.ai renders: "Cuota de 5 horas \n 3% De segunda mano"
        h5 = extractRegex(text, /Cuota de 5 horas[^\d]*(\d+(?:\.\d+)?)%/i);
        weekly = extractRegex(text, /Cuota semanal[^\d]*(\d+(?:\.\d+)?)%/i);
        monthly = extractRegex(text, /Cuota MCP[^\d]*(\d+(?:\.\d+)?)%/i);
        
    } else if (hostname.includes('claude.ai')) {
        llm = 'claude';
        // "Sesión actual ... 100% usado"
        h5 = extractRegex(text, /Sesi[oó]n actual[\s\S]{0,100}?(\d+(?:\.\d+)?)%\s*usado/i);
        // "Todos los modelos ... 58% usado" (Under Límites semanales)
        weekly = extractRegex(text, /Todos los modelos[\s\S]{0,100}?(\d+(?:\.\d+)?)%\s*usado/i);
        
    } else if (hostname.includes('kimi.ai')) {
        llm = 'kimi';
        // "5-hour usage ... Code 0%"
        h5 = extractRegex(text, /5-hour usage[\s\S]{0,100}?(\d+(?:\.\d+)?)%/i);
        // "7-day usage ... Code 100%"
        weekly = extractRegex(text, /7-day usage[\s\S]{0,100}?(\d+(?:\.\d+)?)%/i);
        // "Total usage 41.05%"
        monthly = extractRegex(text, /Total usage\s*(\d+(?:\.\d+)?)%/i);
        
    } else if (hostname.includes('gemini.google.com')) {
        llm = 'gemini';
        // Placeholder for Gemini if it has a usage page
        h5 = 0; 
        weekly = 0;
    }

    if (llm) {
        console.log(`[LLM Telemetry] Scraped ${llm}: h5=${h5}%, weekly=${weekly}%, monthly=${monthly}%`);
        chrome.runtime.sendMessage({
            type: 'update_llm',
            data: {
                llm: llm,
                h5: h5,
                weekly: weekly,
                monthly: monthly
            }
        });
    }
}

// Scrape every 10 seconds
setInterval(scrapeData, 10000);
// Also scrape immediately on load
setTimeout(scrapeData, 2000);
