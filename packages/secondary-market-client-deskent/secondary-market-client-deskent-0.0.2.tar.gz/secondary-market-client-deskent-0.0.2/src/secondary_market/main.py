import json
import time
from json import JSONDecodeError
from dataclasses import dataclass
from typing import Any
import logging

import aiohttp
import aiohttp.client_exceptions
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from .bot_settings import *

if DEBUG:
    from services.scripts.secondary_server import SecondaryManager


@dataclass
class SecondaryClient:
    """Client software for Secondary Market Bot

    Attributes:
        browser: instance of selenium webdriver
        auction_id: int - auction id number for cookie imitation
        product_data: list[dict] - list of products data for buying
        requests_count: int - number of requests for each product will be sent
        proxy_login: str - login for proxy access
        proxy_password: str - password for proxy access

     Methods:
         start
     """

    browser: Any = None
    lot_id: int = 0
    prepare_time: int = 10
    product_data: list[dict] = None
    requests_count: int = None
    sale_time: int = None
    proxy_login: str = None
    proxy_password: str = None
    currency: str = "BUSD"
    headers: dict = None
    check_status_id: int = -1
    license_key: str = None
    place_a_bid_button: str = '//button[@class=" css-1gv20g8"]'
    confim_a_bid_button: str = '//button[@class=" css-1yciwke"]'
    accept_cookie_button_x_path: str = '//*[@id="onetrust-accept-btn-handler"]'
    term_accepted: bool = False
    request_id: int = 0

    @logger.catch
    async def start(self):
        """Main class function"""

        if not DEBUG:
            if not await self._check_license_key():
                return
            if not await self._get_license_approve():
                return

        self._logging_in()
        self._imitation_cookie()
        self._wait_for_time(prepare_time=15)
        self._get_headers()
        if await self._buy_products():
            results: list[str] = await self._get_results()
            self._show_results(results)

    @logger.catch
    async def _check_license_key(self) -> bool:
        """Checks license key"""

        logger.info("Checking license key...")

        self.license_key: str = self._load_license_key()
        if not self.license_key:
            logger.error(f"License not found.")
            return False
        data: dict = {
            "license_key": self.license_key
        }
        answer: dict = await self._send_request(url=LICENSE_CHECK_URL, data=data)
        if not answer:
            logger.error(f"\n\tNo answer from checking license: "
                         f"\n\tLicense key: [{self.license_key}]")
            return False
        success: bool = answer.get("success")
        text: str = answer.get("message")
        logger.info(f"Checking license key: {text}")
        self.check_status_id: int = answer.get("data", {}).get("check_status_id", -1)
        self.status: int = answer.get("data", {}).get("status", -1)

        return success

    @logger.catch
    async def _get_license_approve(self) -> bool:
        """Returns license approved result"""

        logger.debug("Getting license approve...")
        logger.info("\n\t\tПодтвердите запрос в телеграм-боте и нажмите Enter:")
        input()
        for i in range(MAX_LICENSE_WAITING_TIME_SEC, -1, -APPROVE_REQUEST_FREQUENCY):
            logger.success(f"{i=}")
            if await self.__get_license_approve():
                logger.info("License approve: OK")
                return True
            time.sleep(APPROVE_REQUEST_FREQUENCY)
        else:
            logger.warning(f"License {self.license_key} approve: FAIL")
        return False

    @logger.catch
    def _logging_in(self) -> None:
        """Wait for user logging in"""

        self.browser.maximize_window()
        self.browser.get("https://binance.com/ru/nft")
        self._time_sleep(3)
        self._click_to_button(self.accept_cookie_button_x_path)
        self._time_sleep(1)
        log_in_button: str = '//*[@id="header_login"]'
        self._click_to_button(log_in_button)

        logger.success('\n\n\n\t\tLog in Binance account and press ENTER:\n\n')
        input()

    @logger.catch
    def _imitation_cookie(self) -> None:
        """Получение кукисов (прогрев)"""

        logger.info('Simulation of human work for Binance')
        self.browser.get(f'https://www.binance.com/en/nft/balance?tab=nft')
        self._time_sleep(5)
        self.browser.get('https://www.binance.com/en/nft/marketplace')
        self._press_accept_button()
        self._time_sleep(5)
        self._press_accept_button()
        self._time_sleep(10)
        self.browser.get(
            f'https://www.binance.com/ru/nft/goods/blindBox'
            + f'/detail?productId={self.lot_id}&isOpen=true&isProduct=1'
        )

    @logger.catch
    def _wait_for_time(self) -> None:
        """Wait for time before prepare_time to final time"""

        while self.get_current_unix_timestamp() < self.sale_time - self.prepare_time:
            logger.info(
                f'seconds left: '
                f'[{int(self.sale_time - self.get_current_unix_timestamp() - self.prepare_time)}] '
                f'seconds')
            time.sleep(1)

    @logger.catch
    def _get_headers(self) -> None:
        """Получение заголовков"""

        logger.info("Getting headers")
        self._press_pay_a_bid_button()
        self._time_sleep(3)
        for request in self.browser.requests:
            if str(request.url) == 'https://www.binance.com/bapi/nft/v1/private/nft/nft-trade/preorder-create':
                cookies = request.headers['cookie']
                csrftoken = request.headers['csrftoken']
                deviceinfo = 'eyJzY3JlZW5fcmVzb2x1dGlvbiI6IjE5MjAsMTA4MCIsImF2YWlsYWJsZV9zY3JlZW5' \
                             'fcmVzb2x1dGlvbiI6IjE4NTIsMTA1MyIsInN5c3RlbV92ZXJzaW9uIjoiTGludXggeD' \
                             'g2XzY0IiwiYnJhbmRfbW9kZWwiOiJ1bmtub3duIiwic3lzdGVtX2xhbmciOiJlbi1VU' \
                             'yIsInRpbWV6b25lIjoiR01UKzIiLCJ0aW1lem9uZU9mZnNldCI6LTEyMCwidXNlcl9h' \
                             'Z2VudCI6Ik1vemlsbGEvNS4wIChYMTE7IExpbnV4IHg4Nl82NCkgQXBwbGVXZWJLaXQ' \
                             'vNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzk2LjAuNDY2NC45MyBTY' \
                             'WZhcmkvNTM3LjM2IiwibGlzdF9wbHVnaW4iOiJQREYgVmlld2VyLENocm9tZSBQREYg' \
                             'Vmlld2VyLENocm9taXVtIFBERiBWaWV3ZXIsTWljcm9zb2Z0IEVkZ2UgUERGIFZpZXd' \
                             'lcixXZWJLaXQgYnVpbHQtaW4gUERGIiwiY2FudmFzX2NvZGUiOiIzMGYwZWY1YiIsIn' \
                             'dlYmdsX3ZlbmRvciI6Ikdvb2dsZSBJbmMuIChJbnRlbCkiLCJ3ZWJnbF9yZW5kZXJlc' \
                             'iI6IkFOR0xFIChJbnRlbCwgTWVzYSBJbnRlbChSKSBVSEQgR3JhcGhpY3MgNjIwIChL' \
                             'QkwgR1QyKSwgT3BlbkdMIDQuNiAoQ29yZSBQcm9maWxlKSBNZXNhIDIxLjIuMikiLCJ' \
                             'hdWRpbyI6IjEyNC4wNDM0NzUyNzUxNjA3NCIsInBsYXRmb3JtIjoiTGludXggeDg2XzY' \
                             '0Iiwid2ViX3RpbWV6b25lIjoiRXVyb3BlL0NoaXNpbmF1IiwiZGV2aWNlX25hbWUiOiJ' \
                             'DaHJvbWUgVjk2LjAuNDY2NC45MyAoTGludXgpIiwiZmluZ2VycHJpbnQiOiIyMTc5Y' \
                             'jEyNmM4N2Q0YzM3ODc3ZmM5NWFhMTIxNmRkOSIsImRldmljZV9pZCI6IiIsInJlbGF0' \
                             'ZWRfZGV2aWNlX2lkcyI6IjE2Mzk5MTA5Nzg2NjMySE8zeWExNUloV1p3a1M5ZWVCIn0='
                xNftCheckbotSitekey = request.headers['x-nft-checkbot-sitekey']
                xNftCheckbotToken = request.headers['x-nft-checkbot-token']
                xTraceId = request.headers['x-trace-id']
                xUiRequestTrace = request.headers['x-ui-request-trace']
                bnc_uuid = request.headers['bnc-uuid']
                fvideo_id = request.headers['fvideo-id']
                user_agent = request.headers['user-agent']

                self.headers = {
                    'Host': 'www.binance.com',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'clienttype': 'web',
                    'x-nft-checkbot-token': xNftCheckbotToken,
                    'x-nft-checkbot-sitekey': xNftCheckbotSitekey,
                    'x-trace-id': xTraceId,
                    'x-ui-request-trace': xUiRequestTrace,
                    'content-type': 'application/json',
                    'cookie': cookies,
                    'csrftoken': csrftoken,
                    'device-info': deviceinfo,
                    'bnc-uuid': bnc_uuid,
                    'fvideo-id': fvideo_id,
                    'user-agent': user_agent,
                }
        logger.debug(f"Headers: {self.headers}")

    @logger.catch
    async def _buy_products(self) -> bool:
        """Sends request for buying products"""

        logger.info("Send data for buying...")

        data: dict = {
            "headers": self.headers,
            "product_data": self.product_data,
            "requests_count": self.requests_count,
            "proxy_login": self.proxy_login,
            "proxy_password": self.proxy_password,
            "sale_time": self.sale_time,
            "currency": self.currency,
        }
        if DEBUG:
            answer: dict = await SecondaryManager(**data)._main()
        else:
            answer: dict = await self._send_request(url=WORK_URL, data=data)
        if not answer.get("success"):
            logger.error("Buying: FAIL"
                         f"\nAnswer: {answer}")
            return False
        self.request_id: str = answer.get("request_id")
        logger.debug(f"Request_id: {self.request_id}")
        return True

    def _press_accept_button(self):
        logger.debug("_press_accept_button start...")
        if self.term_accepted:
            return
        accept_rules_button: str = '//button[text()="Accept"]'
        if not self._click_to_button(accept_rules_button):
            logger.error(f"Button not found: 'Accept'")
            accept_rules_button: str = '//button[text()="Принять"]'
            if not self._click_to_button(accept_rules_button):
                logger.error(f"Button not found: 'Принять'")
                return
            logger.success("Button found: 'Принять'")
            self.term_accepted = True
            return
        logger.success("Button found: 'Accept'")
        self.term_accepted = True

    @staticmethod
    def _time_sleep(timeout: int) -> None:
        logger.debug(f"Pause {timeout} sec")
        time.sleep(timeout)

    def _click_to_button(self, x_path: str) -> bool:
        try:
            elem = self.browser.find_element(By.XPATH, x_path)
            if not elem:
                return False
            elem.click()
            logger.debug(f"Button with {x_path} clicked: OK")
            return True
        except Exception:
            logger.error(f"Button not found: [{x_path}]")

    @staticmethod
    def get_current_unix_timestamp() -> float:
        return datetime.datetime.utcnow().replace(tzinfo=None).timestamp()

    async def _get_results(self) -> list[str]:

        logger.info("Getting results...")
        sleeping_time: int = self.prepare_time + 5
        logger.success(f"Buying: WAITING {sleeping_time} seconds.")
        time.sleep(sleeping_time)
        results = []
        data: dict = {"request_id": self.request_id}
        answer: dict = await self._send_request(url=WORK_URL, data=data)
        if not answer.get("success"):
            logger.error("Buying: FAIL")
            return results
        if answer.get("status") == 204:
            logger.warning("Results not received. Sleeping 5 seconds and try again."
                           f"\nAnswer: {answer}")
            time.sleep(5)
            return await self._get_results()
        results: list[str] = answer.get("data").get("results")
        logger.success(f"Results: {len(results)}")

        return results

    @staticmethod
    @logger.catch
    def _show_results(results: list[str]) -> None:
        """Shows buying results"""

        if not results:
            logger.info("No results.")
            return
        lot_not_found = total_success = too_many_request_count = expired = paid = 0
        for result in results:
            answer_dict = {}
            if not result.startswith("<!"):
                try:
                    answer_dict: dict = json.loads(result)
                except JSONDecodeError as err:
                    logger.error(f"ErrorsSender: answer_handling: JSON ERROR: {err}")
                except Exception as err:
                    logger.error(f"Exception: {err}")
            message: str = answer_dict.get("message")
            if answer_dict.get("success"):
                total_success += 1
            elif answer_dict.get("code") == "961601015":
                lot_not_found += 1
            elif message == 'The transaction does not exist or has already expired.':
                expired += 1
            elif message == 'This order has already been paid. Kindly check again.':
                paid += 1
            elif message == "Превышен лимит запросов. Повторите попытку позже.":
                too_many_request_count += 1
            else:
                logger.error(f"Answer: {answer_dict}")

        logger.info(
            f"Всего запросов по productId: {len(results)}"
            f"\nПревышен лимит запросов: {too_many_request_count}"
            f"\nПревышен запас: {lot_not_found}"
            f"\nThe transaction does not exist or has already expired: {expired}"
            f"\nThis order has already been paid. Kindly check again.: {paid}"
            f"\nSuccess: {total_success}"
        )

    @staticmethod
    def _load_license_key() -> str:
        """Loads and returns license key from file
        Returns empty string if file not exists"""

        if not os.path.exists(LICENSE_FILE_NAME):
            logger.error(f"License file not found: {LICENSE_FILE_NAME}")
            return ''
        with open(LICENSE_FILE_NAME, 'r', encoding='utf-8') as f:
            license_key: str = f.read()
        logger.debug(f"License: [{license_key}]")
        return license_key

    @logger.catch
    async def __get_license_approve(self) -> bool:
        """Returns approving license request result"""

        data: dict = {
            "license_key": self.license_key,
            "check_status_id": self.check_status_id
        }
        result: dict = await self._send_request(url=LICENSE_APPROVE_URL, data=data)

        return result.get('success', False)

    @logger.catch
    async def _send_request(self, url: str, data: dict) -> dict:
        """Sends post request to url with data"""

        result = {}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=url, json=data) as response:
                    status: int = response.status
                    if status == 200:
                        result: dict = await response.json()
                    else:
                        logger.error(f"\n\t\tERROR:"
                                     f"\n\t\tStatus: {status}"
                        )
            except aiohttp.client_exceptions.ClientConnectorError as err:
                logger.error(
                    f"\n\tClientConnectorError:"
                    f"\n\tError text: {err}"
                )
        logger.debug(
            f"\nSending request:"
            f"\n\t\tURL: {url}"
            f"\n\t\tDATA: {data}"
            f"\n\t\tSTATUS: {status}"
            f"\n\t\tRESULT: {result}"
        )

        return result

    def _press_pay_a_bid_button(self):
        logger.info("Press 'Pay a bid' button...")
        if self._click_to_button(self.place_a_bid_button):
            logger.info("Press 'Pay a bid' button: OK")
            self._time_sleep(3)

    def _press_confirm_a_bid_button(self):
        logger.info("Press 'Pay a bid' button...")
        if self._click_to_button(self.confim_a_bid_button):
            logger.info("Press 'Pay a bid' button: OK")


