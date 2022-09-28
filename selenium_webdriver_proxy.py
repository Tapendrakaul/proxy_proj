import os
import zipfile
import time
# import undetected_chromedriver as uc
import threading
import os
import requests
import selenium
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver


user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    
def create_chromedriver(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS, USER_AGENT):
    
    manifest_json = """
    {
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
            username: "%s",
            password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


    def get_chromedriver(use_proxy=True, user_agent=USER_AGENT):
        chrome_options = webdriver.ChromeOptions()
        if use_proxy:
            pluginfile = 'proxy_auth_plugin.zip'
            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--mute-audio")
        if user_agent:
            chrome_options.add_argument('--user-agent=%s' % USER_AGENT)
        driver =  webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
        return driver

    driver = get_chromedriver(use_proxy=True)
    # driver.get('https://www.google.com/search?q=my+ip+address')
    driver.get("https://whatismyipaddress.com/")
    time.sleep(20)
    driver.quit()
    
    

create_chromedriver('use_your_ip','use_your_port','username','password',user_agent)

