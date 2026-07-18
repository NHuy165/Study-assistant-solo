import { AuthPage } from '@e2e/pages/auth/AuthPage';
import { HomePage } from '@e2e/pages/home/HomePage';
import { type Page } from '@playwright/test';

type UserLoginType = {
  email: string;
  password: string;
};

export const loginUser = async ({
  user,
  page,
}: {
  user: UserLoginType;
  page: Page;
}) => {
  const authPage = new AuthPage(page);

  await authPage.loginForm.fillInputs({ ...user });
  await authPage.loginForm.loginButton.click();

  const homePage = new HomePage(page);
  await homePage.checkLoaded();
};
