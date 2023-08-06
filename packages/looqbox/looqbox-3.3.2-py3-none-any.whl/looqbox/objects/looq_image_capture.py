from looqbox.objects.looq_object import LooqObject
from looqbox.global_calling import GlobalCalling
from looqbox.json_encoder import JsonEncoder
import json
import shutil
import os


class ObjImageCapture(LooqObject):
    """
    Creates a looqbox image object from a webcam picture.

    Attributes:
    --------
        :param str filepath: Path for the script to which the image is returned.
        :param str title: Title of the image box.
        :param dict content: Format that the captured image data will be sent to the interface.

    Example:
    --------
    >>> image = ObjImageCapture(filepath="filePath", title="Captura de Imagem")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, filepath, title=None, content=None, value=None):
        """
        Creates a looqbox image object from a webcam picture.

        Parameters:
        --------
            :param str filepath: Path for the script to which the image is returned.
            :param str title: Title of the image box.
            :param dict content: Format that the captured image data will be sent to the interface.

        Example:
        --------
        >>> image <- ObjImageCapture(filepath="filePath", title="Captura de Imagem")
        """
        super().__init__()
        if content is None:
            content = []
        if title is None:
            title = ""
        self.filepath = filepath
        self.title = title
        self.content = content
        self.value = value

    @property
    def to_json_structure(self):
        """
        Creates the JSON structure to be read by the FES.

        :return: A JSON string.
        """
        json_content = {"objectType": "imageCapture",
                        "title": self.title,
                        "content": self.content,
                        "filepath": self.filepath
                        }

        # Transforming in JSON
        image_capture = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return image_capture
