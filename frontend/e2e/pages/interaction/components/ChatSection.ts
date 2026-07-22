import { expect, type Locator } from '@playwright/test';

export class ChatSection {
  readonly rootLocator: Locator;

  // Chat window
  readonly chatWindow: Locator;
  readonly infoNoChat: Locator;
  readonly chatConversation: Locator;

  // Chat form

  readonly chatButton: Locator;
  readonly chatInput: Locator;

  constructor(rootLocator: Locator) {
    this.rootLocator = rootLocator;

    // Chat window
    this.chatWindow = rootLocator.locator('section');
    this.infoNoChat = this.chatWindow.getByText('No chat history to show.');
    this.chatConversation = this.chatWindow.getByRole('listitem');

    // Chat form
    this.chatButton = rootLocator.getByRole('button', { name: 'Send' });
    this.chatInput = rootLocator.locator('textarea[name="prompt"]');
  }

  checkLoaded = async () => {
    await expect(this.rootLocator).toBeVisible();

    await expect(this.chatButton).toBeVisible();
    await expect(this.chatInput).toBeVisible();
    await expect(this.chatWindow).toBeVisible();
    await expect(this.infoNoChat).toBeVisible();
  };
}
