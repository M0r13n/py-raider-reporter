
import random
from requests.models import Response
import raider_reporter.reporter as r
from raider_reporter.reporter import RaiderReporter, RequestFailedError, get_payment_payload
import unittest


SAMPLE_CONFIG = {
    "host": "affiliates.example.shop",
    "track_token": "REPLACE_THIS_WITH_A_SECRET_TRACK_TOKEN",
}

SAMPLE_TRACKER_ID = "8HWka001eh"


def post_success(*args, **kwargs):
    always_true_response = Response()
    always_true_response.status_code = 200
    return always_true_response


def post_fail(*args, **kwargs):
    fail = Response()
    status_code = random.randint(201, 599)
    fail.status_code = status_code
    return fail


ORIGINAL_FUNC = r.RaiderReporter._post_data


def restore_original():
    r.RaiderReporter._post_data = ORIGINAL_FUNC


class VigilTestSuite(unittest.TestCase):
    """ Testcases for Vigil Reporter """

    def test_init(self):
        reporter = RaiderReporter(
            host=SAMPLE_CONFIG['host'],
            track_token="123"
        )
        assert reporter.host == SAMPLE_CONFIG['host']
        assert reporter.track_token == "123"
        assert reporter.default_currency == "EUR"

        reporter = RaiderReporter(
            host=SAMPLE_CONFIG['host'],
            track_token="123",
            default_currency="USD"
        )

        assert reporter.default_currency == "USD"

    def test_init_invalid(self):
        self.assertRaises(ValueError, lambda: RaiderReporter("", ""))

    def test_init_with_config(self):
        reporter = RaiderReporter.from_config(SAMPLE_CONFIG)
        assert reporter.host == SAMPLE_CONFIG['host']
        assert reporter.track_token == "REPLACE_THIS_WITH_A_SECRET_TRACK_TOKEN"
        assert reporter.default_currency == "EUR"

        reporter = RaiderReporter.from_config({
            "host": "124",
            "track_token": "REPLACE_THIS_WITH_A_SECRET_TRACK_TOKEN",
            "default_currency": "USD"
        })
        assert reporter.default_currency == "USD"

    def test_init_with_config_malformed(self):
        self.assertRaises(ValueError, lambda: RaiderReporter.from_config({
            "host": None,
            "track_token": "REPLACE_THIS_WITH_A_SECRET_TRACK_TOKEN",
        }))

    def test_payment_url(self):
        reporter = RaiderReporter.from_config(SAMPLE_CONFIG)
        url = reporter.get_payment_reporting_url("123")

        assert url == "https://affiliates.example.shop/track/payment/123/"

        self.assertRaises(ValueError, lambda: reporter.get_payment_reporting_url(""))
        self.assertRaises(ValueError, lambda: reporter.get_payment_reporting_url(None))

    def test_signup_url(self):
        reporter = RaiderReporter.from_config(SAMPLE_CONFIG)
        url = reporter.get_signup_reporting_url("123")

        assert url == "https://affiliates.example.shop/track/signup/123/"

        self.assertRaises(ValueError, lambda: reporter.get_signup_reporting_url(""))
        self.assertRaises(ValueError, lambda: reporter.get_signup_reporting_url(None))

    def test_track_payment(self):
        r.RaiderReporter._post_data = post_success
        reporter = RaiderReporter.from_config(SAMPLE_CONFIG)
        assert reporter.track_payment(SAMPLE_TRACKER_ID, 10.0)
        restore_original()

    def test_track_signup(self):
        r.RaiderReporter._post_data = post_success
        reporter = RaiderReporter.from_config(SAMPLE_CONFIG)
        assert reporter.track_signup(SAMPLE_TRACKER_ID)
        restore_original()

    def test_failed_response_raises_error(self):
        r.RaiderReporter._post_data = post_fail
        reporter = RaiderReporter.from_config(SAMPLE_CONFIG)
        self.assertRaises(RequestFailedError, lambda: reporter.track_payment(SAMPLE_TRACKER_ID, 23.0))

    def test_payload(self):
        payload = get_payment_payload(95.00, "EUR", "Plan: Unlimited; Customer: valerian@crisp.chat; Website: crisp.chat")
        assert payload == {
            "amount": 95.00,
            "currency": "EUR",
            "trace": "Plan: Unlimited; Customer: valerian@crisp.chat; Website: crisp.chat"
        }


if __name__ == "__main__":
    unittest.main()
