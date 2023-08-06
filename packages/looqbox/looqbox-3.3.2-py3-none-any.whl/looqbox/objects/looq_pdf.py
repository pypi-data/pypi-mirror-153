from looqbox.objects.looq_object import LooqObject
from looqbox.global_calling import GlobalCalling
from looqbox.json_encoder import JsonEncoder
import shutil
import json
import os


class ObjPDF(LooqObject):
    """
    Renders a PDF in the Looqbox's board using a PDF from the same directory of
    the response or from an external link (only works with HTTPS links).

    Attributes:
    --------
        :param str src: PDF's source.
        :param int initial_page: Page that the PDF will open.
        :param int height: Element height in the frame.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> pdf = ObjPDF(src="cartaoCNPJLooqbox.pdf")

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """
    def __init__(self, src, initial_page=1, height=None, tab_label=None, value=None):
        """
        Renders a PDF in the Looqbox's board using a PDF from the same directory of
        the response or from an external link (only works with HTTPS links).

        Parameters:
        --------
            :param str src: PDF's source.
            :param int initial_page: Page that the PDF will open.
            :param int height: Element height in the frame.
            :param str tab_label: Set the name of the tab in the frame.

        Example:
        --------
        >>> pdf = ObjPDF(src="cartaoCNPJLooqbox.pdf")
        """
        super().__init__()
        self.source = src
        self.initial_page = initial_page
        self.height = height
        self.tab_label = tab_label
        self.value = value

    @property
    def to_json_structure(self):
        """
        Creates the JSON structure to be read by the FES.

        :return: A JSON string.
        """
        if 'https://' not in self.source:
            # From global variable looq
            if os.path.dirname(self.source) == GlobalCalling.looq.temp_dir:
                self.source = "/api/tmp/download/" + os.path.basename(self.source)
            else:
                template_file = os.path.join(GlobalCalling.looq.response_dir() + "/" + self.source)
                temporary_file = GlobalCalling.looq.temp_file(self.source)
                shutil.copy(template_file, temporary_file)
                self.source = "/api/tmp/download/" + os.path.basename(temporary_file)

        height_array = [str(self.height)]

        json_content = {"objectType": "pdf",
                        "src": self.source,
                        "style": {
                            "height": height_array,
                        },
                        "initialPage": self.initial_page,
                        'tabLabel': self.tab_label
                        }

        # Transforming in JSON
        pdf_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return pdf_json
