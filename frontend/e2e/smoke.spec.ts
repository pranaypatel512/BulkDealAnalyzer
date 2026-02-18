import { test, expect } from '@playwright/test';

test.describe('Smoke', () => {
  test('home page loads', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/BulkDeal|Bulk Deal|Analyzer/i);
  });

  test('login page loads from home', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('link', { name: /sign in/i }).first().click();
    await expect(page).toHaveURL(/\/login/);
    await expect(
      page.getByRole('heading', { name: /welcome back/i }),
    ).toBeVisible();
  });

  test('dashboard redirects to login when unauthenticated', async ({
    page,
  }) => {
    await page.goto('/dashboard');
    await expect(page).toHaveURL(/\/login/);
  });
});
