import re
from time import sleep

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.bgeneral.com/personas/banca-en-linea/")
    page.get_by_role("button", name="Enterado").click()
    page.get_by_role("button", name=" Banca en línea").click()
    page.frame_locator("#inbank").get_by_placeholder("Usuario").click()
    page.frame_locator("#inbank").get_by_placeholder("Usuario").fill("xxx")
    sleep(1)
    with page.expect_popup() as page1_info:
        page.frame_locator("#inbank").get_by_role("button").click()
    page1 = page1_info.value
    sleep(2)
    # ---------------------
    context.close()
    browser.close()




if __name__ == '__main__':
    with sync_playwright() as playwright:
        run(playwright)
