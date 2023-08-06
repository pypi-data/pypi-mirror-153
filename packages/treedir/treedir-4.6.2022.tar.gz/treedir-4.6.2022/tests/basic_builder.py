from anytree import RenderTree
from treedir import Builder
from rich import print


def test__builder__only_root(builder):
    schema = {"name": "only-root"}
    tree = builder.do_tree(schema)
    print("JSON Expresion")
    print(tree.toJSON())


def test__builder__root__files_one_level(builder):
    schema = {
        "name": "only-root",
        "files": [{"name": "test.org"}, {"name": "data.xlsx"}]
    }
    tree = builder.do_tree(schema)
    print("JSON Expresion")
    print(tree.toJSON())


def test__builder__root__files_and_dirs(builder):
    schema = {
        "name": "only-root",
        "files": [{"name": "test.org"}, {"name": "data.xlsx"}],
        "directories": [{"name": "mediciones"}, {"name": "documentos"}]
    }
    tree = builder.do_tree(schema)
    print("JSON Expresion")
    print(tree.toJSON())


def test__builder__file__deep_path(builder):
    schema = {
        "name": "only-root",
        "files": [{
            "name": "test.org",
            "deep_path": ["mediciones", "octubre", "juanito"]
        }, {
            "name": "puerta.txt",
            "deep_path": ["mediciones", "octubre", "juanito"]
        }, {
            "name": "ventanas.txt",
            "deep_path": ["mediciones", "noviembre", "pedrito"]
        },
        ],
    }
    tree = builder.do_tree(schema)
    print("JSON Expresion")
    print(tree.toJSON())


def test__builder__root__files_and_dirs_with_children(builder):
    """
    Se crea arbol de directorios que tengan subdirectorios también
    """
    schema = {
        "name": "only-root",
        "files": [{"name": "test.org"}, {"name": "data.xlsx"}],
        "directories": [{"name": "mediciones",
                         "children": ["agua", "temperatura"]},
                        {"name": "documentos"}]
    }
    tree = builder.do_tree(schema)
    print("JSON Expresion directorios with children")
    print(tree.toJSON())


if __name__ == '__main__':
    builder = Builder()
    test__builder__only_root(builder)
    test__builder__root__files_one_level(builder)
    test__builder__root__files_and_dirs(builder)
    test__builder__file__deep_path(builder)
    test__builder__root__files_and_dirs_with_children(builder)
