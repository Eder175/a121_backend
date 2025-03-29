// Inicializar Partículas
if (typeof particlesJS !== 'undefined') {
    particlesJS('particles-js', {
        particles: {
            number: { value: 200, density: { enable: true, value_area: 800 } },
            color: { value: '#00ffcc' },
            shape: { type: 'circle', stroke: { width: 1, color: '#00ffcc' } },
            opacity: { value: 0.7, random: true },
            size: { value: 5, random: true },
            line_linked: { enable: true, distance: 150, color: '#00ffcc', opacity: 0.5, width: 1 },
            move: { enable: true, speed: 6, direction: 'none', random: false, straight: false, out_mode: 'out' }
        },
        interactivity: {
            detect_on: 'canvas',
            events: { onhover: { enable: true, mode: 'repulse' }, onclick: { enable: true, mode: 'push' } },
            modes: { repulse: { distance: 150, duration: 0.4 }, push: { particles_nb: 4 } }
        },
        retina_detect: true
    });
} else {
    console.error('particlesJS não está carregado. Verifique se o script particles.min.js foi incluído.');
}

// Função para obter o CSRF Token
function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Modal de Chat com IA
const modal = document.getElementById('modal');
const chatButton = document.getElementById('chat-button');
const closeModal = document.querySelector('.modal-content .close');
const sendMessageButton = document.getElementById('sendMessage');
const userInput = document.getElementById('userInput');
const chatBox = document.getElementById('chatBox');

if (!modal || !chatButton || !closeModal || !sendMessageButton || !userInput || !chatBox) {
    console.error('Um ou mais elementos do modal de chat não foram encontrados no DOM.');
} else {
    chatButton.addEventListener('click', (e) => {
        e.preventDefault();
        modal.style.display = 'flex';
    });

    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    sendMessageButton.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            processMessage(message, chatBox);
            userInput.value = '';
        }
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessageButton.click();
        }
    });
}

// Chatbot Holográfico
const chatbotMessages = document.getElementById('chatbot-messages');
const chatbotInput = document.getElementById('chatbot-input');
const chatbotText = document.getElementById('chatbot-text');
const chatbotVrScene = document.getElementById('chatbot-vr-scene');
const chatbotVoiceButton = document.getElementById('chatbot-voice');
const chatbotVrButton = document.getElementById('chatbot-vr');
const chatbotLanguageButton = document.getElementById('chatbot-language');

let detectedLanguage = 'pt-br'; // Valor padrão, será atualizado dinamicamente
let languageLessonActive = false;
let currentLesson = null;

