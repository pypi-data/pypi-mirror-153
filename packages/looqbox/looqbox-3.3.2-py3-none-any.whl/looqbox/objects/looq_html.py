from looqbox.objects.looq_object import LooqObject
from looqbox.json_encoder import JsonEncoder
import json


class ObjHTML(LooqObject):
    """
    Wraps a HTML code in a Looqbox object to be used in the interface.

    Attributes:
    --------
        :param str html: Html code that will be wrapped.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> HTML = ObjHTML("<div> Hello Worlds </div>")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, html, tab_label=None, value=None):
        """
        Wraps a HTML code in a Looqbox object to be used in the interface.

        Parameters:
        --------
            :param str html: Html code that will be wrapped.
            :param str tab_label: Set the name of the tab in the frame.

        Example:
        --------
            HTML = ObjHTML("<div> Hello Worlds </div>)
        """
        super().__init__()
        self.html = html
        self.tab_label = tab_label
        self.value = value

    @property
    def to_json_structure(self):
        """
        Creates the JSON structure to be read by the FES.

        :return: A JSON string.
        """
        json_content = {"objectType": "html",
                        "html": self.html,
                        'tabLabel': self.tab_label
                        }

        # Transforming in JSON
        html_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return html_json
