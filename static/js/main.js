// Inicializar Partículas
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

// Holograma com Three.js (para o container geral, se existir)
function createHologram(containerId, geometryType = 'TorusKnot', color = 0x00ffcc) {
    const container = document.getElementById(containerId);
    if (container) {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        let geometry;
        if (geometryType === 'TorusKnot') {
            geometry = new THREE.TorusKnotGeometry(1, 0.3, 100, 16);
        } else if (geometryType === 'Sphere') {
            geometry = new THREE.SphereGeometry(0.5, 32, 32);
        }

        const material = new THREE.MeshBasicMaterial({ color: color, wireframe: true });
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        camera.position.z = geometryType === 'TorusKnot' ? 5 : 2;

        function animate() {
            requestAnimationFrame(animate);
            mesh.rotation.x += 0.01;
            mesh.rotation.y += 0.01;
            renderer.render(scene, camera);
        }
        animate();
    }
}

// Inicializar Hologramas
createHologram('hologram-container', 'TorusKnot', 0x00ffcc);
createHologram('hologram-iphone15', 'Sphere', 0x00ffcc);
createHologram('hologram-iphone16', 'Sphere', 0x00ccff);

// Modal de Chat com IA Avançada
const modal = document.getElementById('modal');
const openModal = document.querySelector('.chat-button');
const closeModal = document.getElementsByClassName('close')[0];
const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendMessage = document.getElementById('sendMessage');

// Abrir o modal automaticamente ao carregar a página
window.onload = function() {
    if (modal) {
        modal.style.display = 'block';
        addIAMessage('Olá! Eu sou a IA A121. Como posso te ajudar hoje? 🚀');
    }
};

if (openModal) {
    openModal.onclick = function() {
        modal.style.display = 'block';
    };
}

if (closeModal) {
    closeModal.onclick = function() {
        modal.style.display = 'none';
    };
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};

// Enviar mensagem com o botão ou pressionando Enter
if (sendMessage) {
    sendMessage.onclick = function() {
        sendUserMessage();
    };
}

if (userInput) {
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendUserMessage();
        }
    });
}

function sendUserMessage() {
    const message = userInput.value.trim();
    if (message) {
        addUserMessage(message);
        fetch('/core/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                addIAMessage(data.response);
            } else {
                addIAMessage('Desculpe, não entendi. Pode repetir ou me dar mais detalhes?');
            }
        })
        .catch(error => {
            console.error('Erro ao se comunicar com o servidor:', error);
            addIAMessage('Desculpe, houve um problema. Tente novamente ou me dê mais detalhes.');
        });
        userInput.value = '';
    }
}

function addUserMessage(message) {
    const userMsg = document.createElement('p');
    userMsg.textContent = message;
    userMsg.classList.add('user-message');
    chatBox.appendChild(userMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addIAMessage(message) {
    const iaMsg = document.createElement('p');
    iaMsg.textContent = message;
    iaMsg.classList.add('ia-message');
    chatBox.appendChild(iaMsg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function getCsrfToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

// Mudança de Moeda com Taxa de Câmbio
const currencySelector = document.getElementById('currency-selector');
if (currencySelector) {
    currencySelector.addEventListener('change', function() {
        const selectedCurrency = this.value;
        fetch('/core/change_currency/', {
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
            }
        })
        .catch(error => console.error('Erro ao mudar moeda:', error));
    });
}

// Atualizar Preços com Taxa de Câmbio
function updatePrices(currency, rate) {
    document.querySelectorAll('.product-price, .course-price').forEach(priceElement => {
        const basePrice = parseFloat(priceElement.getAttribute('data-price'));
        const convertedPrice = basePrice * rate;
        priceElement.textContent = convertedPrice.toFixed(2) + ' ' + currency;
    });
}

// Carregar Taxa de Câmbio (Comentado até corrigir a rota na Tarefa 3)
/*
fetch('/core/get_exchange_rate/?base=EUR')
    .then(response => response.json())
    .then(data => {
        if (data.rates) {
            const currency = document.getElementById('currency-selector')?.value || 'EUR';
            const rate = data.rates[currency] || 1;
            updatePrices(currency, rate);
        }
    })
    .catch(error => console.error('Erro ao carregar taxa de câmbio:', error));
*/

// Realidade Aumentada
document.querySelectorAll('.ar-button').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const scene = this.nextElementSibling;
        const model = scene.querySelector('a-entity');
        model.setAttribute('visible', 'true');
        scene.style.display = 'block';
    });
});

// Navegação Dinâmica com Transições Suaves
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const sectionId = this.getAttribute('data-section');
        const section = document.getElementById(sectionId);
        if (section) {
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            window.scrollTo({
                top: section.offsetTop - 80,
                behavior: 'smooth'
            });
        } else {
            const url = this.getAttribute('href');
            loadSection(url);
        }
    });
});

// Carregar Detalhes do Produto Dinamicamente
document.querySelectorAll('.view-product').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const productId = this.getAttribute('data-product');
        loadProductDetails(productId);
    });
});

function loadSection(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newContent = doc.querySelector('main').innerHTML;
            const main = document.querySelector('main');
            main.style.opacity = '0';
            setTimeout(() => {
                main.innerHTML = newContent;
                main.style.opacity = '1';
            }, 500);
        })
        .catch(error => console.error('Erro ao carregar seção:', error));
}

function loadProductDetails(productId) {
    const productDetails = {
        'iphone15': {
            title: 'iPhone 15 Pro Max (512GB)',
            description: 'O mais avançado iPhone com câmera revolucionária e desempenho incomparável.',
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
    if (product) {
        const productSection = document.createElement('section');
        productSection.classList.add('product-details', 'section-transition');
        productSection.innerHTML = `
            <div class="container">
                <h2>${product.title}</h2>
                <div class="product-detail-content">
                    <img src="{% static '${product.image}' %}" alt="${product.title}" class="product-detail-image">
                    <div class="product-detail-info">
                        <p>${product.description}</p>
                        <p>Preço: ${product.price}</p>
                        <a href="{% url 'core:cadastro' %}" class="btn btn-product">Comprar Agora</a>
                    </div>
                </div>
            </div>
        `;
        const main = document.querySelector('main');
        main.innerHTML = '';
        main.appendChild(productSection);
        setTimeout(() => {
            productSection.classList.add('active');
        }, 100);
    }
}

// Animações de Scroll
document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('hero-video');
    if (video) {
        video.onerror = () => console.error('Erro ao carregar o vídeo:', video.error);
        video.onloadeddata = () => console.log('Vídeo carregado com sucesso!');
    }

    const sections = document.querySelectorAll('.section-transition');
    const observerOptions = {
        threshold: 0.1
    };
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, observerOptions);
    sections.forEach(section => observer.observe(section));
});