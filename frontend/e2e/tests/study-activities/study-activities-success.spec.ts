import test, { expect } from '@playwright/test';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import { InteractionPage } from '@e2e/pages/interaction/InteractionPage';
import { replaceUnderscore, titleString } from '@/utils/format-string';
import { mockCreateStudyActivity } from '@e2e/helpers/study-activities/mock-create-study-activity';
import { StudyActivityPage } from '@e2e/pages/study-activity/StudyActivityPage';

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

  test('Create a study activity via a mocked API call and view its details for each study activity format type.', async ({
    page,
  }) => {
    const studyActivitiesSection = new InteractionPage(page)
      .studyActivitiesSection;

    const interactionId = Number(page.url().split('/').pop());

    const requests = [
      {
        prompt: 'Test prompt 1',
        subject_type: 'MATHS',
        activity_format: 'MULTIPLE_CHOICE_QUESTIONS',
      },
      {
        prompt: 'Test prompt 2',
        subject_type: 'LANGUAGES',
        activity_format: 'OPEN_ENDED',
      },
      {
        prompt: 'Test prompt 3',
        subject_type: 'LITERATURE',
        activity_format: 'FLASHCARDS',
      },
    ];

    // Mocks response
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
          name: `Name of ${originalBody['prompt']}`,
          description: `Description of ${originalBody['prompt']}`,
          n_items: 2,
        };

        await route.continue({
          url: `${process.env.BASE_URL}/api/dev/study-activity/${interactionId}`,
          postData: JSON.stringify(updatedBody),
        });
      },
    );

    // Real test
    for (let i = 0; i < requests.length; i++) {
      await studyActivitiesSection.fillCreationInputs({
        prompt: requests[i].prompt,
        activityFormat: titleString(
          replaceUnderscore(requests[i].activity_format),
        ),
        subjectType: titleString(replaceUnderscore(requests[i].subject_type)),
      });
      await studyActivitiesSection.creationButton.click();

      await expect(studyActivitiesSection.studyActivity).toHaveCount(i + 1);
      await expect(studyActivitiesSection.studyActivity.last()).toContainText(
        `Name of ${requests[i].prompt}`,
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
    const subjectType = 'Literature';

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

  test.describe('Go inside a study activity page then back to the main interaction page for each of the activity type', () => {
    test('Go inside an MCQ page and back to the interaction page', async ({
      page,
      request,
    }) => {
      const interactionPage = new InteractionPage(page);
      const studyActivitiesSection = interactionPage.studyActivitiesSection;

      const interactionId = Number(page.url().split('/').pop());

      const studyActivity = {
        prompt: 'test-prompt',
        activity_format: 'MULTIPLE_CHOICE_QUESTIONS',
        subject_type: 'MATHS',
        name: 'test-name',
        description: 'test-description',
        n_items: 5,
      };

      const studyActivityId = (
        await mockCreateStudyActivity({
          page,
          request,
          interactionId,
          studyActivity,
        })
      ).id as number;
      await page.reload();

      // Goes to the activity page
      await studyActivitiesSection.studyActivity
        .getByRole('button', {
          name: studyActivity.name,
        })
        .click();

      const studyActivityPage = new StudyActivityPage(page);
      await studyActivityPage.checkLoadedMCQ({
        studyActivityId,
        headerText: studyActivity.name,
        descriptionText: studyActivity.description,
        numberItems: studyActivity.n_items,
      });

      // Goes back to the interaction page
      await studyActivityPage.interactionPageLink.click();

      await expect(page).toHaveURL(`/interaction/${interactionId}`);
      await expect(interactionPage.pageHeader).toBeVisible();
      await expect(interactionPage.pageHeader).toContainText(
        interactionData.interaction.name,
      );
      await expect(interactionPage.pageDescription).toContainText(
        interactionData.interaction.description,
      );
    });

    test('Go inside an Open Ended page and back to the interaction page', async ({
      page,
      request,
    }) => {
      const interactionPage = new InteractionPage(page);
      const studyActivitiesSection = interactionPage.studyActivitiesSection;

      const interactionId = Number(page.url().split('/').pop());

      const studyActivity = {
        prompt: 'test-prompt',
        activity_format: 'OPEN_ENDED',
        subject_type: 'LANGUAGES',
        name: 'test-name',
        description: 'test-description',
        n_items: 4,
      };

      const studyActivityId = (
        await mockCreateStudyActivity({
          page,
          request,
          interactionId,
          studyActivity,
        })
      ).id as number;
      await page.reload();

      // Goes to the activity page
      await studyActivitiesSection.studyActivity
        .getByRole('button', {
          name: studyActivity.name,
        })
        .click();

      const studyActivityPage = new StudyActivityPage(page);
      await studyActivityPage.checkLoadedOpenEnded({
        studyActivityId,
        headerText: studyActivity.name,
        descriptionText: studyActivity.description,
        numberItems: studyActivity.n_items,
      });

      // Goes back to the interaction page
      await studyActivityPage.interactionPageLink.click();

      await expect(page).toHaveURL(`/interaction/${interactionId}`);
      await expect(interactionPage.pageHeader).toBeVisible();
      await expect(interactionPage.pageHeader).toContainText(
        interactionData.interaction.name,
      );
      await expect(interactionPage.pageDescription).toContainText(
        interactionData.interaction.description,
      );
    });

    test('Go inside a Flashcards page and back to the interaction page', async ({
      page,
      request,
    }) => {
      const interactionPage = new InteractionPage(page);
      const studyActivitiesSection = interactionPage.studyActivitiesSection;

      const interactionId = Number(page.url().split('/').pop());

      const studyActivity = {
        prompt: 'test-prompt',
        activity_format: 'FLASHCARDS',
        subject_type: 'MATHS',
        name: 'test-name',
        description: 'test-description',
        n_items: 6,
      };

      const studyActivityId = (
        await mockCreateStudyActivity({
          page,
          request,
          interactionId,
          studyActivity,
        })
      ).id as number;
      await page.reload();

      // Goes to the activity page
      await studyActivitiesSection.studyActivity
        .getByRole('button', {
          name: studyActivity.name,
        })
        .click();

      const studyActivityPage = new StudyActivityPage(page);
      await studyActivityPage.checkLoadedFlashcards({
        studyActivityId,
        headerText: studyActivity.name,
        descriptionText: studyActivity.description,
        numberItems: studyActivity.n_items,
      });

      // Goes back to the interaction page
      await studyActivityPage.interactionPageLink.click();

      await expect(page).toHaveURL(`/interaction/${interactionId}`);
      await expect(interactionPage.pageHeader).toBeVisible();
      await expect(interactionPage.pageHeader).toContainText(
        interactionData.interaction.name,
      );
      await expect(interactionPage.pageDescription).toContainText(
        interactionData.interaction.description,
      );
    });
  });

  test('Update a study activity', async ({ page, request }) => {
    const studyActivitiesSection = new InteractionPage(page)
      .studyActivitiesSection;

    const interactionId = Number(page.url().split('/').pop());

    const studyActivity = {
      prompt: 'test-prompt',
      activity_format: 'MULTIPLE_CHOICE_QUESTIONS',
      subject_type: 'MATHS',
      name: 'test-name',
      description: 'test-description',
      n_items: 5,
    };

    await mockCreateStudyActivity({
      page,
      request,
      interactionId,
      studyActivity,
    });
    await page.reload();

    // Clicks update button
    await studyActivitiesSection.studyActivity
      .getByRole('button', {
        name: 'Update',
      })
      .click();

    // Verifies display
    const updatePanel = studyActivitiesSection.studyActivity
      .locator('form')
      .filter({ hasText: 'Update' });
    const nameUpdateField = updatePanel.getByRole('textbox', {
      name: 'New name',
    });
    const descriptionUpdateField = updatePanel.getByRole('textbox', {
      name: 'New description',
    });

    await expect(updatePanel).toBeVisible();
    await expect(nameUpdateField).toHaveValue(studyActivity.name);
    await expect(descriptionUpdateField).toHaveValue(studyActivity.description);

    // Updates
    const newName = 'Updated name';
    await nameUpdateField.fill(newName);

    const newDescription = 'Updated description';
    await descriptionUpdateField.fill(newDescription);

    await updatePanel.getByRole('button', { name: 'Update' }).click();

    // Verifies result
    await expect(updatePanel).not.toBeVisible();
    await expect(studyActivitiesSection.studyActivity).toContainText(newName);

    await studyActivitiesSection.studyActivity
      .getByRole('button', {
        name: 'Details',
      })
      .click();

    const descriptionInfo = studyActivitiesSection.studyActivity
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

    const studyActivity = {
      prompt: 'test-prompt',
      activity_format: 'MULTIPLE_CHOICE_QUESTIONS',
      subject_type: 'MATHS',
      name: 'test-name',
      description: 'test-description',
      n_items: 5,
    };

    await mockCreateStudyActivity({
      page,
      request,
      interactionId,
      studyActivity,
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
