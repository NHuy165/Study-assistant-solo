import { test, expect } from '@playwright/test';
import { resetDatabase } from '@e2e/helpers/database';
import { AuthPage } from '@e2e/pages/auth/AuthPage';
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
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

  test('Switch between the registration and login forms and check if the password field has the correct type', async ({
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

  test('Register, login and logout', async ({ page }) => {
    const authPage = new AuthPage(page);
    await authPage.loginForm.registerLink.click();

    const user = userData.user;

    // Fills in the registration form
    await authPage.registerForm.fillInputs({ ...user });

    await authPage.registerForm.checkFilledContents({ ...user });

    // Registers
    await authPage.registerForm.registerButton.click();
    await authPage.loginForm.checkLoaded();

    // Fills in the login form
    await authPage.loginForm.fillInputs({ ...user });

    await authPage.loginForm.checkFilledContents({ ...user });

    // Logs in
    await authPage.loginForm.loginButton.click();
    const homePage = new HomePage(page);
    await homePage.checkLoaded();

    // Logs out
    await homePage.userProfileSection.logOutButton.click();
    await authPage.loginForm.checkLoaded();
  });
});
