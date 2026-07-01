import { API } from '../api';

export class AuthManager {
  async checkAuth(): Promise<boolean> {
    try {
      const user = await API.get('/api/auth/me');
      return !!user;
    } catch (error) {
      return false;
    }
  }

  async login(phoneNumber: string, code: string, password?: string): Promise<any> {
    try {
      const response = await API.post('/api/auth/sign_in', {
        code,
        password: password || null
      });
      return response;
    } catch (error) {
      throw error;
    }
  }

  async logout(): Promise<void> {
    await API.post('/api/auth/logout', {});
  }
}
