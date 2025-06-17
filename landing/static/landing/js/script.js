// JavaScript file for landing page
console.log('Starting application...');

// Глобальна змінна для відстеження поточного кроку
let currentStep = 1;

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing form...');
    
    initializeForm();
    bindEvents();
    setupNoneLogic();
    setupAnimations();
    
    // Initialize all inputs visibility state
    document.querySelectorAll('input[type="radio"], input[type="checkbox"]').forEach(input => {
        const label = input.nextElementSibling;
        if (label) {
            label.style.outline = 'none';
            label.style.webkitTapHighlightColor = 'transparent';
        }
    });
});

function initializeForm() {
    const firstStep = document.querySelector('.question-step[data-step="1"]');
    if (firstStep) {
        firstStep.classList.add('active');
        
        // Приховуємо кнопку "Назад" на першому кроці
        const prevButton = firstStep.querySelector('.prev-step');
        if (prevButton) {
            prevButton.style.opacity = '0';
            prevButton.style.pointerEvents = 'none';
        }
    }
    
    // Приховуємо всі поля крім обов'язкових
    clearAllFormInputs();
}

function clearAllFormInputs() {
    // Очищуємо всі радіо кнопки та чекбокси
    document.querySelectorAll('input[type="radio"], input[type="checkbox"]').forEach(input => {
        input.checked = false;
        
        const label = input.nextElementSibling;
        if (label) {
            label.classList.remove('selected');
        }
        
        const parentCard = input.closest('.compact-option, .compact-checkbox, .option-card, .checkbox-card');
        if (parentCard) {
            parentCard.classList.remove('selected');
        }
    });
    
    // Очищуємо всі текстові поля
    document.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], textarea').forEach(input => {
        input.value = '';
    });
}

// Функція перенесена до секції utility functions

function bindEvents() {
    // Навігація між кроками
    document.querySelectorAll('.next-step').forEach(button => {
        button.addEventListener('click', nextStep);
    });
    
    document.querySelectorAll('.prev-step').forEach(button => {
        button.addEventListener('click', prevStep);
    });
    
    // Обробка форми відправки
    const questionnaireForm = document.getElementById('questionnaireForm');
    if (questionnaireForm) {
        questionnaireForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitForm();
        });
    }
    
    // Обробка радіо кнопок
    document.querySelectorAll('input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', function() {
            // Очищуємо вибір в групі
            const groupName = this.name;
            document.querySelectorAll(`input[name="${groupName}"]`).forEach(r => {
                const label = r.nextElementSibling;
                const parentCard = r.closest('.compact-option, .option-card');
                if (label) label.classList.remove('selected');
                if (parentCard) parentCard.classList.remove('selected');
            });
            
            // Вибираємо поточний елемент
            const label = this.nextElementSibling;
            const parentCard = this.closest('.compact-option, .option-card');
            if (label) label.classList.add('selected');
            if (parentCard) {
                parentCard.classList.add('selected');
                parentCard.style.animation = 'compactPulse 0.4s ease-out';
                setTimeout(() => {
                    parentCard.style.animation = '';
                }, 400);
            }
            

        });
    });
}

