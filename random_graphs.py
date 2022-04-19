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

    def store_network_as_txt_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.get_size()) + "\n")
            for (n1, n2) in self.edges:
                f.write(n1.value + " " + n2.value + "\n")


def main():
    # parameter for the Erdos-Renyi network creation
    """
    num_nodes_1 = 2000
    p_1 = 0.0001
    network_1 = ER_Network(num_nodes=num_nodes_1, p=p_1,)
    #network_1.print_network()
    filename_1 = "random1.txt"
    network_1.store_network_as_txt_file(filename_1)

    num_nodes_2 = 2000
    p_2 = 0.005
    network_2 = ER_Network(num_nodes=num_nodes_2, p=p_2,)
    #network_2.print_network()
    filename_2 = "random2.txt"
    network_2.store_network_as_txt_file(filename_2)
    """

    # parameter for the Barabasi-Albert network creation
    n_1 = 2000
    m0_1 = 3
    m_1 = 1

    filename_ba1 = "ba1.txt"

    n_2 = 2000
    m0_2 = 5
    m_2 = 2

    filename_ba2 = "ba2.txt"

if __name__ == "__main__":
    main()