import random

class Node:
    def __init__(self, value):
        # no checks for the value or anything, everything is force-parsed into a string
        self.value = str(value)
        self.edges = []

    def __repr__(self):
        return "N"+self.value

    def add_edge(self, node):
        # only adds the edge to the list if it is not there already
        if node not in self.edges:
            self.edges.append(node)
    
    def remove_edge(self, node):
        # only removes the edge if it is in the list
        if node in self.edges:
            self.edges.remove(node)


class ER_Network:
    def __init__(self, num_nodes, p):
        self.nodes = []
        self.edges = []
        for value in range(num_nodes):
            new_node = Node(value)
            for node in self.nodes:
                # only smaller, not smaller-equals, because range goes [0;1[
                if random.random() < p:
                    new_node.add_edge(node)
                    node.add_edge(new_node)
                    self.edges.append((node, new_node)) # stores edge as a tuple
            self.nodes.append(new_node)

    def get_size(self):
        return len(self.nodes)

    def get_num_edges(self):
        return len(self.edges)

    def print_network(self):
        print("Nodes", len(self.nodes), self.nodes)
        print("Edges", len(self.edges), self.edges)

    def store_network_


def main():
    num_nodes = 20 #2000
    p = 0.5 # 0.0001 # 0.005
    network = ER_Network(p=p, num_nodes=num_nodes)

    network.print_network()

if __name__ == "__main__":
    main()