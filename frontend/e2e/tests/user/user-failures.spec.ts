import { registerUser } from '@e2e/helpers/auth/register-user';
import { resetDatabase } from '@e2e/helpers/database';
import test, { expect } from '@playwright/test';
import data from '@e2e/data/user.json' with { type: 'json' };
import { loginUser } from '@e2e/helpers/auth/login-user';
import { HomePage } from '@e2e/pages/home/HomePage';

test.describe('User - Failure tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    const user = data.user;

    await registerUser({ request, user });
    await loginUser({ user, page });
  });

  test('Update username using an empty string', async ({ page }) => {
    const userProfileSection = new HomePage(page).userProfileSection;

    const error = userProfileSection.usernameUpdateForm.getByRole('alert');

    await userProfileSection.usernameInfo
      .getByRole('button', {
        name: 'Update',
      })
      .click();
    await userProfileSection.usernameUpdateForm
      .getByRole('textbox', {
        name: 'New username',
      })
      .clear();
    await userProfileSection.usernameUpdateForm
      .getByRole('button', { name: 'Confirm' })
      .click();

    await expect(error).toBeVisible();
    await expect(error).toContainText('Too small:');
  });

  test('Update email using an empty string and an incorrectly formatted email', async ({
    page,
  }) => {
    const userProfileSection = new HomePage(page).userProfileSection;

    const error = userProfileSection.emailUpdateForm.getByRole('alert');

    await userProfileSection.emailInfo
      .getByRole('button', {
        name: 'Update',
      })
      .click();

    // Updates using empty email
    await userProfileSection.emailUpdateForm
      .getByRole('textbox', {
        name: 'New email',
      })
      .clear();
    await userProfileSection.emailUpdateForm
      .getByRole('button', { name: 'Confirm' })
      .click();

    await expect(error).toBeVisible();
    await expect(error).toHaveText('Invalid email address');

    // Updates using invalid email
    await userProfileSection.emailUpdateForm
      .getByRole('textbox', {
        name: 'New email',
      })
      .fill('invalidEmail');
    await userProfileSection.emailUpdateForm
      .getByRole('button', { name: 'Confirm' })
      .click();

    await expect(error).toBeVisible();
    await expect(error).toHaveText('Invalid email address');
  });

  test('Update password using empty inputs and a wrong password', async ({
    page,
  }) => {
    const homePage = new HomePage(page);

    const errorOldPassword = homePage.userProfileSection.passwordUpdateForm
      .locator('label')
      .filter({ hasText: 'Old password' })
      .getByRole('alert');
    const errorNewPassword = homePage.userProfileSection.passwordUpdateForm
      .locator('label')
      .filter({ hasText: 'New password' })
      .getByRole('alert');

    await homePage.userProfileSection.passwordUpdateShowButton.click();

    // Updates using empty inputs
    await homePage.userProfileSection.passwordUpdateForm
      .getByRole('button', { name: 'Confirm' })
      .click();

    await expect(errorOldPassword).toBeVisible();
    await expect(errorOldPassword).toContainText('Too small:');

    await expect(errorNewPassword).toBeVisible();
    await expect(errorNewPassword).toContainText('Too small:');

    // Updates using wrong password
    await homePage.userProfileSection.passwordUpdateForm
      .getByRole('textbox', {
        name: 'Old password',
      })
      .fill('Wrong password');

    await homePage.userProfileSection.passwordUpdateForm
      .getByRole('textbox', {
        name: 'New password',
      })
      .fill('Updated password');

    await homePage.userProfileSection.passwordUpdateForm
      .getByRole('button', { name: 'Confirm' })
      .click();

    await expect(homePage.toastError).toBeVisible();
    await expect(homePage.toastError).toHaveText('Wrong password entered.');
  });
});
