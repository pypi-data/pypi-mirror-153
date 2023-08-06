from anytree import RenderTree
from treedir import Builder
from rich import print


from formic import FileSet
from pathlib import Path
import os, time

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_bytes):
    """
    this function will return the file size
    """
    return convert_bytes(file_bytes)


def test_formic_builder(builder):
    path = "~/Documentos/EjericioProgramacion"	
    if path.startswith("~"):
        home = Path.home()
        path = path.replace("~", str(home))
    fileset = FileSet(
        directory=path,
        include=["*.org","*.md", "*.pdf", "*.*d.Z"])
    schema = {
        "name": "GNSS",  
        "type":"directory", 
        "options": {},
        "files": []
    }
    for item in fileset: 
        print(item)
        filepath = Path(item)
        base_url = str(filepath.parent).replace(path, "")
        parent = [d for d in base_url.split("/") if d]
        stats = filepath.stat() 
        fsize = file_size(stats.st_size)
        created = time.ctime(stats.st_mtime)
        node = {
            "name": filepath.name,
            "deep_path": parent,
            "type":"file",
            "options":{
                "size": fsize,
                "created": created,
                "url": f"{base_url}/{filepath.name}"
            }
        }
        schema["files"].append(node)
    print(schema)
    tree = builder.do_tree(schema)
    print(tree.toJSON())

if __name__ == '__main__':
    builder = Builder()
    test_formic_builder(builder)
