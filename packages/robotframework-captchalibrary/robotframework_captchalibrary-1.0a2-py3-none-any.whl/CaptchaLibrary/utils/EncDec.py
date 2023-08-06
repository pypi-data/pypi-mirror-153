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
import pyqrcode
from robotlibcore import keyword


class EncDec():
    """
    Encode Decode Class
    """

    def __init__(self):
        pass

    @keyword
    def convert_captcha_image_to_base64(self, imagepath):
        """Converts the supplied Captcha image to a Base64 String.
        Fails if the image does not exist
        Example:
        | `Convert Captcha Image To Base64` | captcha.png |

        Where:
         - `captcha.png` = the captcha image to be converted to \
             Base64 String.
        """
        try:
            with open(imagepath, "rb") as img_file:
                decoded_string = base64.b64encode(img_file.read())
                decoded_string = decoded_string.decode("utf-8")
                return decoded_string
        except Exception as e:
            raise e

    @keyword
    def create_qr_image(self, content, outputPath, scale=6, **kwargs):
        """Creates a QR Image given parameters.
        """
        qr = pyqrcode.create(content)
        qr.png(outputPath, scale=scale, **kwargs)

    @keyword
    def decode_qr_image(self, imagepath):
        """Decodes the given QR Image. Returns an object type variable.
        """
        return self._process_qr_image(imagepath)

    def _process_qr_image(self, imagepath):
        try:
            decoded_qr = decode(Image.open(imagepath))[0]
            return decoded_qr
        except Exception as err:
            raise err