if (!chatbotMessages || !chatbotInput || !chatbotText || !chatbotVrScene || !chatbotVoiceButton || !chatbotVrButton || !chatbotLanguageButton) {
    console.error('Um ou mais elementos do chatbot não foram encontrados no DOM.');
} else {
    // Inicializar Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition;
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.lang = detectedLanguage;
        recognition.continuous = false;

        chatbotVoiceButton.addEventListener('click', () => {
            try {
                recognition.start();
            } catch (error) {
                console.error('Erro ao iniciar o reconhecimento de voz:', error);
                chatbotMessages.innerHTML += '<p>A121Bot: Erro ao iniciar o reconhecimento de voz. Verifique as permissões do microfone.</p>';
            }
        });

        recognition.onresult = (event) => {
            const message = event.results[0][0].transcript;
            chatbotInput.value = message;
            processMessage(message);
        };

        recognition.onerror = (event) => {
            console.error('Erro no reconhecimento de voz:', event.error);
            chatbotMessages.innerHTML += '<p>A121Bot: Erro no reconhecimento de voz. Tente novamente.</p>';
        };
    } else {
        console.warn('SpeechRecognition não é suportado neste navegador.');
        chatbotVoiceButton.disabled = true;
        chatbotVoiceButton.textContent = 'Falar (Não Suportado)';
    }

    chatbotVrButton.addEventListener('click', () => {
        const scene = document.createElement('a-scene');
        scene.setAttribute('vr-mode-ui', 'enabled: true');
        scene.setAttribute('embedded', '');
        scene.setAttribute('renderer', 'colorManagement: true');
        scene.innerHTML = `
            <a-sky color="#000022"></a-sky>
            <a-sphere id="vr-chatbot" color="#00ffcc" radius="0.5" position="0 1.6 -3" animation="property: rotation; to: 0 360 0; loop: true; dur: 5000">
                <a-text id="vr-chatbot-text" value="Bem-vindo ao modo VR! Fale comigo!" align="center" position="0 1 0" color="#00ffcc"></a-text>
            </a-sphere>
            <a-entity light="type: ambient; intensity: 0.5;"></a-entity>
            <a-entity light="type: directional; intensity: 0.5;" position="1 1 1"></a-entity>
            <a-entity camera look-controls position="0 1.6 0"></a-entity>
        `;
        chatbotVrScene.appendChild(scene);
        chatbotVrScene.style.display = 'block';
    });

    chatbotVrScene.addEventListener('click', (e) => {
        if (e.target === chatbotVrScene) {
            chatbotVrScene.style.display = 'none';
            chatbotVrScene.innerHTML = '';
        }
    });

    chatbotLanguageButton.addEventListener('click', () => {
        languageLessonActive = true;
        currentLesson = {
            language: 'en',
            topic: 'tecnologia',
            level: 'iniciante',
            step: 0,
            phrases: [
                { en: "Hello! Let's talk about technology.", pt: "Olá! Vamos falar sobre tecnologia." },
                { en: "Do you like using computers?", pt: "Você gosta de usar computadores?" },
                { en: "Technology makes our lives easier.", pt: "A tecnologia facilita a nossa vida." }
            ]
        };
        chatbotMessages.innerHTML += `<p>A121Bot: Vamos começar uma lição de inglês sobre tecnologia! Diga ou escreva a frase em inglês: ${currentLesson.phrases[0].en}</p>`;
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    });

    chatbotInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && chatbotInput.value.trim() !== '') {
            processMessage(chatbotInput.value.trim());
            chatbotInput.value = '';
        }
    });
}

function detectLanguage(message) {
    const lowerMessage = message.toLowerCase();
    const languageKeywords = {
        'pt-br': ['olá', 'oi', 'tecnologia', 'cursos', 'finanças'],
        'en': ['hello', 'hi', 'technology', 'courses', 'finance'],
        'es': ['hola', 'tecnología', 'cursos', 'finanzas'],
        'fr': ['bonjour', 'technologie', 'cours', 'finances'],
        'de': ['hallo', 'technologie', 'kurse', 'finanzen']
    };
    for (const [lang, keywords] of Object.entries(languageKeywords)) {
        if (keywords.some(keyword => lowerMessage.includes(keyword))) {
            return lang;
        }
    }
    return 'pt-br';
}

