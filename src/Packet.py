"""

    This is the format of packets in our network:
    


                                                **  NEW Packet Format  **
     __________________________________________________________________________________________________________________
    |           Version(2 Bytes)         |         Type(2 Bytes)         |           Length(Long int/4 Bytes)          |
    |------------------------------------------------------------------------------------------------------------------|
    |                                            Source Server IP(8 Bytes)                                             |
    |------------------------------------------------------------------------------------------------------------------|
    |                                           Source Server Port(4 Bytes)                                            |
    |------------------------------------------------------------------------------------------------------------------|
    |                                                    ..........                                                    |
    |                                                       BODY                                                       |
    |                                                    ..........                                                    |
    |__________________________________________________________________________________________________________________|

    Version:
        For now version is 1
    
    Type:
        1: Register
        2: Advertise
        3: Join
        4: Message
        5: Reunion
                e.g: type = '2' => Advertise packet.
    Length:
        This field shows the character numbers for Body of the packet.

    Server IP/Port:
        We need this field for response packet in non-blocking mode.



    ***** For example: ******

    version = 1                 b'\x00\x01'
    type = 4                    b'\x00\x04'
    length = 12                 b'\x00\x00\x00\x0c'
    ip = '192.168.001.001'      b'\x00\xc0\x00\xa8\x00\x01\x00\x01'
    port = '65000'              b'\x00\x00\xfd\xe8'
    Body = 'Hello World!'       b'Hello World!'

    Bytes = b'\x00\x01\x00\x04\x00\x00\x00\x0c\x00\xc0\x00\xa8\x00\x01\x00\x01\x00\x00\xfd\xe8Hello World!'




    Packet descriptions:
    
        Register:
            Request:
        
                                 ** Body Format **
                 ________________________________________________
                |                  REQ (3 Chars)                 |
                |------------------------------------------------|
                |                  IP (15 Chars)                 |
                |------------------------------------------------|
                |                 Port (5 Chars)                 |
                |________________________________________________|
                
                For sending IP/Port of the current node to the root to ask if it can register to network or not.

            Response:
        
                                 ** Body Format **
                 _________________________________________________
                |                  RES (3 Chars)                  |
                |-------------------------------------------------|
                |                  ACK (3 Chars)                  |
                |_________________________________________________|
                
                For now only should just send an 'ACK' from the root to inform a node that it
                has been registered in the root if the 'Register Request' was successful.
                
        Advertise:
            Request:
            
                                ** Body Format **
                 ________________________________________________
                |                  REQ (3 Chars)                 |
                |________________________________________________|
                
                Nodes for finding the IP/Port of their neighbour peer must send this packet to the root.

            Response:

                                ** Packet Format **
                 ________________________________________________
                |                RES(3 Chars)                    |
                |------------------------------------------------|
                |              Server IP (15 Chars)              |
                |------------------------------------------------|
                |             Server Port (5 Chars)              |
                |________________________________________________|
                
                Root will response Advertise Request packet with sending IP/Port of the requester peer in this packet.
                
        Join:

                                ** Body Format **
                 ________________________________________________
                |                 JOIN (4 Chars)                 |
                |________________________________________________|
            
            New node after getting Advertise Response from root must send this packet to the specified peer
            to tell him that they should connect together; When receiving this packet we should update our
            Client Dictionary in the Stream object.


            
        Message:
                                ** Body Format **
                 ________________________________________________
                |             Message (#Length Chars)            |
                |________________________________________________|

            The message that want to broadcast to whole network. Right now this type only includes a plain text.
        
        Reunion:
            Hello:
        
                                ** Body Format **
                 ________________________________________________
                |                  REQ (3 Chars)                 |
                |------------------------------------------------|
                |           Number of Entries (2 Chars)          |
                |------------------------------------------------|
                |                 IP0 (15 Chars)                 |
                |------------------------------------------------|
                |                Port0 (5 Chars)                 |
                |------------------------------------------------|
                |                 IP1 (15 Chars)                 |
                |------------------------------------------------|
                |                Port1 (5 Chars)                 |
                |------------------------------------------------|
                |                     ...                        |
                |------------------------------------------------|
                |                 IPN (15 Chars)                 |
                |------------------------------------------------|
                |                PortN (5 Chars)                 |
                |________________________________________________|
                
                In every interval (for now 4 seconds) peers must send this message to the root.
                Every other peer that received this packet should append their (IP, port) to
                the packet and update Length.

            Hello Back:
        
                                    ** Body Format **
                 ________________________________________________
                |                  RES (3 Chars)                 |
                |------------------------------------------------|
                |           Number of Entries (2 Chars)          |
                |------------------------------------------------|
                |                 IPN (15 Chars)                 |
                |------------------------------------------------|
                |                PortN (5 Chars)                 |
                |------------------------------------------------|
                |                     ...                        |
                |------------------------------------------------|
                |                 IP1 (15 Chars)                 |
                |------------------------------------------------|
                |                Port1 (5 Chars)                 |
                |------------------------------------------------|
                |                 IP0 (15 Chars)                 |
                |------------------------------------------------|
                |                Port0 (5 Chars)                 |
                |________________________________________________|

                Root in an answer to the Reunion Hello message will send this packet to the target node.
                In this packet, all the nodes (IP, port) exist in order by path traversal to target.
            
    
"""
from struct import *


