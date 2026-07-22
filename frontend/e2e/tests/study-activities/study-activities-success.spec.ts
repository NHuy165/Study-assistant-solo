import test, { expect } from '@playwright/test';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import { InteractionPage } from '@e2e/pages/interaction/InteractionPage';
import mockStudyActivitiesData from '@e2e/data/study-activities/mock-study-activities.json' with { type: 'json' };
import { replaceUnderscore, titleString } from '@/utils/format-string';
import { createStudyActivities } from '@e2e/helpers/study-activities/create-study-activity';

test.describe('Study activities - Success tests', () => {
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
  });

  test('Create a study activity via an AI call and view its details for each study activity format type.', async ({
    page,
  }) => {
    const studyActivitiesSection = new InteractionPage(page)
      .studyActivitiesSection;

    const interactionId = Number(page.url().split('/').pop());

    // Builds mock data
    const responses = [
      {
        ...mockStudyActivitiesData[0],
        prompt: 'Test prompt 1',
        subject_type: 'MATHS',
        interaction_id: interactionId,
      },
      {
        ...mockStudyActivitiesData[1],
        prompt: 'Test prompt 2',
        subject_type: 'VIETNAMESE',
        interaction_id: interactionId,
      },
      {
        ...mockStudyActivitiesData[2],
        prompt: 'Test prompt 3',
        subject_type: 'ENGLISH',
        interaction_id: interactionId,
      },
    ];

    const staticResponses = [...responses];
    const history: unknown[] = [];

    // Mocks response
    await page.route(
      `**/api/study-activity/${interactionId}`,
      async (route) => {
        const method = route.request().method();

        if (method === 'GET') {
          await route.fulfill({
            status: 200,
            contentType: 'application/json',
            json: history,
          });
        } else if (method === 'POST') {
          const mockResponse = responses.shift();

          if (mockResponse) {
            history.push(mockResponse);
          }

          await route.fulfill({
            status: 200,
            contentType: 'application/json',
            json: {
              ...mockResponse,
            },
          });
        } else {
          await route.continue();
        }
      },
    );

    // Real test
    for (let i = 0; i < mockStudyActivitiesData.length; i++) {
      await studyActivitiesSection.fillCreationInputs({
        prompt: staticResponses[i].prompt,
        activityFormat: titleString(
          replaceUnderscore(staticResponses[i].activity_format),
        ),
        subjectType: titleString(
          replaceUnderscore(staticResponses[i].subject_type),
        ),
      });
      await studyActivitiesSection.creationButton.click();

      await expect(studyActivitiesSection.studyActivity).toHaveCount(i + 1);
      await expect(studyActivitiesSection.studyActivity.last()).toContainText(
        staticResponses[i].name,
      );

      await expect(studyActivitiesSection.creationPromptInput).toBeEmpty();

      // Click show details button
      const detailsButton = studyActivitiesSection.studyActivity
        .last()
        .getByRole('button', {
          name: 'Details',
        });
      await detailsButton.click();

      const detailsPanel = studyActivitiesSection.studyActivity
        .last()
        .locator('section')
        .filter({ hasText: 'Details' });

      const createdAtInfo = detailsPanel
        .locator('p')
        .filter({ hasText: 'Created at' });
      const descriptionInfo = detailsPanel
        .locator('p')
        .filter({ hasText: 'Description' });
      const subjectTypeInfo = detailsPanel
        .locator('p')
        .filter({ hasText: 'Subject type' });
      const formatTypeInfo = detailsPanel
        .locator('p')
        .filter({ hasText: 'Format type' });
      const creationPromptInfo = detailsPanel
        .locator('p')
        .filter({ hasText: 'Creation prompt' });

      // Checks details
      await expect(detailsPanel).toBeVisible();
      await expect(createdAtInfo).toBeVisible();
      await expect(descriptionInfo).toBeVisible();
      await expect(subjectTypeInfo).toBeVisible();
      await expect(formatTypeInfo).toBeVisible();
      await expect(creationPromptInfo).toBeVisible();

      // Click show details button again
      await detailsButton.click();
      await expect(detailsPanel).not.toBeVisible();
    }
  });

  test('Create a flashcard activity manually via the manual form.', async ({
    page,
  }) => {
    const studyActivitiesSection = new InteractionPage(page)
      .studyActivitiesSection;

    const name = 'test-name';
    const description = 'test-description';
    const subjectType = 'English';

    await studyActivitiesSection.fillFlashcardCreationInputs({
      name,
      description,
      subjectType,
    });

    await studyActivitiesSection.flashcardCreationButton.click();

    await expect(studyActivitiesSection.flashcardCreationNameInput).toBeEmpty();
    await expect(
      studyActivitiesSection.flashcardCreationDescriptionInput,
    ).toBeEmpty();

    await expect(studyActivitiesSection.studyActivity).toBeVisible();
    await expect(studyActivitiesSection.studyActivity).toContainText(name);
  });

  test('Update a study activity', async ({ page, request }) => {
    const studyActivitiesSection = new InteractionPage(page)
      .studyActivitiesSection;

    const interactionId = Number(page.url().split('/').pop());

    const flashcardActivity = {
      name: 'test-name',
      description: 'test-description',
      subject_type: 'MATHS',
    };

    await createStudyActivities({
      page,
      request,
      interactionId,
      flashcard: flashcardActivity,
    });
    await page.reload();

    const studyActivity1 = studyActivitiesSection.studyActivity.first();

    // Clicks update button
    await studyActivity1
      .getByRole('button', {
        name: 'Update',
      })
      .click();

    // Verifies display
    const updatePanel = studyActivity1
      .locator('form')
      .filter({ hasText: 'Update' });
    const nameUpdateField = updatePanel.getByRole('textbox', {
      name: 'New name',
    });
    const descriptionUpdateField = updatePanel.getByRole('textbox', {
      name: 'New description',
    });

    await expect(updatePanel).toBeVisible();
    await expect(nameUpdateField).toHaveValue(flashcardActivity.name);
    await expect(descriptionUpdateField).toHaveValue(
      flashcardActivity.description,
    );

    // Updates
    const newName = 'Updated name';
    await nameUpdateField.fill(newName);

    const newDescription = 'Updated description';
    await descriptionUpdateField.fill(newDescription);

    await updatePanel.getByRole('button', { name: 'Update' }).click();

    // Verifies result
    await expect(updatePanel).not.toBeVisible();
    await expect(studyActivity1).toContainText(newName);

    await studyActivity1
      .getByRole('button', {
        name: 'Details',
      })
      .click();

    const descriptionInfo = studyActivity1
      .locator('section')
      .filter({ hasText: 'Details' })
      .locator('p')
      .filter({ hasText: 'Description' });
    await expect(descriptionInfo).toContainText(newDescription);
  });

  test('Delete a study activity', async ({ page, request }) => {
    const studyActivitiesSection = new InteractionPage(page)
      .studyActivitiesSection;

    const interactionId = Number(page.url().split('/').pop());

    const flashcardActivity = {
      name: 'test-name',
      description: 'test-description',
      subject_type: 'MATHS',
    };

    await createStudyActivities({
      page,
      request,
      interactionId,
      flashcard: flashcardActivity,
    });
    await page.reload();

    // Clicks delete button
    await studyActivitiesSection.studyActivity
      .getByRole('button', {
        name: 'Delete',
      })
      .click();

    // Verifies result
    await expect(studyActivitiesSection.studyActivity).not.toBeVisible();
    await expect(studyActivitiesSection.infoNoItem).toBeVisible();
  });
});
