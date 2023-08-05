from lxml import etree


def convert_rsi_config_to_dict(rsi_file, direction):
    return convert_xml_string_to_dict(convert_config_to_xml_string(rsi_file, direction))


def convert_xml_string_to_dict(xml):
    """ Convert RSI XML string to dict variables.

    Converts an RSI XML string to RSIValue Object values.
    Either takes an XML String or reads from Object.xml value

    Keyword arguments:
        xml - RSI XML String (default None)
    """
    # Convert string to XML object
    xml_string = etree.fromstring(xml)
    new_values = {}
    # Cycle through XML object converting each attribute/value
    # to dict _working storing in the shared value variable
    for xml_row in xml_string:
        if xml_row.text is None:
            new_values[xml_row.tag] = {}
            for a, v in xml_row.items():
                # new_values[xml_row.tag].insert(a, str(v))
                new_values[xml_row.tag][a] = str(v)
        else:
            new_values[xml_row.tag] = xml_row.text
    # logging.debug(new_values)
    return new_values


def get_ipoc(message):
    x = etree.fromstring(message)
    ipoc = x[len(x) - 1].text
    return ipoc


def add_ipoc(xml_string):
    xml = etree.fromstring(xml_string)
    ipoc = etree.Element("IPOC")
    ipoc.text = "0"
    xml.append(ipoc)
    return etree.tostring(xml, encoding="unicode")


def update_ipoc(xml_string, ipoc):
    """ Updates IPOC of send message. """
    xml_val = etree.fromstring(xml_string)
    xml_val[len(xml_val) - 1].text = str(ipoc)
    send_string = etree.tostring(xml_val, encoding="unicode")
    return send_string


def merge_dict_with_xml_string(dict_value, xml_string):
    """ Convert to Object variables to RSI XML string. """
    xml = etree.fromstring(xml_string)

    for xml_row in xml:
        # Iterate each item
        if xml_row.text is None:

            for a, v in xml_row.items():
                xml.find(xml_row.tag).attrib[a] = dict_value[xml_row.tag][a]
        else:
            xml_row.text = dict_value[xml_row.tag]
    xml_string = etree.tostring(xml).decode()

    return xml_string


def load_xml(file):
    """ Load Send XML template _working returns XML root to object """
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(file, parser=parser)
    return tree.getroot()