@logger.catch
def get_sale_timestamp(data: dict) -> int:
    if isinstance(data, dict):
        return int(datetime.datetime(**data).replace(tzinfo=None).timestamp())
    raise TypeError("Sale time must be a dictionary.")


@logger.catch
def check_sale_timestamp(data: dict) -> int:
    timestamp = get_sale_timestamp(data)
    current_time = float(datetime.datetime.utcnow().replace(tzinfo=None).timestamp())
    time_to_sleep: float = float(timestamp - current_time)
    if time_to_sleep <= 0:
        logger.warning(f"Cannot run job in past time.")
        return 0
    return timestamp


@logger.catch
def is_data_valid(data: list[dict]) -> list[dict]:
    if isinstance(data, list):
        try:
            return json.loads(json.dumps(data))
        except Exception:
            logger.error("product_data is not valid list")
            raise
    raise TypeError("product_data must be a list")


@logger.catch
async def main(
        lot_id: int,
        requestsNumber: int,
        product_data: list[dict],
        currency: str,
        saleTime: dict,
        proxy_login: str,
        proxy_password: str
):
    # link == check your device https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html
    if not is_data_valid(product_data):
        return
    sale_timestamp: int = check_sale_timestamp(saleTime)
    if not sale_timestamp:
        return
    logging.getLogger('WDM').setLevel(logging.NOTSET)
    logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.NOTSET)

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--lang=en')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--log-level 3')
    options.add_argument('--disable-logging')
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options,
        service_log_path='/dev/null')
    # browser = webdriver.Chrome(executable_path=path, options=options)

    client = SecondaryClient(
        browser=browser, lot_id=lot_id, requests_count=requestsNumber,
        product_data=product_data, currency=currency, sale_time=sale_timestamp,
        proxy_login=proxy_login, proxy_password=proxy_password,
    )
    await client.start()

    logger.success("\n\n\t\tPress enter to exit...")
    input()
    browser.close()
