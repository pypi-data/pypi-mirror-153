from time import sleep

from client import RSIClient
from echo_server import RSIEchoServer

if __name__ == '__main__':

    config_file = "../../resources/Example Files/ConfigFiles/rsi examples/RSI_EthernetConfig.xml"
    # Create RSI Client
    client = RSIClient(config_file)

    # Start Server
    client.start()

    # Show variables created from config file
    client.display_variables()

    # Set cartesian correction
    client.set_axis("X", 0.1)

    # Set joint correction
    client.set_joint("A1", 0.1)

    # Move axis specific distance
    # TODO if this works, turn into a procedure
    target = 3
    rate = 0.1
    client.set_axis("X", rate)
    current = 0
    while current < target:
        sleep(client.cycle_rate)
        current += rate
    client.set_axis("X", 0)

    # Send message to Teach Pendent
    client.update_pendant("This is a message that will be shown on the pendant")

    # Set individual value
    client.set_value("EStr", "This is a test message")

    # Stop server
    client.stop()

    # Log session
    client.enable_logging()

    # Run echo server
    config_file = "RSI_EthernetConfig.xml"

    # Create RSI Client
    client = RSIEchoServer(config_file, 4)
    client.state = True
    client.run()
