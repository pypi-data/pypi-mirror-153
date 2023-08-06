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

import requests
from robotlibcore import keyword
from CaptchaLibrary.utils import EncDec


class ForgotCaptcha(EncDec):
    """
    """

    def __init__(self, serviceUrl=None,
                 header={'Content-Type': 'application/x-www-form-urlencoded'},
                 payloadType='base64Captcha'):
        self.payloadType = payloadType
        self.header = header
        self.serviceUrl = serviceUrl

    @keyword
    def decode_base64_captcha(self, imagepath):
        """Decodes the Base64 Captcha Image by converting the supplied \
            captcha image by sending a request to the captcha service URL.
        Example:
        | ${captcha_string} | `Decode Base64 Captcha` \
            | path/to/captcha/image |
        """
        base64_string = self.convert_captcha_image_to_base64(imagepath)
        payload = {self.payloadType: base64_string}
        decoded_string = \
            self._send_post_request_to_service_url(self.serviceUrl,
                                                   self.header, payload)
        return decoded_string.text

    def _send_post_request_to_service_url(self, serviceUrl, header, payload):
        """Send a POST Request to the Captcha Service API.
        """
        req = requests.post(serviceUrl, data=payload, headers=header)
        return req
