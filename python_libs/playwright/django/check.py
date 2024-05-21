from time import sleep
from typing import List, Dict, Any

from playwright.sync_api import sync_playwright

from python_libs.playwright.django.config import get_all_configurations, get_configuration
from python_libs.playwright.django.django_admin import do_login
from python_libs.playwright.django.schemas import AdminConfigSchema


def check_admin(config_scheme: AdminConfigSchema) -> Dict[str, Any]:
    check_data = {"users": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(config_scheme.admin_url)
        print(f"{page.title()} ({config_scheme.service_key})")
        do_login(page, config_scheme)
        existing_users: List[str] = do_get_users(page)
        # for user in existing_users:
        #     print(user)
        check_data["users"] = existing_users
        sleep(1)
        browser.close()
    return check_data


def do_get_users(page) -> List[str]:
    page.locator('tr.model-user th a').click()
    page.locator('#content > h1').click()

    rows = page.locator('table#result_list tbody tr')
    users_data = []
    for row in rows.all():
        columns = row.locator('th')
        for column in columns.all():
            users_data.append(column.inner_text())
    return users_data


def main_check():
    service_key = None
    print_users = False
    if service_key:
        admin_config_schema = get_configuration(service_key, 'production')
        check_data = check_admin(admin_config_schema)
        print(f"user count: {len(check_data['users'])}")
        if print_users:
            for user in check_data['users']:
                print(user)
    else:
        admin_config_schemas = get_all_configurations('production')

        for admin_config_schema in admin_config_schemas:
            check_data = check_admin(admin_config_schema)
            print(f"user count: {len(check_data['users'])}")
            if print_users:
                for user in check_data['users']:
                    print(user)
            print('-' * 120)


if __name__ == '__main__':
    main_check()
