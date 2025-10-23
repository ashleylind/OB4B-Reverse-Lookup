import json
from requests import Session, Request
import os
import socket


with open('config/config.json', 'r') as file:
    config = json.load(file)
SPLUNK_AUTH_KEY = config.get("splunk_auth_key")
# Constants (replace with your real values)
SPLUNK_URI = config.get("splunk_uri")
SPLUNK_HEADERS = {
    'Accept': "application/json",
    'Authorization': SPLUNK_AUTH_KEY
}
SPLUNK_INDEX = config.get("splunk_index")

def send_splunk_event(payload):
    """Send an event to Splunk HTTP Event Collector."""
    session = Session()
    request = Request("POST", SPLUNK_URI, data=json.dumps(payload), headers=SPLUNK_HEADERS)
    prepped = request.prepare()
    response = session.send(prepped, verify=False)
    return response

def log_bot_event(start_time, end_time, passed, key_value, logger):
    """Push a fixed structure event to Splunk."""
    payload = {
        "host": socket.gethostname(),
        "event": {
            "start": str(start_time),
            "end": str(end_time),
            "passed": str(passed),
            "unique_id": "1337",
            "bot_machine": socket.gethostname(),
            "bot_user": os.getlogin(),
            "heartbeat": "1",
            "key_type": "Digital ID",
            "key_value": str(key_value)
        },
        "source": "http:acoe_bot_events",
        "sourcetype": "_json",
        "index": SPLUNK_INDEX,
        "fields": {}
    }

    response = send_splunk_event(payload)
    if response.status_code == 200:
        logger.info(f"{str(response.status_code)} SPLUNK SUCCESS FOR ENTRY {key_value}")
    else:
        logger.error(f"{str(response.status_code)} SPLUNK FAILED FOR ENTRY {key_value}")
    return response.status_code, response.text
# if __name__ == "__main__":
#     start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     time.sleep(5)
#     end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     status, text = log_bot_event(start, end, 1, "5196********6789")
#     print(f"Splunk response [{status}]: {text}")
