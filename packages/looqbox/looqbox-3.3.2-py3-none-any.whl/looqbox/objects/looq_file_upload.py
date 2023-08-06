from looqbox.objects.looq_object import LooqObject
from looqbox.json_encoder import JsonEncoder
import json


class ObjFileUpload(LooqObject):
    """
    Creates a view to drag and drop a file that will be read and used in other script of the response.

    Attributes:
    --------
        :param str filepath: Path where file will be upload to.
        :param str title: Title of the dropzone.
        :param str content: Content that will be send to the other script.

    Example:
    --------
    >>> upload = ObjUpload(filepath="secondScript", title="Looq File Upload")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, filepath, title=None, content=None, tab_label=None, value=None):
        """
        Creates a view to drag and drop a file that will be read and used in other script of the response.

        Parameters:
        --------
            :param str filepath: Path where file will be upload to.
            :param str title: Title of the dropzone.
            :param str content: Content that will be send to the other script.

        Example:
        --------
        >>> upload = ObjUpload(filepath="secondScript", title="Looq File Upload")
        """
        super().__init__()
        if title is None:
            title = []
        if content is None:
            content = []
        self.filepath = filepath
        self.title = title
        self.content = content
        self.tab_label = tab_label
        self.value = value

    @property
    def to_json_structure(self):
        """
        Creates the JSON structure to be read by the FES.

        :return: A JSON string.
        """
        json_content = {"objectType": "fileUpload",
                        "title": self.title,
                        "content": self.content,
                        "filepath": self.filepath,
                        'tabLabel': self.tab_label
                        }

        # Transforming in JSON
        file_upload_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return file_upload_json
