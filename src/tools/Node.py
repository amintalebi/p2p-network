from src.tools.simpletcp.clientsocket import ClientSocket


class Node:
    def __init__(self, server_address, set_register=False):
        """
        The Node object constructor.

        This object is our low-level abstraction for other peers in the network.
        Every node has a ClientSocket that should bind to the Node TCPServer address.

        Warnings:
            1. Insert an exception handler when initializing the ClientSocket; when a socket closed here we will face
               an exception and we should detach this Node and clear its output buffer.

        :param server_address:
        :param set_register:
        """

        self.server_ip = Node.parse_ip(server_address[0])
        self.server_port = Node.parse_port(server_address[1])
        self.is_register_node = set_register
        self.out_buff = []

        try:
            self.client = ClientSocket(mode=self.server_ip, port=int(self.server_port), single_use=False)
        except Exception:
            self.out_buff.clear()
            raise ConnectionError('Client socket cannot be initialized')

        print("Server Address: ", server_address)

    def send_message(self):
        """
        Final function to send buffer to the client's socket.

        :return:
        """
        for data in self.out_buff:
            self.client.send(data)

        self.out_buff.clear()

    def add_message_to_out_buff(self, message):
        """
        Here we will add a new message to the server out_buff, then in 'send_message' will send them.

        :param message: The message we want to add to out_buff
        :return:
        """
        self.out_buff.append(message)
        # print('message added to node buff successfully')

    def close(self):
        """
        Closing client's object.
        :return:
        """
        self.client.close()

    def get_server_address(self):
        """
        :return: Server address in a pretty format.
        :rtype: tuple
        """
        return self.server_ip, self.server_port

    @staticmethod
    def parse_ip(ip):
        """
        Automatically change the input IP format like '192.168.001.001'.
        :param ip: Input IP
        :type ip: str

        :return: Formatted IP
        :rtype: str
        """
        return '.'.join(str(int(part)).zfill(3) for part in ip.split('.'))

    @staticmethod
    def parse_port(port):
        """
        Automatically change the input IP format like '05335'.
        :param port: Input IP
        :type port: str

        :return: Formatted IP
        :rtype: str
        """
        return str(int(port)).zfill(5)

    @staticmethod
    def parse_address(address):
        """
        :param address: Input Address
        :type address: tuple ('192.168.1.1', 421)

        :return: Formatted Address
        :rtype: tuple ('192.168.001.001', '00421')
        """
        return Node.parse_ip(address[0]), Node.parse_port(str(address[1]))
