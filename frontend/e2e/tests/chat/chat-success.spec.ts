import test, { expect } from '@playwright/test';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
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

    // Mocks response
    await page.route(`**/api/llm-response/${interactionId}`, async (route) => {
      if (route.request().method() !== 'POST') {
        await route.continue();
        return;
      }

      // Route redirect
      await route.continue({
        url: `${process.env.BASE_URL}/api/dev/llm-response/${interactionId}`,
      });
    });

    // Checks initial message
    await expect(chatSection.infoNoChat).toBeVisible();

    // Sends message
    const prompt1 = 'test prompt 1';

    await chatSection.chatInput.fill(prompt1);
    await chatSection.chatButton.click();

    await expect(chatSection.chatInput).toBeEmpty();
    await expect(chatSection.chatConversation).toHaveCount(1);
    await expect(chatSection.chatConversation.last()).toContainText(
      `User: ${prompt1}`,
    );
    await expect(chatSection.chatConversation.last()).toContainText(
      `Chatbot: Reply to: ${prompt1}`,
    );

    const prompt2 = 'test prompt 2';

    await chatSection.chatInput.fill(prompt2);
    await chatSection.chatButton.click();

    await expect(chatSection.chatInput).toBeEmpty();
    await expect(chatSection.chatConversation).toHaveCount(2);
    await expect(chatSection.chatConversation.last()).toContainText(
      `User: ${prompt2}`,
    );
    await expect(chatSection.chatConversation.last()).toContainText(
      `Chatbot: Reply to: ${prompt2}`,
    );
  });
});
