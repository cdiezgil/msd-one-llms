// extension/content.js

function extractRegex(text, regex, defaultValue = 0) {
    const match = text.match(regex);
    if (match && match[1]) {
        return parseFloat(match[1].replace(',', '.'));
    }
    return defaultValue;
}

function scrapeData() {
    if (!document || !document.body) return;
    const text = (document.body.innerText || "") + "\n" + (document.body.textContent || "");
    const hostname = window.location.hostname;
    
    let llm = '';
    let h5 = 0;
    let weekly = 0;
    let monthly = 0;

    if (hostname.includes('z.ai') || hostname.includes('kimi.ai')) {
        // Kimi / Z.ai Spanish translation
        llm = hostname.includes('z.ai') ? 'z.ai' : 'kimi';
        h5 = extractRegex(text, /Cuota de 5 horas[^\d]*(\d+(?:\.\d+)?)\s*%/i) || extractRegex(text, /5-hour usage[\s\S]{0,100}?(\d+(?:\.\d+)?)\s*%/i);
        weekly = extractRegex(text, /Cuota semanal[^\d]*(\d+(?:\.\d+)?)\s*%/i) || extractRegex(text, /7-day usage[\s\S]{0,100}?(\d+(?:\.\d+)?)\s*%/i);
        monthly = extractRegex(text, /Cuota MCP[^\d]*(\d+(?:\.\d+)?)\s*%/i) || extractRegex(text, /Total usage[\s\S]{0,100}?(\d+(?:\.\d+)?)\s*%/i);
        
        if (h5 === 0 && weekly === 0) {
            console.warn(`[LLM Telemetry] ${llm.toUpperCase()} FAIL. Text extracted:`, text.substring(0, 500));
        }
        
    } else if (hostname.includes('claude.ai')) {
        llm = 'claude';
        h5 = extractRegex(text, /Sesi[oó]n actual[\s\S]{0,100}?(\d+(?:\.\d+)?)\s*%\s*usado/i);
        weekly = extractRegex(text, /Todos los modelos[\s\S]{0,100}?(\d+(?:\.\d+)?)\s*%\s*usado/i);
        
    } else if (hostname.includes('gemini.google.com')) {
        llm = 'gemini';
        // "Uso actual ... 0 % usado"
        h5 = extractRegex(text, /Uso actual[\s\S]{0,100}?(\d+(?:\.\d+)?)\s*%\s*usado/i);
        // "Límite semanal ... 0 % usado"
        weekly = extractRegex(text, /L[íi]mite semanal[\s\S]{0,100}?(\d+(?:\.\d+)?)\s*%\s*usado/i);
        monthly = 0; // Not provided by Gemini
        
        if (h5 === 0 && weekly === 0) {
            console.warn("[LLM Telemetry] GEMINI FAIL. Raw text:", text.substring(0, 500));
        }
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
