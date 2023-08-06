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

from PIL import Image
from robotlibcore import keyword


class Img():
    """
    """

    def __init__(self):
        pass

    @keyword
    def capture_element_from_screenshot(self, imagepath, location,
                                        size, outputpath):
        """Crops the specified element from a screenshot given the \
            location and size using Python's Pillow Module. Fails if \
                the supplied image PATH does not exist.

        Example:
        | `Capture Element From Screenshot` | image.png | ${coordinates} | \
            ${size} | output.jpg |

        Where:
         - `image.png`       = path to the captcha image
         - `${coordinates}`  = element location, must be a dictionary
         - `${size}`         = element size, must be a dictionary
         - `outputpath`      = cropped_image
        """
        try:
            image = Image.open(imagepath)
        except Exception as e:
            raise e
        element = image.crop((int(location['x']),
                              int(location['y']),
                              int(size['width'])+int(location['x']),
                              int(size['height'])+int(location['y'])
                              ))
        element.save(outputpath)
