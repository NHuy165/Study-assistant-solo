import { type Page, type Locator, expect } from '@playwright/test';

export class RegisterForm {
  readonly page: Page;
  readonly formHeader: Locator;

  // Form elements
  readonly usernameInput: Locator;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly descriptionInput: Locator;
  readonly registerButton: Locator;

  // Link
  readonly loginLink: Locator;

  // Errors
  readonly usernameError: Locator;
  readonly emailError: Locator;
  readonly passwordError: Locator;

  constructor(page: Page) {
    this.page = page;
    this.formHeader = page.getByRole('heading', { name: 'Register' });

    // Form elements
    this.usernameInput = page.getByRole('textbox', { name: 'Username:' });
    this.emailInput = page.getByRole('textbox', { name: 'Email:' });
    this.passwordInput = page.getByRole('textbox', { name: 'Password:' });
    this.descriptionInput = page.getByRole('textbox', { name: 'Description:' });
    this.registerButton = page.getByRole('button', { name: 'Register' });

    // Link
    this.loginLink = page.getByRole('link', { name: 'Log into an account' });

    // Errors
    this.usernameError = page
      .locator('label')
      .filter({ hasText: 'Username:' })
      .getByRole('alert');
    this.emailError = page
      .locator('label')
      .filter({ hasText: 'Email:' })
      .getByRole('alert');
    this.passwordError = page
      .locator('label')
      .filter({ hasText: 'Password:' })
      .getByRole('alert');
  }

  checkLoaded = async () => {
    await expect(this.page).toHaveURL('/auth/register');
    await expect(this.formHeader).toBeVisible();

    await expect(this.usernameInput).toBeVisible();
    await expect(this.emailInput).toBeVisible();
    await expect(this.passwordInput).toBeVisible();
    await expect(this.descriptionInput).toBeVisible();
    await expect(this.registerButton).toBeVisible();
    await expect(this.loginLink).toBeVisible();
  };

  fillInputs = async ({
    username,
    email,
    password,
    description,
  }: {
    username: string;
    email: string;
    password: string;
    description: string;
  }) => {
    await this.usernameInput.fill(username);
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.descriptionInput.fill(description);
  };

  checkFilledContents = async ({
    username,
    email,
    password,
    description,
  }: {
    username: string;
    email: string;
    password: string;
    description: string;
  }) => {
    await expect(this.usernameInput).toHaveValue(username);
    await expect(this.emailInput).toHaveValue(email);
    await expect(this.passwordInput).toHaveValue(password);
    await expect(this.descriptionInput).toHaveValue(description);
  };
}
