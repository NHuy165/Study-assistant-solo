import { expect, type Locator } from '@playwright/test';

export class StudyAssessmentsSection {
  readonly rootLocator: Locator;

  // Yesterday assessment
  readonly yesterdayAssessment: Locator;
  readonly yesterdayAssessmentContent: Locator;

  // Assessments history
  readonly assessmentsHistory: Locator;
  readonly assessmentDateInput: Locator;
  readonly resetDateButton: Locator;
  readonly assessmentItem: Locator;
  readonly infoNoItem: Locator;

  constructor(rootLocator: Locator) {
    this.rootLocator = rootLocator;

    // Yesterday assessment
    this.yesterdayAssessment = rootLocator
      .locator('section')
      .filter({ hasText: "Yesterday's assessment:" });
    this.yesterdayAssessmentContent = this.yesterdayAssessment.locator('span');

    // Assessments history
    this.assessmentsHistory = rootLocator
      .locator('section')
      .filter({ hasText: 'Study assessments history:' });
    this.assessmentDateInput =
      this.assessmentsHistory.locator('input[type="date"]');
    this.resetDateButton = this.assessmentsHistory.getByRole('button', {
      name: 'Show all',
    });
    this.assessmentItem = this.assessmentsHistory.getByRole('listitem');
    this.infoNoItem = this.assessmentsHistory.getByText(
      'No study assessment found.',
    );
  }

  checkLoaded = async () => {
    await expect(this.rootLocator).toBeVisible();

    // Yesterday assessment
    await expect(this.yesterdayAssessment).toBeVisible();
    await expect(this.yesterdayAssessmentContent).toBeVisible();

    // Assessments history
    await expect(this.assessmentsHistory).toBeVisible();
    await expect(this.assessmentDateInput).toBeVisible();
    await expect(this.resetDateButton).toBeVisible();
  };
}
