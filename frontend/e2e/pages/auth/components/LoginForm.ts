import { type Page, type Locator, expect } from '@playwright/test';

export class LoginForm {
  readonly page: Page;
  readonly formHeader: Locator;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly registerLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.formHeader = page.getByRole('heading', { name: 'Login' });
    this.emailInput = page.getByRole('textbox', { name: 'Email:' });
    this.passwordInput = page.getByRole('textbox', { name: 'Password:' });
    this.loginButton = page
      .locator('div')
      .filter({ hasText: 'Login' })
      .locator('button[type="submit"]');
    this.registerLink = page.getByRole('link', { name: 'Register an account' });
  }

  fill = async (email: string, password: string) => {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
  };

  checkFilled = async (email: string, password: string) => {
    await expect(this.emailInput).toHaveValue(email);
    await expect(this.passwordInput).toHaveValue(password);
  };

  login = async () => {
    await this.loginButton.click();
  };

  clickRegisterLink = async () => {
    await this.registerLink.click();
  };

  checkLoaded = async () => {
    await expect(this.page).toHaveURL('/auth/login');
    await expect(this.formHeader).toBeVisible();
  };
}
