// ============================================================
// SinoVista - City Detail Page JavaScript
// Handles the AI Recommendation generator
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generateBtn');
    const aiResult = document.getElementById('aiResult');
    const aiLoading = document.getElementById('aiLoading');
    const aiContent = document.getElementById('aiContent');

    if (!generateBtn) return;

    generateBtn.addEventListener('click', function() {
        const cityName = generateBtn.dataset.city;
        const preference = document.getElementById('preference').value;
        const budget = document.getElementById('budget').value;
        const duration = document.getElementById('duration').value;

        // Show loading
        aiResult.style.display = 'block';
        aiLoading.style.display = 'block';
        aiContent.innerHTML = '';
        generateBtn.disabled = true;
        generateBtn.textContent = '✨ Generating...';

        // Scroll to result
        setTimeout(() => {
            aiResult.scrollIntoView({behavior: 'smooth', block: 'start'});
        }, 100);

        // Call API
        fetch('/api/recommend', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                city: cityName,
                preference: preference,
                budget: budget,
                duration: duration
            })
        })
        .then(res => res.json())
        .then(data => {
            aiLoading.style.display = 'none';
            if (data.recommendation) {
                aiContent.innerHTML = formatRecommendation(data.recommendation);
            } else {
                aiContent.innerHTML = '<p style="color:#C8102E">Sorry, could not generate a recommendation. Please try again.</p>';
            }
            generateBtn.disabled = false;
            generateBtn.innerHTML = '✨ Generate Another Recommendation';
        })
        .catch(err => {
            aiLoading.style.display = 'none';
            aiContent.innerHTML = '<p style="color:#C8102E">Connection error: ' + err.message + '</p>';
            generateBtn.disabled = false;
            generateBtn.innerHTML = '✨ Try Again';
        });
    });
});

// Convert markdown-style text to HTML
function formatRecommendation(text) {
    let html = text;

    // Headers (## becomes h2)
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');

    // Bold
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

    // Italics
    html = html.replace(/\*([^*\n]+?)\*/g, '<em>$1</em>');

    // Horizontal rule
    html = html.replace(/^---+$/gm, '<hr>');

    // Lists - convert lines starting with - or • to list items
    const lines = html.split('\n');
    const result = [];
    let inList = false;

    for (let line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('- ') || trimmed.startsWith('• ')) {
            if (!inList) {
                result.push('<ul>');
                inList = true;
            }
            result.push('<li>' + trimmed.substring(2) + '</li>');
        } else {
            if (inList) {
                result.push('</ul>');
                inList = false;
            }
            if (trimmed && !trimmed.startsWith('<')) {
                result.push('<p>' + line + '</p>');
            } else {
                result.push(line);
            }
        }
    }
    if (inList) result.push('</ul>');

    return result.join('\n');
}
