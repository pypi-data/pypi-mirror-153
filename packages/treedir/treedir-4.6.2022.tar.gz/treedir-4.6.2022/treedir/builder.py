from .base import TreeDir
from anytree import RenderTree
import json
from django.utils.text import slugify


class FileNodeDir(TreeDir):
    """
    Is Node and implementation of TreeDir
    """
    __node_type = "file"

    def __init__(self,
                 name,
                 host="localhost",
                 port=80,
                 parent=None,
                 deep_path=[],
                 *args,
                 **kwargs):
        self.__name = name
        self.__deep_path = deep_path
        if deep_path and parent:
            deep_path.reverse()
            parent = self.build_tree(parent, deep_path)
            super().__init__(name, parent, *args, **kwargs)
        else:
            super().__init__(name, parent, *args, **kwargs)
        self.__host = host
        self.__port = port
        self.__parent = parent
        self.__kwargs = kwargs

    def toJSON(self, level=1):
        diccionario = {
            "idx": self.idx,
            "name": self.__name,
            "type": self.__node_type,
            "options": self.options
        }
        return diccionario

    def build_tree(self, parent, deep_path):
        while deep_path:
            directory = deep_path.pop()
            name = directory
            opts = {}
            if isinstance(directory, dict):
                name = directory.get("name")
                opts = directory.get("options")
            for child in parent.children:
                if name == child.name:
                    node = child
                    break
            else:
                node = DirNodeDir(name, parent=parent, options=opts)
            parent = node
        return parent

    @property
    def port(self):
        return self.__port

    @property
    def host(self):
        return self.__host

    @property
    def filename(self):
        return self.__name

    @property
    def url(self):
        if self.__deep_path:
            deep_path = "/".join(self.__deep_path)
            if self.port == 80:
                return f"{self.host}/{deep_path}/{self.filename}"
            else:
                return f"{self.host}:{self.port}/{deep_path}/{self.filename}"
        else:
            if self.port == 80:
                return f"{self.host}/{self.filename}"
            else:
                return f"{self.host}:{self.port}/{self.filename}"

    def get_dict(self):
        return {
            "name": self.filename,
            "host": self.host,
            "port": self.port,
            "url": self.url,
        }

    def children_directories(self):
        """
        Return the children directory path generator for instance
        """
        return []


class DirNodeDir(TreeDir):
    """
    Is Node and implementation of TreeDir
    """
    __node_type = "directory"

    def __init__(self, name,
                 parent=None,
                 deep_path=[],
                 *args,
                 **kwargs):
        self.__name = name
        self.__deep_path = deep_path
        if deep_path and parent:
            deep_path.reverse()
            parent = self.build_tree(parent, deep_path)
            super().__init__(name, parent, *args, **kwargs)
        else:
            super().__init__(name, parent, *args, **kwargs)
        self.__name = name
        self.__parent = parent
        self.__kwargs = kwargs

    def build_tree(self, parent, deep_path):
        while deep_path:
            name = deep_path.pop()
            for child in parent.children:
                if name == child.name:
                    node = child
                    break
            else:
                node = DirNodeDir(name, parent=parent)
            parent = node
        return parent

    def toJSON(self, level=2):
        """
        Level 2 means the node and one level of children
        """
        self.options["slug"] = slugify(self.__name)
        child_level = level - 1
        diccionario = {
            "idx": self.idx,
            "name": self.__name,
            "type": self.__node_type,
            "options": self.options,
            "children": [child.toJSON(child_level) for child in
                         self.children if isinstance(self, DirNodeDir)
                         if child_level>=1]
        }
        return diccionario

    @property
    def filename(self):
        return self.__name

    @property
    def url(self):
        return ""

    def get_dict(self):
        return {
            "name": self.filename,
            "type": self.__node_type,
            "children": []}

    def children_directories(self):
        """
        Return the children directory path generator for instance
        """
        return list(filter(lambda ch: ch.can_have_children,  self.children))


class Builder:
    __dirclass = None
    __fileclass = None

    def __init__(self,
                 dirclass=DirNodeDir,
                 fileclass=FileNodeDir):
        self.__dirclass = dirclass
        self.__fileclass = fileclass

    @property
    def dirclass(self):
        return self.__dirclass

    @property
    def fileclass(self):
        return self.__fileclass

    def do_tree(self, schema: dict) -> TreeDir:
        root = schema.get("name")
        root_opts = schema.get("options")
        if root:
            root_tree = self.dirclass(root, options=root_opts)
            directories = [self.dirclass(parent=root_tree,
                                         fileclass=self.fileclass,
                                         dirclass=self.dirclass,
                                         **opts)
                           for opts in schema.get("directories", {})]
            #do_tree_dir = [directory.do_tree() for directory in directories]
            files = [self.fileclass(parent=root_tree,
                                    fileclass=self.fileclass,
                                    dirclass=self.dirclass, **opts)
                     for opts in schema.get("files", {})]
            return root_tree
        else:
            return DirNodeDir("")
