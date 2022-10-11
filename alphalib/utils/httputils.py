import random

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
    "Mozilla/5.0 (Linux; Android 11; Lenovo YT-J706X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (X11; Linux i686; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/105.0 Mobile/15E148 Safari/605.1.15",
]


def http_headers():
    return {
        "User-Agent": random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }


def random_user_agent():
    return str(random.choice(USER_AGENTS))


def get_tag_value(soup: BeautifulSoup, selector: str, fn):
    tag: Tag | None = soup.select_one(selector)
    if tag:
        return fn(tag.text)
    return fn(None)


# Default HTTP time out in second
DEFAULT_HTTP_TIMEOUT = 10

# Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("user-agent=" + random_user_agent())
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("window-sized1200,600")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
chrome_options.add_argument("--enable-javascript")
content_setting = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", content_setting)

# Web driver
web_driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    chrome_options=chrome_options,
)
web_driver.implicitly_wait(DEFAULT_HTTP_TIMEOUT)
action = ActionChains(web_driver)
