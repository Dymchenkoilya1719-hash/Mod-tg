import { AuthManager } from '../services/auth';
import { API } from '../api';

export class LoginScreen {
  private authManager: AuthManager;
  private step: 'phone' | 'code' | 'password' = 'phone';
  private phoneNumber: string = '';
  private phoneCodeHash: string = '';

  constructor() {
    this.authManager = new AuthManager();
  }

  async render(container: HTMLElement): Promise<void> {
    if (this.step === 'phone') {
      this.renderPhoneStep(container);
    } else if (this.step === 'code') {
      this.renderCodeStep(container);
    } else {
      this.renderPasswordStep(container);
    }
  }

  private renderPhoneStep(container: HTMLElement): void {
    container.innerHTML = `
      <div class="login-container">
        <div class="login-card">
          <div class="login-logo">
            <svg viewBox="0 0 24 24" width="80" height="80" fill="#1f6f3b">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
            </svg>
          </div>
          
          <h1>TG Mod</h1>
          <p class="subtitle">Модифицированный клиент Telegram</p>
          
          <div class="form-group">
            <label for="phone">Номер телефона</label>
            <input 
              type="tel" 
              id="phone" 
              placeholder="+7 (800) 555-35-35"
              class="input-field"
            />
            <small>Формат: +7XXXXXXXXXX</small>
          </div>
          
          <button id="request-code-btn" class="btn btn-primary">Запросить код</button>
          
          <div id="error-message" class="error-message" style="display: none;"></div>
        </div>
      </div>
    `;

    const phoneInput = container.querySelector('#phone') as HTMLInputElement;
    const requestBtn = container.querySelector('#request-code-btn') as HTMLButtonElement;
    const errorDiv = container.querySelector('#error-message') as HTMLDivElement;

    requestBtn.addEventListener('click', async () => {
      this.phoneNumber = phoneInput.value.trim();
      
      if (!this.phoneNumber) {
        errorDiv.textContent = '⚠️ Введи номер телефона';
        errorDiv.style.display = 'block';
        return;
      }

      requestBtn.disabled = true;
      requestBtn.textContent = 'Загрузка...';

      try {
        const response = await API.post('/api/auth/request_code', {
          phone_number: this.phoneNumber
        });
        
        this.phoneCodeHash = response.phone_code_hash;
        this.step = 'code';
        await this.render(container);
      } catch (error: any) {
        errorDiv.textContent = `❌ ${error.message}`;
        errorDiv.style.display = 'block';
        requestBtn.disabled = false;
        requestBtn.textContent = 'Запросить код';
      }
    });
  }

  private renderCodeStep(container: HTMLElement): void {
    container.innerHTML = `
      <div class="login-container">
        <div class="login-card">
          <h2>Введи код</h2>
          <p class="subtitle">Код отправлен на номер ${this.phoneNumber}</p>
          
          <div class="form-group">
            <label for="code">5-значный код</label>
            <input 
              type="text" 
              id="code" 
              maxlength="5"
              placeholder="00000"
              class="input-field code-input"
            />
          </div>
          
          <div class="form-group">
            <label for="password">Пароль 2FA (если требуется)</label>
            <input 
              type="password" 
              id="password" 
              placeholder="Оставь пусто, если нет 2FA"
              class="input-field"
            />
          </div>
          
          <button id="sign-in-btn" class="btn btn-primary">Войти</button>
          <button id="back-btn" class="btn btn-secondary">Вернуться</button>
          
          <div id="error-message" class="error-message" style="display: none;"></div>
        </div>
      </div>
    `;

    const codeInput = container.querySelector('#code') as HTMLInputElement;
    const passwordInput = container.querySelector('#password') as HTMLInputElement;
    const signInBtn = container.querySelector('#sign-in-btn') as HTMLButtonElement;
    const backBtn = container.querySelector('#back-btn') as HTMLButtonElement;
    const errorDiv = container.querySelector('#error-message') as HTMLDivElement;

    // Фокус на инпут кода
    codeInput.focus();

    signInBtn.addEventListener('click', async () => {
      const code = codeInput.value.trim();
      const password = passwordInput.value || null;

      if (!code || code.length !== 5) {
        errorDiv.textContent = '⚠️ Введи 5-значный код';
        errorDiv.style.display = 'block';
        return;
      }

      signInBtn.disabled = true;
      signInBtn.textContent = 'Загрузка...';

      try {
        await API.post('/api/auth/sign_in', {
          code: code,
          password: password
        });

        // Перенаправить на список чатов
        window.location.hash = '#/chats';
      } catch (error: any) {
        errorDiv.textContent = `❌ ${error.message}`;
        errorDiv.style.display = 'block';
        signInBtn.disabled = false;
        signInBtn.textContent = 'Войти';
      }
    });

    backBtn.addEventListener('click', () => {
      this.step = 'phone';
      this.render(container);
    });
  }

  private renderPasswordStep(container: HTMLElement): void {
    container.innerHTML = `<p>Password step placeholder</p>`;
  }
}
