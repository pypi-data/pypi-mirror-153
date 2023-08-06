from saplings import Saplings
from rendering import render_tree, dictify_tree
from entities import ObjectNode
from utilities import init_namespace
import ast

node = ast.parse(open("test.py", "r").read())

# args = init_namespace(["set"])
# trees = Saplings(node, **args, track_modules=False).get_trees()
trees = Saplings(node).get_trees()

for root_node in trees:
    # print(dictify_tree(root_node))
    for branches, n in render_tree(root_node):
        print(f"{branches}{n}")

    print()
