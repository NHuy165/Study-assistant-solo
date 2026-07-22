import test, { expect } from '@playwright/test';
import { HomePage } from '@e2e/pages/home/HomePage';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import { InteractionPage } from '@e2e/pages/interaction/InteractionPage';

test.describe('Interactions - Success tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    const user = userData.user;

    await registerUser({ request, user });
    await loginUser({ user, page });
  });

  test('Create an interaction and view its details.', async ({ page }) => {
    const interactionSection = new HomePage(page).interactionsSection;

    // Creates the interaction
    await interactionSection.fillCreationInputs({
      name: 'test-interaction-1',
      description: 'test-description-1',
    });
    await interactionSection.creationButton.click();

    await expect(interactionSection.interactionItem).toContainText(
      'test-interaction-1',
    );

    // Click show details button
    const detailsButton = await interactionSection.interactionItem.getByRole(
      'button',
      {
        name: 'Details',
      },
    );
    await detailsButton.click();

    const detailsPanel = interactionSection.interactionItem
      .locator('section')
      .filter({ hasText: 'Details' });
    const createdAtInfo = detailsPanel
      .locator('p')
      .filter({ hasText: 'Created at' });
    const descriptionInfo = detailsPanel
      .locator('p')
      .filter({ hasText: 'Description' });

    await expect(detailsPanel).toBeVisible();
    await expect(createdAtInfo).toBeVisible();
    await expect(descriptionInfo).toBeVisible();

    // Click show details button again
    await detailsButton.click();
    await expect(detailsPanel).not.toBeVisible();
  });

  test('Go inside an interaction page', async ({ page, request }) => {
    const interaction = interactionData.interaction;

    const interactionId = await createInteraction({
      page,
      request,
      interaction,
    });
    await page.reload();

    const interactionSection = new HomePage(page).interactionsSection;

    await interactionSection.interactionItem
      .getByRole('button', {
        name: `#${interactionId} ${interaction.name}`,
      })
      .click();

    const interactionPage = new InteractionPage(page);
    await interactionPage.checkLoaded(interactionId);
  });

  test('Update an interaction', async ({ page, request }) => {
    const interaction = interactionData.interaction;

    await createInteraction({ page, request, interaction });
    await page.reload();

    const interactionSection = new HomePage(page).interactionsSection;

    await interactionSection.interactionItem
      .getByRole('button', {
        name: 'Update',
      })
      .click();

    // Verifies display
    const updatePanel = interactionSection.interactionItem
      .locator('form')
      .filter({ hasText: 'Update' });
    const nameUpdateField = updatePanel.getByRole('textbox', {
      name: 'New name',
    });
    const descriptionUpdateField = updatePanel.getByRole('textbox', {
      name: 'New description',
    });

    await expect(updatePanel).toBeVisible();
    await expect(nameUpdateField).toHaveValue(interaction.name);
    await expect(descriptionUpdateField).toHaveValue(interaction.description);

    // Updates
    const newName = 'Updated name';
    await nameUpdateField.clear();
    await nameUpdateField.fill(newName);

    const newDescription = 'Updated description';
    await descriptionUpdateField.clear();
    await descriptionUpdateField.fill(newDescription);

    await updatePanel.getByRole('button', { name: 'Update' }).click();

    // Verifies result
    expect(updatePanel).not.toBeVisible();
    expect(interactionSection.interactionItem).toContainText(newName);

    await interactionSection.interactionItem
      .getByRole('button', {
        name: 'Details',
      })
      .click();

    const descriptionInfo = interactionSection.interactionItem
      .locator('section')
      .filter({ hasText: 'Details' })
      .locator('p')
      .filter({ hasText: 'Description' });
    await expect(descriptionInfo).toContainText(newDescription);
  });

  test('Delete an interaction', async ({ page, request }) => {
    const interaction = interactionData.interaction;

    await createInteraction({ page, request, interaction });
    await page.reload();

    const interactionSection = new HomePage(page).interactionsSection;

    // Clicks delete button
    await interactionSection.interactionItem
      .getByRole('button', {
        name: 'Delete',
      })
      .click();

    // Verifies result
    await expect(interactionSection.interactionItem).not.toBeVisible();
    await expect(interactionSection.infoNoItem).toBeVisible();
  });
});
