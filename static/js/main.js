document.addEventListener('DOMContentLoaded', () => {
    // Partículas (mantido do seu código)
    particlesJS('particles-js', {
        particles: { number: { value: 200 }, color: { value: '#00ffcc' }, shape: { type: 'circle' }, move: { speed: 6 } },
        interactivity: { events: { onhover: { enable: true, mode: 'repulse' } } }
    });

    // Chatbot Holográfico
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotText = document.getElementById('chatbot-text');
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'pt-br';

    async function processMessage(message) {
        chatbotMessages.innerHTML += `<p>Você: ${message}</p>`;
        chatbotText.setAttribute('value', `Processando: ${message}`);
        try {
            const response = await fetch("{% url 'core:chat' %}", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            const aiResponse = data.response || "Explore a revolução cósmica!";
            chatbotMessages.innerHTML += `<p>A121Bot: ${aiResponse}</p>`;
            chatbotText.setAttribute('value', aiResponse);
        } catch (error) {
            chatbotMessages.innerHTML += `<p>A121Bot: Erro quântico! Tente novamente.</p>`;
            chatbotText.setAttribute('value', 'Erro quântico!');
        }
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        chatbotInput.value = '';
    }

    document.getElementById('chatbot-voice').addEventListener('click', () => {
        recognition.start();
        recognition.onresult = (event) => processMessage(event.results[0][0].transcript);
    });

    document.getElementById('chatbot-vr').addEventListener('click', () => {
        const vrScene = document.getElementById('chatbot-vr-scene');
        vrScene.innerHTML = `
            <a-scene vr-mode-ui="enabled: true" embedded>
                <a-sky color="#000022"></a-sky>
                <a-entity gltf-model="{% static 'models/hologram-avatar.glb' %}" scale="0.5 0.5 0.5" position="0 1.6 -3" animation="property: rotation; to: 0 360 0; loop: true; dur: 5000"></a-entity>
                <a-camera position="0 1.6 0"></a-camera>
            </a-scene>
        `;
        vrScene.style.display = 'block';
    });

    // Controle por Gestos (Simulado com mouse por enquanto)
    document.addEventListener('mousemove', (e) => {
        const hologram = document.querySelector('.chatbot-hologram a-entity');
        if (hologram) {
            hologram.setAttribute('rotation', `${e.clientY / 10} ${e.clientX / 10} 0`);
        }
    });

    function getCsrfToken() {
        return document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
    }
});