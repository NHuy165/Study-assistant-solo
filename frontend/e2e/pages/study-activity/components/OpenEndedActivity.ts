import { expect, type Locator } from '@playwright/test';

export class OpenEndedActivity {
  readonly rootLocator: Locator;

  readonly exerciseItem: Locator;
  readonly submitButton: Locator;

  constructor(rootLocator: Locator) {
    this.rootLocator = rootLocator;

    this.exerciseItem = rootLocator.getByRole('listitem');
    this.submitButton = rootLocator.getByRole('button'); // This button will change text
  }

  checkLoaded = async (numberItems: number) => {
    await expect(this.rootLocator).toBeVisible();

    await expect(this.exerciseItem).toHaveCount(numberItems);
    await expect(this.submitButton).toBeVisible();
  };
}
