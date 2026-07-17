import { LoginForm } from '@e2e/pages/auth/components/LoginForm';
import { RegisterForm } from '@e2e/pages/auth/components/RegisterForm';
import { type Page, type Locator } from '@playwright/test';

export class AuthPage {
  readonly page: Page;
  readonly pageHeader: Locator;

  // Components
  readonly loginForm: LoginForm;
  readonly registerForm: RegisterForm;

  // Errors
  readonly toastError: Locator;

  constructor(page: Page) {
    this.page = page;
    this.pageHeader = page.getByRole('heading', { name: 'AUTHENTICATION' });

    // Components
    this.loginForm = new LoginForm(page);
    this.registerForm = new RegisterForm(page);

    // Errors
    this.toastError = page.getByRole('status').last();
  }

  goto = async () => {
    await this.page.goto('/auth');
  };
}
