import argparse
import matplotlib.pyplot as plt

class Node:
    def __init__(self, value):
        # no checks for the value or anything, everything is force-parsed into a string
        self.value = str(value)
        self.children = []
        self.parents = []
        self.pagerank = 1.0

    def __repr__(self):
        return self.value

    def add_edge(self, node):
        # only adds the edge to the list if it is not there already
        if node not in self.children:
            self.children.append(node)
        if self not in node.parents:
            node.parents.append(self)
    
    def remove_edge(self, node):
        # only removes the edge if it is in the list
        if node in self.children:
            self.children.remove(node)
        if self in node.parents:
            node.parents.remove(self)

    def calculate_pagerank(self, beta, num_all_nodes, iteration, verbose):
        """
        Inspiration taken from https://towardsdatascience.com/pagerank-3c568a7d2332
        """
        importance = 0
        for parent in self.parents:
            importance += parent.pagerank / len(parent.children)
        random_teleport = (1-beta) / num_all_nodes
        rank = random_teleport + beta*importance

        if verbose:
            print("Node " + str(self.value) + ": " + str("{:10.8f}".format(rank)) + " at iteration " + str(iteration))
        self.pagerank = rank


class Manual_Network():
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.pagerank_history = []

    def add_node(self, node):
        self.nodes.append(node)
        for edge_out in node.children:
            self.edges.append((node, edge_out))

    def iterate_pagerank(self, beta, iterations, verbose):
        """
        Inspiration taken from https://towardsdatascience.com/pagerank-3c568a7d2332
        """
        for iteration in range(iterations):
            for node in self.nodes:
                node.calculate_pagerank(beta, self.get_size(), iteration+1, verbose)
            self.normalize_pagerank()
            if verbose:
                pagerank_record = []
                for node in self.nodes:
                    pagerank_record.append(node.pagerank)
                self.pagerank_history.append(pagerank_record)

    def normalize_pagerank(self):
        """
        Inspiration taken from https://towardsdatascience.com/pagerank-3c568a7d2332
        """
        pagerank_sum = sum(node.pagerank for node in self.nodes)
        for node in self.nodes:
            node.pagerank /= pagerank_sum

    def get_size(self):
        return len(self.nodes)

    def get_num_edges(self):
        return len(self.edges)

    def print_network(self):
        print("Nodes", len(self.nodes), self.nodes)
        print("Edges", len(self.edges), self.edges)
        page_rank_string = ""
        for node in self.nodes:
            page_rank_string += str(node.value) + ": " + str(node.pagerank) + "; "
        print("PageRank Selfmade:", page_rank_string[:-2])

    def store_network_as_txt_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.get_size()) + "\n")
            for (n1, n2) in self.edges:
                f.write(n1.value + " " + n2.value + "\n")

    def plot_pagerank_history(self, verbose):

        print(self.pagerank_history)
        print(len(self.pagerank_history))

        x = range(1, len(self.pagerank_history)+1) # [node.value for node in self.nodes] #["A", "B", "C"]
        y = self.pagerank_history # list(map(list, zip(*self.pagerank_history))) #[[1,2,3],[4,5,6],[7,8,9]]
        plt.xlabel("Iterations")
        plt.ylabel("PageRank Value")
        plt.title("PageRank History over " + str(len(self.pagerank_history)) + " Iterations")
        for i in range(len(y[0])):
            plt.plot(x,[pt[i] for pt in y],label = "Node "+self.nodes[i].value) #'id %s'%i)
        plt.legend()
        plt.savefig('graph_results/pagerank-plot_' + str(len(self.pagerank_history)) + '-iterations.png')
        if verbose:
            plt.show()


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


def main(args):
    # test parameter for the PageRank model
    pagerank_network = create_pagerank_network()
    print("# of edges", pagerank_network.get_num_edges())    
    pagerank_network.iterate_pagerank(beta=args.beta, iterations=args.iterations, verbose=args.verbose)
    pagerank_network.print_network()
    pagerank_network.plot_pagerank_history(args.verbose)


def range_limited_float_type(arg):
    """
    Taken from https://stackoverflow.com/a/55410582
    Type function for argparse - a float within some predefined bounds
    """
    try:
        f = float(arg)
    except ValueError:    
        raise argparse.ArgumentTypeError("Must be a floating point number")
    if f < 0.0 or f > 1.0:
        raise argparse.ArgumentTypeError("Argument must be < " + str(1.0) + "and > " + str(0.0))
    return f

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--iterations', type=int, default=5, help='iterations of pagerank')
    parser.add_argument('-b', '--beta', type=range_limited_float_type, default=0.85, help='dampening factor for pagerank')
    parser.add_argument('-v', '--verbose', action='store_true', help='toggle informative prints')
    main(parser.parse_args())