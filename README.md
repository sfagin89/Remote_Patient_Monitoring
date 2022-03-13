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

### Phase 1: Device Module
Description: Functions used to act as an interface for supported devices to interact with the application.

Current Status: Complete

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

### Phase 2: Char Module
Current Status: Complete

### Phase 3: TBA
