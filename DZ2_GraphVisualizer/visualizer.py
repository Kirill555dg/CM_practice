import requests
import json
import os
import sys

def read_config_file():
    if len(sys.argv) < 2:
        print("Для корректного запуска программы необходимо ввести: "
              "\"py visualizer.py <путь к конфигурационному файлу>\"")
        sys.exit(1)

    config_file_path = sys.argv[1]
    if not os.path.exists(config_file_path):
        print("Конфигурационный файл по заданному пути не найден.")
        sys.exit(1)
    if not config_file_path.endswith(".json"):
        print("Указанный конфигурационный файл должен быть формата JSON.")
        sys.exit(1)

    try:
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        print("Конфигурационный файл имеет неверный формат JSON.")
        sys.exit(1)

    keys = ["mermaid_path", "npm_registry_url", "package_name", "max_depth"]
    for key in keys:
        if key not in config:
            print(f"В конфигурационном файле отсутствует обязательный ключ: {key}")
            sys.exit(1)

    return config["mermaid_path"], config["npm_registry_url"], config["package_name"], config["max_depth"]



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
    mermaid_path, npm_registry_url, package_name, max_depth = read_config_file()
    # Получение данных о пакете
    package_data = fetch_package_data(package_name, npm_registry_url)
    if package_data:
        print(f"Данные о пакете {package_name} успешно получены.")
        # print(json.dumps(package_data, indent=2))  # Красивый вывод JSON
    else:
        print("Не удалось получить данные о пакете.")

if __name__ == "__main__":
   main()
