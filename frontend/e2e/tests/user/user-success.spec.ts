import { registerUser } from '@e2e/helpers/auth/register-user';
import { expect, test } from '@playwright/test';
import data from '@e2e/data/user.json' with { type: 'json' };
import { loginUser } from '@e2e/helpers/auth/login-user';
import { resetDatabase } from '@e2e/helpers/database';
import { HomePage } from '@e2e/pages/home/HomePage';
import { AuthPage } from '@e2e/pages/auth/AuthPage';

test.describe('User - Success tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    const user = data.user;

    await registerUser({ request, user });
    await loginUser({ user, page });
  });

  test('Check if all fields are properly loaded', async ({ page }) => {
    const userProfileSection = new HomePage(page).userProfileSection;
    const user = data.user;

    // User ID
    await expect(userProfileSection.userIdInfo).toBeVisible();
    await expect(userProfileSection.userIdInfo).toContainText('1');

    // Created at
    await expect(userProfileSection.createdAtInfo).toBeVisible();
    await expect(userProfileSection.createdAtInfo).not.toContainText(
      'Fetching data...',
    );

    // Current login streak
    await expect(userProfileSection.currentLoginStreakInfo).toBeVisible();
    await expect(userProfileSection.currentLoginStreakInfo).toContainText('1');

    // Longest login streak
    await expect(userProfileSection.longestLoginStreakInfo).toBeVisible();
    await expect(userProfileSection.longestLoginStreakInfo).toContainText('1');

    // Username
    await expect(userProfileSection.usernameInfo).toBeVisible();
    await expect(userProfileSection.usernameInfo).toContainText(user.username);

    // Email
    await expect(userProfileSection.emailInfo).toBeVisible();
    await expect(userProfileSection.emailInfo).toContainText(user.email);

    // Description
    await expect(userProfileSection.descriptionInfo).toBeVisible();
    await expect(userProfileSection.descriptionInfo).toContainText(
      user.description,
    );
  });

  test('Update username', async ({ page }) => {
    const user = data.user;

    const userProfileSection = new HomePage(page).userProfileSection;

    // Opens form
    await userProfileSection.usernameInfo
      .getByRole('button', { name: 'Update' })
      .click();

    // Checks displayed information
    await expect(userProfileSection.usernameUpdateForm).toBeVisible();
    const usernameUpdateField = userProfileSection.usernameUpdateForm.getByRole(
      'textbox',
      { name: 'New username' },
    );
    await expect(usernameUpdateField).toHaveValue(user.username);

    // Updates
    const newUsername = 'Updated username';
    await usernameUpdateField.clear();
    await usernameUpdateField.fill(newUsername);
    await userProfileSection.usernameUpdateForm
      .getByRole('button', { name: 'Confirm' })
      .click();

    await expect(userProfileSection.usernameUpdateForm).not.toBeVisible();
    await expect(userProfileSection.usernameInfo).toContainText(newUsername);
  });

  test('Update email', async ({ page }) => {
    const user = data.user;

    const userProfileSection = new HomePage(page).userProfileSection;

    // Opens form
    await userProfileSection.emailInfo
      .getByRole('button', { name: 'Update' })
      .click();

    // Checks displayed information
    await expect(userProfileSection.emailUpdateForm).toBeVisible();
    const emailUpdateField = userProfileSection.emailUpdateForm.getByRole(
      'textbox',
      { name: 'New email' },
    );
    await expect(emailUpdateField).toHaveValue(user.email);

    // Updates
    const newEmail = 'updated@gmail.com';
    await emailUpdateField.clear();
    await emailUpdateField.fill(newEmail);
    await userProfileSection.emailUpdateForm
      .getByRole('button', { name: 'Confirm' })
      .click();

    await expect(userProfileSection.emailUpdateForm).not.toBeVisible();
    await expect(userProfileSection.emailInfo).toContainText(newEmail);
  });

  test('Update description to a new non-blank description and then to a blank description', async ({
    page,
  }) => {
    const user = data.user;

    const userProfileSection = new HomePage(page).userProfileSection;

    // Opens form
    await userProfileSection.descriptionInfo
      .getByRole('button', { name: 'Update' })
      .click();

    // Checks displayed information
    await expect(userProfileSection.descriptionUpdateForm).toBeVisible();
    const descriptionUpdateField =
      userProfileSection.descriptionUpdateForm.getByRole('textbox', {
        name: 'New description',
      });
    await expect(descriptionUpdateField).toHaveValue(user.description);

    // Updates to a non-blank description
    const newDescription = 'Updated description';
    await descriptionUpdateField.clear();
    await descriptionUpdateField.fill(newDescription);
    await userProfileSection.descriptionUpdateForm
      .getByRole('button', { name: 'Confirm' })
      .click();

    await expect(userProfileSection.descriptionUpdateForm).not.toBeVisible();
    await expect(userProfileSection.descriptionInfo).toContainText(
      newDescription,
    );

    // Updates to a blank description
    await userProfileSection.descriptionInfo
      .getByRole('button', { name: 'Update' })
      .click();
    await descriptionUpdateField.clear();
    await userProfileSection.descriptionUpdateForm
      .getByRole('button', { name: 'Confirm' })
      .click();

    await expect(userProfileSection.descriptionInfo).toContainText(
      'No content',
    );
  });

  test('Update password', async ({ page }) => {
    const user = data.user;

    const homePage = new HomePage(page);

    // Opens form
    await homePage.userProfileSection.passwordUpdateShowButton.click();

    // Checks displayed information
    await expect(homePage.userProfileSection.passwordUpdateForm).toBeVisible();
    const oldPasswordField =
      homePage.userProfileSection.passwordUpdateForm.getByRole('textbox', {
        name: 'Old password',
      });
    const newPasswordField =
      homePage.userProfileSection.passwordUpdateForm.getByRole('textbox', {
        name: 'New password',
      });
    await expect(oldPasswordField).toHaveAttribute('type', 'password');
    await expect(newPasswordField).toHaveAttribute('type', 'password');

    // Updates
    const newPassword = 'Updated password';
    await oldPasswordField.fill(user.password);
    await newPasswordField.fill(newPassword);
    await homePage.userProfileSection.passwordUpdateForm
      .getByRole('button', { name: 'Confirm' })
      .click();

    await expect(
      homePage.userProfileSection.passwordUpdateForm,
    ).not.toBeVisible();

    // Logs out and logs back in to ensure the password really is changed
    await homePage.userProfileSection.logOutButton.click();
    const authPage = new AuthPage(page);
    await authPage.loginForm.fillInputs({ ...user, password: newPassword });
    await authPage.loginForm.loginButton.click();
    await homePage.checkLoaded();
  });
});
