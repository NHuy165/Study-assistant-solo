import { type Page, type Locator, expect } from '@playwright/test';

export class HomePage {
  readonly page: Page;
  readonly pageHeader: Locator;

  constructor(page: Page) {
    this.page = page;
    this.pageHeader = page.getByRole('heading', { name: 'HOME PAGE' });
  }

  goto = async () => {
    await this.page.goto('/home');
  };

  checkLoaded = async () => {
    await expect(this.page).toHaveURL('/home');
    await expect(this.pageHeader).toBeVisible();
  };
}
