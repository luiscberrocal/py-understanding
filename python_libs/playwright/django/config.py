import json

from python_libs.playwright.django.constants import ENV_FOLDER
from python_libs.playwright.django.schemas import AdminConfigSchema


def get_configuration(service_key: str, environment: str) -> AdminConfigSchema:
    configuration_file = ENV_FOLDER / f"django_admin_{environment}_config.json"
    with open(configuration_file) as json_file:
        configuration = json.load(json_file)
    config_data = configuration[service_key]
    config_data['service_key'] = service_key
    admin_config = AdminConfigSchema(**config_data)
    return admin_config


if __name__ == '__main__':
    config = get_configuration('DLOC', 'production')
    print(config)