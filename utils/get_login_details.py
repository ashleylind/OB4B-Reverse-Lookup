import requests
import json
import logging
from utils.logging_function import setup_logger

def get_login_details_kibana():
    try:
        with open('config/config.json') as config_file:
            config = json.load(config_file)
        log_file = config['log_file']
        logger = setup_logger(log_file, logging.INFO)
        url = config['mobius_user_cyberark_url']
        # ca_cert_bundle_path = config['SA_acc_api_cert_path']
        # Send a GET request
        response = requests.get(url, verify=False)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Access specific fields in the response
            domain = data["Address"]
            username = data["UserName"]
            password = data["Content"]
        else:
            logger.error(f"Request failed with status code: {response.status_code}") 
        return domain, username, password
    except:
        logger.error("Error retrieving SA credentials from API")