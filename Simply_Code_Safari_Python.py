#!/usr/bin/env python3
import ast
import os
import pydot

def parse_imports(file_path, parent_folder):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    if alias.asname not in imports:
                        imports.append(alias.asname)
                else:
                    if alias.name not in imports:
                        imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module not in imports:
                imports.append(node.module)
                for alias in node.names:
                    if alias.asname:
                        if alias.asname not in imports:
                            imports.append(alias.asname)
                    else:
                        if alias.name not in imports:
                            imports.append(alias.name)
    return [os.path.join(parent_folder, i + ".py") for i in imports if i + ".py" in os.listdir(parent_folder)]



def build_graph(folder_path):
    graph = pydot.Dot(graph_type="digraph", rankdir="UD")
    graph_with_label = pydot.Dot(graph_type="digraph", rankdir="UD")

    for parent, _, filenames in os.walk(folder_path):
        py_files = [f for f in os.listdir(parent) if f.endswith(".py")]
        for filename in filenames:
            if not filename.endswith(".py"):
                continue

            file_path = os.path.join(parent, filename)
            for imported_module in parse_imports(file_path, parent):
                print(imported_module)
                edge = pydot.Edge(imported_module, os.path.join(parent, filename), len=1.0, fillcolor="red")
                #edge_with_label = pydot.Edge(imported_module, os.path.join(parent, filename), label=f"import {os.path.basename(imported_module)}", len=1.0, fillcolor="red")

                graph.add_edge(edge)
                #graph_with_label.add_edge(edge_with_label)

    graph.write_png("code_map.png")
    #graph_with_label.write_png("code_map_with_labels.png")

if __name__ == "__main__":
    build_graph("./")
