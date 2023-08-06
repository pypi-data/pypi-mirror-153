# Copyright (C) 2022 Joshua Kim Rivera

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import base64
import requests
import json
from robotlibcore import keyword
from CaptchaLibrary.utils import EncDec, Configuration
from robot.api import logger


class SimpleCaptcha(EncDec):
    """
    2Captcha Simple Captcha Solver

    The process of solving an normal captcha is as follows:
    we take the image of the captcha from the page of its
    placement and transfer it to the 2captcha service, where
    the employee solves it, after which the answer is returned
    to us, which must be entered in the appropriate field to
    solve the captcha

    Normal Captcha is an image that contains distored but human-readable text.
    To solve the captcha user have to type the text from the image.
    """

    def __init__(self, TC_API_KEY=None):
        self.TC_API_KEY = TC_API_KEY

    @keyword
    def tc_simplecaptcha_solve(self, imagepath, case_sensitive=0):
        """Sends a simple captcha solve request to 2Captcha Service.
        """
        logger.console(imagepath)
        b64String = self.convert_captcha_image_to_base64(imagepath)
        captcha_id = self._tc_submit_simplecaptcha_request(b64String,
                                                           case_sensitive)
        logger.console(captcha_id)
        captcha_value = self._tc_retrieve_captcha(captcha_id)
        return captcha_value

    def _tc_submit_simplecaptcha_request(self, b64String, case_sensitive):
        """
        """
        payload = {
            'key': self.TC_API_KEY,
            'method': 'base64',
            'body': b64String,
            'regsense': case_sensitive
        }
        resp = requests.post(Configuration.TC_SIMPLE_SUBMIT, data=payload)
        captchaId = resp.text.strip('OK|')
        return captchaId

    def _tc_retrieve_captcha(self, captchaId):
        """
        """
        payload = {
            'key': self.TC_API_KEY,
            'action': 'get',
            'id': int(captchaId)
        }
        resp = ''
        while('OK' not in resp):
            resp = requests.get(Configuration.TC_SIMPLE_GET, params=payload)
            resp = resp.text
        return resp.strip('OK|')
