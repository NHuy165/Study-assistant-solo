import { expect, type Locator } from '@playwright/test';

export class StudyActivitiesSection {
  readonly rootLocator: Locator;

  // Creation form
  readonly creationForm: Locator;
  readonly creationPromptInput: Locator;
  readonly creationActivityFormatInput: Locator;
  readonly creationSubjectTypeInput: Locator;
  readonly creationButton: Locator;

  // Flashcard manual creation form
  readonly flashcardCreationForm: Locator;
  readonly flashcardCreationNameInput: Locator;
  readonly flashcardCreationDescriptionInput: Locator;
  readonly flashcardCreationSubjectTypeInput: Locator;
  readonly flashcardCreationButton: Locator;

  // Study activities list
  readonly listHeader: Locator;
  readonly infoNoItem: Locator;
  readonly studyActivity: Locator; // Not studyActivityItem because that's another object

  constructor(rootLocator: Locator) {
    this.rootLocator = rootLocator;

    // Creation form
    this.creationForm = rootLocator
      .locator('form')
      .filter({ hasText: 'Create a study activity' });
    this.creationPromptInput = this.creationForm.getByRole('textbox', {
      name: 'Prompt',
    });
    this.creationActivityFormatInput = this.creationForm.getByRole('combobox', {
      name: 'Activity format',
    });
    this.creationSubjectTypeInput = this.creationForm.getByRole('combobox', {
      name: 'Subject type',
    });
    this.creationButton = this.creationForm.getByRole('button', {
      name: 'Create',
    });

    // Flashcard manual creation form
    this.flashcardCreationForm = rootLocator
      .locator('form')
      .filter({ hasText: 'Create a new blank flashcard activity' });
    this.flashcardCreationNameInput = this.flashcardCreationForm.getByRole(
      'textbox',
      {
        name: 'Name',
      },
    );
    this.flashcardCreationDescriptionInput =
      this.flashcardCreationForm.getByRole('textbox', {
        name: 'Description',
      });
    this.flashcardCreationSubjectTypeInput =
      this.flashcardCreationForm.getByRole('combobox', {
        name: 'Subject type',
      });
    this.flashcardCreationButton = this.flashcardCreationForm.getByRole(
      'button',
      {
        name: 'Create',
      },
    );

    // Study activities list
    this.listHeader = rootLocator.getByRole('heading', {
      name: 'Study activities list:',
    });
    this.infoNoItem = rootLocator.getByText('User has no study activity.');
    this.studyActivity = rootLocator.getByRole('listitem');
  }

  checkLoaded = async () => {
    await expect(this.rootLocator).toBeVisible();

    // Creation form
    await expect(this.creationForm).toBeVisible();
    await expect(this.creationPromptInput).toBeVisible();
    await expect(this.creationActivityFormatInput).toBeVisible();
    await expect(this.creationSubjectTypeInput).toBeVisible();
    await expect(this.creationButton).toBeVisible();

    // Interactions list
    await expect(this.listHeader).toBeVisible();
    await expect(this.infoNoItem).toBeVisible();
  };

  fillCreationInputs = async ({
    prompt,
    activityFormat,
    subjectType,
  }: {
    prompt: string;
    activityFormat: string;
    subjectType: string;
  }) => {
    await this.creationPromptInput.fill(prompt);
    await this.creationActivityFormatInput.selectOption({
      label: activityFormat,
    });
    await this.creationSubjectTypeInput.selectOption({ label: subjectType });
  };

  fillFlashcardCreationInputs = async ({
    name,
    description,
    subjectType,
  }: {
    name: string;
    description: string;
    subjectType: string;
  }) => {
    await this.flashcardCreationNameInput.fill(name);
    await this.flashcardCreationDescriptionInput.fill(description);
    await this.flashcardCreationSubjectTypeInput.selectOption({
      label: subjectType,
    });
  };
}