function setupNoneLogic() {
    // Обробка чекбоксу "Нічого з перерахованого"
    const noneCheckboxes = document.querySelectorAll('input[value="none"]');
    
    noneCheckboxes.forEach(noneCheckbox => {
        noneCheckbox.addEventListener('change', function() {
            const container = this.closest('.compact-checkbox-section, .checkbox-section');
            const otherCheckboxes = container.querySelectorAll('input[type="checkbox"]:not([value="none"])');
            
            if (this.checked) {
                // Якщо вибрано "Нічого", знімаємо всі інші вибори
                otherCheckboxes.forEach(checkbox => {
                    checkbox.checked = false;
                    const label = checkbox.nextElementSibling;
                    const parentCard = checkbox.closest('.compact-checkbox, .checkbox-card');
                    if (label) label.classList.remove('selected');
                    if (parentCard) parentCard.classList.remove('selected');
                });
            }
        });
    });
    
    // Обробка інших чекбоксів (автоматично знімають "Нічого")
    document.querySelectorAll('input[type="checkbox"]:not([value="none"])').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            if (this.checked) {
                const container = this.closest('.compact-checkbox-section, .checkbox-section');
                const noneCheckbox = container.querySelector('input[value="none"]');
                if (noneCheckbox && noneCheckbox.checked) {
                    noneCheckbox.checked = false;
                    const noneLabel = noneCheckbox.nextElementSibling;
                    const noneCard = noneCheckbox.closest('.compact-checkbox, .checkbox-card');
                    if (noneLabel) noneLabel.classList.remove('selected');
                    if (noneCard) noneCard.classList.remove('selected');
                }
            }
            
            // Додаємо/знімаємо клас selected
            const label = this.nextElementSibling;
            const parentCard = this.closest('.compact-checkbox, .checkbox-card');
            if (this.checked) {
                if (label) label.classList.add('selected');
                if (parentCard) {
                    parentCard.classList.add('selected');
                    parentCard.style.animation = 'compactPulse 0.4s ease-out';
                    setTimeout(() => {
                        parentCard.style.animation = '';
                    }, 400);
                }
            } else {
                if (label) label.classList.remove('selected');
                if (parentCard) parentCard.classList.remove('selected');
            }
            

        });
    });
}

