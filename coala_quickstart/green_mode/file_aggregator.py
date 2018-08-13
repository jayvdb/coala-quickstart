import os

from coala_quickstart.green_mode.find_globs import (
    find_globs_from_files,
    )


class Node:
    """
    Tree data-structure that has each directory as a node,
    each subdirectory as children and files as leaves.
    """

    def __init__(self, name, parent, children=[]):
        self.name = name
        self.parent = parent
        self.children = children

    def add_children(self, children):
        self.children.append(children)

    def search_name(self, name):
        if name == self.name:  # pragma: no cover
            return self
        for child in self.children:
            if child.name == name:
                return child
        for child in self.children:
            found_node = child.search_name(name)
            if found_node is not None:  # pragma: no cover
                return found_node
        return None

    def get_files(self, initials):
        for child in self.children:
            name = initials + os.sep + child.name
            # FIXME: What happens in case of empty directories?
            if child.children == []:
                yield name
            else:
                yield from child.get_files(name)

    def get_files_cd(self, initials):
        for child in self.children:
            name = initials + os.sep + child.name
            if child.children == []:
                yield name


def aggregate_files(files, project_dir):
    """
    Aggregates the files field into ignore field and globs.
    :param files:
        The list of files in the files field for a particular
        section.
    :param project_dir:
        The project directory.
    :return:
        The changed files list with globs in it and the ignored
        files list.
    """
    root = Node('project_dir', None, [])
    for file in files:
        file_ = file.replace(project_dir, '')[1:]
        names = file_.split(os.sep)
        root_node = root
        for name in names:
            if not name:
                continue
            node = root_node.search_name(name)
            if node is None:
                new_node = Node(name, root_node, [])
                root_node.add_children(new_node)
                root_node = new_node
            else:
                root_node = node

    dummy = Node('dummy', None, [root])
    files, ignore_list = find_globs_from_files(
        dummy, '', project_dir, files, [], [])
    return files, ignore_list
