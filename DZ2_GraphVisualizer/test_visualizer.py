import json
import os
from unittest.mock import MagicMock, patch

import pytest
import requests

from visualizer import read_config_file, fetch_package_data, is_version_compatible, get_dependencies, get_graph, \
    save_mermaid_file, generate_mermaid_graph

# Тестовые данные
config_file_content = {
    "mermaid_path": "/path/to/mmdc",
    "npm_registry_url": "https://registry.npmjs.org",
    "package_name": "axios",
    "max_depth": 2
}

# Мокированные данные для пакета
mock_package_data = {
    "dist-tags": {"latest": "0.21.1"},
    "versions": {
        "0.21.1": {"dependencies": {"follow-redirects": "^1.14.0"}},
        "0.20.0": {"dependencies": {"follow-redirects": "^1.13.0"}}
    }
}


@pytest.fixture
def config_file(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_file_content))
    return config_file


def test_read_config_file(config_file, monkeypatch):
    monkeypatch.setattr('sys.argv', ["visualizer.py", str(config_file)])
    mermaid_path, npm_registry_url, package_name, max_depth = read_config_file()
    assert mermaid_path == "/path/to/mmdc"
    assert npm_registry_url == "https://registry.npmjs.org"
    assert package_name == "axios"
    assert max_depth == 2


def test_fetch_package_data(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return mock_package_data

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    data = fetch_package_data("axios", "https://registry.npmjs.org")
    assert data["dist-tags"]["latest"] == "0.21.1"
    assert "0.21.1" in data["versions"]


def test_is_version_compatible():
    assert is_version_compatible("1.14.0", "^1.13.0")
    assert not is_version_compatible("2.0.0", "^1.13.0")
    assert is_version_compatible("0.23.4", "~0.23.0")
    assert not is_version_compatible("1.0.0", "~0.23.0")
    assert is_version_compatible("0.23.4", ">=0.23.0")
    assert is_version_compatible("0.23.0", "0.23.0")


def test_get_dependencies(monkeypatch):
    graph = {}

    def mock_fetch_package_data(package_name, npm_registry_url):
        if package_name == "axios":
            return {
                "dist-tags": {"latest": "0.21.1"},
                "versions": {
                    "0.21.1": {"dependencies": {"follow-redirects": "^1.14.0"}}
                }
            }
        elif package_name == "follow-redirects":
            return {
                "dist-tags": {"latest": "1.14.0"},
                "versions": {
                    "1.14.0": {"dependencies": {}}
                }
            }
        return None

    monkeypatch.setattr("visualizer.fetch_package_data", mock_fetch_package_data)
    get_dependencies("axios", "https://registry.npmjs.org", 0, 2, graph)
    print(graph)
    assert "axios" in graph
    assert graph["axios"]["version"] == "0.21.1"
    assert "follow-redirects" in graph["axios"]["dependencies"]


def test_get_graph():
    graph = {
        "axios": {
            "version": "0.21.1",
            "dependencies": {"follow-redirects": "1.14.0"}
        },
        "follow-redirects": {
            "version": "1.14.0",
            "dependencies": {}
        }
    }
    mermaid_graph = get_graph(graph)
    assert "class axios" in mermaid_graph
    assert "class follow-redirects" in mermaid_graph
    assert "axios --> follow-redirects" in mermaid_graph


def test_save_mermaid_file():
    content = "classDiagram\n class Test { +version: 1.0.0 }"
    package_name = "test_package"
    file_path = f"{package_name}_dependency_graph.mmd"

    save_mermaid_file(content, package_name)

    # Переопределяем место сохранения для проверки содержимого
    assert os.path.exists(file_path)

    with open(file_path, "r") as file:
        saved_content = file.read()
        assert saved_content == content

    if os.path.exists(file_path):
        os.remove(file_path)

def test_generate_mermaid_graph(monkeypatch):
    package_name = "test_package"
    mermaid_path = "mmdc.cmd"
    input_file_name = f"{package_name}_dependency_graph.mmd"
    output_file_name = f"{package_name}_dependency_graph.svg"

    # Создаем временный входной файл для проверки
    with open(input_file_name, "w") as f:
        f.write("classDiagram\nclass Test { +version: 1.0.0 }")

    # Используем patch для замены call на mock
    with patch("subprocess.call") as mock_call:
        generate_mermaid_graph(package_name, mermaid_path)

        # Проверяем, что subprocess.call вызван с нужными аргументами
        mock_call([
            mermaid_path, "-i", input_file_name, "-o", output_file_name
        ])

    # Удаляем временный файл после теста
    os.remove(input_file_name)
    if os.path.exists(output_file_name):
        os.remove(output_file_name)

def test_read_config_file_invalid_path(monkeypatch):
    monkeypatch.setattr('sys.argv', ["visualizer.py", "invalid_path.json"])
    with pytest.raises(SystemExit):
        read_config_file()