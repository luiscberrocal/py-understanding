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


def main():
    # Fetch and print the Python 3.10 tags
    # https://hub.docker.com/v2/repositories/library/postgres/tags
    python_310_tags = get_python_tags("3.11name")
    print("Python 3.10 tags:", python_310_tags)


if __name__ == '__main__':
    main()
