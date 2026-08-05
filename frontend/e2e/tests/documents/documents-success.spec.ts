import test, { expect } from '@playwright/test';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import { InteractionPage } from '@e2e/pages/interaction/InteractionPage';
import path from 'path';

test.describe('Documents - Success tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    // Registers and logs in
    const user = userData.user;

    await registerUser({ request, user });
    await loginUser({ user, page });

    // Creates and goes inside interaction
    const interaction = interactionData.interaction;

    const interactionId = await createInteraction({
      page,
      request,
      interaction,
    });
    await page.reload();

    const interactionPage = new InteractionPage(page);
    await interactionPage.goto(interactionId);

    await page.route(`/api/document/${interactionId}*`, async (route) => {
      if (route.request().method() !== 'POST') {
        await route.continue();
        return;
      }

      const requestUrl = new URL(route.request().url());

      // Route redirect
      await route.continue({
        url: `${process.env.BASE_URL}/api/dev/document/${interactionId}${requestUrl.search}`,
      });
    });
  });

  test('Upload a document, autofilling its subject and leaving everything as default.', async ({
    page,
  }) => {
    const documentSection = new InteractionPage(page).documentsSection;

    const filepath = path.join(
      import.meta.dirname,
      '../../data/document/test-file.txt',
    );

    // Fills inputs
    await documentSection.fillCreationInputs({
      filepath,
      automaticSubject: 'Yes',
    });

    // Checks that toggling on subject overwrite has disabled the subject field
    await expect(documentSection.creationSubjectTypeInput).not.toBeVisible();

    // Submits
    await documentSection.creationButton.click();

    await expect(documentSection.documentItem).toBeVisible();
    await expect(documentSection.documentItem).toContainText(
      'test-file.txt (Maths)',
    );
  });

  test('Upload a document, specifying its subject and name.', async ({
    page,
  }) => {
    const documentSection = new InteractionPage(page).documentsSection;

    const filepath = path.join(
      import.meta.dirname,
      '../../data/document/test-file.txt',
    );

    // Fills inputs
    const newName = 'newName';
    const newSubject = 'Literature';

    await documentSection.fillCreationInputs({
      filepath,
      name: newName,
      subjectType: newSubject,
      automaticSubject: 'No',
    });

    // Submits
    await documentSection.creationButton.click();

    await expect(documentSection.documentItem).toBeVisible();
    await expect(documentSection.documentItem).toContainText(
      `${newName} (${newSubject})`,
    );
  });

  test.describe('Tests on an uploaded document', () => {
    test.beforeEach(async ({ page }) => {
      const documentSection = new InteractionPage(page).documentsSection;

      const filepath = path.join(
        import.meta.dirname,
        '../../data/document/test-file.txt',
      );

      // Fills inputs
      const newName = 'newName';
      const newSubject = 'Literature';

      await documentSection.fillCreationInputs({
        filepath,
        name: newName,
        subjectType: newSubject,
        automaticSubject: 'No',
      });

      // Submits
      await documentSection.creationButton.click();
    });

    test("View a document's details.", async ({ page }) => {
      const documentSection = new InteractionPage(page).documentsSection;

      await documentSection.documentItem
        .getByRole('button', {
          name: 'newName (Literature)',
        })
        .click();

      const detailsPanel = documentSection.documentItem
        .locator('section')
        .filter({ hasText: 'Details' });
      const uploadedAtInfo = detailsPanel
        .locator('p')
        .filter({ hasText: 'Uploaded at' });
      const typeInfo = detailsPanel
        .locator('p')
        .filter({ hasText: 'Document type' });
      const summaryInfo = detailsPanel
        .locator('p')
        .filter({ hasText: 'Document summary' });
      const recommendationsInfo = detailsPanel
        .locator('p')
        .filter({ hasText: 'Recommendations' });
      const activityRecommendations = recommendationsInfo
        .locator('section')
        .filter({ hasText: 'Create study activities' });
      const chatRecommendations = recommendationsInfo
        .locator('section')
        .filter({ hasText: 'Chat with LLM' });
      const showUpdateButton = detailsPanel.getByRole('button', {
        name: 'Show update',
      });

      await expect(detailsPanel).toBeVisible();

      await expect(uploadedAtInfo).toBeVisible();

      await expect(typeInfo).toBeVisible();
      await expect(typeInfo).toContainText('TEXT');

      await expect(summaryInfo).toBeVisible();
      await expect(summaryInfo).toContainText('Summary of newName');

      await expect(recommendationsInfo).toBeVisible();

      await expect(activityRecommendations).toBeVisible();
      await expect(chatRecommendations).toBeVisible();

      await expect(showUpdateButton).toBeVisible();
    });

    test('Create a study activity using a recommendation', async ({ page }) => {
      const documentSection = new InteractionPage(page).documentsSection;

      await documentSection.documentItem
        .getByRole('button', {
          name: 'newName (Literature)',
        })
        .click();

      const detailsPanel = documentSection.documentItem
        .locator('section')
        .filter({ hasText: 'Details' });
      const recommendationsInfo = detailsPanel
        .locator('p')
        .filter({ hasText: 'Recommendations' });
      const activityRecommendations = recommendationsInfo
        .locator('section')
        .filter({ hasText: 'Create study activities' });
      const activityRecommendation = activityRecommendations
        .getByRole('listitem')
        .first();

      // Verifies display
      const generateButton = activityRecommendation.getByRole('button', {
        name: 'Generate activity',
      });
      const recommendationInfo = activityRecommendation.locator('div');
      const recommendationPrompt = recommendationInfo
        .locator('p')
        .filter({ hasText: 'Prompt' });
      const recommendationSubject = recommendationInfo
        .locator('p')
        .filter({ hasText: 'Subject type' });
      const recommendationActivityFormat = recommendationInfo
        .locator('p')
        .filter({ hasText: 'Study activity format' });

      await expect(generateButton).toBeVisible();
      await expect(recommendationInfo).toBeVisible();

      await expect(recommendationPrompt).toBeVisible();
      await expect(recommendationPrompt).toContainText(
        'Study activity prompt of document newName',
      );

      await expect(recommendationSubject).toBeVisible();
      await expect(recommendationSubject).toContainText('Literature');

      await expect(recommendationActivityFormat).toBeVisible();
      await expect(recommendationActivityFormat).toContainText(
        'Multiple choice questions',
      );

      // Mocks create study activity endpoint
      const interactionId = Number(page.url().split('/').pop());
      const activityName = 'test-name';
      const activityDescription = 'test-description';

      await page.route(
        `**/api/study-activity/${interactionId}`,
        async (route) => {
          if (route.request().method() !== 'POST') {
            await route.continue();
            return;
          }

          const originalBody = route.request().postDataJSON();
          const updatedBody = {
            ...originalBody,
            name: activityName,
            description: activityDescription,
            n_items: 2,
          };

          await route.continue({
            url: `**/api/dev/study-activity/${interactionId}`,
            postData: JSON.stringify(updatedBody),
          });
        },
      );

      // Creates activity
      await generateButton.click();

      // Views details
      const studyActivitiesSection = new InteractionPage(page)
        .studyActivitiesSection;

      await expect(studyActivitiesSection.studyActivity).toBeVisible();
      await expect(studyActivitiesSection.studyActivity).toContainText(
        activityName,
      );
      await studyActivitiesSection.studyActivity
        .getByRole('button', { name: 'Details' })
        .click();

      const activityDetailsSection = studyActivitiesSection.studyActivity
        .locator('section')
        .filter({ hasText: 'Details' });

      const activityDescriptionInfo = activityDetailsSection
        .locator('p')
        .filter({ hasText: 'Description' });
      await expect(activityDescriptionInfo).toContainText(activityDescription);

      const activitySubjectInfo = activityDetailsSection
        .locator('p')
        .filter({ hasText: 'Subject type' });
      await expect(activitySubjectInfo).toContainText('Literature');
      const activityFormatInfo = activityDetailsSection
        .locator('p')
        .filter({ hasText: 'Format type' });
      await expect(activityFormatInfo).toContainText(
        'Multiple choice questions',
      );
    });

    test('Chat with the LLM using a recommended prompt', async ({ page }) => {
      const documentSection = new InteractionPage(page).documentsSection;

      await documentSection.documentItem
        .getByRole('button', {
          name: 'newName (Literature)',
        })
        .click();

      const detailsPanel = documentSection.documentItem
        .locator('section')
        .filter({ hasText: 'Details' });
      const recommendationsInfo = detailsPanel
        .locator('p')
        .filter({ hasText: 'Recommendations' });
      const chatRecommendations = recommendationsInfo
        .locator('section')
        .filter({ hasText: 'Chat with LLM' });
      const chatRecommendation = chatRecommendations
        .getByRole('listitem')
        .first();

      // Verifies display
      const chatButton = chatRecommendation.getByRole('button', {
        name: 'Chat with LLM',
      });
      const recommendationInfo = chatRecommendation.locator('div');
      const recommendationPrompt = recommendationInfo
        .locator('p')
        .filter({ hasText: 'Prompt' });

      await expect(chatButton).toBeVisible();
      await expect(recommendationInfo).toBeVisible();

      await expect(recommendationPrompt).toBeVisible();
      await expect(recommendationPrompt).toContainText(
        'Chat prompt of document newName',
      );

      // Mocks chat endpoint
      const interactionId = Number(page.url().split('/').pop());

      await page.route(
        `**/api/llm-response/${interactionId}`,
        async (route) => {
          if (route.request().method() !== 'POST') {
            await route.continue();
            return;
          }

          // Route redirect
          await route.continue({
            url: `${process.env.BASE_URL}/api/dev/llm-response/${interactionId}`,
          });
        },
      );

      // Creates activity
      await chatButton.click();

      // Views details
      const chatSection = new InteractionPage(page).chatSection;

      await expect(chatSection.chatConversation).toBeVisible();
      await expect(chatSection.chatConversation).toContainText(
        'Reply to: Chat prompt of document newName',
      );
    });

    test('Update an uploaded document', async ({ page }) => {
      const documentSection = new InteractionPage(page).documentsSection;

      await documentSection.documentItem
        .getByRole('button', {
          name: 'newName (Literature)',
        })
        .click();

      const detailsPanel = documentSection.documentItem
        .locator('section')
        .filter({ hasText: 'Details' });
      await detailsPanel.getByRole('button', { name: 'Show update' }).click();

      // Verifies display
      const updatePanel = documentSection.documentItem
        .locator('form')
        .filter({ hasText: 'Update' });
      const nameUpdateField = updatePanel.getByRole('textbox', {
        name: 'New name',
      });
      const subjectUpdateField = updatePanel.getByRole('combobox', {
        name: 'New subject type',
      });

      await expect(updatePanel).toBeVisible();
      await expect(nameUpdateField).toHaveValue('newName');
      await expect(subjectUpdateField.locator('option:checked')).toHaveText(
        'Literature',
      );

      // Updates
      const newName = 'Updated name';
      await nameUpdateField.fill(newName);

      const newSubject = 'Arts';
      await subjectUpdateField.selectOption({ label: newSubject });

      await updatePanel.getByRole('button', { name: 'Update' }).click();

      // Verifies result
      await expect(updatePanel).not.toBeVisible();
      await expect(documentSection.documentItem.first()).toContainText(
        `${newName} (${newSubject})`,
      );
    });

    test('Delete an uploaded document', async ({ page }) => {
      const documentSection = new InteractionPage(page).documentsSection;

      await documentSection.documentItem
        .getByRole('button', {
          name: 'Delete',
        })
        .click();

      await expect(documentSection.documentItem).not.toBeVisible();
    });
  });
});
