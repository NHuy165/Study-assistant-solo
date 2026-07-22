import test, { expect } from '@playwright/test';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
import mockChatData from '@e2e/data/chat/mock-chat.json' with { type: 'json' };
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import { InteractionPage } from '@e2e/pages/interaction/InteractionPage';

test.describe('Chat - Success tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    // Registers and logs in
    const user = userData.user;

    await registerUser({ request, user });
    await loginUser({ user, page });

    // Creates and goes inside interaction
    const interaction = interactionData.interaction;

    const interactionId = await createInteraction({
      page,
      request,
      interaction,
    });
    await page.reload();

    const interactionPage = new InteractionPage(page);
    await interactionPage.goto(interactionId);
  });

  test('Make multiple conversations and check if they are all properly loaded', async ({
    page,
  }) => {
    const chatSection = new InteractionPage(page).chatSection;

    const interactionId = Number(page.url().split('/').pop());

    // Builds mock data
    const responses = [
      {
        ...mockChatData[0],
        prompt: 'Test prompt 1',
        interaction_id: interactionId,
      },
      {
        ...mockChatData[1],
        prompt: 'Test prompt 2',
        interaction_id: interactionId,
      },
    ];

    const staticResponses = [...responses];
    const history: unknown[] = [];

    // Mocks response
    await page.route(`**/api/llm-response/${interactionId}`, async (route) => {
      const method = route.request().method();

      if (method === 'GET') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          json: history,
        });
      } else if (method === 'POST') {
        const mockResponse = responses.shift();

        if (mockResponse) {
          history.push(mockResponse);
        }

        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          json: {
            ...mockResponse,
          },
        });
      } else {
        await route.continue();
      }
    });

    // Real test
    for (let i = 0; i < mockChatData.length; i++) {
      await chatSection.chatInput.fill(staticResponses[i].prompt);
      await chatSection.chatButton.click();

      await expect(chatSection.chatInput).toBeEmpty();
      await expect(chatSection.chatConversation).toHaveCount(i + 1);
      await expect(chatSection.chatConversation.last()).toContainText(
        `User: ${staticResponses[i].prompt}`,
      );
      await expect(chatSection.chatConversation.last()).toContainText(
        `Chatbot: ${staticResponses[i].answer}`,
      );
    }
  });
});
