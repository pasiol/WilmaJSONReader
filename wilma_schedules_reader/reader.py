import os
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
        logger.info("Response: {}".format(r.text))
        if "SessionID" in json_response.keys():
            return json_response["SessionID"]
        else:
            return ""
    except Exception as error:
        logger.error(str(error))
        sys.exit(1)


def __fidate2pydate(date_fi: str, logger: logging.Logger = None) -> date:
    try:
        splitted_date = str(date_fi).split(".")
        return date(int(splitted_date[2]), int(splitted_date[1]), int(splitted_date[0]))
    except Exception as error:
        if logger is not None:
            logger.error(f"Getting timedelta failed: {error}")
        else:
            print(f"Getting timedelta failed: {error}")
        sys.exit(1)


def __get_time_delta() -> timedelta:
    s = date.today()
    e = __fidate2pydate(f"1.1.{date.today().year}", None)
    return s - e


def __get_dates(logger: logging.Logger = None) -> List[str]:
    dates = list()
    delta = __get_time_delta()
    start_date_as_date = __fidate2pydate(f"1.1.{date.today().year}")
    for d in range(delta.days + 1):
        day = start_date_as_date + timedelta(days=d)
        dates.append(str(day.strftime("%d.%m.%Y")))
    return dates


@click.command()
@click.argument("resource", type=click.STRING)
@click.argument("startDate", type=click.STRING)
@click.argument("endDate", type=click.STRING)
@click.argument("wilmaURL", type=click.STRING)
@click.argument("user", type=click.STRING)
@click.argument("password", type=click.STRING)
@click.argument("apikey", type=click.STRING)
@click.argument("path", type=click.File)
def main(resource, startDate, endDate, wilmaURL, user, password, apikey):
    wilma_url = f"https://{wilmURL}"
    s = requests.Session()
    sessionid = __get_session_key(wilma_url, s)
    apikey = hashlib.sha1(
        str(f"{user}|{sessionid}|{apikey}").encode("utf-8")
    ).hexdigest()
    data = {
        "Login": os.environ["USER"],
        "Password": os.environ["PASSWORD"],
        "SessionId": sessionid,
        "ApiKey": "sha1:" + apikey,
        "format": "json",
    }
    headers = {"accept": "application/json"}
    r = s.post(wilma_url + "login", data=data, headers=headers, verify=True)

    if r.status_code == 200:
        logger.info(f"Logged succesfully in. Getting status code {r.status_code}.")
        dates = __get_dates()
        for day in dates:
            schedule = f"schedule/index_json?p={day}&f={day}&{resource}=all"
            succeed = False
            r = None
            while not succeed:
                try:
                    r = s.get(wilma_url + schedule)
                    succeed = True
                except Exception as error:
                    logger.error(
                        f"Failing to get url: {wilma_url + schedule}.\n{error}"
                    )
                    time.sleep(20)
            try:
                with open(
                    f"data/{resource}-{day}-data.json", "w", encoding="utf-8"
                ) as output_file:
                    json.dump(r.json(), output_file)
            except Exception as error:
                logger.critical(f"Writing output file failed: {error}. Nothing to do.")
                sys.exit(1)
            time.sleep(2)
            logger.info(f"Processed resource {resource} at the date {day}.")
    else:
        logger.critical(
            f"Loging failed. Getting status code {r.status_code}. Nothing to do."
        )


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
