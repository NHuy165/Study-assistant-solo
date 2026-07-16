import { test, expect } from '@playwright/test';
import { resetDatabase } from '@e2e/helpers/database';
import { AuthPage } from '@e2e/pages/auth/AuthPage';
import data from '@e2e/data/user.json' with { type: 'json' };
import { HomePage } from '@e2e/pages/home/HomePage';

test.describe('Authentication - Success tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    const authPage = new AuthPage(page);
    await authPage.goto();
  });

  test('Go to authentication page', async ({ page }) => {
    const authPage = new AuthPage(page);

    // Default destination is login form
    await expect(authPage.pageHeader).toBeVisible();
    await authPage.loginForm.checkLoaded();
  });

  test('Switch between registration and login and checking the password field to be censored', async ({
    page,
  }) => {
    const authPage = new AuthPage(page);

    await authPage.loginForm.registerLink.click();
    await authPage.registerForm.checkLoaded();
    await expect(authPage.registerForm.passwordInput).toHaveAttribute(
      'type',
      'password',
    );

    await authPage.registerForm.loginLink.click();
    await authPage.loginForm.checkLoaded();
    await expect(authPage.loginForm.passwordInput).toHaveAttribute(
      'type',
      'password',
    );
  });

  test('Register and login', async ({ page }) => {
    const authPage = new AuthPage(page);
    await authPage.loginForm.registerLink.click();

    const user = data.user;

    // Fills in the registration form
    await authPage.registerForm.fill(
      user.username,
      user.email,
      user.password,
      user.description,
    );

    await authPage.registerForm.checkFilled(
      user.username,
      user.email,
      user.password,
      user.description,
    );

    // Registers
    await authPage.registerForm.register();
    await authPage.loginForm.checkLoaded();

    // Fills in the login form
    await authPage.loginForm.fill(user.email, user.password);

    await authPage.loginForm.checkFilled(user.email, user.password);

    // Logs in
    await authPage.loginForm.login();
    const homePage = new HomePage(page);
    await homePage.checkLoaded();
  });
});
