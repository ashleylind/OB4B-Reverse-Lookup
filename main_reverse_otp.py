from utils.compare_di_with_otp_dest import compare_di_with_otp
from utils.extract_from_kibana import extract_from_kibana
from utils.block_digital_ids_on_staff_web import deactive_digital_ids
from utils.logging_function import setup_logger
import json
import logging
from utils.send_emails_to_team import process_email_statuses
import time


if __name__ == '__main__':
    with open('config/config.json') as config_file:
        config = json.load(config_file)
    log_file = config['log_file']
    logger = setup_logger(log_file, logging.INFO)

    extract_from_kibana(logger)
    matched, unmatched, exceptions = compare_di_with_otp(logger)
    if unmatched:
        disabled_report = deactive_digital_ids(logger, unmatched)
        if disabled_report:
            process_email_statuses(disabled_report, logger)
    time.sleep(60)



