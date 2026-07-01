import { API } from '../api';

export class ChatViewScreen {
  private dialogId: number;
  private messages: any[] = [];

  constructor(dialogId: number) {
    this.dialogId = dialogId;
  }

  async render(container: HTMLElement): Promise<void> {
    container.innerHTML = `
      <div class="app-container">
        <!-- Header -->
        <header class="chat-header">
          <button id="back-btn" class="icon-btn">←</button>
          <div class="chat-title">
            <h2>Чат #${this.dialogId}</h2>
          </div>
        </header>

        <!-- Messages -->
        <div class="messages-container" id="messages-container">
          <div class="loading">⏳ Загрузка сообщений...</div>
        </div>

        <!-- Input -->
        <div class="message-input-container">
          <textarea 
            id="message-input" 
            class="message-input" 
            placeholder="Напиши сообщение..."
            rows="1"
          ></textarea>
          <button id="send-btn" class="btn btn-primary">📤</button>
        </div>
      </div>
    `;

    // Загрузить сообщения
    await this.loadMessages();

    // Обработчики
    const backBtn = container.querySelector('#back-btn') as HTMLButtonElement;
    backBtn.addEventListener('click', () => {
      window.location.hash = '#/chats';
    });

    const sendBtn = container.querySelector('#send-btn') as HTMLButtonElement;
    const messageInput = container.querySelector('#message-input') as HTMLTextAreaElement;

    sendBtn.addEventListener('click', () => this.sendMessage(messageInput));
    messageInput.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.key === 'Enter') {
        this.sendMessage(messageInput);
      }
    });
  }

  private async loadMessages(): Promise<void> {
    try {
      const response = await API.get(`/api/dialogs/${this.dialogId}/messages`);
      this.messages = response.messages || [];
      this.renderMessages();
    } catch (error) {
      console.error('Ошибка загрузки сообщений:', error);
      const container = document.querySelector('.messages-container');
      if (container) {
        container.innerHTML = '<div class="error">❌ Ошибка загрузки сообщений</div>';
      }
    }
  }

  private renderMessages(): void {
    const container = document.querySelector('.messages-container') as HTMLElement;
    
    if (this.messages.length === 0) {
      container.innerHTML = '<div class="empty-state">📭 Нет сообщений</div>';
      return;
    }

    container.innerHTML = this.messages.map(msg => `
      <div class="message ${msg.sender_id === msg.user_id ? 'sent' : 'received'}">
        <div class="message-bubble">
          ${msg.text}
          <small class="message-time">${new Date(msg.created_at).toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'})}</small>
        </div>
      </div>
    `).join('');

    // Прокрутить вниз
    container.scrollTop = container.scrollHeight;
  }

  private async sendMessage(input: HTMLTextAreaElement): Promise<void> {
    const text = input.value.trim();
    
    if (!text) return;

    try {
      await API.post('/api/messages/send', {
        dialog_id: this.dialogId,
        text: text
      });

      input.value = '';
      await this.loadMessages();
    } catch (error) {
      console.error('Ошибка отправки сообщения:', error);
      alert('❌ Ошибка отправки сообщения');
    }
  }
}
