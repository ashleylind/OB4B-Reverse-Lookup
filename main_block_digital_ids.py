import json
import logging
from utils.logging_function import setup_logger
from utils.block_digital_ids_on_staff_web import get_staff_assist_usernames



if __name__ == '__main__':
    with open('config/config.json') as config_file:
        config = json.load(config_file)
    log_file = config['log_file']
    logger = setup_logger(log_file, logging.INFO)

    get_staff_assist_usernames(logger)



