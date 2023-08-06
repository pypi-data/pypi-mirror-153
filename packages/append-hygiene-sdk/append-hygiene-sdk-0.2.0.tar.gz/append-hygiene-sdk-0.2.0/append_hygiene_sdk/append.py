import os
import json
import time

import requests as req
from dotenv import load_dotenv

from append_hygiene_sdk.logs import get_logger

load_dotenv()
ENV = os.getenv

logger = get_logger(os.path.basename(__file__))


class Append:
    append_id = None

    @staticmethod
    def push_append(payload: dict) -> str:
        """
        The push_append function pushes a new append to the OnDemand service.
        It takes in a payload, which is the JSON object that will be sent to
        the OnDemand service as an append. It returns the response from
        OnDemand.
        :param payload:dict: Pass the data to be appended
        :return: The status of the append request
        :doc-author: TheBridgeDan
        """
        logger.info("SENDING APPEND...")
        try:
            payload = payload
            response = req.post(f"{ENV('ONDEMAND_URL')}/appends", json=payload, timeout=60)
            logger.info(json.dumps(payload, indent=4))
            logger.info(f"FROM APPEND PUSH: {response.status_code}: {response.json()['status']}")
            logger.info(f"APPEND ID: {response.json()['id']}")
        except req.exceptions.RequestException as e:
            logger.error(e)
            return f"Error: Unexpected response {e}"
        # Update to Append id
        Append.append_id = response.json()["id"]

    @staticmethod
    def append_status(append_id: str, max_tries=5) -> bool:
        """
        The append_status function checks the status of an append job.
        It returns True if the Append is still in progress, and False if it has completed.
        :param append_id:str: Pass the append_id from the create_append function to this function
        :param max_tries: Determine how many times the function will try to get the status of an append before giving up
        :return: A boolean value
        :doc-author: TheBridgeDan
        """
        success_codes = (200, 201)
        success_statuses = ("in_progress", "new")
        tries_404 = 0
        while tries_404 < max_tries:
            try:
                response = req.get(f"{ENV('ONDEMAND_URL')}/appends/{append_id}", timeout=60)
                logger.info(f"APPEND STATUS: {response.status_code}")
                logger.info(f"START TIME: {response.json()['start_time']}")
                logger.info(f"END TIME: {response.json()['end_time']}")
                if response.status_code not in success_codes:
                    tries_404 += 1
                    time.sleep(5)
                    logger.info("Try again...")
                    continue
                if response.json()['status'] in success_statuses and response.json()['end_time'] is None:
                    logger.info(response.json()['status'])
                    return True
                else:
                    logger.info(response.json()['status'])
                    logger.info("APPEND COMPLETE")
                    return False
            except req.exceptions.RequestException as e:
                logger.error(e)
                return False
