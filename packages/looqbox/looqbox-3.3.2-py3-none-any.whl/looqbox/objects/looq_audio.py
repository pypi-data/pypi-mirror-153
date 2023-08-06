from looqbox.objects.looq_object import LooqObject
from looqbox.global_calling import GlobalCalling
from looqbox.json_encoder import JsonEncoder
import shutil
import json
import os


class ObjAudio(LooqObject):
    """
    Creates a Looqbox audio object from an audio file which is in the same directory of the script or from a https
    web link.

    Attributes:
    --------
        :param str src: Source of the audio to be displayed (filepath or https link).
        :param bool auto_play: Defines if the audio starts as soon as the board is opened.

    Example:
    --------
    >>> audio = ObjAudio("/Users/looqbox/Downloads/armstrong.mp3")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """

    def __init__(self, src, auto_play=False, tab_label=None, value=None):
        """
        Creates a Looqbox audio object from an audio file which is in the same directory of the script or from a https
        web link.

        Parameters:
        --------
            :param str src: Source of the audio to be displayed (filepath or https link).
            :param bool auto_play: Defines if the audio starts as soon as the board is opened.
            :param str tab_label: Set the name of the tab in the frame.
            :return: A Looqbox ObjAudio object.

        Example:
        --------
        >>> audio = ObjAudio("/Users/looqbox/Downloads/armstrong.mp3")
        """
        super().__init__()
        self.source = src
        self.auto_play = auto_play
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

        json_content = {
            "objectType": "audio",
            "src": source,
            "autoPlay": self.auto_play,
            'tabLabel': self.tab_label
        }

        # Transforming in JSON
        audio_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return audio_json
