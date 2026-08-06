import { MCQActivity } from '@e2e/pages/study-activity/components/MCQActivity';
import { OpenEndedActivity } from '@e2e/pages/study-activity/components/OpenEndedActivity';
import { FlashcardsActivity } from '@e2e/pages/study-activity/components/FlashcardsActivity';
import { expect, type Locator, type Page } from '@playwright/test';

export class StudyActivityPage {
  readonly page: Page;
  readonly pageHeader: Locator;
  readonly pageDescription: Locator;
  readonly interactionPageLink: Locator;

  // Components
  readonly MCQActivity: MCQActivity;
  readonly OpenEndedActivity: OpenEndedActivity;
  readonly FlashcardsActivity: FlashcardsActivity;

  // Errors
  readonly toastError: Locator;

  constructor(page: Page) {
    this.page = page;
    this.pageHeader = page.getByRole('heading').first();
    this.pageDescription = page
      .locator('p')
      .filter({ has: page.getByText('Description:', { exact: true }).first() });
    this.interactionPageLink = page.getByRole('link', {
      name: 'Back to main interaction',
    });

    // Components
    this.MCQActivity = new MCQActivity(
      page
        .locator('section')
        .first()
        .filter({
          has: page.getByRole('heading', { name: 'Multiple Choice Questions' }),
        }),
    );
    this.OpenEndedActivity = new OpenEndedActivity(
      page
        .locator('section')
        .first()
        .filter({
          has: page.getByRole('heading', { name: 'Open Ended' }),
        }),
    );
    this.FlashcardsActivity = new FlashcardsActivity(
      page
        .locator('section')
        .first()
        .filter({
          has: page.getByRole('heading', { name: 'Flashcards' }),
        }),
    );

    // Errors
    this.toastError = page.getByRole('status').last();
  }

  goto = async (studyActivityId: number) => {
    await this.page.goto(`/study-activity/${studyActivityId}`);
  };

  checkLoaded = async ({
    studyActivityId,
    headerText,
    descriptionText,
  }: {
    studyActivityId: number;
    headerText: string;
    descriptionText: string;
  }) => {
    await expect(this.page).toHaveURL(`/study-activity/${studyActivityId}`);
    await expect(this.pageHeader).toBeVisible();

    await expect(this.pageHeader).toContainText(headerText);
    await expect(this.pageDescription).toContainText(descriptionText);
  };

  checkLoadedMCQ = async ({
    studyActivityId,
    headerText,
    descriptionText,
    numberItems,
  }: {
    studyActivityId: number;
    headerText: string;
    descriptionText: string;
    numberItems: number;
  }) => {
    await this.checkLoaded({ studyActivityId, headerText, descriptionText });

    await this.MCQActivity.checkLoaded(numberItems);
  };

  checkLoadedOpenEnded = async ({
    studyActivityId,
    headerText,
    descriptionText,
    numberItems,
  }: {
    studyActivityId: number;
    headerText: string;
    descriptionText: string;
    numberItems: number;
  }) => {
    await this.checkLoaded({ studyActivityId, headerText, descriptionText });

    await this.OpenEndedActivity.checkLoaded(numberItems);
  };

  checkLoadedFlashcards = async ({
    studyActivityId,
    headerText,
    descriptionText,
    numberItems,
  }: {
    studyActivityId: number;
    headerText: string;
    descriptionText: string;
    numberItems: number;
  }) => {
    await this.checkLoaded({ studyActivityId, headerText, descriptionText });

    await this.FlashcardsActivity.checkLoaded(numberItems);
  };
}
