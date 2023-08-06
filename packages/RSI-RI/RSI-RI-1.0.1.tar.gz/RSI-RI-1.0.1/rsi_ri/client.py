from multiprocessing import Process, Manager
from time import sleep

from log import log_process
from server import rsi_process
from tools import \
    convert_rsi_config_to_dict, \
    extract_config_from_rsi_config, \
    check_position_values


class RSIClient:
    """ RSI Client Object """

    def __init__(self, file, cycle_rate=4):
        """RSI Client Object

        Object used to provide interface to RSI Variables.
        :param file: RSI Config File
        :param ip: Local IP address
        :param port: Port used in RSI Config file
        """
        self.file = file
        self.ip, self.port, self.sen_type, self.only_send = extract_config_from_rsi_config(file)
        self.manager = Manager()
        self.send = self.manager.dict(convert_rsi_config_to_dict(file, "send"))
        self.receive = self.manager.dict(convert_rsi_config_to_dict(file, "receive"))
        self.status = self.manager.dict({"State": False, "Logging": False, "Error": ""})
        self.movement_type = None
        self.rsi = Process(target=rsi_process, args=(self.file,
                                                     self.receive,
                                                     self.send,
                                                     self.status))
        if cycle_rate == 4:
            self.cycle_rate = 0.004
        elif cycle_rate == 12:
            self.cycle_rate = 0.012
        self.log_location = ""
        self.logging = False

    def set_log_location(self, location):
        """

        Args:
            location:

        Returns:

        """
        self.log_location = location

    def enable_logging(self):
        self.logging = Process(target=log_process, args=(self.send,
                                                         self.receive,
                                                         self.status,
                                                         self.log_location,
                                                         self.cycle_rate))

    def display_variables(self):
        """
        :return:
        """
        print("Receive Variables")
        for key, value in self.receive.items():
            print(key, ' : ', value)

        print("Send Variables")
        for key, value in self.send.items():
            print(key, ' : ', value)

    def start(self):
        """
        Start RSI Network process
        :return:
        """
        self.rsi.start()
        if self.logging is not False:
            self.logging.start()
        self.status["State"] = True
        # self.rsi.join()

    def stop(self):
        """
        Stop RSI Network process
        :return:
        """
        self.status["State"] = False
        sleep(1)
        self.rsi.terminate()
        sleep(1)
        self.rsi.kill()
        sleep(1)
        self.rsi = Process(target=rsi_process, args=(self.file,
                                                     self.ip,
                                                     self.port,
                                                     self.receive,
                                                     self.send,
                                                     self.status))

    def check_receive_value(self, key):
        try:
            return self.receive[key]
        except NameError:
            return "Key does not exist"

    def check_send_value(self, key):
        try:
            return self.send[key]
        except NameError:
            return "Key does not exist"

    def update_pendant(self, value):
        try:
            self.send["EStr"] = value
        except ValueError:
            return "EStr internal variable not present in config file"

    def set_value(self, key, value):
        """
        :param key:
        :param value:
        :return:
        """
        try:
            self.send[key] = value
        except ValueError:
            return "{} not present in config file".format(key)

    def set_value_attribute(self, key, axis, value):
        """Sets the value of a multi value variable.

        :param key:
        :param axis:
        :param value:
        :return:
        """
        try:
            send_value = self.send
            values = send_value[key]
            values[axis] = str(value)
            send_value[key] = values
            self.send = send_value
            return "OK"
        except ValueError:
            return "{} is not present in config file".format(key)

    def set_axis(self, axis, value):
        """

        :param axis:
        :param value:
        :return:
        """
        try:
            self.set_value_attribute("RKorr", axis, value)
        except NameError:
            return "RKorr is not present in config file"

    def set_joint(self, joint, value):
        """

        :param joint:
        :param value:
        :return:
        """
        try:
            self.set_value_attribute("AKorr", joint, value)
        except NameError:
            return "AKorr is not present in config file"

    def check_send_values(self, key):
        """

        :param key:
        :return:
        """
        return self.send[key]

    def check_receive_values(self, key):
        """

        :param key:
        :return:
        """
        return self.receive[key]

    def test(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        try:
            self.send[key] = value
        except ValueError:
            return "{} not present in config file".format(key)

    def move_basic_ptp(self, coord, rate):
        """

        :param coord:
        :param rate:
        :return:
        """
        values = {"X": coord[0], "Y": coord[1], "Z": coord[2], "A": coord[3], "B": coord[4], "C": coord[5]}
        send_values = self.check_send_values("RKorr")
        rec_values = self.check_receive_values("RIst")

        self.send["RKorr"] = check_position_values(values, send_values, rec_values, rate)

    def move_joints(self, a1, a2, a3, a4, a5, a6, rate):
        """

        :param a1:
        :param a2:
        :param a3:
        :param a4:
        :param a5:
        :param a6:
        :param rate:
        :return:
        """
        values = {"A1": a1, "A2": a2, "A3": a3, "A4": a4, "A5": a5, "A6": a6}
        send_values = self.check_send_values("RKorr")
        rec_values = self.check_receive_values("RIst")

        self.send["AKorr"] = check_position_values(values, send_values, rec_values, rate)


if __name__ == '__main__':
    pass
