// Элементы модального окна и формы
const dialog = document.getElementById('contactDialog');
const openBtn = document.getElementById('openDialog');
const closeBtn = document.getElementById('closeDialog');
const form = document.getElementById('contactForm');
let lastActiveElement = null;

// Маска для телефона
const phoneInput = document.getElementById('phone');

phoneInput?.addEventListener('input', function(e) {
    const input = e.target;
    let value = input.value.replace(/\D/g, '');
    
    // Ограничиваем до 11 цифр
    value = value.slice(0, 11);
    
    // Заменяем первую 8 на 7
    if (value.startsWith('8')) {
        value = '7' + value.slice(1);
    }
    
    // Форматируем номер
    let formattedValue = '';
    if (value.length > 0) {
        formattedValue = '+7';
        if (value.length > 1) {
            formattedValue += ` (${value.slice(1, 4)}`;
        }
        if (value.length >= 4) {
            formattedValue += `) ${value.slice(4, 7)}`;
        }
        if (value.length >= 7) {
            formattedValue += `-${value.slice(7, 9)}`;
        }
        if (value.length >= 9) {
            formattedValue += `-${value.slice(9, 11)}`;
        }
    }
    
    input.value = formattedValue;
});

// Открытие модального окна
openBtn.addEventListener('click', () => {
    lastActiveElement = document.activeElement;
    dialog.showModal();
    
    // Фокусируемся на первом поле формы
    const firstInput = dialog.querySelector('input, select, textarea');
    if (firstInput) {
        firstInput.focus();
    }
});

// Закрытие модального окна
closeBtn.addEventListener('click', () => {
    dialog.close('cancel');
    resetForm();
});

// Обработка закрытия модального окна
dialog.addEventListener('close', (e) => {
    if (dialog.returnValue === 'success') {
        showSuccessMessage();
    }
    lastActiveElement?.focus();
});

// Клик по подложке для закрытия
dialog.addEventListener('click', (e) => {
    if (e.target === dialog) {
        dialog.close('cancel');
        resetForm();
    }
});

// Валидация формы
form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Сбрасываем кастомные сообщения об ошибках
    resetValidation();
    
    // Проверяем валидность формы
    if (!form.checkValidity()) {
        showValidationErrors();
        return;
    }
    
    // Если форма валидна, закрываем модальное окно
    dialog.close('success');
    resetForm();
});

// Функция сброса валидации
function resetValidation() {
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.setCustomValidity('');
        input.removeAttribute('aria-invalid');
        
        // Скрываем сообщения об ошибках
        const errorElement = input.nextElementSibling;
        if (errorElement && errorElement.classList.contains('error-message')) {
            errorElement.classList.remove('show');
        }
    });
}

// Функция показа ошибок валидации
function showValidationErrors() {
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        if (!input.checkValidity()) {
            input.setAttribute('aria-invalid', 'true');
            
            // Создаем или показываем сообщение об ошибке
            let errorElement = input.nextElementSibling;
            if (!errorElement || !errorElement.classList.contains('error-message')) {
                errorElement = document.createElement('div');
                errorElement.className = 'error-message';
                input.parentNode.insertBefore(errorElement, input.nextSibling);
            }
            
            // Устанавливаем текст ошибки
            if (input.validity.valueMissing) {
                errorElement.textContent = 'Это поле обязательно для заполнения';
            } else if (input.validity.typeMismatch) {
                errorElement.textContent = 'Пожалуйста, введите корректный формат';
            } else if (input.validity.patternMismatch) {
                errorElement.textContent = 'Неверный формат. Пример: +7 (900) 000-00-00';
            } else if (input.validity.tooShort) {
                errorElement.textContent = `Минимальная длина: ${input.minLength} символов`;
            } else {
                errorElement.textContent = 'Неверное значение';
            }
            
            errorElement.classList.add('show');
        }
    });
    
    // Показываем браузерные подсказки
    form.reportValidity();
}

// Функция сброса формы
function resetForm() {
    form.reset();
    resetValidation();
}

// Функция показа сообщения об успехе
function showSuccessMessage() {
    alert('Форма успешно отправлена! Мы свяжемся с вами в ближайшее время.');
}

// Обработка изменения полей для динамической валидации
form.querySelectorAll('input, select, textarea').forEach(input => {
    input.addEventListener('blur', () => {
        if (!input.checkValidity()) {
            input.setAttribute('aria-invalid', 'true');
        } else {
            input.removeAttribute('aria-invalid');
            const errorElement = input.nextElementSibling;
            if (errorElement && errorElement.classList.contains('error-message')) {
                errorElement.classList.remove('show');
            }
        }
    });
});

// Обработка Escape для закрытия модального окна
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && dialog.open) {
        dialog.close('cancel');
        resetForm();
    }
});