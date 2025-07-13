
from playwright.sync_api import sync_playwright
import base64

class BrowserAutomation:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = None
        self.page = None

    def launch_browser(self, headless=True):
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()
        return self.capture_screenshot()

    def navigate(self, url):
        self.page.goto(url)
        return self.capture_screenshot()

    def type_text(self, selector, text):
        self.page.fill(selector, text)
        return self.capture_screenshot()

    def click_element(self, selector):
        self.page.click(selector)
        return self.capture_screenshot()

    def capture_screenshot(self):
        screenshot_bytes = self.page.screenshot()
        return base64.b64encode(screenshot_bytes).decode("utf-8")

    def close_browser(self):
        if self.browser:
            self.browser.close()
        self.playwright.stop()


