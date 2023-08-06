import requests
from elasticsearch_dsl import Search
from elasticsearch_dsl.response import Response
from minetext.config import Config
from minetext.domain.es_request import EsRequest
from datetime import datetime


class Mine:
    _host: str
    _es_request: EsRequest
    _internal_token: str
    _device_code: str
    _user_code: str
    _verification_uri: str
    _verification_uri_complete: str
    _access_token: str
    _refresh_token: str
    _token_creation_time: float
    _expiration_time: int

    def __init__(self, es_request: EsRequest, host: str = Config.host):
        """
        Initialize the MINE object.

        :param host: the endpoint of the REST API
        :param es_request: the object containing request information to Elasticsearch
        """
        self._host = host
        self._es_request = es_request
        self._device_code = ''
        self._user_code = ''
        self._verification_uri = ''
        self._verification_uri_complete = ''
        self._access_token = ''
        self._refresh_token = ''
        self._token_creation_time = -1
        self._expiration_time = -1

    def search(self) -> Response:
        """
        Call the search endpoint with parameters provided via the :py:attr:`_es_request` property.

        Returns
        -------
        result : Response
            the search result wrapped in the :py:class:`Response` object.

        Raises
        ------
        HTTPError
            if the request failed.
        """
        url = f'{self._host}/document/search'

        payload = {
            'q': self._es_request.search_term,
            'f[]': self._es_request.filters,
            'a': self._es_request.aggregation,
            'p': self._es_request.page,
            's': self._es_request.size,
            'wa': self._es_request.analytics
        }

        if self._access_token:

            # Refresh the access token if necessary
            if self._token_needs_refresh():
                self._refreshing_token()

            # Use the access token
            headers = {
                'Authorization': f'Bearer {self._access_token}'
            }

            try:
                result = requests.get(url, params=payload, headers=headers)
            except requests.HTTPError as e:
                # This is when the user is unauthorized. If they have an _access_token but 
                # are unauthorized the _access_token probably expired. 401 is unauthorized.
                if e.response.status_code == 401:
                    self._refreshing_token()
                    headers['Authorization'] = f'Bearer {self._access_token}'
                    result = requests.get(url, params=payload, headers=headers)
                else:
                    raise e
        else:
            result = requests.get(url, params=payload)

        # Parse the result using Elasticsearch Response
        response = Response(Search(), result.json())

        return response

    def _token_needs_refresh(self) -> bool:
        """
        Checks if the access token is still usable within the next 20 seconds.

        Returns
        -------
        True
            if the token is (almost) expired.
        False
            if the token is still usable.
        """
        curr_time = datetime.now().timestamp()
        return curr_time - self._token_creation_time > 1000 * (self._expiration_time - 20)

    def _refreshing_token(self) -> None:
        """
        Creates a new access token with the refresh token.

        Sets a new refresh token, access token and updates the expiration times.
        When the refresh token does not work the user is forwarded to login again.

        Raises
        -------
        HTTPError 
            When the token could not be refreshed.
        """
        payload = {
            'refresh_token': self._refresh_token
        }
        try:
            token_response = requests.post(f"{self.host}/auth/refresh_token", json=payload)
        except requests.HTTPError:
            # This should realistically not happen as the refresh token gets updated every time the 
            # authorization token is updated and the refresh token has a very long expiration time.
            print('You need to login again.')
            self.login()
            return
        self._set_values(token_response.json())

    def _set_values(self, json) -> None:
        self._access_token = json['access_token']
        self._refresh_token = json['refresh_token']
        self._expiration_time = json['expires_in']
        self._refresh_expiration_time = json['refresh_expires_in']
        self._token_creation_time = datetime.now().timestamp()

    def _create_device_token(self) -> None:
        """
        Sets device token from mine-graph-api.

        Sets the uris, device_code and user_code from response.

        Raises
        -------
        HTTPError
            When device token could not be created.
        """
        device_token_response = requests.get(f'{self.host}/auth/device_token')
        device_token_response.raise_for_status()
        token_json = device_token_response.json()
        self._device_code = token_json['device_code']
        self._user_code = token_json['user_code']
        self._verification_uri = token_json['verification_uri']
        self._verification_uri_complete = token_json['verification_uri_complete']

    def _create_access_token(self) -> None:
        """
        Sets access token from authentication.

        Posts the device_code to MINE-API. If the user logged in properly
        the device code should now authorize them. Sets the access_token of Auth object.

        Raises
        -------
        HTTPError
            When access token could not be created. This happens mostly when the user did not log in properly
            but stated they did so.
        """
        token_response = requests.post(f'{self.host}/auth/token', json={'device_code': self._device_code})
        token_response.raise_for_status()
        self._set_values(token_response.json())
        print('Login successful! You are now authorized.')

    def login(self) -> None:
        """
        Calls the functions to authorize user.

        Waits for the user to log in into the verification uri and afterwards creates an access token if the user
        stated they granted access.
        """
        self._create_device_token()
        print(f'Please sign in at this website and grant access: {self._verification_uri_complete}')
        input_str = input('Did you grant the access? [y/N]')
        if input_str != 'y':
            return
        self._create_access_token()

    def get_identifiers(self):
        """
        Call the get_identifiers endpoint

        :return: the result return list of identifiers
        """
        result = self.search()

        response = []
        for hit in result.hits:
            identifier = hit.meta.id
            response.append(identifier)

        return response

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def es_request(self):
        return self._es_request

    @es_request.setter
    def es_request(self, value):
        self._es_request = value
