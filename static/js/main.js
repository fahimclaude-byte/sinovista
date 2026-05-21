// ============================================================
// SinoVista - Main JavaScript
// Handles: search autocomplete, AI chat, mobile menu
// ============================================================

document.addEventListener('DOMContentLoaded', function() {

    // ---------- Mobile Menu ----------
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.querySelector('.nav-links');
    if (mobileToggle) {
        mobileToggle.addEventListener('click', () => {
            navLinks.classList.toggle('mobile-open');
        });
    }

    // ---------- Hero Search with Autocomplete ----------
    const heroSearch = document.getElementById('heroSearch');
    const searchSuggestions = document.getElementById('searchSuggestions');
    const heroSearchBtn = document.getElementById('heroSearchBtn');

    if (heroSearch) {
        let searchTimeout;
        heroSearch.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            if (query.length < 1) {
                searchSuggestions.classList.remove('show');
                return;
            }
            searchTimeout = setTimeout(() => {
                fetch(`/api/cities/search?q=${encodeURIComponent(query)}`)
                    .then(res => res.json())
                    .then(data => {
                        if (data.cities && data.cities.length > 0) {
                            searchSuggestions.innerHTML = data.cities.map(c => `
                                <div class="search-suggestion-item" data-city="${c.name}">
                                    ${c.name} <span class="search-suggestion-cn">${c.name_cn}</span>
                                    <span style="float:right; color:#999; font-size:13px;">${c.province}</span>
                                </div>
                            `).join('');
                            searchSuggestions.classList.add('show');

                            // Click handler for suggestions
                            document.querySelectorAll('.search-suggestion-item').forEach(item => {
                                item.addEventListener('click', () => {
                                    window.location.href = `/city/${encodeURIComponent(item.dataset.city)}`;
                                });
                            });
                        } else {
                            searchSuggestions.classList.remove('show');
                        }
                    });
            }, 200);
        });

        heroSearchBtn.addEventListener('click', () => {
            const q = heroSearch.value.trim();
            if (q) window.location.href = `/cities?search=${encodeURIComponent(q)}`;
        });

        heroSearch.addEventListener('keypress', e => {
            if (e.key === 'Enter') heroSearchBtn.click();
        });

        // Close suggestions on outside click
        document.addEventListener('click', e => {
            if (!e.target.closest('.hero-search')) {
                searchSuggestions.classList.remove('show');
            }
        });
    }

    // ---------- AI Chat Widget ----------
    const chatToggleBtn = document.getElementById('chatToggleBtn');
    const chatPanel = document.getElementById('chatPanel');
    const chatClose = document.getElementById('chatClose');
    const chatInput = document.getElementById('chatInput');
    const chatSendBtn = document.getElementById('chatSendBtn');
    const chatMessages = document.getElementById('chatMessages');

    if (chatToggleBtn) {
        chatToggleBtn.addEventListener('click', () => {
            chatPanel.classList.toggle('open');
            if (chatPanel.classList.contains('open')) chatInput.focus();
        });
        chatClose.addEventListener('click', () => chatPanel.classList.remove('open'));

        function sendChatMessage() {
            const message = chatInput.value.trim();
            if (!message) return;

            // Add user message
            const userMsg = document.createElement('div');
            userMsg.className = 'chat-msg user-msg';
            userMsg.textContent = message;
            chatMessages.appendChild(userMsg);

            chatInput.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // Show typing
            const typingMsg = document.createElement('div');
            typingMsg.className = 'chat-msg ai-msg';
            typingMsg.innerHTML = '<em>thinking...</em>';
            chatMessages.appendChild(typingMsg);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // Get current city if on city page
            const cityElement = document.querySelector('[data-city]');
            const cityName = cityElement ? cityElement.dataset.city : null;

            fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message, city: cityName})
            })
            .then(res => res.json())
            .then(data => {
                typingMsg.innerHTML = formatChatResponse(data.response);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            })
            .catch(err => {
                typingMsg.textContent = 'Sorry, something went wrong. Try again!';
            });
        }

        chatSendBtn.addEventListener('click', sendChatMessage);
        chatInput.addEventListener('keypress', e => {
            if (e.key === 'Enter') sendChatMessage();
        });
    }
});

// Format chat response (handle bold, basic markdown)
function formatChatResponse(text) {
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');
}
