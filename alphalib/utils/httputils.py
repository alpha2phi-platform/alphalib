# import os
import random
import shutil

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# from pathlib import Path


USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (X11; Linux i686; rv:105.0) Gecko/20100101 Firefox/105.0",
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
DEFAULT_HTTP_TIMEOUT = 20

# HTTP retry
DEFAULT_HTTP_RETRY = 3

# Chrome options
chrome_options = webdriver.ChromeOptions()

# Use Brave browser if exist
brave_path = shutil.which("which brave")
if brave_path:
    chrome_options.binary_location = brave_path

chrome_options.headless = False
chrome_options.binary_location = "/usr/bin/brave"  # Use brave
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("user-agent=" + random_user_agent())
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("window-sized1200,600")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
chrome_options.add_argument("--enable-javascript")
content_setting = {
    "profile.managed_default_content_settings.images": 2,
    "profile.default_content_setting_values.cookies": 1,
    "profile.cookie_controls_mode": 0,
}
chrome_options.add_experimental_option("prefs", content_setting)

# user_data = os.path.join(Path.home(), ".config", "google-chrome")
# profile_dir = "Default"
# chrome_options.add_argument(f"--user-data-dir={user_data}")
# chrome_options.add_argument(f"--profile-directory={profile_dir}")


# Web driver - default Chrome
web_driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    chrome_options=chrome_options,
)
web_driver.implicitly_wait(DEFAULT_HTTP_TIMEOUT)
action = ActionChains(web_driver)
