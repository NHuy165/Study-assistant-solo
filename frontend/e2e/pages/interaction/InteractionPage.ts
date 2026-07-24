import { ChatSection } from '@e2e/pages/interaction/components/ChatSection';
import { DocumentsSection } from '@e2e/pages/interaction/components/DocumentsSection';
import { StudyActivitiesSection } from '@e2e/pages/interaction/components/StudyActivitiesSection';
import { type Page, type Locator, expect } from '@playwright/test';

export class InteractionPage {
  readonly page: Page;
  readonly pageHeader: Locator;
  readonly pageDescription: Locator;

  // Components
  readonly chatSection: ChatSection;
  readonly documentsSection: DocumentsSection;
  readonly studyActivitiesSection: StudyActivitiesSection;

  // Errors
  readonly toastError: Locator;

  constructor(page: Page) {
    this.page = page;
    this.pageHeader = page.getByRole('heading').first();
    this.pageDescription = page
      .locator('p')
      .filter({ has: page.getByText('Description:', { exact: true }).first() });

    // Components
    const chatSectionHeader = page.getByRole('heading', {
      name: 'Chat',
      exact: true,
    });
    this.chatSection = new ChatSection(
      page.locator('section').filter({ has: chatSectionHeader }),
    );

    const documentsSectionHeader = page.getByRole('heading', {
      name: 'Documents',
      exact: true,
    });
    this.documentsSection = new DocumentsSection(
      page.locator('section').filter({ has: documentsSectionHeader }),
    );

    const studyActivitiesSectionHeader = page.getByRole('heading', {
      name: 'Study Activities',
      exact: true,
    });
    this.studyActivitiesSection = new StudyActivitiesSection(
      page.locator('section').filter({ has: studyActivitiesSectionHeader }),
    );

    // Errors
    this.toastError = page.getByRole('status').last();
  }

  goto = async (interactionId: number) => {
    await this.page.goto(`/interaction/${interactionId}`);
  };

  checkLoaded = async ({
    interactionId,
    headerText,
    descriptionText,
  }: {
    interactionId: number;
    headerText: string;
    descriptionText: string;
  }) => {
    await expect(this.page).toHaveURL(`/interaction/${interactionId}`);
    await expect(this.pageHeader).toBeVisible();

    await expect(this.pageHeader).toContainText(headerText);
    await expect(this.pageDescription).toContainText(descriptionText);

    // Checks loaded components
    await this.chatSection.checkLoaded();
    await this.documentsSection.checkLoaded();
    await this.studyActivitiesSection.checkLoaded();
  };
}
