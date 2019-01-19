import time


class GraphNode:
    def __init__(self, address):
        """

        :param address: (ip, port)
        :type address: tuple

        """
        self.address = address
        self.parent = None
        self.right = None
        self.left = None
        self.alive = False

    def set_parent(self, parent):
        self.parent = parent

    def set_address(self, new_address):
        self.address = new_address

    def __reset(self):
        self.parent = None
        self.right = None
        self.left = None
        self.alive = False

    def add_child(self, child):
        if self.right is None:
            self.right = child
        else:
            self.left = child

    def can_be_neighbour(self):
        return not (self.right and self.left)


class NetworkGraph:
    def __init__(self, root):
        self.root = root
        root.alive = True
        self.nodes = [root]

    def find_live_node(self, sender):
        """
        Here we should find a neighbour for the sender.
        Best neighbour is the node who is nearest the root and has not more than one child.

        Code design suggestion:
            1. Do a BFS algorithm to find the target.

        Warnings:
            1. Check whether there is sender node in our NetworkGraph or not; if exist do not return sender node or
               any other nodes in it's sub-tree.

        :param sender: The node address we want to find best neighbour for it.
        :type sender: tuple

        :return: Best neighbour for sender.
        :rtype: GraphNode

        """

        try:
            assert self.find_node(sender[0], sender[1]) is None
        except AssertionError:
            print('sender is already in network graph')

        root = self.root
        to_visit = [root]

        while to_visit:
            current = to_visit.pop(0)

            if current.can_be_neghbour():
                self.add_node(sender[0], sender[1], current.address)
                return current

            if current.left:
                to_visit.append(current.left)
            if current.right:
                to_visit.append(current.right)

    def find_node(self, ip, port):
        address = (ip, port)

        root = self.root
        to_visit = [root]

        while to_visit:
            current = to_visit.pop(0)
            if current.address == address:
                return current

            if current.left:
                to_visit.append(current.left)
            if current.right:
                to_visit.append(current.right)

        return None

    def turn_on_node(self, node_address):
        node = self.find_node(node_address[0], node_address[1])
        node.alive = True

    def turn_off_node(self, node_address):
        node = self.find_node(node_address[0], node_address[1])
        node.alive = False

    def remove_node(self, node_address):
        node = self.find_node(node_address[0], node_address[1])
        node.alive = False
        if node.right:
            self.remove_node(node.right.address)
        if node.left:
            self.remove_node(node.left.address)
        return

    def add_node(self, ip, port, father_address):
        """
        Add a new node with node_address if it does not exist in our NetworkGraph and set its father.

        Warnings:
            1. Don't forget to set the new node as one of the father_address children.
            2. Before using this function make sure that there is a node which has father_address.

        :param ip: IP address of the new node.
        :param port: Port of the new node.
        :param father_address: Father address of the new node

        :type ip: str
        :type port: int
        :type father_address: tuple

        :return:
        """
        father = self.find_node(father_address[0], father_address[1])

        new_node = GraphNode((ip, port))
        new_node.set_parent(father)

        father.add_child(new_node)



