import json
import logging
from utils.logging_function import setup_logger
from utils.delink_devices_from_bpid_copy_2 import delink_from_bpids


if __name__ == '__main__':
    with open('config/config.json') as config_file:
        config = json.load(config_file)
    log_file = config['log_file']
    logger = setup_logger(log_file, logging.INFO)


    delink_from_bpids(logger)



