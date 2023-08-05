import logging
from time import sleep

from network import Network
from tools import \
    get_ipoc, \
    update_ipoc, \
    convert_xml_string_to_dict, \
    convert_config_to_xml_string, \
    convert_rsi_config_to_dict, \
    extract_config_from_rsi_config, \
    add_ipoc

# Log file location
# Define the log format
log_format = '[%(asctime)s] %(levelname)-8s %(name)-12s %(funcName)20s() %(lineno)s %(message)s'
# Define basic configuration
logging.basicConfig(level=logging.DEBUG, format=log_format, handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)


class RSIEchoServer:
    def __init__(self, config_file, cycle_rate):
        self.network = Network("", int(extract_config_from_rsi_config(config_file)[1]), True)
        # RSI Variables
        self.send_string = convert_config_to_xml_string(config_file, "receive")
        self.send_values = convert_rsi_config_to_dict(config_file, "receive")
        self.receive_string = convert_config_to_xml_string(config_file, "send")
        self.receive_values = convert_rsi_config_to_dict(config_file, "send")
        # Status (State": "Inactive", "Status": "", "Config": "")
        self.status = {"State": False, "Error": ""}
        self.ipoc = 0
        self.cycle_rate = cycle_rate
        self.send_string = add_ipoc(self.send_string)

    def run(self):
        """ Operates RSI communication loop.

        Main method that runs a continuous loop polling the network socket,
        polling client pipe, processing data _working sending a reply
        """
        while True:
            self.send_data()
            logger.debug("Echo Send: {}".format(self.send_string))
            try:
                self.receive_data()
                self.send_string = update_ipoc(self.send_string, self.ipoc)
                self.process_data()
                logger.debug("Echo receive: {}".format(self.receive_string))
            except(TimeoutError, ConnectionResetError):
                pass

    def send_data(self):
        # self.send_values.update(convert_xml_string_to_dict(self.send_string))
        self.network.send(self.send_string)
        sleep(self.cycle_rate / 1000)

    def receive_data(self):
        """ Get RSI data from robot _working process.

        Polls network socket _working then updates RSIValues.values
        Gets IPOC from message _working updates self.ipoc
        """
        # Polls network, returns a string of XML
        self.receive_string = self.network.receive()
        # Get IPOC
        self.ipoc = int(get_ipoc(self.receive_string)) + self.cycle_rate

        # Convert XML string into Dict
        self.receive_values.update(convert_xml_string_to_dict(self.receive_string))

    def process_data(self):
        pass


if __name__ == '__main__':
    pass
