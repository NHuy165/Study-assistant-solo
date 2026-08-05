import test, { expect } from '@playwright/test';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import { mockCreateStudyActivity } from '@e2e/helpers/study-activities/mock-create-study-activity';
import { StudyActivityPage } from '@e2e/pages/study-activity/StudyActivityPage';
import { mockSubmitStudyActivity } from '@e2e/helpers/study-activities/mock-submit-study-activity';

test.describe('Flashcards - Success tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    // Registers and logs in
    const user = userData.user;

    await registerUser({ request, user });
    await loginUser({ user, page });

    // Creates interaction
    const interaction = interactionData.interaction;

    const interactionId = await createInteraction({
      page,
      request,
      interaction,
    });

    // Creates study activity
    const studyActivity = {
      prompt: 'test-Flashcards-prompt',
      activity_format: 'FLASHCARDS',
      subject_type: 'LITERATURE',
      name: 'test-Flashcards-name',
      description: 'test-Flashcards-description',
      n_items: 3,
    };
    const studyActivityId = (
      await mockCreateStudyActivity({
        page,
        request,
        interactionId,
        studyActivity,
      })
    ).id as number;

    // Mocks submit response
    await page.route(
      `**/api/study-activity/${studyActivityId}/submit`,
      async (route) => {
        const mockData = await mockSubmitStudyActivity({
          page,
          request,
          studyActivityId,
        });
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          json: mockData,
        });
      },
    );

    const studyActivityPage = new StudyActivityPage(page);
    await studyActivityPage.goto(studyActivityId);
  });

  test('Test the Previous, Next and the core flashcard buttons.', async ({
    page,
  }) => {
    const flashcardsActivity = new StudyActivityPage(page).FlashcardsActivity;

    // Checks disability and content
    await expect(flashcardsActivity.previousButton).toBeDisabled();
    await expect(flashcardsActivity.nextButton).not.toBeDisabled();

    await flashcardsActivity.checkCurrentCard({
      front: 'Test front 1',
      back: 'Test back 1',
    });

    // Switches card and does the same
    await flashcardsActivity.nextButton.click();

    await expect(flashcardsActivity.previousButton).not.toBeDisabled();
    await expect(flashcardsActivity.nextButton).not.toBeDisabled();

    await flashcardsActivity.checkCurrentCard({
      front: 'Test front 2',
      back: 'Test back 2',
    });

    // Switches one more time
    await flashcardsActivity.nextButton.click();

    await expect(flashcardsActivity.previousButton).not.toBeDisabled();
    await expect(flashcardsActivity.nextButton).toBeDisabled();

    await flashcardsActivity.checkCurrentCard({
      front: 'Test front 3',
      back: 'Test back 3',
    });

    // Switches back to card 1
    await flashcardsActivity.previousButton.click();
    await flashcardsActivity.previousButton.click();

    await expect(flashcardsActivity.previousButton).toBeDisabled();
    await expect(flashcardsActivity.nextButton).not.toBeDisabled();

    await flashcardsActivity.checkCurrentCard({
      front: 'Test front 1',
      back: 'Test back 1',
    });
  });

  test('Update current card', async ({ page }) => {
    const flashcardsActivity = new StudyActivityPage(page).FlashcardsActivity;

    const frontContent = await flashcardsActivity.cardButton.innerText();
    await flashcardsActivity.cardButton.click(); // Goes to back
    const backContent = await flashcardsActivity.cardButton.innerText();
    await flashcardsActivity.cardButton.click(); // Goes back to front

    // Verifies display
    await flashcardsActivity.showUpdateButton.click();

    await expect(flashcardsActivity.updateForm).toBeVisible();

    await expect(flashcardsActivity.updateFrontInput).toHaveValue(frontContent);
    await expect(flashcardsActivity.updateBackInput).toHaveValue(backContent);

    // Updates
    const updatedFront = 'Updated front';
    const updatedBack = 'Updated back';

    await flashcardsActivity.updateFrontInput.fill(updatedFront);
    await flashcardsActivity.updateBackInput.fill(updatedBack);
    await flashcardsActivity.updateButton.click();

    // Verifies result
    await expect(flashcardsActivity.updateForm).not.toBeVisible();
    await flashcardsActivity.checkCurrentCard({
      front: updatedFront,
      back: updatedBack,
    });
  });

  test('Deleting a non-last card in the deck.', async ({ page }) => {
    const flashcardsActivity = new StudyActivityPage(page).FlashcardsActivity;

    await flashcardsActivity.deleteButton.click();

    // Verifies result (current card moves forward)
    await flashcardsActivity.checkCurrentCard({
      front: 'Test front 2',
      back: 'Test back 2',
    });
  });

  test('Deleting the last card of the deck.', async ({ page }) => {
    const flashcardsActivity = new StudyActivityPage(page).FlashcardsActivity;

    await flashcardsActivity.nextButton.click();
    await flashcardsActivity.nextButton.click();

    expect(flashcardsActivity.nextButton).toBeDisabled();

    await flashcardsActivity.deleteButton.click();

    // Verifies result (current card moves backwards)
    await flashcardsActivity.checkCurrentCard({
      front: 'Test front 2',
      back: 'Test back 2',
    });
  });

  test('Deleting all the cards of the deck.', async ({ page }) => {
    const studyActivityPage = new StudyActivityPage(page);
    const flashcardsActivity = studyActivityPage.FlashcardsActivity;

    const numDelete = 3;

    for (let i = 0; i < numDelete; i++) {
      const currentFlashcard = await flashcardsActivity.cardButton.innerText();
      await flashcardsActivity.deleteButton.click();
      await expect(
        flashcardsActivity.cardButton.filter({ hasText: currentFlashcard }),
      ).not.toBeVisible();
    }

    const studyActivityId = Number(page.url().split('/').pop());

    await studyActivityPage.checkLoadedFlashcards({
      studyActivityId,
      headerText: 'test-Flashcards-name',
      descriptionText: 'test-Flashcards-description',
      numberItems: 0,
    });
  });

  test('Create a new flashcard', async ({ page }) => {
    const flashcardsActivity = new StudyActivityPage(page).FlashcardsActivity;

    const newFront = 'Test front 4';
    const newBack = 'Test back 4';

    await flashcardsActivity.creationFrontInput.fill(newFront);
    await flashcardsActivity.creationBackInput.fill(newBack);
    await flashcardsActivity.createButton.click();

    await flashcardsActivity.nextButton.click();
    await flashcardsActivity.nextButton.click();
    await flashcardsActivity.nextButton.click();

    await flashcardsActivity.checkCurrentCard({
      front: newFront,
      back: newBack,
    });
  });
});