class Packet:
    # header general info
    HEADER_SIZE = 20
    VERSION = 1

    # packet general types
    REGISTER = 1
    ADVERTISE = 2
    JOIN = 3
    MESSAGE = 4
    REUNION = 5

    # body general info
    NUMBER_OF_ENTRIES_SIZE = 2
    IP_SIZE = 15
    PORT_SIZE = 5
    BODY_REQ = 'REQ'
    BODY_RES = 'RES'
    BODY_JOIN = 'JOIN'
    BODY_ACK = 'ACK'

    def __init__(self, buf):
        """
        The decoded buffer should convert to a new packet.

        :param buf: Input buffer was just decoded.
        :type buf: str
        """
        version_str, type_str, length_str, self.source_server_ip, self.source_server_port, self.body = buf.split('|')
        self.version = int(version_str)
        self.type = int(type_str)
        self.length = int(length_str)
        self.header = version_str + '|' + type_str + '|' + self.source_server_ip + '|' + self.source_server_port

    def get_header(self):
        """

        :return: Packet header
        :rtype: str
        """
        return self.header

    def get_version(self):
        """

        :return: Packet Version
        :rtype: int
        """
        return self.version

    def get_type(self):
        """

        :return: Packet type
        :rtype: int
        """
        return self.type

    def get_length(self):
        """

        :return: Packet length (in Bytes)
        :rtype: int
        """
        return self.length

    def get_body(self):
        """

        :return: Packet body
        :rtype: str
        """
        return self.body

    def get_buf(self):
        """
        In this function, we will make our final buffer that represents the Packet with the Struct class methods.

        :return The parsed packet to the network format.
        :rtype: bytearray
        """

        ip_part1_str, ip_part2_str, ip_part3_str, ip_part4_str = self.source_server_ip.split('.')

        header_bytearray = pack('!2HL4HL', self.version, self.type, self.length, int(ip_part1_str),
                                int(ip_part2_str), int(ip_part3_str), int(ip_part4_str), int(self.source_server_port))
        body_bytearray = bytearray(self.get_body(), 'utf-8')
        return header_bytearray + body_bytearray

    def get_source_server_ip(self):
        """

        :return: Server IP address for the sender of the packet.
        :rtype: str
        """
        return self.source_server_ip

    def get_source_server_port(self):
        """

        :return: Server Port address for the sender of the packet.
        :rtype: str
        """
        return self.source_server_port

    def get_source_server_address(self):
        """

        :return: Server address; The format is like ('192.168.001.001', '05335').
        :rtype: tuple
        """
        return self.source_server_ip, self.source_server_port


