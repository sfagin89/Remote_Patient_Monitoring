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

###################
# Data Structures #
###################

dev_reg = {}
chat_sessions = {}

#######################################
# Put Argument Rules for Data Parsing #
#######################################

# Rules for put arguments for Device Module
put_device = reqparse.RequestParser()
put_device.add_argument("user_uid", type=int, required=True)
put_device.add_argument("device_uid", type=int, required=True)
put_device.add_argument("device_type", type=str, required=True)
put_device.add_argument("msrmt_type", type=str, required=True)
put_device.add_argument("msrmt_val", type=int, required=True)
put_device.add_argument("msrmt_unit", type=str, required=True)
put_device.add_argument("msrmt_date", type=str, required=True)

# Rules for put arguments for Chat Module
put_chat = reqparse.RequestParser()
put_chat.add_argument("ses_id", type=int, required=True)
put_chat.add_argument("msg_id", type=int, required=True)
put_chat.add_argument("msg_src", type=int, required=True)
put_chat.add_argument("msg_dst", type=int, required=True)
put_chat.add_argument("msg_content", type=str, required=True)
put_chat.add_argument("msg_date", type=str, required=True)

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

class Device(Resource):
    def get(self, device_uid):
        if device_uid not in dev_reg:
            abort(404, message="device not registered")
        else:
            return dev_reg[device_uid]
    def put(self, device_uid):
        if device_uid in dev_reg:
            abort(404, message="device already registered")
        else:
            data = put_device.parse_args()
            dev_reg[device_uid] = data
            return dev_reg[device_uid], 201
    def delete(self, device_uid):
        if device_uid not in dev_reg:
            abort(404, message="device not registered")
        else:
            del dev_reg[device_uid]
            return '', 204

class Chat(Resource):
    def get(self, ses_id, msg_id):
        if ses_id not in chat_sessions:
            abort(404, message="session does not exist")
        else:
            if msg_id not in chat_sessions[ses_id]:
                abort(404, message="message does not exist within current session")
            else:
                return chat_sessions[ses_id[msg_id]]
    def put(self, ses_id, msg_id):
        if ses_id in chat_sessions:
            if msg_id in chat_sessions[ses_id]:
                abort(404, message="message already exists within current session")
            else:
                data = put_chat.parse_args()
                chat_sessions[ses_id[msg_id]] = data
                return chat_sessions[ses_id[msg_id]], 201
        else:
            data = put_chat.parse_args()
            chat_sessions[ses_id[msg_id]] = data
            return chat_sessions[ses_id[msg_id]], 201
    def delete(self, ses_id, msg_id):
        if ses_id not in chat_sessions:
            abort(404, message="session does noe exist")
        else:
            del chat_sessions[ses_id]
            return '', 204

class ValidateDevice(Resource):
    def get(self, json_file):
        returnCode, message = device_module.validate_input(json_file)

        if api_call_successful(return_code=returnCode,
                               msg=message):

            return {"result": returnCode,
                    "message": message,
                    "data": json_file}


class ValidateChat(Resource):
    def get(self, json_file):
        returnCode, message = chat_module.validate_input(json_file)

        if api_call_successful(return_code=returnCode,
                               msg=message):

            return {"result": returnCode,
                    "message": message,
                    "data": json_file}

# endpont for default homepage
api.add_resource(HomePage, "/")

# endpoint for device module
api.add_resource(Device, "/device/<string:device_uid>")

# endpoint for chat module
api.add_resource(Chat, "/chat/<string:ses_id>/<string:msg_id>")

# endpoints for JSON Validation
api.add_resource(ValidateDevice, "/chat-validate/<string:json_file>")
api.add_resource(ValidateChat, "/device-validate/<string:json_file>")

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, port=5001)
