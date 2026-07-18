import { expect, type Locator } from '@playwright/test';

export class UserProfileSection {
  readonly rootLocator: Locator;

  constructor(rootLocator: Locator) {
    this.rootLocator = rootLocator;
  }

  checkLoaded = async () => {
    await expect(this.rootLocator).toBeVisible();
  };
}
