import { expect, type Locator } from '@playwright/test';

export class StudyProgressSection {
  readonly rootLocator: Locator;

  // Search input
  readonly searchInput: Locator;

  // Activities count section
  readonly activityCountSection: Locator;
  readonly totalActivityCount: Locator;
  readonly activityCountByFormat: Locator;
  readonly activityCountBySubject: Locator;

  // Activity items count section
  readonly activityItemsCountSection: Locator;
  readonly totalActivityItemsCount: Locator;
  readonly activityItemsCountByFormat: Locator;
  readonly activityItemsCountBySubject: Locator;

  // Activity score section
  readonly activityScoreSection: Locator;
  readonly averageActivityScore: Locator;
  readonly averageActivityScoreByFormat: Locator;
  readonly averageActivityScoreBySubject: Locator;

  constructor(rootLocator: Locator) {
    this.rootLocator = rootLocator;

    // Search input
    this.searchInput = rootLocator.getByRole('combobox', {
      name: 'Statistics range:',
    });

    // Activities count section
    this.activityCountSection = rootLocator
      .locator('section')
      .filter({ hasText: 'Total study activities generated' });
    this.totalActivityCount = this.activityCountSection
      .getByRole('heading', {
        name: 'Total study activities generated',
      })
      .locator('span')
      .nth(1);
    this.activityCountByFormat = this.activityCountSection
      .locator('section')
      .filter({ hasText: 'Study activities count grouped by format' });
    this.activityCountBySubject = this.activityCountSection
      .locator('section')
      .filter({ hasText: 'Study activities count grouped by subject' });

    // Activity items count section
    this.activityItemsCountSection = rootLocator
      .locator('section')
      .filter({ hasText: 'Total study activity items generated' });
    this.totalActivityItemsCount = this.activityItemsCountSection
      .getByRole('heading', {
        name: 'Total study activity items generated',
      })
      .locator('span')
      .nth(1);
    this.activityItemsCountByFormat = this.activityItemsCountSection
      .locator('section')
      .filter({ hasText: 'Study activity items count grouped by format' });
    this.activityItemsCountBySubject = this.activityItemsCountSection
      .locator('section')
      .filter({ hasText: 'Study activity items count grouped by subject' });

    // Activity score section
    this.activityScoreSection = rootLocator
      .locator('section')
      .filter({ hasText: 'Exercise average grades' })
      .first();
    this.averageActivityScore = this.activityScoreSection
      .getByRole('heading', {
        name: 'Exercise average grades',
      })
      .locator('span')
      .nth(1);
    this.averageActivityScoreByFormat = this.activityScoreSection
      .locator('section')
      .filter({ hasText: 'Exercise average grades grouped by format' });
    this.averageActivityScoreBySubject = this.activityScoreSection
      .locator('section')
      .filter({ hasText: 'Exercise average grades grouped by subject' });
  }

  checkLoaded = async () => {
    await expect(this.rootLocator).toBeVisible();

    // Search input
    await expect(this.searchInput).toBeVisible();

    // Activities count section
    await expect(this.activityCountSection).toBeVisible();
    await expect(this.totalActivityCount).toBeVisible();
    await expect(this.activityCountByFormat).toBeVisible();
    await expect(this.activityCountBySubject).toBeVisible();

    // Activity items count section
    await expect(this.activityItemsCountSection).toBeVisible();
    await expect(this.totalActivityItemsCount).toBeVisible();
    await expect(this.activityItemsCountByFormat).toBeVisible();
    await expect(this.activityItemsCountBySubject).toBeVisible();

    // Activity score section
    await expect(this.activityScoreSection).toBeVisible();
    await expect(this.averageActivityScore).toBeVisible();
    await expect(this.averageActivityScoreByFormat).toBeVisible();
    await expect(this.averageActivityScoreBySubject).toBeVisible();
  };

  checkContent = async ({
    section,
    contents,
  }: {
    section:
      | 'activityCountByFormat'
      | 'activityCountBySubject'
      | 'activityItemsCountByFormat'
      | 'activityItemsCountBySubject'
      | 'averageActivityScoreByFormat'
      | 'averageActivityScoreBySubject';
    contents: Record<string, string>;
  }) => {
    const searchSection = this[section];

    for (const [key, value] of Object.entries(contents)) {
      const realValue = await searchSection
        .locator('dl')
        .locator('div')
        .filter({ hasText: key })
        .locator('dd')
        .innerText();
      await expect(realValue).toBe(value);
    }
  };
}
