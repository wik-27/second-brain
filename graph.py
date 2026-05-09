# This file defines the graph class - it will store all of the nodes

import json
import os

from node import Node

class Graph:
    def __init__(self, filepath = "second_brain.json"):
        self.filepath = filepath
        # Dictionary of nodes
        self.nodes = {}
        # When a graph is loaded, load everything that has existed previously
        self.load()

# Adds a new piece of knowledge to the graph
    def add_node(self, name, category, description=""):

        # Checks to see if a node with the same name already exists
        if name in self.nodes:
            print(f"A node called '{name}' already exists")
            return

        # Creating a new node using the imported Node
        new_node = Node(name=name, category=category, description=description)

        # Stores the new node in the dictionary using its own name as the key
        self.nodes[name] = new_node

        print(f"Added node: '{name}' ({category})")

        # Saves automatically as soon as something is added
        self.save()

    # Creating a connection between two existing nodes
    def add_connection(self, from_name, to_name, relationship):
        if from_name not in self.nodes:
            print(f"Cannot connect, '{from_name}' doesn't exist")
            return
        if to_name not in self.nodes:
            print(f"Cannot connect, '{to_name}' doesn't exist")
            return

        # Find the starting node and call the add_connection method
        self.nodes[from_name].add_connection(to_name, relationship)
        print(f"Connected {from_name} to {to_name} via {relationship}")

        self.save()

    # Finding a node using a key
    def get_node(self, name):
        return self.nodes.get(name, None)

    #Prints a summary of everything in the graph
    def summary(self):
        print(f"\n === Second Brain - {len(self.nodes)} nodes === ")

        if not self.nodes:
            print("The graph is empty")
            return

        for node in self.nodes.values():
            connection_count = len(node.connections)
            print(f" • {node.name} ({node.category}) - {connection_count} connection(s)")

    #Saving the entire thing into a JSON file to the disk via serialisation
    def save(self):
        data = {}
        for name, node in self.nodes.items():
            data[name] = {
                "name" : node.name,
                "category" : node.category,
                "description" : node.description,
                "connections" : node.connections,
                "metadata" : node.metadata
            }
        # Writes the data into a JSON file
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    #Loading the graph from the JSON file via deserialisation
    def load(self):
        if not os.path.exists(self.filepath):
            return

        with open(self.filepath, "r") as f:
            data = json.load(f)

        for name, node_data in data.items():
            node = Node(
                name = node_data["name"],
                category = node_data["category"],
                description = node_data["description"]
            )

            node.connections = node_data["connections"]
            node.metadata = node_data["metadata"]

            self.nodes[name] = node


# ==============================================================
# TEST AREA
# ==============================================================

if __name__ == "__main__":

    brain = Graph()

    brain.add_node("Paris", "Geography", "Capital city of France")
    brain.add_node("France", "Geography", "Country in western Europe")
    brain.add_node("Python", "Technology", "A programming language")
    brain.add_node("Wiktoria", "Person", "The architect of this second brain")

    brain.add_connection("Paris", "France", "capital of")
    brain.add_connection("France", "Paris", "contains capital")
    brain.add_connection("Wiktoria", "Python", "is learning")
    brain.add_connection("Wiktoria", "Paris", "wants to visit")

    brain.summary()

    node = brain.get_node("Wiktoria")
    if node:
        node.describe()

