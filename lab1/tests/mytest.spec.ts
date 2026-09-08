import { test, expect } from '@playwright/test';

test('Амжилттай нэвтрэх', async ({ page }) => {

  // 1. Website нээх
  await page.goto('https://www.saucedemo.com');

  await page 
    .getByPlaceholder('Username')
    .fill('standard_user');

  await page 
    .getByPlaceholder('Password')
    .fill('secret_sauce');

  await page 
    .getByRole('button', {name: 'Login'})
    .click();

  await expect(
    page.getByText('Products')
  ).toBeVisible();

  await expect(page).toHaveURL(/inventory/);
});

test('Буруу нууц үгээр нэвтрэх', async ({ page }) => {
  await page.goto('https://www.saucedemo.com');

  await page
    .getByPlaceholder('Username')
    .fill('standard_user');

  await page
    .getByPlaceholder('Password')
    .fill('wrong_password');

  await page
    .getByRole('button', { name: 'Login' })
    .click();

  await expect(
    page.getByText(/Username and password do not match/)
  ).toBeVisible();
});

test('Нэвтэрсний дараа бараа сагсанд нэмэх', async ({ page }) => {
  await page.goto('https://www.saucedemo.com');

  await page
    .getByPlaceholder('Username')
    .fill('standard_user');

  await page
    .getByPlaceholder('Password')
    .fill('secret_sauce');

  await page
    .getByRole('button', { name: 'Login' })
    .click();

  await expect(
    page.getByText('Products')
  ).toBeVisible();

  await page
    .getByRole('button', { name: 'Add to cart' })
    .first()
    .click();

  await expect(
    page.locator('.shopping_cart_badge')
  ).toHaveText('1');
});