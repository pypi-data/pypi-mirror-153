from looqbox.objects.looq_object import LooqObject
from looqbox.json_encoder import JsonEncoder
from collections import OrderedDict
import json


class ObjWebFrame(LooqObject):
    """
    Creates a looqbox web frame from a web content link.
    This functions only works with https links for web security reasons.

    Attributes:
    --------
        :param str src: HTTPS web link of the content.
        :param int width: Width of the frame to be displayed in the interface.
        :param int height: Height of the frame to be displayed in the interface.
        :param bool enable_fullscreen: Enable "fullscreen" button.
        :param bool open_fullscreen: The web frame is opened in fullscreen mode inside the interface.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> frame = ObjWebFrame("https://toggl.com/online-stopwatch/", width=500, height=480)

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, src, width=None, height=500, enable_fullscreen=False,
                 open_fullscreen=False, tab_label=None, value=None):
        """
        Creates a looqbox web frame from a web content link.
        This functions only works with https links for web security reasons.

        Parameters:
        --------
            :param str src: HTTPS web link of the content.
            :param int width: Width of the frame to be displayed in the interface.
            :param int height: Height of the frame to be displayed in the interface.
            :param bool enable_fullscreen: Enable "fullscreen" button.
            :param bool open_fullscreen: The web frame is opened in fullscreen mode inside the interface.
            :param str tab_label: Set the name of the tab in the frame.
            :return: A looqbox web frame object to be displayed inside the Looqbox's interface.

        Example:
        --------
        >>> frame = ObjWebFrame("https://toggl.com/online-stopwatch/", width=500, height=480)
        """
        super().__init__()
        self.source = src
        self.width = width
        self.height = height
        self.enable_fullscreen = enable_fullscreen
        self.open_fullscreen = open_fullscreen
        self.tab_label = tab_label
        self.value = value

    @property
    def to_json_structure(self):
        """
        Creates the JSON structure to be read by the FES.

        :return: A JSON string.
        """
        if self.width is None:
            self.width = ""
        else:
            self.width = str(self.width)

        json_content = OrderedDict(
            {
                "objectType": "webframe",
                "src": self.source,
                "style": {
                    "width": str(self.width),
                    "height": str(self.height)
                },
                "enableFullscreen": self.enable_fullscreen,
                "openFullscreen": self.open_fullscreen,
                'tabLabel': self.tab_label
            }
        )

        # Transforming in JSON
        web_frame_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return web_frame_json
