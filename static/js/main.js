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

// Holograma com Three.js
const hologramContainer = document.getElementById('hologram-container');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, hologramContainer.clientWidth / hologramContainer.clientHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(hologramContainer.clientWidth, hologramContainer.clientHeight);
hologramContainer.appendChild(renderer.domElement);

const geometry = new THREE.TorusKnotGeometry(1, 0.3, 100, 16);
const material = new THREE.MeshBasicMaterial({ color: 0x00ffcc, wireframe: true });
const torusKnot = new THREE.Mesh(geometry, material);
scene.add(torusKnot);

camera.position.z = 5;

function animate() {
    requestAnimationFrame(animate);
    torusKnot.rotation.x += 0.01;
    torusKnot.rotation.y += 0.01;
    renderer.render(scene, camera);
}
animate();

// Modal de Chat com IA Avançada
const modal = document.getElementById('modal');
const openModal = document.querySelector('.chat-button');
const closeModal = document.getElementsByClassName('close')[0];
const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');
const sendMessage = document.getElementById('sendMessage');

// Abrir o modal automaticamente ao carregar a página
window.onload = function() {
    modal.style.display = 'block';
    // Mensagem de boas-vindas
    addIAMessage('Olá! Eu sou a IA A121. Como posso te ajudar hoje? 🚀');
};

openModal.onclick = function() {
    modal.style.display = 'block';
};

closeModal.onclick = function() {
    modal.style.display = 'none';
};

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};

// Enviar mensagem com o botão ou pressionando Enter
sendMessage.onclick = function() {
    sendUserMessage();
};

userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendUserMessage();
    }
});

function sendUserMessage() {
    const message = userInput.value.trim();
    if (message) {
        addUserMessage(message);
        // Enviar mensagem para o Dialogflow
        fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCsrfToken()
            },
            body: 'message=' + encodeURIComponent(message)
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
            console.error('Erro ao se comunicar com o Dialogflow:', error);
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
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Mudança de Moeda com Taxa de Câmbio
document.getElementById('currency-selector').addEventListener('change', function() {
    var selectedCurrency = this.value;
    fetch('/change_currency/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()
        },
        body: 'currency=' + selectedCurrency
    }).then(response => response.json()).then(data => {
        if (data.success) {
            location.reload();
        }
    });
});

// Atualizar Preços com Taxa de Câmbio
function updatePrices(currency, rate) {
    document.querySelectorAll('.product-price, .course-price').forEach(priceElement => {
        var basePrice = parseFloat(priceElement.getAttribute('data-price'));
        var convertedPrice = basePrice * rate;
        priceElement.textContent = convertedPrice.toFixed(2) + ' ' + currency;
    });
}

// Carregar Taxa de Câmbio
fetch('/get_exchange_rate/?base=EUR')
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            var currency = document.getElementById('currency-selector').value || 'EUR';
            var rate = data.rates[currency] || 1;
            updatePrices(currency, rate);
        }
    });

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

// Hologramas nos Produtos
function createProductHologram(containerClass, color) {
    const container = document.querySelector(`.${containerClass}`);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(renderer.domElement);

    const geometry = new THREE.SphereGeometry(0.5, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: color, wireframe: true });
    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    camera.position.z = 2;

    function animate() {
        requestAnimationFrame(animate);
        sphere.rotation.x += 0.02;
        sphere.rotation.y += 0.02;
        renderer.render(scene, camera);
    }
    animate();
}

createProductHologram('hologram-iphone15', 0x00ffcc);
createProductHologram('hologram-iphone16', 0x00ccff);