async function processMessage(message, targetElement = chatbotMessages) {
    if (!targetElement) {
        console.error('Elemento alvo para mensagens não encontrado.');
        return;
    }

    targetElement.innerHTML += `<p>Você: ${message}</p>`;
    targetElement.scrollTop = targetElement.scrollHeight;

    detectedLanguage = detectLanguage(message);
    if (recognition) {
        recognition.lang = detectedLanguage;
    }

    if (languageLessonActive && currentLesson) {
        let lessonResponse = '';
        if (currentLesson.step < currentLesson.phrases.length) {
            const expectedPhrase = currentLesson.phrases[currentLesson.step].en;
            if (message.toLowerCase().trim() === expectedPhrase.toLowerCase().trim()) {
                lessonResponse = `A121Bot: Correto! A tradução em português é: ${currentLesson.phrases[currentLesson.step].pt}`;
                currentLesson.step++;
                if (currentLesson.step < currentLesson.phrases.length) {
                    lessonResponse += ` Próxima frase: ${currentLesson.phrases[currentLesson.step].en}`;
                } else {
                    lessonResponse += ` Parabéns! Você concluiu a lição. Ganhou 5 A121Coin!`;
                    languageLessonActive = false;
                    currentLesson = null;
                    try {
                        const response = await fetch('/chat/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCsrfToken(),
                            },
                            body: JSON.stringify({ message: 'lesson_completed' }),
                        });
                        const data = await response.json();
                        if (response.ok) {
                            const a121coinBalance = data.a121coin_balance;
                            targetElement.innerHTML += `<p>Saldo total de A121Coin: ${a121coinBalance}</p>`;
                        } else {
                            targetElement.innerHTML += `<p>A121Bot: Erro ao registrar A121Coin. Tente novamente.</p>`;
                        }
                    } catch (error) {
                        console.error('Erro ao registrar A121Coin:', error);
                        targetElement.innerHTML += `<p>A121Bot: Erro de conexão ao registrar A121Coin. Tente novamente.</p>`;
                    }
                }
            } else {
                lessonResponse = `A121Bot: Quase! A frase correta é: ${expectedPhrase}. Tente novamente!`;
            }
        }
        targetElement.innerHTML += `<p>${lessonResponse}</p>`;
        targetElement.scrollTop = targetElement.scrollHeight;
        chatbotText.setAttribute('value', lessonResponse);
        const vrChatbotText = document.getElementById('vr-chatbot-text');
        if (vrChatbotText) {
            vrChatbotText.setAttribute('value', lessonResponse);
        }
        return;
    }

    try {
        const response = await fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({ message: message }),
        });
        const data = await response.json();
        if (response.ok) {
            const responseMessage = data.response;
            const a121coinBalance = data.a121coin_balance;
            chatbotText.setAttribute('value', responseMessage);
            const vrChatbotText = document.getElementById('vr-chatbot-text');
            if (vrChatbotText) {
                vrChatbotText.setAttribute('value', responseMessage);
            }
            targetElement.innerHTML += `<p>A121Bot: ${responseMessage}</p>`;
            targetElement.innerHTML += `<p>Saldo total de A121Coin: ${a121coinBalance}</p>`;
        } else {
            targetElement.innerHTML += `<p>A121Bot: Erro ao processar sua mensagem. Tente novamente!</p>`;
        }
    } catch (error) {
        console.error('Erro ao processar mensagem:', error);
        targetElement.innerHTML += `<p>A121Bot: Erro de conexão. Tente novamente!</p>`;
    }
    targetElement.scrollTop = targetElement.scrollHeight;
}

// Mudança de Moeda com Taxa de Câmbio
const currencySelector = document.getElementById('currency-selector');
if (currencySelector) {
    currencySelector.addEventListener('change', function () {
        const selectedCurrency = this.value;
        fetch('/change_currency/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCsrfToken()
            },
            body: 'currency=' + selectedCurrency
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    console.error('Erro ao mudar moeda:', data.error);
                }
            })
            .catch(error => console.error('Erro ao mudar moeda:', error));
    });
}

// Atualizar Preços com Taxa de Câmbio
function updatePrices(currency, rate) {
    document.querySelectorAll('.product-price, .course-price').forEach(priceElement => {
        const basePrice = parseFloat(priceElement.getAttribute('data-price'));
        if (!isNaN(basePrice)) {
            const convertedPrice = basePrice * rate;
            priceElement.textContent = convertedPrice.toFixed(2) + ' ' + currency;
        }
    });
}

fetch('/get_exchange_rate/?base=USD')
    .then(response => response.json())
    .then(data => {
        if (data.rates) {
            const currency = document.getElementById('currency-selector')?.value || 'USD';
            const rate = data.rates[currency] || 1;
            updatePrices(currency, rate);
        } else {
            console.error('Taxas de câmbio não encontradas:', data);
        }
    })
    .catch(error => console.error('Erro ao carregar taxa de câmbio:', error));

