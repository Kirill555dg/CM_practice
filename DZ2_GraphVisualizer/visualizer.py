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


def get_dependencies(package_name, npm_registry_url, depth, max_depth, graph):
    if depth > max_depth:
        return

    package_data = fetch_package_data(package_name, npm_registry_url)
    if not package_data:
        return

    # Извлекаем зависимости пакета
    dependencies = package_data.get('versions', {}).get(package_data['dist-tags']['latest'], {}).get('dependencies', {})
    graph[package_name] = list(dependencies.keys())

    # Рекурсивно обрабатываем каждую зависимость
    for dep in dependencies:
        get_dependencies(dep, npm_registry_url, depth + 1, max_depth, graph)


def generate_mermaid_graph(graph):
    mermaid_syntax = "graph TD;\n"
    for package, dependencies in graph.items():
        for dep in dependencies:
            mermaid_syntax += f"  {package} --> {dep};\n"
    return mermaid_syntax


def save_mermaid_file(content, package_name):
    file_name = f"{package_name}_dependency_graph.mmd"
    with open(file_name, "w") as file:
        file.write(content)
    print(f"Mermaid файл сохранен как {file_name} в папке с визуализатором")


def main():
    mermaid_path, npm_registry_url, package_name, max_depth = read_config_file()
    # Получение данных о пакете
    graph = {}

    package_data = fetch_package_data(package_name, npm_registry_url)
    if not package_data:
        print(f"Не удалось получить данные о пакете {package_name}")
        exit(1)

    print(f"Данные о пакете {package_name} успешно получены.")
    # print(json.dumps(package_data, indent=2))  # Красивый вывод JSON

    get_dependencies(package_name, npm_registry_url, 0, max_depth, graph)
    # print("Граф зависимостей пакета:")
    # print(json.dumps(graph, indent=2))
    mermaid_graph = generate_mermaid_graph(graph)

    save_mermaid_file(mermaid_graph, package_name)


if __name__ == "__main__":
    main()
