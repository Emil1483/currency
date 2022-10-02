import json

import requests
from app.utils.helpers import (env_is_true, get_nested_value, read_txt,
                               write_txt)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager


def _browser_logs_from_events(logs):
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if (
            'Network.response' in log['method']
            or 'Network.request' in log['method']
            or 'Network.webSocket' in log['method']
        ):
            yield log

def _get_auth_from_event(event):
    return get_nested_value(event, 'params', 'request', 'headers', 'authorization')

def fetch_auth():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    capabilities = DesiredCapabilities.CHROME
    capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

    HAS_CHROME_DRIVER = env_is_true('HAS_CHROME_DRIVER', default=False)

    if HAS_CHROME_DRIVER:
        driver = webdriver.Chrome(
            desired_capabilities=capabilities,
            options=options
        )
    else:
        driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            desired_capabilities=capabilities,
            options=options
        )

    driver.get('http://www.xe.com')

    logs = driver.get_log('performance')
    
    driver.quit()

    for event in _browser_logs_from_events(logs):
        auth = _get_auth_from_event(event)
        if auth is not None:
            return auth
    
    for event in _browser_logs_from_events:
        auth = _get_auth_from_event(event)
        if auth is not None:
            return auth

def fetch_rates():
    API_URL = 'https://www.xe.com/api/protected/midmarket-converter/'

    auth = read_txt('xe_auth.txt')

    response = requests.get(API_URL, headers={
        'authorization': auth,
    })

    if not response.ok:
        auth = fetch_auth()
        write_txt('xe_auth.txt', auth)
        response = requests.get(API_URL, headers={
            'authorization': auth
        })

    rates = response.json()['rates']
    return rates
