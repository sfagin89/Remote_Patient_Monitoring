# save this as app.py
from flask import Flask, escape, request, render_template, Response
from flask_restful import Api, Resource, reqparse, abort
import logging
import sys
sys.path.insert(0, './device_module_files')
sys.path.insert(0, './chat_module_files')
import device_module
import chat_module

app = Flask(__name__)
api = Api(app, catch_all_404s=True)

####################
# Helper Functions #
####################

# Handles errors
# Calls abort function using the error_code and error_msg parameters
def error_handler(error_code: int, error_msg: str) -> None:
    abort(Response(error_msg, error_code))

# Was the API call successful?
# If successful, returns true
# If failed, calls error_handler
def api_call_successful(return_code: int, msg: str) -> bool:
    if return_code == 0:
        return True
    else:
        error_handler(error_code=return_code, error_msg=msg)
        return False

###############
# API Classes #
###############

class HomePage(Resource):
    def get(self):
        return "Home Page"


class ValidateDeviceJSON(Resource):
    def get(self, json_file):
        returnCode, message = device_module.validate_input(json_file)

        if api_call_successful(return_code=returnCode,
                               msg=message):

            return {"result": returnCode,
                    "message": message,
                    "data": json_file}


class ValidateChatJSON(Resource):
    def get(self, json_file):
        returnCode, message = chat_module.validate_input(json_file)

        if api_call_successful(return_code=returnCode,
                               msg=message):

            return {"result": returnCode,
                    "message": message,
                    "data": json_file}


class UploadDeviceMeasurements(Resource):
    def post(self, json_file):
        returnCode, message = device_module.upload_data(json_file)

        if api_call_successful(return_code=returnCode,
                               msg=message):

            return {"result": returnCode,
                    "message": message,
                    "data": json_file}

class RegisterDevice(Resource):
    def post(self, device_id):
        registered_result = device.register_device(device_id)

        if api_call_successful(operation_success=registered_result[0],
                               msg=registered_result[1],
                               error_code=registered_result[2]):

            return {"result": registered_result[0],
                    "message": registered_result[1],
                    "device_id": device_id}

class UnregisterDevice(Resource):
    def delete(self, device_id):
        remove_result = device.remove_device(device_id)

        if api_call_successful(operation_success=remove_result[0],
                               msg=remove_result[1],
                               error_code=remove_result[2]):

            return {"result": remove_result[0],
                    "message": remove_result[1],
                    "device_id": device_id}


api.add_resource(HomePage, "/")

# endpoints for device module
api.add_resource(ValidateDeviceJSON, "/device/validate/<string:json_file>")
api.add_resource(UploadDeviceMeasurements, "/device/uploadmeasurements/<string:json_file>")
api.add_resource(RegisterDevice, "/device/register/<int:device_uid>")
api.add_resource(UnregisterDevice, "/device/unregister/<int:device_uid>")

# endpoints for chat module
api.add_resource(ValidateChatJSON, "/chat/validate/<string:chat_json>")

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, port=5001)
