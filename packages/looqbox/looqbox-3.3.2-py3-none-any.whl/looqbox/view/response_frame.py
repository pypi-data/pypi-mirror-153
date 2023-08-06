from looqbox.global_calling import GlobalCalling
from looqbox.objects.looq_object import LooqObject
from looqbox.json_encoder import JsonEncoder
from collections import OrderedDict
import json


class ResponseFrame(LooqObject):
    """
    Content: LooqObjects that will be inside the frame
    Class: Class of the Looqbox Frame
    Style: A list of CSS styles to change the Frame appearance (List)
    Stacked: Define if the frames will be stacked inside the board
    Title: Title of the frame (String)
    Insights: Information that goes in the top of the frame with the most important informations
        Must be in the format
        {
            'tabs':[
                {
                    'title': Title of the tab,
                    'sections': [
                        {
                            'title': Title of the section (optional)
                            'content': [
                                {
                                    'title': Title of the info
                                    'value': Value of the info
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    """

    def __init__(self, content=None, frame_class=None, style=None, stacked=True, title=None, tab_view=False,
                 insights=None):
        super().__init__()
        if frame_class is None:
            frame_class = []
        if content is None:
            content = []
        if title is None:
            title = []
        if style is None:
            style = {}
        if insights is None:
            insights = {}
        # Convert a simple string in to list
        if isinstance(title, str):
            title = [title]

        self.content = content
        self.frame_class = frame_class
        self.style = style
        self.stacked = stacked
        self.title = title
        self.tab_view = tab_view
        self.insights = insights

    @property
    def to_json_structure(self):
        # Dynamic error message to help the users to understand the error
        if type(self.content) is not list:
            raise TypeError("Content is not a list")

        objects_json_list = [json.loads(looq_object.to_json_structure) for looq_object in
                             self.content if looq_object is not None]

        json_content = OrderedDict(
            {
                'type': 'frame',
                'class': self.frame_class,
                'content': objects_json_list,
                'style': self.style,
                'stacked': self.stacked,
                'title': self.title,
                'tabView': self.tab_view,
                'insights': self.insights
            }
        )

        # Transforming in JSON
        frame_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return frame_json