class PacketFactory:
    """
    This class is only for making Packet objects.
    """

    @staticmethod
    def parse_buffer(buffer):
        """
        In this function we will make a new Packet from input buffer with struct class methods.

        :param buffer: The buffer that should be parse to a validate packet format

        :return new packet
        :rtype: Packet

        """
        raw_header, raw_body = unpack('!' + str(Packet.HEADER_SIZE) + 's' + str(len(buffer) - Packet.HEADER_SIZE) + 's',
                                      buffer)
        version, packet_type, length, raw_source_server_ip, source_server_port = unpack('!2HL8sL', raw_header)
        ip_part1, ip_part2, ip_part3, ip_part4 = unpack('!4H', raw_source_server_ip)
        source_server_ip = '.'.join([str(ip_part1).zfill(3), str(ip_part2).zfill(3), str(ip_part3).zfill(3),
                                     str(ip_part4).zfill(3)])

        body = raw_body.decode('utf-8')

        string_buffer = '|'.join(
            [str(version), str(packet_type), str(length), source_server_ip, str(source_server_port).zfill(5), body])

        return Packet(string_buffer)

    @staticmethod
    def new_reunion_packet(type, source_address, nodes_array):
        """
        :param type: Reunion Hello (REQ) or Reunion Hello Back (RES)
        :param source_address: IP/Port address of the packet sender.
        :param nodes_array: [(ip0, port0), (ip1, port1), ...] It is the path to the 'destination'.

        :type type: str
        :type source_address: tuple
        :type nodes_array: list

        :return New reunion packet.
        :rtype Packet
        """

        source_ip, source_port = source_address[0], source_address[1]
        packet_length = len(type) + Packet.NUMBER_OF_ENTRIES_SIZE + len(nodes_array) * (
                Packet.IP_SIZE + Packet.PORT_SIZE)
        header = '|'.join([str(Packet.VERSION), str(Packet.REUNION), str(packet_length), source_ip, source_port])

        number_of_entries = str(len(nodes_array)).zfill(2)
        entries = ''
        for ip, port in nodes_array:
            entries += str(ip) + str(port)
        body = type + number_of_entries + entries

        string_buffer = '|'.join([header, body])

        return Packet(string_buffer)

    @staticmethod
    def new_advertise_packet(type, source_server_address, neighbour=None):
        """
        :param type: Type of Advertise packet (REQ or RES)
        :param source_server_address Server address of the packet sender.
        :param neighbour: The neighbour for advertise response packet; The format is like ('192.168.001.001', '05335').

        :type type: str
        :type source_server_address: tuple
        :type neighbour: tuple

        :return New advertise packet.
        :rtype Packet

        """

        source_ip, source_port = source_server_address[0], source_server_address[1]
        if type == Packet.BODY_REQ:
            packet_length = len(type)
            header = '|'.join([str(Packet.VERSION), str(Packet.ADVERTISE), str(packet_length), source_ip, source_port])
            body = type
        else:
            packet_length = len(type) + Packet.IP_SIZE + Packet.PORT_SIZE
            header = '|'.join([str(Packet.VERSION), str(Packet.ADVERTISE), str(packet_length), source_ip, source_port])
            body = type + neighbour[0] + neighbour[1]

        string_buffer = '|'.join([header, body])
        return Packet(string_buffer)

    @staticmethod
    def new_join_packet(source_server_address):
        """
        :param source_server_address: Server address of the packet sender.

        :type source_server_address: tuple

        :return New join packet.
        :rtype Packet

        """

        source_ip, source_port = source_server_address[0], source_server_address[1]
        packet_length = len(Packet.BODY_JOIN)
        header = '|'.join([str(Packet.VERSION), str(Packet.JOIN), str(packet_length), source_ip, source_port])
        body = Packet.BODY_JOIN
        string_buffer = '|'.join([header, body])
        return Packet(string_buffer)

    @staticmethod
    def new_register_packet(type, source_server_address, address=(None, None)):
        """
        :param type: Type of Register packet
        :param source_server_address: Server address of the packet sender.
        :param address: If 'type' is 'REQ' we need an address; The format is like ('192.168.001.001', '05335').

        :type type: str
        :type source_server_address: tuple
        :type address: tuple

        :return New Register packet.
        :rtype Packet

        """

        source_ip, source_port = source_server_address[0], source_server_address[1]
        if type == Packet.BODY_REQ:
            packet_length = len(type) + Packet.IP_SIZE + Packet.PORT_SIZE
            body = type + address[0] + address[1]
        else:
            packet_length = len(type) + len(Packet.BODY_ACK)
            body = type + Packet.BODY_ACK

        header = '|'.join([str(Packet.VERSION), str(Packet.REGISTER), str(packet_length), source_ip, source_port])
        string_buffer = '|'.join([header, body])
        return Packet(string_buffer)

    @staticmethod
    def new_message_packet(message, source_server_address):
        """
        Packet for sending a broadcast message to the whole network.

        :param message: Our message
        :param source_server_address: Server address of the packet sender.

        :type message: str
        :type source_server_address: tuple

        :return: New Message packet.
        :rtype: Packet
        """

        source_ip, source_port = source_server_address[0], source_server_address[1]
        packet_length = len(message)
        header = '|'.join([str(Packet.VERSION), str(Packet.MESSAGE), str(packet_length), source_ip, source_port])
        body = message
        string_buffer = '|'.join([header, body])
        return Packet(string_buffer)
