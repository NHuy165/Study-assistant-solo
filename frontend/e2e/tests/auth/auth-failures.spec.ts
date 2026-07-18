import { test, expect } from '@playwright/test';
import { resetDatabase } from '@e2e/helpers/database';
import { AuthPage } from '@e2e/pages/auth/AuthPage';
import data from '@e2e/data/user.json' with { type: 'json' };
import { registerUser } from '@e2e/helpers/auth/register-user';

test.describe('Authentication - Failure tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    const user = data.user;
    await registerUser({ request, user });

    const authPage = new AuthPage(page);
    await authPage.goto();
  });

  test('Register with empty inputs.', async ({ page }) => {
    const authPage = new AuthPage(page);

    await authPage.loginForm.registerLink.click();
    await authPage.registerForm.emailInput.fill('dummy');
    await authPage.registerForm.registerButton.click();

    await expect(authPage.registerForm.usernameError).toContainText(
      'Too small:',
    );
    await expect(authPage.registerForm.emailError).toHaveText(
      'Invalid email address',
    );
    await expect(authPage.registerForm.passwordError).toContainText(
      'Too small:',
    );
  });

  test('Register using existing email.', async ({ page }) => {
    const authPage = new AuthPage(page);
    await authPage.loginForm.registerLink.click();

    const user = data.user;

    await authPage.registerForm.fillInputs({
      username: 'different username',
      email: user.email,
      password: 'different password',
      description: 'different description',
    });
    await authPage.registerForm.registerButton.click();

    await expect(authPage.toastError).toHaveText(
      'Another user with this email already exists.',
    );
  });

  test('Log in with empty inputs.', async ({ page }) => {
    const authPage = new AuthPage(page);

    await authPage.loginForm.loginButton.click();

    await expect(authPage.loginForm.emailError).toHaveText(
      'Invalid email address',
    );
    await expect(authPage.loginForm.passwordError).toContainText('Too small:');
  });

  test('Log in with wrong email', async ({ page }) => {
    const authPage = new AuthPage(page);

    const user = data.user;

    await authPage.loginForm.fillInputs({
      email: 'wrong-email@gmail.com',
      password: user.password,
    });
    await authPage.loginForm.loginButton.click();

    await expect(authPage.toastError).toHaveText('Invalid credentials.');
  });

  test('Log in with wrong password', async ({ page }) => {
    const authPage = new AuthPage(page);

    const user = data.user;

    await authPage.loginForm.fillInputs({
      email: user.email,
      password: 'Wrong password',
    });
    await authPage.loginForm.loginButton.click();

    await expect(authPage.toastError).toHaveText('Invalid credentials.');
  });
});
