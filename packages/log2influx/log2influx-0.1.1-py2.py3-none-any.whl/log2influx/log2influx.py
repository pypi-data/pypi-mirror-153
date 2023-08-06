"""Main module."""
import logging
from datetime import datetime, timedelta
from unittest import result
from black import err
from influxdb_client import InfluxDBClient, Point, WritePrecision, QueryApi
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

logger = logging.getLogger(__name__)


class Log2Influx(object):
    def __init__(
        self, url: str, org: str, token: str, bucket: str, app_id: str
    ) -> None:
        """This utility only supports InfluxDB 2.x.

        Args:
            url (str): Influx database connection URL
            org (str): org
            token (str): access token
            bucket (str): bucket to read and write
        """
        self.url = url
        self.org = org
        self.token = token
        self.bucket = bucket

        self.app_id = app_id

        self.connect()

    # Calling destructor
    def __del__(self):
        logger.info("Log2Influx Destructor called")
        try:
            self.client.close()
            del self.client
        except Exception:
            pass

    def connect(self):
        logger.info(f"connect to influxdb: {self.url} {self.org} {self.bucket}")
        self.client = InfluxDBClient(
            url="https://influxdb.swarm.edmonton.ca", token=self.token, org=self.org
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    # https://docs.influxdata.com/influxdb/v2.2/reference/syntax/line-protocol/
    def push_metrics(
        self,
        measurement: str,
        tags: dict,
        metrics: dict,
        time: datetime = datetime.utcnow(),
    ):
        """fucntion to store metrics

        Args:
            measurement (str): name of measurement. Same as table in RDBMS
            tags (dict): tags. Same as column in RDBMS
            metrics (dict): Store as Influxdb field. most of them are numbers.
            time (datetime, optional): timestamp. Defaults to datetime.utcnow().

        Returns:
            _type_: _description_
        """
        data = {
            "measurement": measurement,
            "tags": tags,
            "fields": metrics,
            "time": time,
        }
        point = Point.from_dict(data)

        try:
            ret = self.write_api.write(self.bucket, self.org, record=point)
        except InfluxDBError as ex:
            # if ex.response.status == 401:
            logger.error(ex)

        return ret

    def event_login(self, user):
        tags = {"app_id": self.app_id, "user": user}
        metrics = {"count": 1}
        self.push_metrics("login", tags, metrics)

    def event_logout(self, user):
        tags = {"app_id": self.app_id, "user": user}
        metrics = {"count": 1}
        self.push_metrics("logout", tags, metrics)

    def event_data_load(self, user=None, success=True):
        tags = {"app_id": self.app_id, "user": user}
        if success is True:
            metrics = {"success": 1}
        else:
            metrics = {"failure": 1}

        self.push_metrics("data_load", tags, metrics)

    def event_others(self, event_name, user=None, metrics=None):
        tags = {"app_id": self.app_id, "user": user}
        if metrics is None:
            metrics = {"count", 1}

        self.push_metrics(event_name, tags, metrics)

    def log(self, log_level, message):
        data = {
            "measurement": "logging",
            "tags": {"app_id": self.app_id, "log_level": log_level},
            "fields": {"message": message, "count": 1},
            "time": datetime.utcnow(),
        }
        point = Point.from_dict(data)

        try:
            ret = self.write_api.write(self.bucket, self.org, record=point)
        except InfluxDBError as ex:
            # if ex.response.status == 401:
            logger.error(ex)

        return ret

    def delete_data(
        self,
        measurement: str,
        start: str = "1970-01-01T00:00:00Z",
        stop: str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        ):
        """This function clear out data for a measurement/table.

        Args:
            measurement (str): measurement name

            start (str, optional): isoformat datetime. Defaults to "1970-01-01T00:00:00Z".
            stop (str, optional): isoformat datetime. Defaults to datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        """
        error = False
        try:
            ret = self.client.delete_api().delete(
                start, stop, f"_measurement={measurement}", 
                bucket=self.bucket, org=self.org
            )
        except InfluxDBError as ex:
            # if ex.response.status == 401:
            logger.error(ex)
            error = True

        return error

    # query examples
    # https://github.com/influxdata/influxdb-client-python/blob/master/examples/query.py
    def get_query_api(self) -> QueryApi:
        """The function return Influxdb query api.
            Because the query is very flexible,
            this util does not wrap the query funciton for you.
            please reference to this example to write your own query.
            https://github.com/influxdata/influxdb-client-python/blob/master/examples/query.py

        Returns:
            QueryApi: influxdb queery api
        """

        return self.client.query_api()
