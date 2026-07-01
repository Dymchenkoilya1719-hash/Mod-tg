import { API } from '../api';

export class ChatsManager {
  async getDialogs(): Promise<any[]> {
    try {
      const response = await API.get('/api/dialogs');
      return response.dialogs || [];
    } catch (error) {
      console.error('Error fetching dialogs:', error);
      return [];
    }
  }

  async getMessages(dialogId: number): Promise<any[]> {
    try {
      const response = await API.get(`/api/dialogs/${dialogId}/messages`);
      return response.messages || [];
    } catch (error) {
      console.error('Error fetching messages:', error);
      return [];
    }
  }

  async sendMessage(dialogId: number, text: string): Promise<any> {
    try {
      return await API.post('/api/messages/send', {
        dialog_id: dialogId,
        text
      });
    } catch (error) {
      throw error;
    }
  }
}
