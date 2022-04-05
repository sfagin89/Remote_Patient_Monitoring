# RemotePatientMonitoring
Platform to monitor patients at home or in the hospitals

## Branching Strategy
Main Branch will be the primary code and only confirmed finished/working modules.
New branches will be created for each module. Once the new module has been completed, and tested both on it's own and with the main script, it will be merged back into the main branch.

## Error Codes

0x = Input Error
- 01: Filename
- 02: JSON Input Validation

1x = Format Errors for Device Data Input
- 11: User ID
- 12: Device ID
- 13: Device Type
- 14: Measurement Type
- 15: Measurement Value
- 16: Measurement Unit Type
- 17: Date

2x = Format Errors for Message Packets
- 21: Source User ID
- 22: Destination User ID
- 27: Date

?x = Database Errors to be Added

## Phase 1: Device Module
Description: Functions used to act as an interface for supported devices to interact with the application.

Current Status: Functional, QoL Updates In Progress

- Expects Data Input from device in JSON format
- Validates Filename
- Validates JSON data
- Expects the following data from all devices
  - Device Entries:
    - User associated with Measurements
    - Unique Device ID
    - Device Type
    - Type of Measurement (Must match with Device Type)
    - Value of Measurement
    - Unit of Measurement (Must match with Device Type)
    - Date of Measurement
  - Example Provided Below:
  ```json
  {
      "device_entry":
      [
          {
              "user_uid" : 1,
              "device_uid" : 1,
              "device_type" : "thermometer",
              "msrmt_type" : "temperature",
              "msrmt_val" : 98.6,
              "msrmt_unit" : "fahrenheit",
              "msrmt_date" : "12-31-2021"
          }
      ]
  }
  ```
### Device Module API
```
"URL" + "/device/<device_uid>" + data
```


## Phase 2: Chat Module
Current Status: Functional, QoL Updates In Progress

- Expects Message from User over Web GUI in JSON format
- Validates Filename
- Validates JSON data
- Expects the following data from all messages
  - Message Metadata:
    - Session ID of Message
    - Message ID of Message
    - Source User ID of Message
    - Destination User ID of Message
    - Content of Message
    - Date of Message
  - Example Provided Below:
  ```json
  {
      "message_metadata":
      [
          {
              "ses_id": 1,
              "msg_id": 2,
              "msg_src": 1,
              "msg_dst": 2,
              "msg_content" : "Hello User 2!",
              "msg_date" : "12-31-2021"
          }
      ]
  }
  ```
### Chat Module API
```
"URL" + "/chat/<session_id>/<message_id>" + data
```

### JSON Validator API
```
"URL" + "/chat-validate/" + json_file
"URL" + "/device-validate/" + json_file
```


## Phase 3: TBA
