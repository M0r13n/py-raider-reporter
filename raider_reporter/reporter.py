
import typing

import requests
from requests.sessions import InvalidSchema


class RequestFailedError(Exception):
    pass


def get_payment_payload(amount: float, currency: str, trace: str):
    return {
        "amount": amount,
        "currency": currency,
        "trace": trace
    }


class RaiderReporter(object):
    __slots__ = (
        'host',
        'track_token',
        'default_currency'
    )

    def __init__(
            self,
            host: str,
            track_token: str,
            default_currency: str = "EUR"
    ) -> None:
        """
        Create a new reporter instance.

        @param host: This is the host domain on which raider is running. Example: affiliates.example.com
        @param track_token: This is your secret track_token that you setup in your raider config.cfg
        @param default_currency: This is your default currency, that will be used for tracking payments. Defaults to EUR
        """
        self.host: str = host
        self.track_token: str = track_token
        self.default_currency: str = default_currency

        # prevent important values from beeing None
        for slot in self.__slots__:
            if not getattr(self, slot):
                raise ValueError("%s must not be None!" % slot)

    @classmethod
    def from_config(cls, config: typing.Dict):
        """
        Create a new RaiderReporter instance from a dict object.
        """
        return cls(
            config['host'],
            config['track_token'],
            config.get('default_currency', "EUR"),
        )

    def get_payment_reporting_url(self, tracking_id: str) -> str:
        if not tracking_id:
            raise ValueError("You need to provide a tracking_id!")

        url = "https://%s/track/payment/%s/" % (self.host, tracking_id)
        return url

    def get_signup_reporting_url(self, tracking_id: str) -> str:
        if not tracking_id:
            raise ValueError("You need to provide a tracking_id!")

        url = "https://%s/track/signup/%s/" % (self.host, tracking_id)
        return url

    def _make_request(self, url: str, data: typing.Dict) -> requests.Response:
        return requests.post(
            url=url,
            auth=('Authorization', self.track_token),
            json=data,
        )

    def _post_data(self, url: str, data: typing.Dict) -> requests.Response:
        try:
            response = self._make_request(url, data)
            return response
        except InvalidSchema as e:
            raise ValueError("Invalid URL schema! Make sure that you provide a valid host.") from e
        except requests.exceptions.ConnectionError:
            raise RequestFailedError("Raider could not be reached!")

    def _post_payment(self, tracking_id: str, data: typing.Dict) -> requests.Response:
        payment_url = self.get_payment_reporting_url(tracking_id)
        return self._post_data(url=payment_url, data=data)

    def _post_signup(self, tracking_id: str, data: typing.Dict) -> requests.Response:
        signup_url = self.get_signup_reporting_url(tracking_id)
        return self._post_data(url=signup_url, data=data)

    def _handle_raider_response(self, response: requests.Response) -> bool:
        # 4XX errors indicate a malformed request and are most likely caused through missconfiguration
        if 400 <= response.status_code < 500:
            raise RequestFailedError(
                "Could not complete tracking request! Vigil responded with %i - Please check your config." % response.status_code
            )
        if response.status_code != 200:
            raise RequestFailedError(
                "Could not complete tracking request! Vigil responded with %i!" % response.status_code
            )
        return True

    def track_payment(self, tracking_id: str, amount: float, currency: str = None, trace: str = None) -> bool:
        """
        Track a single payment.

        @param tracking_id:
        The tracking ID taken from the URL.

        @param amount:
        The full amount of the payment (Raider process the commission amount itself,
        eg. with 20% commission you send 100.00 and Raider processes it as 20.00)

        @param currency:
        The payment currency code (if the currency is different than the default currency configured with payout.currency,
        a conversion is applied using current day market rates)

        @param trace:
        An optional trace value which is logged in the database
        (may be used for your own records; this is never visible to your affiliate users
        """
        if not currency:
            currency = self.default_currency
        if not trace:
            trace = ""

        payload = get_payment_payload(amount, currency, trace)
        response = self._post_payment(tracking_id, payload)
        return self._handle_raider_response(response)

    def track_signup(self, tracking_id: str) -> bool:
        response = self._post_signup(tracking_id, {})
        return self._handle_raider_response(response)
