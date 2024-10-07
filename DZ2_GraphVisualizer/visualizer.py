import requests
import json
import os
import sys
from subprocess import call

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


def is_version_compatible(version, spec):
    # Преобразуем версию в массив чисел, игнорируя нестандартные элементы
    version_parts = [int(part) for part in version.split(".") if part.isdigit()]
    spec = spec.strip()

    # '^' - совместимая мажорная или минорная версия
    if spec.startswith("^"):
        base_version = [int(part) for part in spec[1:].split(".") if part.isdigit()]
        return version_parts >= base_version and version_parts[0] == base_version[0]

    # '~' - совместимая минорная версия
    elif spec.startswith("~"):
        base_version = [int(part) for part in spec[1:].split(".") if part.isdigit()]
        return version_parts >= base_version and version_parts[:2] == base_version[:2]

    # '>=', точная версия и простые версии
    elif spec.startswith(">="):
        base_version = [int(part) for part in spec[2:].split(".") if part.isdigit()]
        return version_parts >= base_version

    # Простой вариант точного совпадения версии
    else:
        base_version = [int(part) for part in spec.split(".") if part.isdigit()]
        return version_parts == base_version

def get_dependencies(package_name, npm_registry_url, depth, max_depth, graph):
    if depth > max_depth:
        return

    package_data = fetch_package_data(package_name, npm_registry_url)
    if not package_data:
        return

    latest_version = package_data['dist-tags']['latest']
    dependencies = package_data.get('versions', {}).get(latest_version, {}).get('dependencies', {})

    graph[package_name] = {
        'version': latest_version,
        'dependencies': {}
    }

    for dep, version_spec in dependencies.items():
        dep_data = fetch_package_data(dep, npm_registry_url)
        if not dep_data:
            continue

        dep_versions = dep_data.get('versions', {}).keys()
        suitable_version = None
        for version in sorted(dep_versions, reverse=True):
            if is_version_compatible(version, version_spec):
                suitable_version = version
                break

        if suitable_version:
            graph[package_name]['dependencies'][dep] = suitable_version
            get_dependencies(dep, npm_registry_url, depth + 1, max_depth, graph)

def get_graph(graph):
    mermaid_syntax = "classDiagram\n"
    for package, data in graph.items():
        # Определяем класс с массивом версий
        mermaid_syntax += f"  class {package} {{\n"
        mermaid_syntax += f"    +version: {data['version']}\n"
        mermaid_syntax += "  }\n"

        # Связи между пакетами
        for dep in data['dependencies']:
            if dep in graph:
                mermaid_syntax += f"  {package} --> {dep}\n"
            else:
                print(f"Предупреждение: Зависимость '{dep}' для пакета '{package}' не найдена.")

    return mermaid_syntax


def save_mermaid_file(content, package_name):
    file_name = f"{package_name}_dependency_graph.mmd"
    with open(file_name, "w") as file:
        file.write(content)
    print(f"Mermaid файл сохранен как {file_name} в папке с визуализатором")


def generate_mermaid_graph(package_name, mermaid_path):
    input_file = f"{package_name}_dependency_graph.mmd"
    output_file = f"{package_name}_dependency_graph.svg"
    try:
        call([mermaid_path, "-i", input_file, "-o", output_file])
        print(f"Граф успешно сгенерирован и сохранен как {output_file} в папке с визуализатором")
    except OSError as e:
        print(f"Ошибка при генерации графа: {e}")


def main():
    mermaid_path, npm_registry_url, package_name, max_depth = read_config_file()
    graph = {}

    package_data = fetch_package_data(package_name, npm_registry_url)
    if not package_data:
        print(f"Не удалось получить данные о пакете {package_name}")
        exit(1)

    print(f"Данные о пакете {package_name} успешно получены.")

    get_dependencies(package_name, npm_registry_url, 0, max_depth, graph)
    print(graph)
    mermaid_graph = get_graph(graph)

    save_mermaid_file(mermaid_graph, package_name)

    generate_mermaid_graph(package_name, mermaid_path)

if __name__ == "__main__":
    main()
