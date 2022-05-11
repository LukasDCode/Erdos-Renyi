import random

class Node:
    def __init__(self, value):
        # no checks for the value or anything, everything is force-parsed into a string
        self.value = str(value)
        self.edges = []

    def __repr__(self):
        return self.value

    def add_edge(self, node):
        # only adds the edge to the list if it is not there already
        if node not in self.edges:
            self.edges.append(node)
    
    def remove_edge(self, node):
        # only removes the edge if it is in the list
        if node in self.edges:
            self.edges.remove(node)


class Manual_Network():
    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)
        for edge_out in node.edges:
            self.edges.append((node, edge_out))

    def calculate_pagerank(self, verbose):
        # initialize with 1/n
        ranks = [1/self.get_size()] * self.get_size()
        iteration_counter = 0
        meaningful_changes = True
        while meaningful_changes:
            # TODO actual PageRank
            iteration_counter += 1
            if True: #TODO some other criteria
                meaningful_changes = False
            if verbose:
                print("iteration:", iteration_counter)
                for node, rank in zip(self.nodes, ranks):
                    print(node, rank)
                print("\n")
                

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


def create_pagerank_network():
    # create empty network
    network = Manual_Network()
    # create nodes
    node_A = Node("A")
    node_B = Node("B")
    node_C = Node("C")
    node_D = Node("D")
    node_E = Node("E")
    node_F = Node("F")
    node_G = Node("G")

    # draw edges between nodes
    node_A.add_edge(node_B)
    node_B.add_edge(node_C)
    node_B.add_edge(node_D)
    node_B.add_edge(node_E)
    node_C.add_edge(node_D)
    node_D.add_edge(node_B)
    node_E.add_edge(node_D)
    node_B.add_edge(node_F)
    node_F.add_edge(node_G)
    node_G.add_edge(node_F)

    # add nodes to network
    network.add_node(node_A)
    network.add_node(node_B)
    network.add_node(node_C)
    network.add_node(node_D)
    network.add_node(node_E)
    network.add_node(node_F)
    network.add_node(node_G)

    return network


def main():
    # -------------------------------------------------------

    # test parameter for the PageRank model
    pagerank_network = create_pagerank_network()
    print("# of edges", pagerank_network.get_num_edges())
    pagerank_network.print_network()
    pagerank_network.calculate_pagerank(verbose=True)

if __name__ == "__main__":
    main()