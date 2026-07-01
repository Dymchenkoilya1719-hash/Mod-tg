import { ChatsManager } from '../services/chats';
import { API } from '../api';

export class ChatsScreen {
  private chatsManager: ChatsManager;
  private dialogs: any[] = [];
  private showOnlyUnread: boolean = false;

  constructor() {
    this.chatsManager = new ChatsManager();
  }

  async render(container: HTMLElement): Promise<void> {
    container.innerHTML = `
      <div class="app-container">
        <!-- Header -->
        <header class="app-header">
          <h1>TG Mod - Чаты</h1>
          <div class="header-actions">
            <button id="search-btn" class="icon-btn" title="Поиск">
              🔍
            </button>
            <button id="settings-btn" class="icon-btn" title="Настройки">
              ⚙️
            </button>
          </div>
        </header>

        <!-- Filters -->
        <div class="filters-bar">
          <button class="filter-chip special-chip" id="support-btn">
            🆘 Поддержка
          </button>
          <button class="filter-chip special-chip" id="ai-btn">
            🤖 ИИ Чат
          </button>
          <button class="filter-chip" id="unread-filter" data-active="false">
            ⭕ Непрочитанные
          </button>
        </div>

        <!-- Chats List -->
        <div class="chats-list" id="chats-list">
          <div class="loading">⏳ Загрузка чатов...</div>
        </div>
      </div>
    `;

    // Загрузить диалоги
    await this.loadDialogs();

    // Событие на фильтр
    const unreadFilter = container.querySelector('#unread-filter') as HTMLButtonElement;
    unreadFilter.addEventListener('click', () => {
      this.showOnlyUnread = !this.showOnlyUnread;
      unreadFilter.dataset.active = String(this.showOnlyUnread);
      this.renderChatsList(container);
    });

    // Специальные чаты
    const supportBtn = container.querySelector('#support-btn') as HTMLButtonElement;
    supportBtn.addEventListener('click', async () => {
      try {
        const response = await API.post('/api/special/support', {});
        // Открыть чат поддержки
        console.log('Открыт чат поддержки:', response);
      } catch (error) {
        console.error('Ошибка открытия чата поддержки:', error);
      }
    });

    const aiBtn = container.querySelector('#ai-btn') as HTMLButtonElement;
    aiBtn.addEventListener('click', async () => {
      console.log('Открыт ИИ чат');
    });

    // Settings
    const settingsBtn = container.querySelector('#settings-btn') as HTMLButtonElement;
    settingsBtn.addEventListener('click', () => {
      window.location.hash = '#/settings';
    });
  }

  private async loadDialogs(): Promise<void> {
    try {
      const response = await API.get('/api/dialogs');
      this.dialogs = response.dialogs || [];
      console.log(`✅ Загружено ${this.dialogs.length} чатов`);
      
      const container = document.querySelector('.chats-list');
      if (container) {
        this.renderChatsList(container.parentElement!);
      }
    } catch (error) {
      console.error('Ошибка загрузки чатов:', error);
      const chatsList = document.querySelector('.chats-list');
      if (chatsList) {
        chatsList.innerHTML = '<div class="error">❌ Ошибка загрузки чатов</div>';
      }
    }
  }

  private renderChatsList(container: HTMLElement): void {
    const chatsList = container.querySelector('.chats-list') as HTMLElement;
    
    const filteredDialogs = this.showOnlyUnread 
      ? this.dialogs.filter(d => d.unread_count > 0)
      : this.dialogs;

    if (filteredDialogs.length === 0) {
      chatsList.innerHTML = '<div class="empty-state">📭 Нет чатов</div>';
      return;
    }

    chatsList.innerHTML = filteredDialogs.map(dialog => `
      <div class="chat-item" data-id="${dialog.id}">
        <div class="chat-avatar">
          ${dialog.name.charAt(0).toUpperCase()}
        </div>
        <div class="chat-info">
          <div class="chat-header">
            <span class="chat-name">${dialog.name}</span>
            <span class="chat-time">${new Date(dialog.last_message_date).toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'})}</span>
          </div>
          <div class="chat-preview">${dialog.last_message || '(нет сообщений)'}</div>
        </div>
        ${dialog.unread_count > 0 ? `<div class="unread-badge">${dialog.unread_count}</div>` : ''}
      </div>
    `).join('');

    // Обработчики клика
    chatsList.querySelectorAll('.chat-item').forEach(item => {
      item.addEventListener('click', () => {
        const dialogId = item.getAttribute('data-id');
        window.location.hash = `#/chat/${dialogId}`;
      });
    });
  }
}
