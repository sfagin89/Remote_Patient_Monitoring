# Chat Module
# Allows Users to send and receive messages to/from eachother
# Expected JSON Input from All User Messages
# message = {
# "message_metadata":
# [
# {
# "msg_src": "u###",
# "msg_dst": "u###",
# "msg_content": "string",
# "msg_date": "mm/dd/yyyy"
# }
# ]
# }

import json
from datetime import datetime

# Manually Validates Data
def validate_msg(unvalidated):

    for message in unvalidated['message_metadata']:
        src_id = message['msg_src']
        dst_id = message['msg_dst']
        content = message['msg_content']
        message_date = message['msg_date']

    # Validate that msg_src is a number
    if isinstance(src_id, int) == False:
        return 21, "Source User ID is not a number value"

    # Validate that msg_dst is a number
    if isinstance(dst_id, int) == False:
        return 22, "Destination User ID is not a number value"

    # Sanitize Message against SQL Injections
    # To Be Done at Later Date

    # Validate that msg_date is in the correct format
    try:
        dateCheck = datetime.strptime(message_date, "%m-%d-%Y")
    except ValueError:
        return 27, "Date is not formatted correctly, must be in the format mm-dd-yyyy"

    return 0, "JSON data successfully validated"

# Validates Input File, checking for valid file path, JSON structure & Schema
def validate_input(filename):
    try:
        with open(filename, 'r') as file:
            # json.load() converts JSON to Python Object (type Dict)
            rawData = json.load(file)
    except IOError as err1:
        msg = ("File IO Error: Couldn't open or write to file (%s)." % err1)
        return 1, msg
    except ValueError as err2:
        msg = ("ValueError: JSON data cannot be decoded (%s)." % err2)
        return 2, msg

    returnCode, message = validate_msg(rawData)

    return returnCode, message
