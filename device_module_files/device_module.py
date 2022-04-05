# Device Module
# Allows Devices to Connect to the Central System and add data
# Expected JSON Input from All Devices
# entry = {
# "device_entry":
# [
# {
# "user_uid": "u###",
# "device_uid": "d###",
# "device_type": "string",
# "msrmt_type": "string",
# "msrmt_val": "int",
# "msrmt_unit": "string",
# "msrmt_date": "mm/dd/yyyy"
# }
# ]
# }

import json
from datetime import datetime
# Need to install jsonschema using pip install jsonschema
import jsonschema
from jsonschema import validate, ValidationError, SchemaError

# Defining expected JSON Schema
entrySchema = {
    "type" : "object",
    "properties": {
        "user_uid": {"type": "number"},
        "device_uid": {"type": "number"},
        "device_type": {"type": "string"},
        "msrmt_type": {"type": "string"},
        "msrmt_val": {"type": "number"},
        "msrmt_unit": {"type": "string"},
        "msrmt_date": {"type": "string"},
    },
    "required": ["user_uid", "device_uid", "device_type", "msrmt_type", "msrmt_val", "msrmt_unit", "msrmt_date"]
}

# Placeholder for actual database interaction
# Currently outputs to a text file
def upload_data(filename):
    code, msg = validate_input(filename)
    if code == 0:
        try:
            to_database(json.load(filename))
        except IOError as err1:
            msg = ("File IO Error: Couldn't open or write to file (%s)." % err1)
            return 1, msg
        return 0, "Data Written to Database"
    return code, msg

def to_database(valid_data):
    with open('device_output.txt', 'w') as output_file:
        output_file.write(json.dumps(valid_data))

# Manually Validates Data
def validate_data(unvalidated):
    thermometer = {"temperature": "fahrenheit"}
    weight_scale = {"weight": "pounds"}
    device_types = ["thermometer", "weight_scale"]


    for entry in unvalidated['device_entry']:
        user_id = entry['user_uid']
        device_id = entry['device_uid']
        device_type = entry['device_type']
        measurement_type = entry['msrmt_type']
        measurement_value = entry['msrmt_val']
        measurement_unit = entry['msrmt_unit']
        measurement_date = entry['msrmt_date']

    # Validate that user_uid is a number
    if isinstance(user_id, int) == False:
        return 11, "User ID is not a number value"

    # Validate that device_uid is a number
    if isinstance(device_id, int) == False:
        return 12, "Device ID is not a number value"

    # Validate that device_type is a supported device
    if device_type not in device_types:
        return 13, "Device is not a supported device type"

    # Validate that msrmt_type is
    if measurement_type not in eval(device_type):
        return 14, "Measurement Type does not match with device type"

    # Validate that msrmt_val is a number (dependent on type?)
    if isinstance(measurement_value, float) == False:
        return 15, "Measurement is not a number value"

    # Validate that msrmt_unit is appropriate for device type
    if measurement_unit != eval(device_type)[measurement_type]:
        return 16, "Unit is not correct for measurement type"

    # Validate that msrmt_date is in the correct format
    try:
        dateCheck = datetime.strptime(measurement_date, "%m-%d-%Y")
    except ValueError:
        return 17, "Date is not formatted correctly, must be in the format mm-dd-yyyy"

    valiated = unvalidated
    return 0, validated

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

    returnCode, message = validate_data(rawData)

    return returnCode, message

    # try:
    #     validate(instance=rawData['device_entry'], schema=entrySchema)
    # except SchemaError as err3:
    #     msg = ("JSON Schema Error: The Schema is incorrect.")
    #     return 3, msg
    # except ValidationError as err4:
    #     msg = ("JSON Validation Error: JSON does not match expected Schema (%s)." % err4)
    #     return 4, msg
    #
    # return 0, rawData
