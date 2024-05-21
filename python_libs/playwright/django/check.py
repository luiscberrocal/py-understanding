from time import sleep
from typing import List, Dict

from playwright.sync_api import sync_playwright

from python_libs.playwright.django.config import get_all_configurations, get_configuration
from python_libs.playwright.django.django_admin import do_login
from python_libs.playwright.django.schemas import AdminConfigSchema


def check_admin(config_scheme: AdminConfigSchema):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(config_scheme.admin_url)
        print(page.title())
        do_login(page, config_scheme)
        existing_users = do_get_users(page)
        for user in existing_users:
            print(user)
        sleep(1)
        browser.close()


def do_get_users2(page) -> List[str]:
    page.locator('tr.model-user th a').click()
    page.locator('#content > h1').click()

    users = page.locator('table#result_list tbody tr')
    existing_users = [username.text_content() for username in users.all()]
    return existing_users


def do_get_users(page) -> List[Dict[str, str]]:
    page.locator('tr.model-user th a').click()
    page.locator('#content > h1').click()

    rows = page.locator('table#result_list tbody tr')
    users_data = []
    for row in rows.all():
        columns = row.locator('th')
        for column in columns.all():
            users_data.append(column.inner_text())
    return users_data

if __name__ == '__main__':
    service_key = None
    if service_key:
        admin_config_schema = get_configuration(service_key, 'production')
        check_admin(admin_config_schema)
    else:
        admin_config_schemas = get_all_configurations('production')

        for admin_config_schema in admin_config_schemas:
            check_admin(admin_config_schema)
            print('-' * 120)
