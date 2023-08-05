import logging

from network import Network
from tools import \
    get_ipoc, \
    update_ipoc, \
    convert_xml_string_to_dict, \
    merge_dict_with_xml_string, \
    convert_config_to_xml_string, \
    extract_config_from_rsi_config

# Log file location
# Define the log format
log_format = '[%(asctime)s] %(levelname)-8s %(name)-12s %(funcName)20s() %(lineno)s %(message)s'
# Define basic configuration
logging.basicConfig(level=logging.DEBUG, format=log_format, handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)


def rsi_process(file, send, receive, status):
    """Process containing the RSI networking functions

    This process operates the networking side of the RSI RI Functions.
    :param file: RSI config file
    :param send: Variable containing Manager.Dict variable with RSI values
    :param receive: Variable containing Manager.Dict variable with RSI values
    :param status: Variable containing Manager.Dict variable with RSI status values
    :return:
    """
    rsi_server = RSIServer(file, receive, send, status)
    rsi_server.state = True
    rsi_server.run()


class RSIServer:
    def __init__(self, config_file, receive, send, status):
        """ RSI Communication Object.

            Main Object for operating an RSI connection.

            Keyword arguments:
                config_file - *.rsi.xml config file (default None)
                client_ip - IP address of the local network socket (default None)
                client_port - Port of the local network socket (default None)
            """
        # Network connection Object
        self.network = Network("", int(extract_config_from_rsi_config(config_file)[1]))
        # RSI Variables
        self.send_string = convert_config_to_xml_string(config_file, "send")
        self.send_values = receive

        self.receive_string = convert_config_to_xml_string(config_file, "receive")
        self.receive_values = send

        # Status (State": "Inactive", "Status": "", "Config": "")
        self.status = status
        self.ipoc = 0

    def stop(self):
        """

        :return:
        """
        self.network.udp_socket.close()

    def run(self):
        """ Operates RSI communication loop.

        Main method that runs a continuous loop polling the network socket,
        polling client pipe, processing data _working sending a reply
        """
        logger.debug("RSI Server Waiting")

        while True:
            self.get_robot_data()
            self.send_reply()
        else:
            self.stop()

    def get_robot_data(self):
        """ Get RSI data from robot _working process.

        Polls network socket _working then updates RSIValues.values
        Gets IPOC from message _working updates self.ipoc
        """
        # Polls network, returns a string of XML
        self.receive_string = self.network.receive()
        # Get IPOC
        self.ipoc = get_ipoc(self.receive_string)
        # Convert XML string into Dict
        self.receive_values.update(convert_xml_string_to_dict(self.receive_string))

    def send_reply(self):
        """ Send RSI Message.

        Updates IPOC of message _working sends the RSIValues Object .xml values
        """
        new_string = merge_dict_with_xml_string(self.send_values, self.send_string)
        new_string = update_ipoc(new_string, self.ipoc)
        self.send_string = new_string
        self.network.send(self.send_string)


if __name__ == '__main__':
    pass
