import { type Page, type Locator, expect } from '@playwright/test';

export class LoginForm {
  readonly page: Page;
  readonly formHeader: Locator;

  // Form elements
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;

  // Link
  readonly registerLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.formHeader = page.getByRole('heading', { name: 'Login' });

    // Form elements
    this.emailInput = page.getByRole('textbox', { name: 'Email:' });
    this.passwordInput = page.getByRole('textbox', { name: 'Password:' });
    this.loginButton = page
      .locator('div')
      .filter({ hasText: 'Login' })
      .locator('button[type="submit"]');

    // Link
    this.registerLink = page.getByRole('link', { name: 'Register an account' });
  }

  checkLoaded = async () => {
    await expect(this.page).toHaveURL('/auth/login');
    await expect(this.formHeader).toBeVisible();
  };

  fillInputs = async (email: string, password: string) => {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
  };

  checkFilledContents = async (email: string, password: string) => {
    await expect(this.emailInput).toHaveValue(email);
    await expect(this.passwordInput).toHaveValue(password);
  };
}
