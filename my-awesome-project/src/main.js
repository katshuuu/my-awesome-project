// ===== THEME TOGGLE =====
class ThemeManager {
  constructor() {
    this.KEY = 'theme';
    this.toggleBtn = document.querySelector('.theme-toggle');
    this.prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    this.init();
  }
  
  init() {
    this.loadTheme();
    this.bindEvents();
  }
  
  loadTheme() {
    const savedTheme = localStorage.getItem(this.KEY);
    const shouldBeDark = savedTheme === 'dark' || (!savedTheme && this.prefersDark);
    
    if (shouldBeDark) {
      document.body.classList.add('theme-dark');
      this.toggleBtn?.setAttribute('aria-pressed', 'true');
    }
  }
  
  bindEvents() {
    this.toggleBtn?.addEventListener('click', () => {
      this.toggleTheme();
    });
    
    // Слушаем изменения системной темы
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem(this.KEY)) {
        if (e.matches) {
          document.body.classList.add('theme-dark');
        } else {
          document.body.classList.remove('theme-dark');
        }
      }
    });
  }
  
  toggleTheme() {
    const isDark = document.body.classList.toggle('theme-dark');
    this.toggleBtn?.setAttribute('aria-pressed', String(isDark));
    localStorage.setItem(this.KEY, isDark ? 'dark' : 'light');
  }
}

// ===== MODAL MANAGER =====
class ModalManager {
  constructor() {
    this.modals = new Map();
    this.init();
  }
  
  init() {
    this.registerModals();
    this.bindGlobalEvents();
  }
  
  registerModals() {
    document.querySelectorAll('[data-modal]').forEach(trigger => {
      const modalId = trigger.dataset.modal;
      const modal = document.getElementById(modalId);
      
      if (modal) {
        this.modals.set(modalId, modal);
        
        trigger.addEventListener('click', () => {
          this.openModal(modalId);
        });
      }
    });
    
    document.querySelectorAll('[data-close-modal]').forEach(closeBtn => {
      closeBtn.addEventListener('click', () => {
        this.closeCurrentModal();
      });
    });
  }
  
  openModal(modalId) {
    const modal = this.modals.get(modalId);
    if (modal) {
      modal.showModal();
      this.trapFocus(modal);
    }
  }
  
  closeCurrentModal() {
    document.querySelector('dialog[open]')?.close();
  }
  
  trapFocus(modal) {
    const focusableElements = modal.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    if (focusableElements.length > 0) {
      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];
      
      modal.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
          if (e.shiftKey) {
            if (document.activeElement === firstElement) {
              e.preventDefault();
              lastElement.focus();
            }
          } else {
            if (document.activeElement === lastElement) {
              e.preventDefault();
              firstElement.focus();
            }
          }
        }
        
        if (e.key === 'Escape') {
          this.closeCurrentModal();
        }
      });
      
      firstElement.focus();
    }
  }
  
  bindGlobalEvents() {
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.closeCurrentModal();
      }
    });
    
    document.addEventListener('click', (e) => {
      if (e.target.tagName === 'DIALOG') {
        this.closeCurrentModal();
      }
    });
  }
}

// ===== FORM VALIDATION =====
class FormValidator {
  constructor(form) {
    this.form = form;
    this.init();
  }
  
  init() {
    this.form.setAttribute('novalidate', '');
    this.form.addEventListener('submit', (e) => this.validateForm(e));
    
    this.form.querySelectorAll('[data-validate]').forEach(input => {
      input.addEventListener('blur', () => this.validateField(input));
    });
  }
  
  validateForm(e) {
    e.preventDefault();
    
    let isValid = true;
    this.form.querySelectorAll('[data-validate]').forEach(input => {
      if (!this.validateField(input)) {
        isValid = false;
      }
    });
    
    if (isValid) {
      this.form.submit();
    }
  }
  
