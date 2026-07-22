import { expect, type Locator } from '@playwright/test';

export class UserProfileSection {
  readonly rootLocator: Locator;

  // User info
  readonly userIdInfo: Locator;
  readonly createdAtInfo: Locator;
  readonly currentLoginStreakInfo: Locator;
  readonly longestLoginStreakInfo: Locator;

  readonly usernameInfo: Locator;
  readonly usernameUpdateForm: Locator;

  readonly emailInfo: Locator;
  readonly emailUpdateForm: Locator;

  readonly descriptionInfo: Locator;
  readonly descriptionUpdateForm: Locator;

  readonly passwordUpdateShowButton: Locator;
  readonly passwordUpdateForm: Locator;

  // Log out
  readonly logOutButton: Locator;

  constructor(rootLocator: Locator) {
    this.rootLocator = rootLocator;

    // User info

    // User ID
    this.userIdInfo = rootLocator
      .locator('div')
      .filter({ hasText: 'User ID' })
      .last();

    // Created at
    this.createdAtInfo = rootLocator
      .locator('div')
      .filter({ hasText: 'Account creation time' })
      .last();

    // Current login streak
    this.currentLoginStreakInfo = rootLocator
      .locator('div')
      .filter({ hasText: 'Current login streak' })
      .last();

    // Longest login streak
    this.longestLoginStreakInfo = rootLocator
      .locator('div')
      .filter({ hasText: 'Longest login streak' })
      .last();

    // Username
    this.usernameInfo = rootLocator
      .locator('div')
      .filter({ hasText: 'Username' })
      .last();

    this.usernameUpdateForm = rootLocator
      .locator('form')
      .filter({ hasText: 'New username' })
      .last();

    // Email
    this.emailInfo = rootLocator
      .locator('div')
      .filter({ hasText: 'Email' })
      .last();
    this.emailUpdateForm = rootLocator
      .locator('form')
      .filter({ hasText: 'New email' });

    // Description
    this.descriptionInfo = rootLocator
      .locator('div')
      .filter({ hasText: 'Description' })
      .last();
    this.descriptionUpdateForm = rootLocator
      .locator('form')
      .filter({ hasText: 'New description' });

    // Password
    this.passwordUpdateShowButton = rootLocator.getByRole('button', {
      name: 'Change password',
    });
    this.passwordUpdateForm = rootLocator
      .locator('form')
      .filter({ hasText: 'Old password' })
      .filter({ hasText: 'New password' });

    // Log out button
    this.logOutButton = rootLocator.getByRole('button', { name: 'Log out' });
  }

  checkLoaded = async () => {
    await expect(this.rootLocator).toBeVisible();

    // User info
    await expect(this.userIdInfo).toBeVisible();
    await expect(this.createdAtInfo).toBeVisible();
    await expect(this.currentLoginStreakInfo).toBeVisible();
    await expect(this.longestLoginStreakInfo).toBeVisible();
    await expect(this.usernameInfo).toBeVisible();
    await expect(this.emailInfo).toBeVisible();
    await expect(this.descriptionInfo).toBeVisible();

    await expect(this.passwordUpdateShowButton).toBeVisible();
    await expect(this.logOutButton).toBeVisible();
  };
}
