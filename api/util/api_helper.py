import abc
import requests
import simplejson
import os
import itertools
import datetime


class AbstractAPIHelper(object):
    """
    This is a base helper class that should be inherited by all
    classes that make api calls. The following methods should be overwritten
    according to the api's request and return structure:

     * `build_request()`
     * `parse_data()`

    All of the below properties and parameters may not be needed for every service.
    Additionally, this object may be missing certain properties needed for some services.
    This object is meant to act as a base class and is structured based on the parameters
    used by most api's. It can be extended and additional class properties can be added as needed
    depending on the service or platform being called.

    :param api_key: The api_key assigned by the service. Used to access said service's api.
    :type api_key: str

    :param api: The name of the service or platform (e.g. Instapush, etc.)
    :type api: str

    :param endpoint: The name of the endpoint being accessed.
    :type endpoint: str

    :param return_format: The return format for this request (e.g. "json").
    :type return_format: str

    :param api_version: The version of the api being called.
    :type api_version: str

    :param base_url: The base url for the api call. This will typically contain string formatting brackets to be replaced later.
    :type base_url: str

    :param params: key, value containing param name and param value. e.g. {'countryCode': 'US'}
    :type params: dict

    :param _parse_params: a variable method that returns params in url format k=v&k=v etc.
    :returns: str

    :param execute_call: a variable method that executes the api call.
    :returns: requests response object
    """

    def __init__(self):
        pass

    @abc.abstractproperty
    def api_key(self):
        return None

    @abc.abstractproperty
    def api(self):
        return None

    @abc.abstractproperty
    def endpoint(self):
        return None

    @abc.abstractproperty
    def return_format(self):
        return None

    @abc.abstractproperty
    def api_version(self):
        return None

    @abc.abstractproperty
    def base_url(self):
        return None

    @abc.abstractproperty
    def params(self):
        return None

    def _now(self):
        """
        Helper method to return the current time. This can be used to measure
        api token expirations and set token retrieval times.

        :returns: datetime object reflecting utc time
        """
        return datetime.datetime.utcnow()

    def _dedupe(self, rows):
        """
        Dedupes a list of lists

        :param rows: A list of lists representing rows of a table. This structure is what is fed into the parse_data method.
        :type rows: list
        """
        rows.sort()
        return list(k for k,_ in itertools.groupby(rows))

    @property
    def _parse_params(self):
        return '&'.join(["{0}={1}".format(k,v) for k, v in self.params.items()])

    def build_request(self):
        """
        Override to build the actual api request
        This may be a raw url, or headers and payloads.
        Typically, this will call self._pars_params
        """
        raise NotImplementedError

    @abc.abstractproperty
    def execute_call(self):
        return requests.get(self.build_request())

    def fetch_data(self):
        """
        Used to call the api to retrieve data and parse the return object.

        :returns: dict of the parsed data
        """
        return simplejson.loads(self.execute_call.text)

    def parse_data(self, data):
        """
        Override me to return rows that will be inserted
        into the database

        This method should return a list of lists that represents the table.

        Example:
        ```
        [
            [data, data],
            [data, data],
            [data, data]
        ]
        ```
        """
        raise NotImplementedError

    def run(self):
        """
        Programmatically calls the following methods to return an object that
        can be written to the database-upload file:

         * `execute_call`
         * `fetch_data`
         * `parse_data`

        :returns: A list of lists that represents the table.
        """
        return self.parse_data(self.fetch_data())