  validateField(input) {
    const value = input.value.trim();
    const errorElement = input.nextElementSibling;
    let isValid = true;
    let errorMessage = '';
    
    // Сброс состояния
    input.removeAttribute('aria-invalid');
    if (errorElement?.classList.contains('form__error')) {
      errorElement.classList.remove('form__error--show');
    }
    
    // Проверки
    if (input.hasAttribute('required') && !value) {
      isValid = false;
      errorMessage = 'Это поле обязательно для заполнения';
    }
    
    if (input.type === 'email' && value && !this.isValidEmail(value)) {
      isValid = false;
      errorMessage = 'Введите корректный email адрес';
    }
    
    if (input.type === 'tel' && value && !this.isValidPhone(value)) {
      isValid = false;
      errorMessage = 'Введите корректный номер телефона';
    }
    
    if (input.hasAttribute('minlength') && value.length < input.minLength) {
      isValid = false;
      errorMessage = `Минимальная длина: ${input.minLength} символов`;
    }
    
    if (input.hasAttribute('pattern') && value) {
      const pattern = new RegExp(input.pattern);
      if (!pattern.test(value)) {
        isValid = false;
        errorMessage = 'Неверный формат';
      }
    }
    
    // Установка состояния
    if (!isValid) {
      input.setAttribute('aria-invalid', 'true');
      if (errorElement?.classList.contains('form__error')) {
        errorElement.textContent = errorMessage;
        errorElement.classList.add('form__error--show');
      }
    }
    
    return isValid;
  }
  
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
  
  isValidPhone(phone) {
    const phoneRegex = /^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$/;
    return phoneRegex.test(phone);
  }
}

// ===== IMAGE LAZY LOADING =====
class LazyLoader {
  constructor() {
    this.observer = null;
    this.init();
  }
  
  init() {
    if ('IntersectionObserver' in window) {
      this.observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.loadImage(entry.target);
            this.observer.unobserve(entry.target);
          }
        });
      }, {
        rootMargin: '200px 0px',
        threshold: 0.1
      });
      
      this.observeImages();
    } else {
      this.loadAllImages();
    }
  }
  
  observeImages() {
    document.querySelectorAll('img[data-src]').forEach(img => {
      this.observer.observe(img);
    });
  }
  
  loadImage(img) {
    const src = img.dataset.src;
    if (src) {
      img.src = src;
      img.removeAttribute('data-src');
      
      if (img.dataset.srcset) {
        img.srcset = img.dataset.srcset;
        img.removeAttribute('data-srcset');
      }
    }
  }
  
  loadAllImages() {
    document.querySelectorAll('img[data-src]').forEach(img => {
      this.loadImage(img);
    });
  }
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
  // Инициализация менеджера тем
  new ThemeManager();
  
  // Инициализация модальных окон
  new ModalManager();
  
  // Инициализация валидации форм
  document.querySelectorAll('form[data-validate]').forEach(form => {
    new FormValidator(form);
  });
  
  // Ленивая загрузка изображений
  new LazyLoader();
  
  // Плавная прокрутка для якорных ссылок
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
  
  // Подсветка активного пункта навигации
  const currentPath = window.location.pathname;
  document.querySelectorAll('.site-nav__link').forEach(link => {
    const linkPath = link.getAttribute('href');
    if (linkPath === currentPath || (currentPath.endsWith('/') && linkPath === 'index.html')) {
      link.classList.add('site-nav__link--active');
    }
  });
});

// ===== PHONE MASK =====
function initPhoneMask() {
  const phoneInputs = document.querySelectorAll('input[type="tel"]');
  
  phoneInputs.forEach(input => {
    input.addEventListener('input', function (e) {
      let value = e.target.value.replace(/\D/g, '');
      
      if (value.startsWith('7')) {
        value = '7' + value.slice(1);
      } else if (value.startsWith('8')) {
        value = '7' + value.slice(1);
      }
      
      value = value.slice(0, 11);
      
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
      
      e.target.value = formattedValue;
    });
  });
}

// Инициализация маски телефона при загрузке
document.addEventListener('DOMContentLoaded', initPhoneMask);