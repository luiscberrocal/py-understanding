import requests


def get_python_tags(name: str):
    url = "https://hub.docker.com/v2/repositories/library/python/tags"
    params = {
        "page_size": 100,  # Adjust as necessary
        "name": name  # Filter for Python 3.10
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        tags_data = response.json()

        tags = [tag['name'] for tag in tags_data['results'] if name in tag['name']]
        return tags
    except requests.RequestException as e:
        print(f"Error fetching Python 3.10 tags: {e}")
        return []


def get_docker_tags(image: str, version: str) -> list[str]:
    url = f"https://hub.docker.com/v2/repositories/library/{image}/tags"
    params = {
        "page_size": 100,  # Adjust as necessary
        "name": version  # Filter for Python 3.10
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        tags_data = response.json()

        tags = [tag['name'] for tag in tags_data['results'] if version in tag['name']]
        return tags
    except requests.RequestException as e:
        print(f"Error fetching {image} for version {version} tags: {e}")
        return []


def main():
    # Fetch and print the Python 3.10 tags
    # https://hub.docker.com/v2/repositories/library/postgres/tags
    python_tags = get_docker_tags("python", "3.11")
    postgres_tags = get_docker_tags("postgres", "15")

    print("Python 3.11 tags:", python_tags)
    print("Postgres 15 tags:", postgres_tags)


if __name__ == '__main__':
    main()
