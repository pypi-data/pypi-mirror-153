from looqbox.objects.looq_object import LooqObject
from looqbox.global_calling import GlobalCalling
from looqbox.json_encoder import JsonEncoder
import shutil
import json
import os


class ObjImage(LooqObject):
    """
    Creates a looqbox image object.

    Attributes:
    --------
        :param str src: Image source.
        :param int width: Image width.
        :param int height: Image height.
        :param dict style: A dict of CSS styles to change the frame.
        :param str tooltip: Text in pop-up message.
        :param str link: Add link to image.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> img = ObjImage(src="http://www.velior.ru/wp-content/uploads/2009/05/Test-Computer-Key-by-Stuart-Miles.jpg",
    ...                width=100, height=100, style={"border-radius": "8px"}, tooltip="test", link="https://www.looqbox.com/")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, src, width=None, height=None, style=None, tooltip=None, link=None, tab_label=None, value=None):
        """
        Creates a looqbox image object.

        Parameters:
        --------
            :param str src: Image source.
            :param int width: Image width.
            :param int height: Image height.
            :param dict style: A dict of CSS styles to change the frame.
            :param str tooltip: Text in pop-up message.
            :param str link: Add link to image.
            :param str tab_label: Set the name of the tab in the frame.

        Example:
        --------
        >>> img = ObjImage(src="http://www.velior.ru/wp-content/uploads/2009/05/Test-Computer-Key-by-Stuart-Miles.jpg",
        ...                width=100, height=100, style={"border-radius": "8px"}, tooltip="test", link="https://www.looqbox.com/")

        """
        super().__init__()
        if link is None:
            link = {}
        if tooltip is None:
            tooltip = {}
        if style is None:
            style = []
        self.source = src
        self.width = width
        self.height = height
        self.style = style
        self.tooltip = tooltip
        self.link = link
        self.tab_label = tab_label
        self.value = value

    @property
    def to_json_structure(self):
        """
        Creates the JSON structure to be read by the FES.

        :return: A JSON string.
        """
        source = self.source
        if 'https://' not in self.source:
            # From global variable looq
            if os.path.dirname(self.source) == GlobalCalling.looq.temp_dir:
                source = "/api/tmp/download/" + os.path.basename(self.source)
            else:
                template_file = os.path.join(GlobalCalling.looq.response_dir() + "/" + self.source)
                temporary_file = GlobalCalling.looq.temp_file(self.source)
                shutil.copy(template_file, temporary_file)
                source = "/api/tmp/download/" + os.path.basename(temporary_file)

        width_array = [str(self.width)]
        height_array = [str(self.height)]

        style_array = {
            "width": width_array,
            "height": height_array
        }

        if len(self.style) != 0:
            for key, value in self.style.items():
                self.style[key] = [str(value)]
            style_array.update(self.style)

        json_content = {"objectType": "image",
                        "src": source,
                        "style": style_array,
                        "link": self.link,
                        "tooltip": self.tooltip,
                        'tabLabel': self.tab_label
                        }

        # Transforming in JSON
        image_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return image_json
