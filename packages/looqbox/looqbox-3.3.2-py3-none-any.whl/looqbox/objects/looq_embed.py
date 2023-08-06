from looqbox.objects.looq_object import LooqObject
from looqbox.json_encoder import JsonEncoder
import json


class ObjEmbed(LooqObject):
    """
    Creates a frame inside the Looqbox interface using an iframe HTML tag as source.

    Attributes:
    --------
        :param str iframe: Embedded element dimensions and source in HTML format.

    Example:
    --------
    >>> webframe0 = ObjEmbed("<iframe frameborder=\"0\" width=\"560\" height=\"315\"
    ...                      src=\"https://app.biteable.com/watch/embed/looqbox-presentation-1114895\">
    ...                      </iframe>")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, iframe, tab_label=None, value=None):
        """
        Creates a frame inside the Looqbox interface using an iframe HTML tag as source.

        Parameters:
        --------
            :param str iframe: Embedded element dimensions and source in HTML format.
            :return: A Looqbox ObjEmbed object.

        Example:
        --------
        >>> webframe0 = ObjEmbed("<iframe frameborder=\"0\" width=\"560\" height=\"315\"
        ...                      src=\"https://app.biteable.com/watch/embed/looqbox-presentation-1114895\">
        ...                      </iframe>")
        """
        super().__init__()
        self.iframe = iframe
        self.tab_label = tab_label
        self.value = value

    @property
    def to_json_structure(self):
        """
        Creates the JSON structure to be read by the FES.

        :return: A JSON string.
        """
        json_content = {"objectType": "embed",
                        "iframe": self.iframe,
                        'tabLabel': self.tab_label
                        }

        # Transforming in JSON
        embed = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return embed
