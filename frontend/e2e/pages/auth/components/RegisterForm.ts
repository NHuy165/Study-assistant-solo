import { type Page, type Locator, expect } from '@playwright/test';

export class RegisterForm {
  readonly page: Page;
  readonly formHeader: Locator;
  readonly usernameInput: Locator;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly descriptionInput: Locator;
  readonly registerButton: Locator;
  readonly loginLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.formHeader = page.getByRole('heading', { name: 'Register' });
    this.usernameInput = page.getByRole('textbox', { name: 'Username:' });
    this.emailInput = page.getByRole('textbox', { name: 'Email:' });
    this.passwordInput = page.getByRole('textbox', { name: 'Password:' });
    this.descriptionInput = page.getByRole('textbox', { name: 'Description:' });
    this.registerButton = page
      .locator('div')
      .filter({ hasText: 'Register' })
      .locator('button[type="submit"]');
    this.loginLink = page.getByRole('link', { name: 'Log into an account' });
  }

  fill = async (
    username: string,
    email: string,
    password: string,
    description: string,
  ) => {
    await this.usernameInput.fill(username);
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.descriptionInput.fill(description);
  };

  checkFilled = async (
    username: string,
    email: string,
    password: string,
    description: string,
  ) => {
    await expect(this.usernameInput).toHaveValue(username);
    await expect(this.emailInput).toHaveValue(email);
    await expect(this.passwordInput).toHaveValue(password);
    await expect(this.descriptionInput).toHaveValue(description);
  };

  register = async () => {
    await this.registerButton.click();
  };

  clickLoginLink = async () => {
    await this.loginLink.click();
  };

  checkLoaded = async () => {
    await expect(this.page).toHaveURL('/auth/register');
    await expect(this.formHeader).toBeVisible();
  };
}