def convert_config_to_xml_string(file, direction):
    """Opens the KUKA RobotSensorInterface XML config file _working creates the XML template
    for sending _working receiving messages"""

    internal = {
        "ComStatus": "String",
        "RIst": ["X", "Y", "Z", "A", "B", "C"],
        "RSol": ["X", "Y", "Z", "A", "B", "C"],
        "AIPos": ["A1", "A2", "A3", "A4", "A5", "A6"],
        "ASPos": ["A1", "A2", "A3", "A4", "A5", "A6"],
        "ELPos": ["E1", "E2", "E3", "E4", "E5", "E6"],
        "ESPos": ["E1", "E2", "E3", "E4", "E5", "E6"],
        "MaCur": ["A1", "A2", "A3", "A4", "A5", "A6"],
        "MECur": ["E1", "E2", "E3", "E4", "E5", "E6"],
        "IPOC": 000000,
        "BMode": "Status",
        "IPOSTAT": "",
        "Delay": ["D"],
        "EStr": "EStr Test",
        "Tech.C1": ["C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C110"],
        "Tech.C2": ["C21", "C22", "C23", "C24", "C25", "C26", "C27", "C28", "C29", "C210"],
        "Tech.C3": ["C31", "C32", "C33", "C34", "C35", "C36", "C37", "C38", "C39", "C310"],
        "Tech.C4": ["C41", "C42", "C43", "C44", "C45", "C46", "C47", "C48", "C49", "C410"],
        "Tech.C5": ["C51", "C52", "C53", "C54", "C55", "C56", "C57", "C58", "C59", "C510"],
        "Tech.C6": ["C61", "C62", "C63", "C64", "C65", "C66", "C67", "C68", "C69", "C610"],
        "Tech.T1": ["T11", "T12", "T13", "T14", "T15", "T16", "T17", "T18", "T19", "T110"],
        "Tech.T2": ["T21", "T22", "T23", "T24", "T25", "T26", "T27", "T28", "T29", "T210"],
        "Tech.T3": ["T31", "T32", "T33", "T34", "T35", "T36", "T37", "T38", "T39", "T310"],
        "Tech.T4": ["T41", "T42", "T43", "T44", "T45", "T46", "T47", "T48", "T49", "T410"],
        "Tech.T5": ["T51", "T52", "T53", "T54", "T55", "T56", "T57", "T58", "T59", "T510"],
        "Tech.T6": ["T61", "T62", "T63", "T64", "T65", "T66", "T67", "T68", "T69", "T610"],
    }

    # Sets variables for new xml structure
    config_root = load_xml(file)
    new_root_name = None
    root_type = None
    root_index = None

    for i, c in enumerate(config_root):
        # Cycle through root of config file to get values
        if c.tag == "SEND" and direction == "receive":
            root_index = i
            root_type = "KUKA"
            new_root_name = "Rob"
        if c.tag == "RECEIVE" and direction == "send":
            root_index = i
            for item in config_root[0]:
                if item.tag == "SENTYPE":
                    root_type = item.text
            new_root_name = "Sen"
    # Create new XML object _working set the root name _working type
    new_root = etree.Element(new_root_name, Type=root_type)
    new_root_count = -1
    temp_multi_value = {}

    # Cycle through elements of each item in config_root
    for i, item in enumerate(config_root[root_index][0]):
        tag = item.values()[0]
        # Future use type = item.values()[1]
        indx = item.values()[2]
        # Internal variable check
        if indx == "INTERNAL":
            # Strip off the def_
            tag = tag[4:]
            # Get values out of internal catalogue
            values = internal[tag]
            # Create elements for tag in new root
            new_root.append(etree.Element(str(tag)))
            new_root_count += 1
            # Checks value type _working set default values
            if isinstance(values, list):
                for a in values:
                    new_root[i].set(a, "0")
            else:
                new_root[i].text = values

        elif tag.__contains__("."):
            # Finds the suffix _working tag
            suffix = tag[tag.find(".") + 1:]
            tag = tag[:tag.find(".")]
            # if temp value exists
            if temp_multi_value.__contains__(tag):
                values = temp_multi_value[tag]
                values.append(suffix)
                temp_multi_value[tag] = values
                new_root[new_root_count].set(suffix, "")
            else:
                # Create the temp value _working add initial value
                new_root_count += 1
                temp_multi_value = {tag: [suffix]}
                new_root.append(etree.Element(str(tag)))
                new_root[new_root_count].set(suffix, "")
        else:
            # Remove any blank lines
            if tag.startswith("FREE"):
                new_root_count += 1
            else:
                # Add single value elements
                new_root.append(etree.Element(str(tag)))
                temp_multi_count = len(new_root)
                new_root[temp_multi_count - 1].text = "0"
                new_root_count += 1
    # If send values add IPOC
    if direction == "send":
        new_root.append(etree.Element("IPOC"))
        new_root[len(new_root) - 1].text = str("0")

    return etree.tostring(new_root, pretty_print=True, encoding='unicode')


def change_config_port(file):
    return file + 1


def extract_config_from_rsi_config(file):
    xml_root = load_xml(file)
    ip, port, sen_type, only_send = None, None, None, None

    for item in xml_root[0]:
        if item.tag == "IP_NUMBER":
            ip = item.text
        if item.tag == "PORT":
            port = item.text
        if item.tag == "SENTYPE":
            sen_type = item.text
        if item.tag == "ONLYSEND":
            if item.text == "FALSE":
                only_send = False
            else:
                only_send = True

    return str(ip), int(port), str(sen_type), only_send


def extract_hold_values_from_config(file):
    xml_root = load_xml(file)
    hold = {}
    send_index = 0

    for index, value in enumerate(xml_root):
        if value.tag == "RECEIVE":
            send_index = index

    for index, item in enumerate(xml_root[send_index][0]):
        try:
            hold[item.values()[0]] = bool(int(item.values()[3]))
        except IndexError:
            pass
    return hold


def merge_send_receive(send, receive):
    for item in receive.keys():
        if item in send:
            if item == "IPOC":
                pass
            else:
                send[item] = receive[item]
    return send


def check_position_values(values, send_values, rec_values, rate):
    """Checks

    :param values:
    :param send_values:
    :param rec_values:
    :param rate:
    :return:
    """
    for key, val in values.items():
        if float(rec_values[key]) > val:
            send_values[key] = str(rate)
        if float(rec_values[key]) < val:
            send_values[key] = str(rate * -1)
        if float(rec_values[key]) == val:
            send_values[key] = 0
    return send_values


if __name__ == '__main__':
    pass
