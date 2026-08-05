import { expect, type Locator } from '@playwright/test';

export class DocumentsSection {
  readonly rootLocator: Locator;

  // Creation form
  readonly creationFormHeader: Locator;
  readonly creationForm: Locator;
  readonly creationFileInput: Locator;
  readonly creationNameInput: Locator;
  readonly creationPageStartsAtInput: Locator;
  readonly creationSubjectTypeInput: Locator;
  readonly creationToggleAutomaticSubjectInput: Locator;
  readonly creationButton: Locator;

  // Documents list
  readonly listHeader: Locator;
  readonly infoNoItem: Locator;
  readonly documentItem: Locator;

  constructor(rootLocator: Locator) {
    this.rootLocator = rootLocator;

    // Creation form
    this.creationForm = rootLocator
      .locator('form')
      .filter({ hasText: 'File' })
      .filter({ hasText: 'Name' })
      .filter({ hasText: 'Page starts at' });
    this.creationFormHeader = this.creationForm.getByRole('heading', {
      name: 'Upload a document',
    });

    this.creationFileInput = this.creationForm.locator('input[name="file"]');
    this.creationNameInput = this.creationForm.getByRole('textbox', {
      name: 'Name',
    });
    this.creationPageStartsAtInput = this.creationForm.getByRole('spinbutton', {
      name: 'Page starts at',
    });
    this.creationSubjectTypeInput = this.creationForm.getByRole('combobox', {
      name: 'Subject type',
      exact: true,
    });
    this.creationToggleAutomaticSubjectInput = this.creationForm.getByRole(
      'combobox',
      { name: 'Allow automatic subject type overwrite' },
    );
    this.creationButton = this.creationForm.getByRole('button', {
      name: 'Upload',
    });

    // Documents list
    this.listHeader = rootLocator.getByRole('heading', {
      name: 'Documents list:',
    });
    this.infoNoItem = rootLocator.getByText('User has no uploaded document.');
    this.documentItem = rootLocator.getByRole('listitem');
  }

  checkLoaded = async () => {
    await expect(this.rootLocator).toBeVisible();
  };

  fillCreationInputs = async ({
    filepath,
    name,
    pageStartsAt,
    subjectType,
    automaticSubject,
  }: {
    filepath: string;
    name?: string;
    pageStartsAt?: string;
    subjectType?: string;
    automaticSubject: string;
  }) => {
    await this.creationFileInput.setInputFiles(filepath);
    if (name) {
      await this.creationNameInput.fill(name);
    }
    if (pageStartsAt) {
      await this.creationPageStartsAtInput.fill(pageStartsAt);
    }
    if (subjectType) {
      await this.creationSubjectTypeInput.selectOption({ label: subjectType });
    }
    await this.creationToggleAutomaticSubjectInput.selectOption({
      label: automaticSubject,
    });
  };
}
