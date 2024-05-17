from playwright.sync_api import sync_playwright

from python_libs.playwright.django.config import get_configuration, get_all_configurations
from python_libs.playwright.django.schemas import AdminConfigSchema


def check_admin(config_scheme: AdminConfigSchema):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(config_scheme.admin_url)
        print(page.title())


if __name__ == '__main__':
    # admin_config_schema = get_configuration('DLOC', 'production')
    # check_admin(admin_config_schema)
    admin_config_schemas = get_all_configurations('production')

    for admin_config_schema in admin_config_schemas:
        check_admin(admin_config_schema)
