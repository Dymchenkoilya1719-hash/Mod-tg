import { Router } from './router';
import { AuthManager } from './services/auth';
import { ChatsManager } from './services/chats';

export class App {
  private router: Router;
  private authManager: AuthManager;
  private chatsManager: ChatsManager;

  constructor() {
    this.router = new Router();
    this.authManager = new AuthManager();
    this.chatsManager = new ChatsManager();
  }

  async init(): Promise<void> {
    console.log('🚀 TG Mod инициализируется...');
    
    const appDiv = document.getElementById('app');
    if (!appDiv) {
      console.error('App div not found');
      return;
    }

    // Проверить авторизацию
    const isAuthenticated = await this.authManager.checkAuth();
    
    if (isAuthenticated) {
      console.log('✅ Пользователь авторизован');
      await this.router.navigate('chats');
    } else {
      console.log('🔓 Требуется авторизация');
      await this.router.navigate('login');
    }
  }
}
