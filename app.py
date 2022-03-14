# save this as app.py
from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/device_module_files')
def device_interface():
    return "Device Interface, Coming Soon"

@app.route('/chat_module_files')
def chat_interface():
    return "Chat Interface, Coming Soon"
