from looqbox.objects.looq_object import LooqObject
from looqbox.json_encoder import JsonEncoder
import json


class ObjMessage(LooqObject):
    """
    Creates a looqbox standard message box.

    Attributes:
    --------
        :param str text: Text to be displayed.
        :param str type: Type of the message. Types: alert-warning (yellow), alert-danger (red), alert-success (green),
            alert-default (gray), alert-info (blue).
        :param str align: Text align.
        :param dict style: A dict of CSS styles to change the frame.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> message = ObjMessage("Teste!", type='alert-warning')

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, text, type="alert-default", align="center", style=None, tab_label=None, value=None):
        """
        Creates a looqbox standard message box.

        Parameters:
        --------
            :param str text: Text to be displayed.
            :param str type: Type of the message. Types: alert-warning (yellow), alert-danger (red), alert-success (green),
                alert-default (gray), alert-info (blue).
            :param str align: Text align.
            :param dict style: A dict of CSS styles to change the frame.
            :param str tab_label: Set the name of the tab in the frame.
            :return: A looqbox ObjMessage object.

        Example:
        --------
        >>> message = ObjMessage("Teste!", type = 'alert-warning')
        """
        super().__init__()
        if style is None:
            style = {}
        self.text = text
        self.text_type = type
        self.text_align = align
        self.text_style = style
        self.tab_label = tab_label
        self.value = value

    @property
    def to_json_structure(self):
        """
        Creates the JSON structure to be read by the FES.

        :return: A JSON string.
        """
        json_content = {'objectType': 'message',
                        'text': [self.text],
                        'type': self.text_type,
                        'style': {"text-align": [self.text_align]},
                        'tabLabel': self.tab_label
                        }

        # Adding the dynamic style parameters
        for style in list(self.text_style.keys()):
            json_content['style'].setdefault(style, []).append(self.text_style[style])

        # Transforming in JSON
        message_json = json.dumps(json_content, sort_keys=True, indent=1, allow_nan=True, cls=JsonEncoder)

        return message_json
