import device_module
import json
def test_device_module():
    # JSON Data is not related
    #error_code, data = device_module.validate_input('wrong_data.json')
    #print(data)
    #assert error_code == 0

    # Entry is Valid
    error_code, data = device_module.validate_input('valid_schema.json')
    print(data)
    assert error_code == 0

    # Testing for invalid User ID
    error_code, data = device_module.validate_input('invalid_uid.json')
    print(data)
    assert error_code == 11

    # Testing for invalid Device ID
    error_code, data = device_module.validate_input('invalid_did.json')
    print(data)
    assert error_code == 12

    # Testing for unsupported Device Type
    error_code, data = device_module.validate_input('unsupported_dev_type.json')
    print(data)
    assert error_code == 13

    # Testing for incorrect measurement type
    error_code, data = device_module.validate_input('wrong_mes_type.json')
    print(data)
    assert error_code == 14

    # Testing for correctly formatted measurement value
    error_code, data = device_module.validate_input('invalid_mes_val.json')
    print(data)
    assert error_code == 15

    # Testing for incorrect measurement unit
    error_code, data = device_module.validate_input('wrong_mes_unit.json')
    print(data)
    assert error_code == 16

    # Testing for incorrectly formatted date
    error_code, data = device_module.validate_input('invalid_date_format.json')
    print(data)
    assert error_code == 17

    # Testing Improper JSON format
    error_code, data = device_module.validate_input('invalid_json.json')
    print(data)
    assert error_code == 2

    # Testing missing or incorrect file name
    error_code, data = device_module.validate_input('missing_file.json')
    print(data)
    assert error_code == 1
