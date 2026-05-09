# Defining what a node is
# A node is a fundamental unit of knowledge here
# Every concept, fact or idea will be added as an instance of this class

class Node:
    """
    A Node represents a single piece of knowledge in the second brain. 

    Think of it as one bubble in the network topology graph - 
    it has its own identity, category and connections to other bubbles. 
    """

    def __init__(self, name, category, description=""):
        self.name = name
        self.category = category
        self.description = description

        self.connections = []

        self.metadata = {}

    def add_connection(self, other_node_name, relationship):
        connection ={
            "to": other_node_name,
            "relationship" : relationship
        }

        self.connections.append(connection)

    def describe(self):
        print(f"\n --- Node: {self.name} ---")
        print(f"Category: {self.category}")

        if self.description:
            print(f"Description: {self.description}")

        if self.connections:
            print("Connections:")
            for conn in self.connections:
                print(f" -> {conn['relationship']} -> {conn['to']}")
        else:
            print("Connections: none yet")


# ======================================================================
# Test Area
# ======================================================================

if __name__ == "__main__":
    paris = Node(
        name="Paris",
        category="Geography",
        description="The capital city of France, located in Europe"
    )

    france = Node(
        name="France",
        category="Geography",
        description="Country located in south western Europe"
    )

    paris.add_connection("France", "capital of")
    france.add_connection("Paris", "contains capital")

    paris.describe()
    france.describe()



