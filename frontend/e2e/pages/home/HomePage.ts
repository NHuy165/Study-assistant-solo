import { InteractionsSection } from '@e2e/pages/home/components/InteractionsSection';
import { StudyAssessmentsSection } from '@e2e/pages/home/components/StudyAssessmentsSection';
import { StudyProgressSection } from '@e2e/pages/home/components/StudyProgressSection';
import { UserProfileSection } from '@e2e/pages/home/components/UserProfileSection';
import { type Page, type Locator, expect } from '@playwright/test';

export class HomePage {
  readonly page: Page;
  readonly pageHeader: Locator;

  // Components
  readonly userProfileSection: UserProfileSection;
  readonly studyAssessmentsSection: StudyAssessmentsSection;
  readonly interactionsSection: InteractionsSection;
  readonly studyProgressSection: StudyProgressSection;

  // Errors
  readonly toastError: Locator;

  constructor(page: Page) {
    this.page = page;
    this.pageHeader = page.getByRole('heading', { name: 'HOME PAGE' });

    // Components
    const userProfileHeader = page.getByRole('heading', {
      name: 'User profile',
      exact: true,
    });
    this.userProfileSection = new UserProfileSection(
      page.locator('section').filter({ has: userProfileHeader }),
    );

    const studyAssessmentsHeader = page.getByRole('heading', {
      name: 'Study assessments',
      exact: true,
    });
    this.studyAssessmentsSection = new StudyAssessmentsSection(
      page.locator('section').filter({ has: studyAssessmentsHeader }),
    );

    const interactionsHeader = page.getByRole('heading', {
      name: 'Interactions',
      exact: true,
    });
    this.interactionsSection = new InteractionsSection(
      page.locator('section').filter({ has: interactionsHeader }),
    );

    const studyProgressHeader = page.getByRole('heading', {
      name: 'Study progress',
      exact: true,
    });
    this.studyProgressSection = new StudyProgressSection(
      page.locator('section').filter({ has: studyProgressHeader }),
    );

    // Errors
    this.toastError = page.getByRole('status').last();
  }

  goto = async () => {
    await this.page.goto('/home');
  };

  checkLoaded = async () => {
    await expect(this.page).toHaveURL('/home');
    await expect(this.pageHeader).toBeVisible();

    // Checks loaded components
    await this.userProfileSection.checkLoaded();
    await this.studyAssessmentsSection.checkLoaded();
    await this.interactionsSection.checkLoaded();
    await this.studyProgressSection.checkLoaded();
  };
}
