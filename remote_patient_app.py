# Main Application
# Acting as placeholder and stub function for in progress modules
import sys
sys.path.insert(0, './device_module_files')
import device_module

# Function used by all Devices to upload
# Measurement Data
# Device Module Performs Data Validation then passes data
# to database.
def dev_data_upload(filename):
    returnCode, data = device_module.validate_input(filename)

    if returnCode != 0:
        print(data)
        exit()

    else:
        print(data)

    return returnCode, data
