import json
import os
from pathlib import Path
from time import sleep
from typing import List, Dict, Any

from playwright.sync_api import sync_playwright

from python_libs.internet_speed.check_speed import load_environment_variables
from python_libs.playwright.django.schemas import AdminConfigSchema


def generate_random_pwd():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase
                                  + string.digits + string.ascii_lowercase, k=64))


def create_super_users(prefix: str, users_list: List[str]) -> List[Dict[str, Any]]:
    results = []
    load_environment_variables('playwright/django_admin_vars.txt')
    url = os.getenv(f'{prefix}_ADMIN_URL')
    username = os.getenv(f'{prefix}_ADMIN_USERNAME')
    pwd = os.getenv(f'{prefix}_ADMIN_PASSWORD')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        print(page.title())
        do_login_deprecated(page, pwd, username)

        # Got to users
        page.locator('tr.model-user th a').click()
        page.locator('#content > h1').click()

        users = page.locator('table#result_list tbody tr')
        print(users.count())
        existing_users = [username.text_content() for username in users.all()]
        for username in users_list:
            if username in existing_users:
                print(f'User {username} already exists')
                continue
            user_pwd = generate_random_pwd()
            user_dict = {"username": username, "password": user_pwd, "admin_url": url}
            results.append(user_dict)
            create_user(page, user_pwd, username)
            page.locator('#id_email').fill(f'{username}@payjoy.com')
            page.locator('#id_is_staff').check()
            page.locator('#id_is_superuser').check()
            page.locator('input[type="submit"][name="_save"]').click()

        # content-main > ul > li > a
        sleep(2)
        browser.close()
        print('Finished')
        return results


def do_login_deprecated(page, pwd, username):
    page.locator('#id_username').fill(username)
    page.locator('#id_password').fill(pwd)
    page.locator('.submit-row').click()


def do_login(page, admin_config: AdminConfigSchema):
    page.locator('#id_username').fill(admin_config.username)
    page.locator('#id_password').fill(admin_config.password)
    page.locator('.submit-row').click()


def create_user(page, user_pwd, username):
    page.locator('#content-main ul.object-tools li a.addlink').click()
    page.locator('#id_username').fill(username)
    page.locator('#id_password1').fill(user_pwd)
    page.locator('#id_password2').fill(user_pwd)
    page.locator('input[type="submit"][name="_save"]').click()


def create_cx_users(prefix: str, users_list: List[str], environment: str = 'PRODUCTION') -> List[Dict[str, Any]]:
    results = []
    if environment == 'PRODUCTION':
        load_environment_variables('playwright/django_admin_vars.txt')
    else:
        load_environment_variables('playwright/django_admin_staging_vars.txt')

    url = os.getenv(f'{prefix}_ADMIN_URL')
    username = os.getenv(f'{prefix}_ADMIN_USERNAME')
    pwd = os.getenv(f'{prefix}_ADMIN_PASSWORD')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        print(page.title())
        do_login_deprecated(page, pwd, username)

        # Got to users
        page.locator('tr.model-user th a').click()
        page.locator('#content > h1').click()

        users = page.locator('table#result_list tbody tr')
        print(users.count())
        existing_users = [username.text_content() for username in users.all()]
        for username in users_list:
            if username in existing_users:
                print(f'User {username} already exists')
                continue
            user_pwd = generate_random_pwd()
            user_dict = {"username": username, "password": user_pwd, "admin_url": url}
            results.append(user_dict)
            create_user(page, user_pwd, username)
            page.locator('#id_email').fill(f'{username}@payjoy.com')
            page.locator('#id_is_staff').check()
            # page.locator('option[title="pj_django_payments | payment | Can view payment"]').dblclick()
            # page.locator(
            #     'option[title="pj_django_payments | customer information | Can view customer information"]').dblclick()

            page.locator('input[type="submit"][name="_save"]').click()

        # content-main > ul > li > a
        sleep(2)
        browser.close()
        print('Finished')
        return results


# result_list > tbody > tr:nth-child(1) > th
# content > h1
if __name__ == '__main__':
    service_prefix = 'WUI'
    environment = 'PRODUCTION'

    admin_users_list = [
        #    'vijay.chinnakannan',
        #    'jorge.alviarez',
        'elio.linarez',
        'arturo.chong'
    ]
    cx_user_list = ['amanda.amaral']
    test_user_list = ['javier.mora', ]
    # results = create_super_users(service_prefix, users_list=admin_users_list)

    results = create_cx_users(service_prefix, users_list=test_user_list, environment=environment)

    output_folder = Path(__file__).parent.parent.parent / 'output'
    for user in results:
        filename = output_folder / f'{service_prefix.lower()}_{user["username"]}.json'
        with open(filename, 'w') as f:
            json.dump(user, f, indent=4)
        print(f'Saved file {filename}')
