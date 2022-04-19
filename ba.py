class Node:
    def __init__(self, value):
        # no checks for the value or anything, everything is force-parsed into a string
        self.value = str(value)
        self.edges = []

    def add_edge(self, node):
        # only adds the edge to the list if it is not there already
        if node not in self.edges:
            self.edges.append(node)
    
    def remove_edge(self, node):
        # only removes the edge if it is in the list
        if node in self.edges:
            self.edges.remove(node)


class Network:
    def __init__(self):
        self.nodes = []

    def __init__(self, num_nodes):
        self.nodes = []

    def add_node(self, a_node, p):
        if a_node not in self.nodes:
            self.nodes.append(a_node)
            # TODO set the edges for both nodes with probability p

    def remove_node(self, r_node):
        if r_node in self.nodes:
            for node in self.nodes:
                node.remove_edge(r_node)
            self.nodes.remove(r_node)

def create_erdos_renyi_network(p, num_nodes=2000):
    network = Network()
    for value in range(num_nodes):
        node = Node(value)
        network.add_node(node, p)
    
    



def main():
    s = "string"
    v = str(s)
    print(v)

    num_nodes = 2000
    p = 0.0001 # 0.005
    network = create_erdos_renyi_network(p=p, num_nodes=num_nodes)

if __name__ == "__main__":
    main()