import requests
import json

def load_config(config_file="config.json"):
    try:
        with open(config_file, "r") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("Конфигурационный файл не найден!")
        return None

def fetch_package_data(package_name, npm_registry_url):
    url = f"{npm_registry_url}/{package_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Не удалось получить данные для пакета {package_name}: {e}")
        return None

def main():
    config = load_config()
    if config:
        package_data = fetch_package_data(config["packageName"], config["npmRegistryUrl"])
        if package_data:
            print(f"Данные о пакете {config['packageName']}:")
            print(json.dumps(package_data, indent=2))  # Красивый вывод JSON
        else:
            print("Не удалось получить данные о пакете.")
    else:
        print("Ошибка загрузки конфигурации.")

if __name__ == "__main__":
    main()
