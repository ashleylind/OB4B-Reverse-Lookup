import json
import logging
from utils.logging_function import setup_logger
from utils.get_pended_alert_details_and_save_to_sql import extract_pended_and_write_to_sql
from utils.get_staff_web_usernames import get_staff_assist_usernames
from utils.get_ping_ids import ping_ids
from utils.get_slam_data import get_slam_data


if __name__ == '__main__':
    with open('config/config.json') as config_file:
        config = json.load(config_file)
    log_file = config['log_file']
    logger = setup_logger(log_file, logging.INFO)

    extract_pended_and_write_to_sql(logger)
    get_staff_assist_usernames(logger)
    ping_ids(logger)
    get_slam_data(logger)



