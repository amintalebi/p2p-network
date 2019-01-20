from src.tools.simpletcp.tcpserver import TCPServer
from src.tools.Node import Node
import threading


class Stream:
    def __init__(self, ip, port, root_address=None):
        """
        The Stream object constructor.

        Code design suggestion:
            1. Make a separate Thread for your TCPServer and start immediately.


        :param ip: 15 characters
        :param port: 5 characters
        """
        self.nodes = dict()
        self.register_node = None

        self.root_address = root_address

        ip = Node.parse_ip(ip)
        port = Node.parse_port(port)

        self._server_in_buf = []

        def callback(address, queue, data):
            """
            The callback function will run when a new data received from server_buffer.

            :param address: Source address.
            :param queue: Response queue.
            :param data: The data received from the socket.
            :return:
            """
            queue.put(bytes('ACK', 'utf8'))
            self._server_in_buf.append(data)

        self.tcp_server = TCPServer(mode=ip, port=int(port), read_callback=callback)

        server_thread = threading.Thread(target=self.tcp_server.run)
        server_thread.start()

    def get_server_address(self):
        """

        :return: Our TCPServer address
        :rtype: tuple
        """
        return self.tcp_server.ip, self.tcp_server.port

    def clear_in_buff(self, snapshot_size):
        """
        Discard any data in TCPServer input buffer.

        :return:
        """
        self._server_in_buf = self._server_in_buf[snapshot_size:]

    def add_node(self, server_address, set_register_connection=False):
        """
        Will add new a node to our Stream.

        :param server_address: New node TCPServer address.
        :param set_register_connection: Shows that is this connection a register_connection or not.

        :type server_address: tuple
        :type set_register_connection: bool

        :return:
        """

        if set_register_connection:
            self.register_node = Node(server_address, set_register=set_register_connection)
            return

        new_node = Node(server_address, set_register=set_register_connection)
        self.nodes[str((new_node.server_ip, new_node.server_port))] = new_node

    def remove_node(self, node):
        """
        Remove the node from our Stream.

        Warnings:
            1. Close the node after deletion.

        :param node: The node we want to remove.
        :type node: Node

        :return:
        """
        try:
            if node.is_register_node:
                self.register_node.close()
                self.register_node = None
                return

            node = self.nodes[str((node.server_ip, node.server_port))]
            node.close()
            self.nodes.pop(str((node.server_ip, node.server_port)))
        except KeyError or IOError:
            print('could not remover node')

    def get_node_by_server(self, ip, port):
        """

        Will find the node that has IP/Port address of input.

        Warnings:
            1. Before comparing the address parse it to a standard format with Node.parse_### functions.

        :param ip: input address IP
        :param port: input address Port

        :return: The node that input address.
        :rtype: Node
        """
        try:
            return self.nodes[str((Node.parse_ip(ip), Node.parse_port(port)))]
        except KeyError:
            print('get node by server, could not find node')

        return None

    def add_message_to_out_buff(self, address, message):
        """
        In this function, we will add the message to the output buffer of the node that has the input address.
        Later we should use send_out_buf_messages to send these buffers into their sockets.

        :param address: Node address that we want to send the message
        :param message: Message we want to send

        Warnings:
            1. Check whether the node address is in our nodes or not.

        :return:
        """

        try:
            node = self.nodes[str((Node.parse_ip(address[0]), Node.parse_port(address[1])))]
            node.add_message_to_out_buff(message)
        except KeyError:
            print('add message to out buff, could not find node')

    def read_in_buf(self):
        """
        Only returns the input buffer of our TCPServer.

        :return: TCPServer input buffer.
        :rtype: list
        """
        return self._server_in_buf

    def send_messages_to_node(self, node):
        """
        Send buffered messages to the 'node'

        Warnings:
            1. Insert an exception handler here; Maybe the node socket you want to send the message has turned off and
            you need to remove this node from stream nodes.

        :param node:
        :type node Node

        :return:
        """
        try:
            node.send_message()
        except IOError:
            print('send message to node, could not send message')
            self.remove_node(node)

    def send_out_buf_messages(self, only_register=False):
        """
        In this function, we will send hole out buffers to their own clients.

        :return:
        """
        if only_register:
            self.send_messages_to_node(self.register_node)
            return

        for node in list(self.nodes.values()):
            self.send_messages_to_node(node)
