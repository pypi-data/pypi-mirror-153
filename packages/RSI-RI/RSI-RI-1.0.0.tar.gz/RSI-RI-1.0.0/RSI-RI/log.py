import csv
from time import sleep


def log_process(send, receive, status, location, rate):
    location = "{}/log.csv".format(location)
    output_file = open(location, "w+")

    file_writer = csv.writer(output_file, lineterminator='\n')
    file_writer.writerow(create_log(send, receive, "header"))
    status["Logging"] = "Logging active"
    while status["State"] is True:
        file_writer.writerow(create_log(send, receive, "row"))
        sleep(rate)
    else:
        status["Logging"] = "Logging complete"


def open_csv(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        data = [row for row in reader]
    return data


def create_log(send, receive, entry_type):
    row = []
    for direction in (send, receive):
        for item, value in direction.items():
            if item == "IPOC":
                if entry_type == "row":
                    row.insert(0, value)
                elif entry_type == "header":
                    row.insert(0, item)
            else:
                if type(value) is dict:
                    for items, values in value.items():
                        if entry_type == "row":
                            row.append(values)
                        elif entry_type == "header":
                            row.append("{}.{}".format(item, items))
                else:
                    if entry_type == "row":
                        row.append(value)
                    elif entry_type == "header":
                        row.append(item)
    return row
