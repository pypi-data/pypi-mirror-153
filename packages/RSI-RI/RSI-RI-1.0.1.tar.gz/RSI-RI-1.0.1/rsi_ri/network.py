import logging
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_RCVBUF

from tools import change_config_port


class Network:
    """Network class for RSI networking.

    Keyword arguments:
    client_ip - IP address of the local network socket (default None)
    client_port - Port of the local network socket (default None)
    """

    def __init__(self, client_ip, client_port, echo=False):
        self.client_address = (client_ip, change_config_port(client_port) if echo is True else client_port)
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.udp_socket.bind(self.client_address)
        self.udp_socket.setsockopt(SOL_SOCKET, SO_RCVBUF, 1)
        self.controller_ip = ("127.0.0.1", client_port)
        logging.debug("Network Socket Established")

    def receive(self):
        """Polls network, returns output an XML string."""
        data, self.controller_ip = self.udp_socket.recvfrom(400)
        return data

    def send(self, message):
        """Send message to controller IP.

        Keyword arguments:
        message - binary message (default binary)
        """
        self.udp_socket.sendto(bytes(message, "utf8"), self.controller_ip)


if __name__ == '__main__':
    pass
