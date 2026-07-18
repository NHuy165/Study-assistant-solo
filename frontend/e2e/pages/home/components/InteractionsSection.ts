import { expect, type Locator } from '@playwright/test';

export class InteractionsSection {
  readonly rootLocator: Locator;

  constructor(rootLocator: Locator) {
    this.rootLocator = rootLocator;
  }

  checkLoaded = async () => {
    await expect(this.rootLocator).toBeVisible();
  };
}
