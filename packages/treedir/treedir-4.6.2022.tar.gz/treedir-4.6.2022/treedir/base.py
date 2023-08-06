from anytree import AnyNode
from anytree.node.nodemixin import NodeMixin
from abc import ABC, abstractmethod


from networktools.library import set_id


class TreeDir(NodeMixin):
    __node_types = {"directory", "file"}
    idx_list = []
    node_map = {}

    def __init__(self, name, parent, options={}, *args, **kwargs):
        super().__init__()
        self.name = name
        self.parent = parent
        self.options = options if options else {}
        self.idx = self.new_idx()
        if parent:
            self.node_map = parent.node_map
        else:
            self.set_idx_node("root")
        self.set_idx_node(self.idx)

    def new_idx(self):
        idx = set_id(self.idx_list, uin=12)
        return idx

    def get_node(self, idx):
        return self.node_map.get(idx)

    def set_idx_node(self, idx:str):        
        self.node_map[idx] = self

    @property
    def can_have_children(self):
        return self.__node_type == "directory"

    @property
    def filename(self) -> str:
        """
        return the filename as string
        """
        pass

    @property
    def url(self) -> str:
        """
        return the url as string
        """
        pass

    def get_dict(self):
        return {}

    def children_directories(self):
        """
        Return the children directory path generator for instance
        """
        pass
