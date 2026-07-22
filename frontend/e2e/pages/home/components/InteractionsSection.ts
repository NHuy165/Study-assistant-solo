import { expect, type Locator } from '@playwright/test';

export class InteractionsSection {
  readonly rootLocator: Locator;

  // Creation form
  readonly creationFormHeader: Locator;
  readonly creationForm: Locator;
  readonly creationNameInput: Locator;
  readonly creationDescriptionInput: Locator;
  readonly creationButton: Locator;

  // Interactions list
  readonly listHeader: Locator;
  readonly infoNoItem: Locator;
  readonly interactionItem: Locator;

  constructor(rootLocator: Locator) {
    this.rootLocator = rootLocator;

    // Creation form
    this.creationForm = rootLocator
      .locator('form')
      .filter({ hasText: 'Name' })
      .filter({ hasText: 'Description' });
    this.creationFormHeader = this.creationForm.getByRole('heading', {
      name: 'Create an interaction',
    });
    this.creationNameInput = this.creationForm.getByRole('textbox', {
      name: 'Name',
    });
    this.creationDescriptionInput = this.creationForm.getByRole('textbox', {
      name: 'Description',
    });
    this.creationButton = this.creationForm.getByRole('button', {
      name: 'Create',
    });

    // Interactions list
    this.listHeader = rootLocator.getByRole('heading', {
      name: 'Interactions list:',
    });
    this.infoNoItem = rootLocator.getByText('User has no interaction.');
    this.interactionItem = rootLocator.getByRole('listitem');
  }

  checkLoaded = async () => {
    await expect(this.rootLocator).toBeVisible();

    // Creation form
    await expect(this.creationFormHeader).toBeVisible();
    await expect(this.creationForm).toBeVisible();
    await expect(this.creationNameInput).toBeVisible();
    await expect(this.creationDescriptionInput).toBeVisible();
    await expect(this.creationButton).toBeVisible();

    // Interactions list
    await expect(this.listHeader).toBeVisible();
    await expect(this.infoNoItem).toBeVisible();
  };

  fillCreationInputs = async ({
    name,
    description,
  }: {
    name: string;
    description: string;
  }) => {
    await this.creationNameInput.fill(name);
    await this.creationDescriptionInput.fill(description);
  };
}
