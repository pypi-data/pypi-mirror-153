import os
import json
import time

import requests as req
from dotenv import load_dotenv

from append_hygiene_sdk.logs import get_logger

load_dotenv()
ENV = os.getenv

logger = get_logger(os.path.basename(__file__))


class Hygiene:
    hygiene_id = None

    @staticmethod
    def push_hygiene(payload: dict) -> str:
        """
        The push_hygiene function is used to send a POST request to the OnDemand service.
        The function takes in a dictionary payload and uses it as the body of the POST request.
        It then returns an HTTP response code from the post request.

        :param payload:dict: Pass in the payload to be sent to the api
        :return: The status code of the post request and the response body
        :doc-author: TheBridgeDan
        """
        logger.info("SENDING HYGIENE...")
        try:
            payload = payload
            response = req.post(f"{ENV('ONDEMAND_URL')}/hygiene_and_verification", json=payload, timeout=60)
            logger.info(json.dumps(payload, indent=4))
            logger.info(f"FROM HYGIENE PUSH: {response.status_code}: {response.json()['status']}")
            logger.info(f"HYGIENE ID: {response.json()['id']}")
        except req.exceptions.RequestException as e:
            logger.error(e)
            return f"Error: Unexpected response {e}"
        # Update the hygiene id
        Hygiene.hygiene_id = response.json()["id"]

    @staticmethod
    def hygiene_status(hygiene_id: str, max_tries=5) -> bool:
        """
        The hygiene_status function checks the status of a hygiene task.
        It returns True if the task is still in progress, and False if it has completed.
        :param hygiene_id:str: Pass the hygiene_id to the function
        :param max_tries: Set the number of times the function will try to query the api before returning false
        :return: A boolean value
        :doc-author: TheBridgeDan
        """

        success_codes = (200, 201)
        success_statuses = ("in_progress", "new")
        tries_404 = 0
        while tries_404 < max_tries:
            try:
                response = req.get(f"{ENV('ONDEMAND_URL')}/hygiene_and_verification/{hygiene_id}", timeout=60)
                logger.info(f"QUERY STATUS: {response.status_code}")
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
                    logger.info("HYGIENE COMPLETE")
                    return False
            except req.exceptions.RequestException as e:
                logger.error(e)
                return False
