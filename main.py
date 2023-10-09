import requests
import json

def get_dependencies(package_name):
    """
    Возвращает список зависимостей пакета npm.

    Args:
        package_name: Имя пакета npm.

    Returns:
        Список зависимостей пакета.
    """

    url = f"https://registry.npmjs.org/package/{package_name}/dist-tags/latest"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["dependencies"]

def generate_graph(dependencies):
    """
    Генерирует граф зависимостей пакета npm.

    Args:
        dependencies: Список зависимостей пакета.

    Returns:
        Текст графа зависимостей на языке Graphviz.
    """

    graph = ""
    for dependency in dependencies:
        graph += f"    {dependency} -> {dependency}\n"
        for child_dependency in dependencies[dependency]:
            graph += f"    {dependency} -> {child_dependency}\n"
    return graph

def main():
    """
    Основная функция.
    """

    package_name = input("Введите имя пакета npm: ")
    dependencies = get_dependencies(package_name)
    graph = generate_graph(dependencies)
    print(graph)

if __name__ == "__main__":
    main()
