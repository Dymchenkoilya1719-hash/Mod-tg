export class SettingsScreen {
  async render(container: HTMLElement): Promise<void> {
    container.innerHTML = `
      <div class="app-container">
        <header class="app-header">
          <button id="back-btn" class="icon-btn">←</button>
          <h1>Настройки</h1>
        </header>

        <div class="settings-content">
          <div class="settings-section">
            <h2>Профиль</h2>
            <div class="setting-item">
              <label>Тема</label>
              <select id="theme-select" class="select-field">
                <option value="dark">🌙 Тёмная</option>
                <option value="light">☀️ Светлая</option>
              </select>
            </div>
          </div>

          <div class="settings-section">
            <h2>Безопасность</h2>
            <div class="setting-item">
              <label>
                <input type="checkbox" id="pin-enabled" />
                Защита PIN-кодом
              </label>
            </div>
          </div>

          <div class="settings-section">
            <h2>Аккаунт</h2>
            <button id="logout-btn" class="btn btn-danger">🚪 Выйти</button>
          </div>
        </div>
      </div>
    `;

    // Обработчики
    const backBtn = container.querySelector('#back-btn') as HTMLButtonElement;
    backBtn.addEventListener('click', () => {
      window.location.hash = '#/chats';
    });

    const logoutBtn = container.querySelector('#logout-btn') as HTMLButtonElement;
    logoutBtn.addEventListener('click', () => {
      if (confirm('Ты уверен, что хочешь выйти?')) {
        localStorage.clear();
        window.location.hash = '#/login';
      }
    });
  }
}
