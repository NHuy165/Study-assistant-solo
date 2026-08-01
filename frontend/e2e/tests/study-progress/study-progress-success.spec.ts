import test, { expect } from '@playwright/test';
import { HomePage } from '@e2e/pages/home/HomePage';
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc.js';

dayjs.extend(utc);

test.describe('Study progress - Success tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    const user = userData.user;

    await registerUser({ request, user });
    await loginUser({ user, page });
  });

  test('View study progress without data', async ({ page }) => {
    const studyProgressSection = new HomePage(page).studyProgressSection;

    // Activities count section
    await expect(studyProgressSection.totalActivityCount).toHaveText('0');
    await expect(
      studyProgressSection.activityCountByFormat
        .locator('dd')
        .filter({ hasNotText: '0' }),
    ).not.toBeVisible();
    await expect(
      studyProgressSection.activityCountBySubject
        .locator('dd')
        .filter({ hasNotText: '0' }),
    ).not.toBeVisible();

    // Activitiy items count section
    await expect(studyProgressSection.totalActivityItemsCount).toHaveText('0');
    await expect(
      studyProgressSection.activityItemsCountByFormat
        .locator('dd')
        .filter({ hasNotText: '0' }),
    ).not.toBeVisible();
    await expect(
      studyProgressSection.activityItemsCountBySubject
        .locator('dd')
        .filter({ hasNotText: '0' }),
    ).not.toBeVisible();

    // Activity score section
    await expect(studyProgressSection.averageActivityScore).toHaveText(
      'No data',
    );
    await expect(
      studyProgressSection.averageActivityScoreByFormat
        .locator('dd')
        .filter({ hasNotText: 'No data' }),
    ).not.toBeVisible();
    await expect(
      studyProgressSection.averageActivityScoreBySubject
        .locator('dd')
        .filter({ hasNotText: 'No data' }),
    ).not.toBeVisible();
  });

  test.describe('View study progress with data', () => {
    test.beforeEach(async ({ page }) => {
      await page.route('**/api/study-progress*', async (route) => {
        // Building mock data
        const activityByFormat = {
          MULTIPLE_CHOICE_QUESTIONS: 5,
          OPEN_ENDED: 4,
          FLASHCARDS: 3,
        };
        const activityBySubject = {
          MATHS: 3,
          LANGUAGES: 4,
          LITERATURE: 5,
        };

        const gradeByFormat = {
          MULTIPLE_CHOICE_QUESTIONS: [400, 500],
          OPEN_ENDED: [200, 400],
        };
        const gradeBySubject = {
          MATHS: [200, 300],
          LANGUAGES: [100, 300],
          LITERATURE: [300, 300],
        };

        const now = dayjs.utc();
        const lastWeek = now.subtract(1, 'week').format('YYYY-MM-DD');
        const lastMonth = now.subtract(1, 'month').format('YYYY-MM-DD');
        const lastYear = now.subtract(1, 'year').format('YYYY-MM-DD');

        // Subtract according to time
        const requestBody = (route.request().postDataJSON() || []) as {
          attribute: string;
          value: string;
          operator: string;
        }[];

        const timeRestraint = requestBody.find(
          (criterion) =>
            criterion.attribute === 'created_at' && criterion.operator === 'GE',
        );

        const removeLastYear = () => {
          // Removes 1 Literature Flashcard
          // Removes 1 Languages Open Ended (40/100)

          activityByFormat.FLASHCARDS -= 1;
          activityBySubject.LITERATURE -= 1;

          activityByFormat.OPEN_ENDED -= 1;
          activityBySubject.LANGUAGES -= 1;

          gradeByFormat.OPEN_ENDED = [
            gradeByFormat.OPEN_ENDED[0] - 40,
            gradeByFormat.OPEN_ENDED[1] - 100,
          ];
          gradeBySubject.LANGUAGES = [
            gradeBySubject.LANGUAGES[0] - 40,
            gradeBySubject.LANGUAGES[1] - 100,
          ];
        };

        const removeLastMonth = () => {
          // Removes 1 Maths Open Ended (70/100)

          activityByFormat.OPEN_ENDED -= 1;
          activityBySubject.MATHS -= 1;

          gradeByFormat.OPEN_ENDED = [
            gradeByFormat.OPEN_ENDED[0] - 70,
            gradeByFormat.OPEN_ENDED[1] - 100,
          ];
          gradeBySubject.MATHS = [
            gradeBySubject.MATHS[0] - 70,
            gradeBySubject.MATHS[1] - 100,
          ];
        };

        const removeLastWeek = () => {
          // Removes 1 Literature MCQ (100/100)

          activityByFormat.MULTIPLE_CHOICE_QUESTIONS -= 1;
          activityBySubject.LITERATURE -= 1;

          gradeByFormat.MULTIPLE_CHOICE_QUESTIONS = [
            gradeByFormat.MULTIPLE_CHOICE_QUESTIONS[0] - 100,
            gradeByFormat.MULTIPLE_CHOICE_QUESTIONS[1] - 100,
          ];
          gradeBySubject.LITERATURE = [
            gradeBySubject.LITERATURE[0] - 100,
            gradeBySubject.LITERATURE[1] - 100,
          ];
        };

        if (timeRestraint) {
          if (timeRestraint.value === lastWeek) {
            removeLastWeek();
            removeLastMonth();
            removeLastYear();
          } else if (timeRestraint.value === lastMonth) {
            removeLastMonth();
            removeLastYear();
          } else if (timeRestraint.value === lastYear) {
            removeLastYear();
          }
        }

        // Mocks data
        const requestUrl = new URL(route.request().url());
        const target = requestUrl.searchParams.get('target');

        switch (target) {
          // Activities count
          case 'COUNT_ACTIVITY': {
            const groupBy = requestBody.find(
              (criterion) => criterion.operator === 'GROUP_BY',
            );

            if (groupBy) {
              switch (groupBy.attribute) {
                // By format
                case 'activity_format':
                  await route.fulfill({
                    status: 200,
                    contentType: 'application/json',
                    json: Object.entries(activityByFormat).map(
                      ([key, value]) => [value, key],
                    ),
                  });
                  break;

                // By subject
                case 'subject_type':
                  await route.fulfill({
                    status: 200,
                    contentType: 'application/json',
                    json: Object.entries(activityBySubject).map(
                      ([key, value]) => [value, key],
                    ),
                  });
                  break;

                default:
                  throw new Error(
                    `Wrong request: ${JSON.stringify(requestBody)}`,
                  );
              }
            } else {
              throw new Error(`Wrong request: ${JSON.stringify(requestBody)}`);
            }

            break;
          }

          // Activity items count
          case 'COUNT_ITEM': {
            const groupBy = requestBody.find(
              (criterion) => criterion.operator === 'GROUP_BY',
            );

            if (groupBy) {
              switch (groupBy.attribute) {
                // By format
                case 'activity_format':
                  await route.fulfill({
                    status: 200,
                    contentType: 'application/json',
                    json: Object.entries(activityByFormat).map(
                      ([key, value]) => [value * 10, key],
                    ),
                  });
                  break;

                // By subject
                case 'subject_type':
                  await route.fulfill({
                    status: 200,
                    contentType: 'application/json',
                    json: Object.entries(activityBySubject).map(
                      ([key, value]) => [value * 10, key],
                    ),
                  });
                  break;

                default:
                  throw new Error(
                    `Wrong request: ${JSON.stringify(requestBody)}`,
                  );
              }
            } else {
              throw new Error(`Wrong request: ${JSON.stringify(requestBody)}`);
            }

            break;
          }

          // Activity score
          case 'SCORE': {
            const groupBy = requestBody.find(
              (criterion) => criterion.operator === 'GROUP_BY',
            );

            if (groupBy) {
              switch (groupBy.attribute) {
                // By format
                case 'activity_format':
                  await route.fulfill({
                    status: 200,
                    contentType: 'application/json',
                    json: Object.entries(gradeByFormat).map(([key, value]) => [
                      value[0],
                      value[1],
                      key,
                    ]),
                  });
                  break;

                // By subject
                case 'subject_type':
                  await route.fulfill({
                    status: 200,
                    contentType: 'application/json',
                    json: Object.entries(gradeBySubject).map(([key, value]) => [
                      value[0],
                      value[1],
                      key,
                    ]),
                  });
                  break;

                default:
                  throw new Error(
                    `Wrong request: ${JSON.stringify(requestBody)}`,
                  );
              }
            } else {
              throw new Error(`Wrong request: ${JSON.stringify(requestBody)}`);
            }

            break;
          }

          default:
            throw new Error(`Wrong request: ${JSON.stringify(requestBody)}`);
        }
      });

      await page.reload();
    });

    test('See all statistics', async ({ page }) => {
      const studyProgressSection = new HomePage(page).studyProgressSection;

      // Activities count section
      await expect(studyProgressSection.totalActivityCount).toHaveText('12');
      await studyProgressSection.checkContent({
        section: 'activityCountByFormat',
        contents: {
          'Multiple Choice Questions:': '5',
          'Open Ended:': '4',
          'Flashcards:': '3',
        },
      });
      await studyProgressSection.checkContent({
        section: 'activityCountBySubject',
        contents: {
          'Maths:': '3',
          'Languages:': '4',
          'Literature:': '5',
        },
      });

      // Activitiy items count section
      await expect(studyProgressSection.totalActivityItemsCount).toHaveText(
        '120',
      );
      await studyProgressSection.checkContent({
        section: 'activityItemsCountByFormat',
        contents: {
          'Multiple Choice Questions:': '50',
          'Open Ended:': '40',
          'Flashcards:': '30',
        },
      });
      await studyProgressSection.checkContent({
        section: 'activityItemsCountBySubject',
        contents: {
          'Maths:': '30',
          'Languages:': '40',
          'Literature:': '50',
        },
      });

      // Activity score section
      await expect(studyProgressSection.averageActivityScore).toHaveText(
        '6.67 out of 10',
      );
      await studyProgressSection.checkContent({
        section: 'averageActivityScoreByFormat',
        contents: {
          'Multiple Choice Questions:': '8.00 out of 10',
          'Open Ended:': '5.00 out of 10',
        },
      });
      await studyProgressSection.checkContent({
        section: 'averageActivityScoreBySubject',
        contents: {
          'Maths:': '6.67 out of 10',
          'Languages:': '3.33 out of 10',
          'Literature:': '10.00 out of 10',
        },
      });
    });

    test('See statistics 1 year back', async ({ page }) => {
      const studyProgressSection = new HomePage(page).studyProgressSection;

      await studyProgressSection.searchInput.selectOption({
        label: 'Last Year',
      });

      // Activities count section
      await expect(studyProgressSection.totalActivityCount).toHaveText('10');
      await studyProgressSection.checkContent({
        section: 'activityCountByFormat',
        contents: {
          'Multiple Choice Questions:': '5',
          'Open Ended:': '3',
          'Flashcards:': '2',
        },
      });
      await studyProgressSection.checkContent({
        section: 'activityCountBySubject',
        contents: {
          'Maths:': '3',
          'Languages:': '3',
          'Literature:': '4',
        },
      });

      // Activity items count section
      await expect(studyProgressSection.totalActivityItemsCount).toHaveText(
        '100',
      );
      await studyProgressSection.checkContent({
        section: 'activityItemsCountByFormat',
        contents: {
          'Multiple Choice Questions:': '50',
          'Open Ended:': '30',
          'Flashcards:': '20',
        },
      });
      await studyProgressSection.checkContent({
        section: 'activityItemsCountBySubject',
        contents: {
          'Maths:': '30',
          'Languages:': '30',
          'Literature:': '40',
        },
      });

      // Activity score section
      await expect(studyProgressSection.averageActivityScore).toHaveText(
        '7.00 out of 10',
      );
      await studyProgressSection.checkContent({
        section: 'averageActivityScoreByFormat',
        contents: {
          'Multiple Choice Questions:': '8.00 out of 10',
          'Open Ended:': '5.33 out of 10',
        },
      });
      await studyProgressSection.checkContent({
        section: 'averageActivityScoreBySubject',
        contents: {
          'Maths:': '6.67 out of 10',
          'Languages:': '3.00 out of 10',
          'Literature:': '10.00 out of 10',
        },
      });
    });

    test('See statistics 1 month back', async ({ page }) => {
      const studyProgressSection = new HomePage(page).studyProgressSection;

      await studyProgressSection.searchInput.selectOption({
        label: 'Last Month',
      });

      // Activities count section
      await expect(studyProgressSection.totalActivityCount).toHaveText('9');
      await studyProgressSection.checkContent({
        section: 'activityCountByFormat',
        contents: {
          'Multiple Choice Questions:': '5',
          'Open Ended:': '2',
          'Flashcards:': '2',
        },
      });
      await studyProgressSection.checkContent({
        section: 'activityCountBySubject',
        contents: {
          'Maths:': '2',
          'Languages:': '3',
          'Literature:': '4',
        },
      });

      // Activity items count section
      await expect(studyProgressSection.totalActivityItemsCount).toHaveText(
        '90',
      );
      await studyProgressSection.checkContent({
        section: 'activityItemsCountByFormat',
        contents: {
          'Multiple Choice Questions:': '50',
          'Open Ended:': '20',
          'Flashcards:': '20',
        },
      });
      await studyProgressSection.checkContent({
        section: 'activityItemsCountBySubject',
        contents: {
          'Maths:': '20',
          'Languages:': '30',
          'Literature:': '40',
        },
      });

      // Activity score section
      await expect(studyProgressSection.averageActivityScore).toHaveText(
        '7.00 out of 10',
      );
      await studyProgressSection.checkContent({
        section: 'averageActivityScoreByFormat',
        contents: {
          'Multiple Choice Questions:': '8.00 out of 10',
          'Open Ended:': '4.50 out of 10',
        },
      });
      await studyProgressSection.checkContent({
        section: 'averageActivityScoreBySubject',
        contents: {
          'Maths:': '6.50 out of 10',
          'Languages:': '3.00 out of 10',
          'Literature:': '10.00 out of 10',
        },
      });
    });

    test('See statistics 1 week back', async ({ page }) => {
      const studyProgressSection = new HomePage(page).studyProgressSection;

      await studyProgressSection.searchInput.selectOption({
        label: 'Last Week',
      });

      // Activities count section
      await expect(studyProgressSection.totalActivityCount).toHaveText('8');
      await studyProgressSection.checkContent({
        section: 'activityCountByFormat',
        contents: {
          'Multiple Choice Questions:': '4',
          'Open Ended:': '2',
          'Flashcards:': '2',
        },
      });
      await studyProgressSection.checkContent({
        section: 'activityCountBySubject',
        contents: {
          'Maths:': '2',
          'Languages:': '3',
          'Literature:': '3',
        },
      });

      // Activity items count section
      await expect(studyProgressSection.totalActivityItemsCount).toHaveText(
        '80',
      );
      await studyProgressSection.checkContent({
        section: 'activityItemsCountByFormat',
        contents: {
          'Multiple Choice Questions:': '40',
          'Open Ended:': '20',
          'Flashcards:': '20',
        },
      });
      await studyProgressSection.checkContent({
        section: 'activityItemsCountBySubject',
        contents: {
          'Maths:': '20',
          'Languages:': '30',
          'Literature:': '30',
        },
      });

      // Activity score section
      await expect(studyProgressSection.averageActivityScore).toHaveText(
        '6.50 out of 10',
      );
      await studyProgressSection.checkContent({
        section: 'averageActivityScoreByFormat',
        contents: {
          'Multiple Choice Questions:': '7.50 out of 10',
          'Open Ended:': '4.50 out of 10',
        },
      });
      await studyProgressSection.checkContent({
        section: 'averageActivityScoreBySubject',
        contents: {
          'Maths:': '6.50 out of 10',
          'Languages:': '3.00 out of 10',
          'Literature:': '10.00 out of 10',
        },
      });
    });
  });
});
