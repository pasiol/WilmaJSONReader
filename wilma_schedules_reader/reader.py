import sys
import hashlib
import time
import requests
import json
import logging
import click
import mypy
from datetime import date, timedelta
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def __get_session_key(url: str, s: requests.Session) -> str:
    try:
        r = s.get(url + "index_json", verify=True)
        json_response = json.loads(r.text)
        if "SessionID" in json_response.keys():
            logger.info(f"Getting session key succesfully.")
            return json_response["SessionID"]
        else:
            return ""
    except Exception as error:
        logger.error(f"Getting session key failed: {error}")
        sys.exit(1)


def __fidate2pydate(fi_date: str, logger: logging.Logger) -> date:
    try:
        splitted_date = str(fi_date).split(".")
        return date(int(splitted_date[2]), int(splitted_date[1]), int(splitted_date[0]))
    except Exception as error:
        logger.error(f"Getting timedelta failed: {error}")
        sys.exit(1)


def __get_time_delta(start: str, end: str, logger: logging.Logger) -> timedelta:
    s = __fidate2pydate(start, logger)
    e = __fidate2pydate(end, logger)
    return e - s


def __get_dates(start: str, end: str, logger: logging.Logger) -> List[str]:
    dates = list()
    delta = __get_time_delta(start, end, logger)
    print(f"{delta}")
    for d in range(delta.days + 1):
        day = __fidate2pydate(start, logger) + timedelta(days=d)
        dates.append(str(day.strftime("%d.%m.%Y")))
    return dates


def valid_type(type: str) -> bool:
    if type in ["rooms", "teachers", "students"]:
        return True
    else:
        return False


@click.command()
@click.argument("resource_type", type=click.STRING)
@click.argument("start_date", type=click.STRING)
@click.argument("end_date", type=click.STRING)
@click.argument("wilma_url", type=click.STRING)
@click.argument("user", type=click.STRING)
@click.argument("password", type=click.STRING)
@click.argument("apikey", type=click.STRING)
@click.argument("output_path", type=click.Path(exists=True))
def main(
    resource_type, start_date, end_date, wilma_url, user, password, apikey, output_path
):
    if valid_type(resource_type):
        wilma_url = f"https://{wilma_url}/"
        s = requests.Session()
        sessionid = __get_session_key(wilma_url, s)
        apikey = hashlib.sha1(
            str(f"{user}|{sessionid}|{apikey}").encode("utf-8")
        ).hexdigest()
        data = {
            "Login": user,
            "Password": password,
            "SessionId": sessionid,
            "ApiKey": "sha1:" + apikey,
            "format": "json",
        }
        headers = {"accept": "application/json"}
        r = s.post(wilma_url + "login", data=data, headers=headers, verify=True)

        if r.status_code == 200:
            logger.info(f"Logged succesfully in. Getting status code {r.status_code}.")
            dates = __get_dates(start=start_date, end=end_date, logger=logger)
            print(f"{dates}")
            for day in dates:
                schedule = f"schedule/index_json?p={day}&f={day}&{resource_type}=all"
                succeed = False
                r = None
                while not succeed:
                    try:
                        r = s.get(wilma_url + schedule)
                        succeed = True
                    except Exception as error:
                        logger.error(
                            f"Failing to get url: {wilma_url + schedule}: {error}"
                        )
                        logger.info("Sleeping 20 seconds.")
                        time.sleep(20)
                try:
                    with open(
                        f"{output_path}/{resource_type}-{day}-data.json",
                        "w",
                        encoding="utf-8",
                    ) as output_file:
                        json.dump(r.json(), output_file)
                except Exception as error:
                    logger.critical(
                        f"Writing output file failed: {error}. Nothing to do."
                    )
                    sys.exit(1)
                time.sleep(1)
                logger.info(f"Processed resource {resource_type} at the date {day}.")
        else:
            logger.critical(
                f"Loging failed. Getting status code {r.status_code}. Nothing to do."
            )
    else:
        logger.critical(f"Resource type {resource_type} is not valid.")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter