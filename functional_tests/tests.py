# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from datetime import datetime

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Create your tests here.

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)

class HomeTest(StaticLiveServerTestCase):

    def setUp(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(chrome_options=self.options)

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            for ix, handle in enumerate(self.browser.window_handles):
                self._windowid = ix
                self.browser.switch_to_window(handle)
                self.take_screenshot()
        self.browser.quit()
        super(StaticLiveServerTestCase, self).tearDown()

    def _test_has_failed(self):
        # slightly obscure but couldn't find a better way!
        return any(error for (method, error) in self._resultForDoCleanups.failures)

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print 'screenshotting to' + filename
        self.browser.get_screenshot_as_file(filename)

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )

    def test_can_reach_home(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Welcome to Django', self.browser.title)

    def test_fake_fail(self):
        self.browser.get(self.live_server_url)
        self.fail('Failed.')
