# py-raider-reporter
[![PyPI](https://img.shields.io/pypi/v/py-raider-reporter)](https://pypi.org/project/py-raider-reporter/)
[![license](https://img.shields.io/pypi/l/py-raider-reporter)](https://github.com/M0r13n/py-raider-reporter/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/M0r13n/py-raider-reporter/branch/master/graph/badge.svg)](https://codecov.io/gh/M0r13n/py-raider-reporter)
[![downloads](https://img.shields.io/pypi/dm/py-raider-reporter)](https://pypi.org/project/py-raider-reporter/)

#### Raider Reporter for Python. Used in pair with [Raider](https://github.com/valeriansaliou/raider), the Affiliates Tracker Page.


## Who uses it?

<table>
<tr>
<td align="center"><a href="https://smartphoniker.shop/"><img src="https://smartphoniker.shop/static/images/smartphoniker-logo.svg" height="64" /></a></td>
</tr>
<tr>
<td align="center">Smartphoniker</td>
</tr>
</table>



# How to install
Install with pip:

```sh
$ pip install py-raider-reporter
```


# How to use
`raider-reporter` can be instantiated as such:

```py
SAMPLE_CONFIG = {
    "host": "affiliates.example.shop",
    "track_token": "REPLACE_THIS_WITH_A_SECRET_TRACK_TOKEN",
}

reporter = RaiderReporter.from_config(SAMPLE_CONFIG)

# track payment
reporter.track_payment(SAMPLE_TRACKER_ID, 10.0)

# track signup
reporter.track_signup(SAMPLE_TRACKER_ID)
```


# What is Raider?
ℹ️ **Wondering what Vigil is?** Check out **[valeriansaliou/vigil](https://github.com/valeriansaliou/raider)**.
