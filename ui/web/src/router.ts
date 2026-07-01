import { LoginScreen } from './screens/LoginScreen';
import { ChatsScreen } from './screens/ChatsScreen';
import { ChatViewScreen } from './screens/ChatViewScreen';
import { SettingsScreen } from './screens/SettingsScreen';

export class Router {
  private currentScreen: any = null;
  private appDiv: HTMLElement;

  constructor() {
    this.appDiv = document.getElementById('app')!;
  }

  async navigate(route: string, params?: any): Promise<void> {
    console.log(`📍 Навигация на: ${route}`);

    let screen;
    
    switch (route) {
      case 'login':
        screen = new LoginScreen();
        break;
      case 'chats':
        screen = new ChatsScreen();
        break;
      case 'chat':
        screen = new ChatViewScreen(params?.dialogId);
        break;
      case 'settings':
        screen = new SettingsScreen();
        break;
      default:
        screen = new LoginScreen();
    }

    this.appDiv.innerHTML = '';
    this.currentScreen = screen;
    await screen.render(this.appDiv);
  }
}
