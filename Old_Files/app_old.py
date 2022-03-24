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

#@app.route('/')
#def index():
#    return render_template('index.html')

#@app.route('/device_interface')
#def device_interface():
#    return render_template('device_interface.html')

#@app.route('/chat_interface')
#def chat_interface():
#    return render_template('chat_interface.html')

#@app.route('/user_interface')
#def user_interface():
#    return "User Interface, Coming Soon"


# chat interface page rule.
#@app.route('/chat_interface/<path>', defaults={'path_flag':0})
#@app.route('/chat_interface/<path>/<path_flag>')
#def flask_validate_chat_json(path, path_flag):
#    return str(validate_chat_json(path, int(path_flag)))

# device interface page rule.
#@app.route('/device_interface/<path>', defaults={'path_flag':0})
#@app.route('/device_interface/<path>/<path_flag>')
#def flask_validate_device_json(path, path_flag):
#    return str(validate_device_json(path, int(path_flag)))

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


api.add_resource(HomePage, "/")

# endpoints for device module
api.add_resource(ValidateDeviceJSON, "/device/validate/<string:json_file>")
api.add_resource(UploadDeviceMeasurements, "/device/uploadmeasurements/<string:json_file>")

# endpoints for chat module
api.add_resource(ValidateChatJSON, "/chat/validate/<string:chat_json>")

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, port=5001)