// Navegação Dinâmica com Transições Suaves
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();
        const sectionId = this.getAttribute('data-section');
        const section = document.getElementById(sectionId);
        if (section) {
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            window.scrollTo({ top: section.offsetTop - 80, behavior: 'smooth' });
        } else {
            const url = this.getAttribute('href');
            loadSection(url);
        }
    });
});

// Carregar Detalhes do Produto Dinamicamente
document.querySelectorAll('.view-product').forEach(button => {
    button.addEventListener('click', function (e) {
        e.preventDefault();
        const productId = this.getAttribute('data-product');
        loadProductDetails(productId);
    });
});

function loadSection(url) {
    const main = document.querySelector('main');
    if (!main) {
        console.error('Elemento <main> não encontrado.');
        return;
    }

    main.style.opacity = '0';
    main.innerHTML = '<p>Carregando...</p>'; // Feedback visual

    fetch(url)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newContent = doc.querySelector('main').innerHTML;
            setTimeout(() => {
                main.innerHTML = newContent;
                main.style.opacity = '1';
            }, 500);
        })
        .catch(error => {
            console.error('Erro ao carregar seção:', error);
            main.innerHTML = '<p>Erro ao carregar a seção. Tente novamente.</p>';
            main.style.opacity = '1';
        });
}

function loadProductDetails(productId) {
    const productDetails = {
        'iphone15': {
            title: 'iPhone 15 Pro Max (512GB)',
            description: 'O mais avançado iPhone com câmera revolucionária e desempenho excepcional.',
            price: '1399.00 €',
            image: 'images/iPhone 15 Pro Max (512GB).jpg'
        },
        'iphone16': {
            title: 'iPhone 16 Pro Max Titânio Deserto',
            description: 'Design futurista com tecnologia de ponta para o futuro.',
            price: '1499.00 €',
            image: 'images/iPhone 16 Pro Max Titanio Deserto.jpg'
        }
    };
    const product = productDetails[productId];
    const main = document.querySelector('main');
    if (!main) {
        console.error('Elemento <main> não encontrado.');
        return;
    }

    if (product) {
        const productSection = document.createElement('section');
        productSection.classList.add('product-details', 'section-transition');
        productSection.innerHTML = `
            <div class="container">
                <h2>${product.title}</h2>
                <div class="product-detail-content">
                    <img src="/static/${product.image}" alt="${product.title}" class="product-detail-image">
                    <div class="product-detail-info">
                        <p>${product.description}</p>
                        <p>Preço: ${product.price}</p>
                        <a href="/cadastro/" class="btn btn-product">Comprar Agora</a>
                    </div>
                </div>
            </div>
        `;
        main.innerHTML = '';
        main.appendChild(productSection);
        setTimeout(() => {
            productSection.classList.add('active');
        }, 100);
    } else {
        main.innerHTML = '<p>Produto não encontrado.</p>';
    }
}

// Animações de Scroll e Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Animação com GSAP para a logo
    if (typeof gsap !== 'undefined') {
        gsap.to(".logo", { duration: 1, y: 20, repeat: -1, yoyo: true });
    } else {
        console.error('GSAP não está carregado. Verifique se o script gsap.min.js foi incluído.');
    }

    // Observador de interseção para animações de scroll
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, observerOptions);
    const sections = document.querySelectorAll('.section-transition');
    sections.forEach(section => observer.observe(section));

    // Inicializar mensagens do chatbot
    if (chatbotMessages) {
        chatbotMessages.innerHTML = '<p>A121Bot: Bem-vindo ao A121 Evolution! Fale comigo para explorar cursos, ganhar A121Coin ou NFTs!</p>';
    }
    if (chatBox) {
        chatBox.innerHTML = '<p>A121Bot: Bem-vindo ao A121 Evolution! Fale comigo para explorar cursos, ganhar A121Coin ou NFTs!</p>';
    }
});