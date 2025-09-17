import requests
from datetime import datetime
import time

# Ensure the inputs are passed in the correct order from the VI
def send_http_post( test_id, 
                    environment_id, 
                    sample_id, 
                    sensors_dict, 
                    operator_name):
    try:
        # JSON payload
        # The API will accept any JSON payload
        # The structure is not important, you can structure this however you want/need to
        # In the API you will then need to parse the JSON payload and extract the data you need
        data = {
            "sample_id": sample_id,
            "environment_id": environment_id,
            "operator_name": operator_name,
            "sensors_dict": sensors_dict,
            "timestamp_now": int(time.time() * 1000)
        }
        
        # Send POST request
        # Anatomy of the post request: 
        # [URL TO YOUR API] is the URL to your API
        # /data is the endpoint or route to send data to on the API
        # {test_id} will be used by the API as the KEY under which the data will be stored
        response = requests.post(f"[URL TO YOUR API]/data/{test_id}", json=data)
        
        # change the return to return whatever response you want or need to work with in LabVIEW.
        # e.g. if you need a particular value from a model that has been executed in Quix, you 
        # can parse the response and return the value you need.
        return f'{datetime.now()} \r\n\r\n\sent:\r\n{data}\r\n\r\nResponse:\r\n{response.json()}'
    
    except Exception as e:
        return f'ERROR: {e}'