import { expect, type Locator } from '@playwright/test';

export class FlashcardsActivity {
  readonly rootLocator: Locator;

  // Main flashcard
  readonly cardIndex: Locator;
  readonly previousButton: Locator;
  readonly cardButton: Locator;
  readonly nextButton: Locator;
  readonly infoNoItem: Locator;

  // Update and delete
  readonly showUpdateButton: Locator;

  readonly updateForm: Locator;
  readonly updateFrontInput: Locator;
  readonly updateBackInput: Locator;
  readonly updateButton: Locator;

  readonly deleteButton: Locator;

  // Flashcard creation
  readonly creationForm: Locator;
  readonly creationFrontInput: Locator;
  readonly creationBackInput: Locator;
  readonly createButton: Locator;

  constructor(rootLocator: Locator) {
    this.rootLocator = rootLocator;

    // Main flashcard
    this.cardIndex = rootLocator.getByText('Current card index:');

    const mainFlashcardButtons = rootLocator.locator('section').first();
    this.previousButton = mainFlashcardButtons.getByRole('button', {
      name: 'Previous',
      exact: true,
    });
    this.cardButton = mainFlashcardButtons.getByRole('button').nth(1);
    this.nextButton = mainFlashcardButtons.getByRole('button', {
      name: 'Next',
      exact: true,
    });
    this.infoNoItem = mainFlashcardButtons.getByText('No flashcard to show');

    // Update and delete
    const updateDelete = rootLocator.locator('section').nth(1);
    this.showUpdateButton = updateDelete.getByRole('button', {
      name: 'Update current flashcard',
    });

    this.updateForm = updateDelete
      .locator('form')
      .filter({ hasText: 'New front content' })
      .filter({ hasText: 'New back content' });
    this.updateFrontInput = this.updateForm.getByRole('textbox', {
      name: 'New front content',
    });
    this.updateBackInput = this.updateForm.getByRole('textbox', {
      name: 'New back content',
    });
    this.updateButton = this.updateForm.getByRole('button', { name: 'Update' });

    this.deleteButton = updateDelete.getByRole('button', {
      name: 'Delete current flashcard',
    });

    // Flashcard creation
    this.creationForm = rootLocator
      .locator('form')
      .filter({ hasText: 'Front' })
      .filter({ hasText: 'Back' })
      .last();
    this.creationFrontInput = this.creationForm.getByRole('textbox', {
      name: 'Front',
    });
    this.creationBackInput = this.creationForm.getByRole('textbox', {
      name: 'Back',
    });
    this.createButton = this.creationForm.getByRole('button', {
      name: 'Create',
    });
  }

  checkLoaded = async (numberItems: number) => {
    await expect(this.rootLocator).toBeVisible();

    if (numberItems === 0) {
      // Main flashcard
      await expect(this.cardIndex).not.toBeVisible();
      await expect(this.previousButton).not.toBeVisible();
      await expect(this.cardButton).not.toBeVisible();
      await expect(this.nextButton).not.toBeVisible();

      await expect(this.infoNoItem).toBeVisible();

      // Update and delete
      await expect(this.showUpdateButton).not.toBeVisible();
      await expect(this.deleteButton).not.toBeVisible();
    } else {
      // Main flashcard
      await expect(this.cardIndex).toBeVisible();

      // Checks number of cards shown
      const realNumberItems = Number(
        (await this.cardIndex.innerText()).split('/')[1],
      );
      await expect(realNumberItems).toBe(numberItems);

      await expect(this.previousButton).toBeVisible();
      await expect(this.previousButton).toBeDisabled();
      await expect(this.cardButton).toBeVisible();
      await expect(this.nextButton).toBeVisible();

      // Update and delete
      await expect(this.showUpdateButton).toBeVisible();
      await expect(this.deleteButton).toBeVisible();
    }

    // Flashcard creation
    await expect(this.creationForm).toBeVisible();
    await expect(this.creationFrontInput).toBeVisible();
    await expect(this.creationBackInput).toBeVisible();
    await expect(this.createButton).toBeVisible();
  };

  checkCurrentCard = async ({
    front,
    back,
  }: {
    front: string;
    back: string;
  }) => {
    await expect(this.cardButton).toHaveText(front);
    await this.cardButton.click();

    await expect(this.cardButton).toHaveText(back);
    await this.cardButton.click();
  };
}
