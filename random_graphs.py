import random
import copy

class Node:
    def __init__(self, value):
        # no checks for the value or anything, everything is force-parsed into a string
        self.value = str(value)
        self.edges = []

    def __repr__(self):
        return "N"+self.value # the 'N' to clarify it is a Node

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


class BA_Network:
    def __init__(self, num_nodes, m0, m):
        self.nodes = []
        self.edges = [] # stores edges as tuples
        self.nodes_pref = []

        # create fully-connected graph
        for value in range(m0):
            new_node = Node(value)
            for node in self.nodes:
                new_node.add_edge(node)
                node.add_edge(new_node)
                self.edges.append((node, new_node)) # stores edge as a tuple
            self.nodes.append(new_node)

        # initialize preferential priority list
        for node in self.nodes:
            for _ in range(len(node.edges)):
                self.nodes_pref.append(node)

        # attach other nodes with preferential attachment
        for value in range(m0, num_nodes):
            new_node = Node(value)
            m_now = min(m, len(self.nodes)) # check if m smaller than amount of all nodes
            sample_list = self.__get_sample_from_pref_list(copy.copy(self.nodes_pref), m_now)
            for node in sample_list:
                new_node.add_edge(node)
                node.add_edge(new_node)
                self.edges.append((node, new_node)) # stores edge as a tuple
                self.nodes_pref.extend([node, new_node]) # updates pref attachment list
            self.nodes.append(new_node)

    def __get_sample_from_pref_list(self, pref_list, m):
        result = []
        for _ in range(m):
            random_node = random.choice(pref_list)
            result.append(random_node)
            # Source of the following line: https://stackoverflow.com/a/1157160 (modified)
            pref_list = list(filter(lambda a: a.value != random_node.value, pref_list))
            # attention: the above line only works, because every node value is unique
        return result


    def get_size(self):
        return len(self.nodes)

    def get_num_edges(self):
        return len(self.edges)

    def print_network(self):
        print("Nodes", len(self.nodes))#, self.nodes)
        print("Edges", len(self.edges))#, self.edges)
        print("Prefs", len(self.nodes_pref))#, self.nodes_pref)

    def store_network_as_txt_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.get_size()) + "\n")
            for (n1, n2) in self.edges:
                f.write(n1.value + " " + n2.value + "\n")


def main():

    # parameter for the Erdos-Renyi network creation
    
    num_nodes_1 = 2000
    p_1 = 0.0001
    network_1 = ER_Network(num_nodes=num_nodes_1, p=p_1,)
    #network_1.print_network()
    filename_1 = "graph_results/random1.txt"
    network_1.store_network_as_txt_file(filename_1)

    num_nodes_2 = 2000
    p_2 = 0.005
    network_2 = ER_Network(num_nodes=num_nodes_2, p=p_2,)
    #network_2.print_network()
    filename_2 = "graph_results/random2.txt"
    network_2.store_network_as_txt_file(filename_2)
    

    # -------------------------------------------------------

    # parameter for the Barabasi-Albert network creation
    n_1 = 2000
    m0_1 = 3
    m_1 = 1
    network_3 = BA_Network(n_1, m0_1, m_1)
    filename_ba1 = "graph_results/ba1.txt"
    network_3.print_network()
    network_3.store_network_as_txt_file(filename_ba1)

    
    n_2 = 2000
    m0_2 = 5
    m_2 = 2
    network_4 = BA_Network(n_2, m0_2, m_2)
    filename_ba2 = "graph_results/ba2.txt"
    network_4.print_network()
    network_4.store_network_as_txt_file(filename_ba2)
    
    # -------------------------------------------------------

    # test parameter for both models
    """
    num_nodes_test = 2000
    p_test = 0.0001
    network_er_test = ER_Network(num_nodes=num_nodes_test, p=p_test,)
    network_er_test.print_network()
    
    n_test = 8
    m0_test = 4
    m_test = 4
    network_test = BA_Network(n_test, m0_test, m_test)
    network_test.print_network()
    """

if __name__ == "__main__":
    main()