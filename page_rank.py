import argparse
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

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
            pagerank_record = []
            # it has to be iterated again, because of the normalization
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

    def reset_pagerank(self):
        self.pagerank_history = []
        for node in self.nodes:
            node.pagerank = 1.0

    def get_pagerank_history(self):
        return self.pagerank_history.copy()

    def get_size(self):
        return len(self.nodes)

    def get_num_edges(self):
        return len(self.edges)

    def get_node_names(self):
        names = []
        for node in self.nodes:
            names.append(node.value)
        return names

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

    def plot_pagerank_history(self, beta, path, verbose):
        x = range(1, len(self.pagerank_history)+1) # [node.value for node in self.nodes] #["A", "B", "C"]
        y = self.pagerank_history # list(map(list, zip(*self.pagerank_history))) #[[1,2,3],[4,5,6],[7,8,9]]

        plt.clf()
        plt.xlabel("Iterations")
        plt.ylabel("PageRank Value")
        plt.title("PageRank History over " + str(len(self.pagerank_history)) + " Iterations with Beta " + str(beta))
        for i in range(len(y[0])):
            plt.plot(x,[pt[i] for pt in y],label = "Node "+self.nodes[i].value) #'id %s'%i)
        plt.legend()
        plt.savefig(path + 'pagerank-plot_' + str(beta).replace(".", "") + "-beta_" + str(len(self.pagerank_history)) + '-iterations.png')
        if verbose:
            plt.show()
        plt.clf()


def calculate_convergence(history):
    convergence_criteria = 0.001
    convergence_iteration = []
    history_transp = list(map(list, zip(*history)))
    for hindex, entry in enumerate(history_transp):
        #print(entry)
        already_below_criteria_once = False
        for eindex in range(len(entry)-1):
            if abs(entry[eindex]-entry[eindex+1]) < convergence_criteria:
                if already_below_criteria_once:
                    convergence_iteration.append(eindex)
                    break
                else:
                    already_below_criteria_once = True
    return max(convergence_iteration)


def plot_convergence(track, list_of_betas):
    print("Betas", list_of_betas, len(list_of_betas))
    print("Track", track, len(track))

    list_of_betas = [str(x) for x in list_of_betas]
    
    plt.figure(figsize = (8, 4))
    # creating the bar plot
    plt.bar(list_of_betas, track, color ='cornflowerblue')#, width = 0.4)
    
    plt.xlabel("Beta")
    plt.ylabel("# of iterations until convergence")
    plt.title("# of Iterations until Convergence for each Beta")
    plt.show()
    plt.clf()


def plot_final_pagerank(beta, rank, node_names, path, verbose):
    x = beta #[str(x) for x in list_of_betas] #range(1, len(self.rank[0])+1) # [node.value for node in self.nodes] #["A", "B", "C"]
    y = rank # list(map(list, zip(*self.pagerank_history))) #[[1,2,3],[4,5,6],[7,8,9]]

    plt.figure(figsize = (8, 4))
    plt.xlabel("Betas")
    plt.ylabel("Final PageRank Value")
    plt.title("Final PageRank Values")
    for i in range(len(y[0])):
        plt.plot(x,[pt[i] for pt in y],label = "Node "+node_names[i]) #'id %s'%i)
    plt.legend()
    plt.show()
    plt.clf()


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
    # Task 3 & 4
    # test parameter for the PageRank model
    pagerank_network = create_pagerank_network()
    pagerank_network.iterate_pagerank(beta=args.beta, iterations=args.iterations, verbose=args.verbose)
    pagerank_network.print_network()
    pagerank_network.plot_pagerank_history(args.beta, "pagerank_results/task4/", args.verbose)

    # Task 5
    convergence_track = []
    last_pagerank_values = []
    list_of_betas = [float(f'{x:.2f}') for x in list(np.arange(0.0, 1.01, 0.05))]
    for loop_beta in tqdm(list_of_betas):
        pagerank_network.reset_pagerank() # reset pageranks to 1.0, keep nodes and edges
        pagerank_network.iterate_pagerank(beta=loop_beta, iterations=args.iterations, verbose=False)
        if args.verbose:
            pagerank_network.plot_pagerank_history(loop_beta, "pagerank_results/task5/", verbose=False)
        
        pagerank_history = pagerank_network.get_pagerank_history()
        convergence_track.append(calculate_convergence(pagerank_history))
        last_pagerank_values.append(pagerank_history[-1].copy())
    
    # Task 5 a
    plot_convergence(convergence_track, list_of_betas)

    # Task 5 b
    plot_final_pagerank(list_of_betas, last_pagerank_values, pagerank_network.get_node_names(), "pagerank_results/task5/", False)


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
    parser.add_argument('-i', '--iterations', type=int, default=100, help='iterations of pagerank')
    parser.add_argument('-b', '--beta', type=range_limited_float_type, default=0.85, help='dampening factor for pagerank')
    parser.add_argument('-v', '--verbose', action='store_true', help='toggle informative prints')
    main(parser.parse_args())