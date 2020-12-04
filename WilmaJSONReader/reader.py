import sys
import hashlib
import time
import requests
import json
import logging
import click
import validators
import mypy
from datetime import date, timedelta
from typing import List, Optional


class WilmaJSONReader:

    logger = None
    wilma_url = None
    session = requests.Session()
    _session_api_key = None
    _apikey = None
    _user = None
    _password = None

    def __init__(self, wilma_url: str, user: str, password: str, apikey: str):

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.wilma_url = f"https://{wilma_url}/"
        if not validators.url(self.wilma_url):
            self.logger.critical(f"Wilma URL {self.wilma_url} is not valid.")
            sys.exit(1)
        self._user = user
        self._password = password
        self._apikey = apikey
        self.logger.info(f"WilmaJSONReader object initialized succesfully.")

    def get_session_key(self) -> str:
        try:
            r = self.session.get(self.wilma_url + "index_json", verify=True)
            json_response = json.loads(r.text)
            if "SessionID" in json_response.keys():
                self.logger.info(f"Getting session key succesfully.")
                return json_response["SessionID"]
            else:
                return ""
        except Exception as error:
            self.logger.error(f"Getting session key failed: {error}")
            sys.exit(1)

    def login(self):
        sessionid = self.get_session_key()
        self._session_api_key = hashlib.sha1(
            str(f"{self._user}|{sessionid}|{self._apikey}").encode("utf-8")
        ).hexdigest()
        data = {
            "Login": self._user,
            "Password": self._password,
            "SessionId": sessionid,
            "ApiKey": "sha1:" + self._session_api_key,
            "format": "json",
        }
        headers = {"accept": "application/json"}
        r = self.session.post(
            self.wilma_url + "login", data=data, headers=headers, verify=True
        )
        if r.status_code == 200:
            self.logger.info(
                f"Logged succesfully in. Getting status code {r.status_code}."
            )
        else:
            self.logger.info(
                f"Loging failed, status code {r.status_code}. Nothing to do."
            )
            sys.exit(1)

    def _fidate2pydate(self, fi_date: str, logger: logging.Logger) -> date:
        try:
            splitted_date = str(fi_date).split(".")
            return date(
                int(splitted_date[2]), int(splitted_date[1]), int(splitted_date[0])
            )
        except Exception as error:
            self.logger.error(f"Getting timedelta failed: {error}")
            sys.exit(1)

    def _get_time_delta(
        self, start: str, end: str, logger: logging.Logger
    ) -> timedelta:
        s = self._fidate2pydate(start, logger)
        e = self._fidate2pydate(end, logger)
        return e - s

    def get_dates(self, start: str, end: str, logger: logging.Logger) -> List[str]:
        dates = list()
        delta = self._get_time_delta(start, end, logger)
        for d in range(delta.days + 1):
            day = self._fidate2pydate(start, logger) + timedelta(days=d)
            dates.append(str(day.strftime("%d.%m.%Y")))
        return dates

    def _validate_schedule_type(self, type: str) -> bool:
        if type in ["rooms", "teachers", "students"]:
            return True
        else:
            return False

    def get_schedule(
        self, day: str, resource_type: str
    ) -> Optional[requests.models.Response]:
        schedule = None
        if self._validate_schedule_type(resource_type):
            try:
                schedule = f"schedule/index_json?p={day}&f={day}&{resource_type}=all"
                r = self.session.get(self.wilma_url + schedule)
                return r
            except Exception as error:
                self.logger.error(
                    f"Failing to get url: {self.wilma_url + schedule}: {error}"
                )
                return None
        else:
            self.logger.critical(
                f"Resource type {resource_type} is not valid Wilma resource type."
            )
            sys.exit(1)


def write_json_file(
    filename: str, r: requests.models.Response, logger: logging.Logger
) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as output_file:
            json.dump(r.json(), output_file)
    except Exception as error:
        logger.critical(f"Writing output file failed: {error}. Nothing to do.")
        sys.exit(1)


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
    resource_type,
    start_date,
    end_date,
    wilma_url,
    user,
    password,
    apikey,
    output_path,
):

    reader = WilmaJSONReader(wilma_url, user, password, apikey)
    reader.login()
    dates = reader.get_dates(start=start_date, end=end_date, logger=reader.logger)
    for day in dates:
        succeed = False
        while not succeed:
            r = reader.get_schedule(day, resource_type)
            if r is not None:
                if r.status_code == 200:
                    succeed = True
                    write_json_file(
                        f"{output_path}/{resource_type}-{day}-data.json",
                        r,
                        reader.logger,
                    )
                else:
                    reader.logger.error(
                        f"Getting status code: {r.status_code}. Nothing to save."
                    )
            else:
                reader.logger.error(
                    f"Request failed. Sleeping 20 seconds and trying again."
                )
                time.sleep(20)
        time.sleep(1)
        reader.logger.info(f"Processed resource {resource_type} at the date {day}.")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter