from time import sleep

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.bgeneral.com/personas/banca-en-linea/")
    print(page.title())
    page.locator('#wt-cli-accept-all-btn').click()
    page.get_by_role('button', name='Banca en línea').click()
    sleep(1)
    # login = page.locator('#txtLoginD') # .fill('ddddd')
    login = page.wait_for_selector('#txtLoginD', state='attached') # .fill('ddddd')
    login.fill('5555')
    print(login)
    sleep(1)
    browser.close()
    print('Finished')

if __name__ == '__main__':
    sync_playwright()