function setupAnimations() {
    // Анімація floating cards
    const floatingCards = document.querySelectorAll('.floating-card');
    floatingCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
    });
    
    const animationDots = document.querySelectorAll('.animation-dot');
    animationDots.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.03}s`;
    });
    
    // Анімація при завантаженні сторінки
    const heroContent = document.querySelector('.hero-content');
    const heroVisual = document.querySelector('.hero-visual');
    
    if (heroContent) {
        setTimeout(() => {
            heroContent.style.opacity = '1';
            heroContent.style.transform = 'translateY(0)';
        }, 100);
    }
    
    if (heroVisual) {
        setTimeout(() => {
            heroVisual.style.opacity = '1';
            heroVisual.style.transform = 'translateY(0)';
        }, 150);
    }
}

function validateCurrentStep() {
    const currentStepElement = document.querySelector(`.question-step[data-step="${currentStep}"]`);
    if (!currentStepElement) return false;
    
    const requiredRadios = currentStepElement.querySelectorAll('input[type="radio"][required]');
    const requiredCheckboxes = currentStepElement.querySelectorAll('input[type="checkbox"][required]');
    const requiredInputs = currentStepElement.querySelectorAll('input[required], textarea[required]');
    
    // Перевіряємо радіо кнопки
    const radioGroups = new Set();
    requiredRadios.forEach(radio => radioGroups.add(radio.name));
    
    for (const groupName of radioGroups) {
        const groupRadios = currentStepElement.querySelectorAll(`input[name="${groupName}"]`);
        const isChecked = Array.from(groupRadios).some(radio => radio.checked);
        if (!isChecked) {
            // Анімація помилки
            groupRadios.forEach(radio => {
                const parentCard = radio.closest('.compact-option, .option-card');
                if (parentCard) {
                    parentCard.style.animation = 'shake 0.6s ease-in-out';
                    setTimeout(() => {
                        parentCard.style.animation = '';
                    }, 500);
                }
            });
            return false;
        }
    }
    
    // Перевіряємо текстові поля
    for (const input of requiredInputs) {
        if (!validateField(input)) {
            return false;
        }
    }
    
    return true;
}

function validateField(field) {
    const value = field.value.trim();
    const container = field.closest('.contact-field, .contact-field-new');
    
    // Очищуємо попередні помилки
    clearFieldError(container);
    
    if (!value) {
        showFieldError(container, 'Це поле обов\'язкове');
        return false;
    }
    
    // Валідація email
    if (field.type === 'email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(container, 'Невірний формат email');
            return false;
        }
    }
    
    // Валідація телефону
    if (field.type === 'tel') {
        const phoneRegex = /^[\+]?[0-9\s\-\(\)]{10,}$/;
        if (!phoneRegex.test(value)) {
            showFieldError(container, 'Невірний формат телефону');
            return false;
        }
    }
    
    return true;
}

function showFieldError(container, message) {
    if (!container) return;
    
    let errorElement = container.querySelector('.field-error');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        container.appendChild(errorElement);
    }
    
    errorElement.textContent = message;
    errorElement.style.color = '#ef4444';
    errorElement.style.fontSize = '0.875rem';
    errorElement.style.marginTop = '0.25rem';
    errorElement.style.animation = 'fadeInDown 0.3s ease-out';
    
    const input = container.querySelector('input, textarea');
    if (input) {
        input.style.borderColor = '#ef4444';
        input.style.animation = 'shake 0.6s ease-in-out';
        setTimeout(() => {
            input.style.animation = '';
        }, 500);
    }
}

function clearFieldError(container) {
    if (!container) return;
    
    const errorElement = container.querySelector('.field-error');
    if (errorElement) {
        errorElement.remove();
    }
    
    const input = container.querySelector('input, textarea');
    if (input) {
        input.style.borderColor = '';
    }
}

function nextStep() {
    if (!validateCurrentStep()) return;
    
    const currentStepElement = document.querySelector(`.question-step[data-step="${currentStep}"]`);
    const nextStepElement = document.querySelector(`.question-step[data-step="${currentStep + 1}"]`);
    
    if (nextStepElement) {
        // Анімація виходу поточного кроку
        currentStepElement.classList.add('slide-out-left');
        currentStepElement.classList.remove('active');
        
        setTimeout(() => {
            // Приховуємо поточний крок
            currentStepElement.style.display = 'none';
            currentStepElement.classList.remove('slide-out-left');
            
            // Показуємо наступний крок
            nextStepElement.style.display = 'block';
            nextStepElement.classList.add('slide-in-right', 'active');
            
            // Оновлюємо номер кроку
            currentStep++;
            
            // Показуємо кнопку "Назад" на всіх кроках окрім першого
            const prevButton = nextStepElement.querySelector('.prev-step');
            if (prevButton && currentStep > 1) {
                prevButton.style.opacity = '1';
                prevButton.style.pointerEvents = 'auto';
            }
            
            setTimeout(() => {
                nextStepElement.classList.remove('slide-in-right');
            }, 300);
        }, 300);
    }
}

function prevStep() {
    const currentStepElement = document.querySelector(`.question-step[data-step="${currentStep}"]`);
    const prevStepElement = document.querySelector(`.question-step[data-step="${currentStep - 1}"]`);
    
    if (prevStepElement) {
        // Анімація виходу поточного кроку
        currentStepElement.classList.add('slide-out-right');
        currentStepElement.classList.remove('active');
        
        setTimeout(() => {
            // Приховуємо поточний крок
            currentStepElement.style.display = 'none';
            currentStepElement.classList.remove('slide-out-right');
            
            // Показуємо попередній крок
            prevStepElement.style.display = 'block';
            prevStepElement.classList.add('slide-in-left', 'active');
            
            // Оновлюємо номер кроку
            currentStep--;
            
            // Приховуємо кнопку "Назад" на першому кроці
            if (currentStep === 1) {
                const prevButton = prevStepElement.querySelector('.prev-step');
                if (prevButton) {
                    prevButton.style.opacity = '0';
                    prevButton.style.pointerEvents = 'none';
                }
            }
            
            setTimeout(() => {
                prevStepElement.classList.remove('slide-in-left');
            }, 300);
        }, 300);
    }
}

function scrollToForm() {
    document.getElementById('questionnaire').scrollIntoView({ 
        behavior: 'smooth' 
    });
}

async function submitForm() {
    const form = document.getElementById('questionnaireForm');
    const formData = new FormData(form);
    const submitButton = document.querySelector('.submit-btn');
    
    // Додаємо вибрані checkbox значення з правильними іменами
    const priorities = [];
    document.querySelectorAll('input[name="priorities_selected"]:checked').forEach(input => {
        priorities.push(input.value);
    });
    
    const trafficSources = [];
    document.querySelectorAll('input[name="traffic_sources_selected"]:checked').forEach(input => {
        trafficSources.push(input.value);
    });
    
    const features = [];
    document.querySelectorAll('input[name="features_selected"]:checked').forEach(input => {
        features.push(input.value);
    });
    
    // Додаємо дані до FormData
    priorities.forEach(priority => formData.append('priorities', priority));
    trafficSources.forEach(source => formData.append('traffic_sources', source));
    features.forEach(feature => formData.append('needed_features', feature));
    
    // Показуємо стан завантаження
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Обробляємо...';
    submitButton.disabled = true;
    
    try {
        const response = await fetch('/process/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showResults(data);
        } else {
            throw new Error(data.error || 'Помилка обробки запиту');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Виникла помилка при обробці запиту. Спробуйте ще раз.');
    } finally {
        submitButton.innerHTML = '<i class="fas fa-paper-plane"></i> Отримати результат';
        submitButton.disabled = false;
    }
}

function showResults(data) {
    const motivationPhrases = [
        "Ваш сайт буде неймовірним! ✨",
        "Готуємо щось особливе для вас! 🚀",
        "Ваша ідея заслуговує на найкраще! 💎",
        "Створюємо магію для вашого бізнесу! 🌟",
        "Ваш успіх - наша мета! 🎯"
    ];
    
    const randomPhrase = motivationPhrases[Math.floor(Math.random() * motivationPhrases.length)];
    
    // Використовуємо ціну з backend (вже розрахована залежно від складності)
    const calculatedPrice = data.estimated_price || 259;
    const minPrice = Math.max(209, calculatedPrice - 30); // Мінімальна ціна на 30 менше
    const maxPrice = Math.min(499, calculatedPrice + 30); // Максимальна ціна на 30 більше
    
    // Переконуємося, що ціни закінчуються на "9"
    const adjustToNine = (price) => {
        const lastDigit = price % 10;
        if (lastDigit !== 9) {
            return price - lastDigit + 9;
        }
        return price;
    };
    
    const finalMinPrice = adjustToNine(minPrice);
    const finalMaxPrice = adjustToNine(maxPrice);
    
    const mockupHTML = generateAdvancedMockup(data);
    
    const resultContent = document.getElementById('resultContent');
    resultContent.innerHTML = `
        <div class="motivation-banner">
            <div class="motivation-text">${randomPhrase}</div>
        </div>
        
        <div class="price-display-new">
            <div class="price-header">
                <h4>Приблизна вартість проекту:</h4>
            </div>
            <div class="price-range">
                <span class="price-from">$${finalMinPrice}</span>
                <span class="price-separator">-</span>
                <span class="price-to" id="priceAmount">$${finalMaxPrice}</span>
            </div>
            <div class="price-timeline">
                Приблизна готовність до <strong>${data.estimated_days} ${data.estimated_days === 1 ? 'дня' : 'днів'}</strong>
            </div>
            <div class="price-note">
                *Точна вартість залежить від ваших потреб
            </div>
        </div>
        
        <div class="contact-order-section-new">
            <div class="contact-header-new">
                <h3>Отримати безкоштовну візуалізацію</h3>
                <p class="contact-subtitle">Залиште контакти і ми зв'яжемося з вами протягом години</p>
            </div>
            
            <div class="contact-benefits">
                <div class="benefits-row">
                    <span class="benefit-badge">🎯 Безкоштовна консультація</span>
                    <span class="benefit-badge">⚡ Швидкий старт</span>
                </div>
                <div class="benefits-row">
                    <span class="benefit-badge">💎 Гарантія якості</span>
                    <span class="benefit-badge">🔧 Технічна підтримка</span>
                </div>
            </div>
            
            <form id="contactForm" class="contact-form-new">
                <div class="contact-fields-vertical">
                    <div class="contact-field-new">
                        <div class="input-wrapper-new">
                            <i class="fas fa-user input-icon-new"></i>
                            <input type="text" name="name" class="form-input-new" placeholder="Ваше ім'я" required>
                        </div>
                    </div>
                    <div class="contact-field-new">
                        <div class="input-wrapper-new">
                            <i class="fas fa-envelope input-icon-new"></i>
                            <input type="email" name="email" class="form-input-new" placeholder="Email" required>
                        </div>
                    </div>
                    <div class="contact-field-new">
                        <div class="input-wrapper-new">
                            <i class="fas fa-phone input-icon-new"></i>
                            <input type="tel" name="phone" class="form-input-new" placeholder="Телефон (необов'язково)">
                        </div>
                    </div>
                </div>
                
                <button type="submit" class="btn-order-new">
                    Замовити безкоштовну візуалізацію
                </button>
            </form>
            
            <div class="contact-note">
                Або напишіть нам в <a href="https://t.me/prometeylabs" target="_blank" class="telegram-link">Telegram</a>
            </div>
        </div>
        
        <div class="row mb-4">
            <div class="col-lg-6 mb-4">
                <div class="whats-included">
                    <h5><i class="fas fa-check-circle text-success me-2"></i>Що входить у вартість:</h5>
                    <div class="included-list">
                        <div class="included-item"><i class="fas fa-paint-brush"></i>Унікальний дизайн</div>
                        <div class="included-item"><i class="fas fa-mobile-alt"></i>Мобільна адаптація</div>
                        <div class="included-item"><i class="fas fa-rocket"></i>Швидка загрузка</div>
                        <div class="included-item"><i class="fas fa-search"></i>Базове SEO</div>
                        <div class="included-item"><i class="fas fa-shield-alt"></i>SSL сертифікат</div>
                        <div class="included-item"><i class="fas fa-headset"></i>Технічна підтримка</div>
                    </div>
                </div>
            </div>
            <div class="col-lg-6 mb-4">
                <div class="mockup-section">
                    ${mockupHTML}
                </div>
            </div>
        </div>
        
        <div class="row mb-4">
            <div class="col-md-4 mb-3">
                <div class="detail-card">
                    <div class="detail-header">
                        <i class="fas fa-cog text-primary"></i>
                        <h6>Функціонал</h6>
                    </div>
                    <div class="detail-content">
                        ${data.functionality ? data.functionality.replace(/\n/g, '<br>') : 'Базовий функціонал'}
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="detail-card">
                    <div class="detail-header">
                        <i class="fas fa-palette text-info"></i>
                        <h6>Стиль</h6>
                    </div>
                    <div class="detail-content">
                        ${data.style || 'Сучасний дизайн'}
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="detail-card">
                    <div class="detail-header">
                        <i class="fas fa-plug text-success"></i>
                        <h6>Інтеграції</h6>
                    </div>
                    <div class="detail-content">
                        ${data.integrations || 'Базові інтеграції'}
                    </div>
                </div>
            </div>
        </div>
        
        ${data.recommendations ? `
        <div class="recommendations-card mb-4">
            <h5><i class="fas fa-lightbulb text-warning me-2"></i>Рекомендації:</h5>
            <div class="recommendations-grid">
                ${data.recommendations.map(rec => `<div class="recommendation-item">${rec}</div>`).join('')}
            </div>
        </div>
        ` : ''}
    `;
    
    // Показуємо модальне вікно
    const resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
    resultModal.show();
    
    // Анімація збільшення ціни
    const priceElement = document.getElementById('priceAmount');
    if (priceElement) {
        animateValue(priceElement, finalMinPrice, finalMaxPrice, 2000);
    }
    
    // Обробка форми замовлення
    const contactForm = document.getElementById('contactForm');
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        submitContactForm(data);
    });
}

function submitContactForm(data) {
    const form = document.getElementById('contactForm');
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Показуємо стан завантаження
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Відправляємо...';
    submitBtn.disabled = true;
    
    const formData = new FormData(form);
    formData.append('estimated_price', data.estimated_price);
    formData.append('estimated_days', data.estimated_days);
    formData.append('functionality', data.functionality);
    formData.append('style', data.style);
    formData.append('integrations', data.integrations);
    formData.append('recommendations', JSON.stringify(data.recommendations));
    
    fetch('/submit-contact/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            // Показуємо успішне повідомлення
            submitBtn.innerHTML = '<i class="fas fa-check"></i> Відправлено!';
            submitBtn.classList.remove('btn-order-new');
            submitBtn.classList.add('btn-success');
            
            // Показуємо повідомлення про успіх
            const successMessage = document.createElement('div');
            successMessage.className = 'alert alert-success mt-3';
            successMessage.innerHTML = `
                <i class="fas fa-check-circle"></i>
                <strong>Дякуємо!</strong> Ми зв'яжемося з вами протягом години.
            `;
            form.appendChild(successMessage);
            
            // Очищуємо форму
            form.reset();
            
            setTimeout(() => {
                successMessage.style.animation = 'fadeOut 0.5s ease-out';
                setTimeout(() => {
                    if (successMessage.parentNode) {
                        successMessage.remove();
                    }
                }, 500);
            }, 5000);
        } else {
            throw new Error(result.error || 'Помилка відправки');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        submitBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Спробуйте ще раз';
        submitBtn.classList.add('btn-warning');
        
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.classList.remove('btn-warning');
            submitBtn.classList.add('btn-order-new');
            submitBtn.disabled = false;
        }, 3000);
    });
}

function generateAdvancedMockup(data) {
    return `
        <div class="demo-container">
            <img src="/static/landing/img/result.png" 
                 alt="Приклад сайту для ${data.business_sphere || 'вашого бізнесу'}" 
                 class="demo-image"
                 loading="lazy">
        </div>
    `;
}

function showError(message) {
    const resultContent = document.getElementById('resultContent');
    resultContent.innerHTML = `
        <div class="alert alert-danger" role="alert" style="animation: fadeInUp 0.6s ease-out;">
            <h4 class="alert-heading">
                <i class="fas fa-exclamation-triangle"></i>
                Помилка
            </h4>
            <p>${message}</p>
            <hr>
            <p class="mb-0">
                Будь ласка, спробуйте ще раз або зв'яжіться з нами напряму:
                <a href="https://t.me/prometeylabs" target="_blank" class="alert-link">
                    @prometeylabs
                </a>
            </p>
        </div>
    `;
    const resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
    resultModal.show();
}

// Utility functions
function animateValue(element, start, end, duration) {
    const startTimestamp = Date.now();
    const step = () => {
        const elapsed = Date.now() - startTimestamp;
        const progress = Math.min(elapsed / duration, 1);
        const easeOutCubic = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(easeOutCubic * (end - start) + start);
        element.textContent = '$' + current;
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    };
    requestAnimationFrame(step);
}

// Function to scroll to contact form from price block
function scrollToContactForm() {
    const contactSection = document.querySelector('.contact-order-section-new');
    if (contactSection) {
        contactSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
        
        // Add a highlight effect
        contactSection.style.animation = 'none';
        setTimeout(() => {
            contactSection.style.animation = 'highlightPulse 1.5s ease-out';
        }, 100);
    }
}

// Export functions for global access
window.scrollToForm = scrollToForm;
window.scrollToContactForm = scrollToContactForm;

console.log('JavaScript file loaded successfully');
