from looqbox.objects.looq_object import LooqObject
from looqbox.json_encoder import JsonEncoder
import plotly.graph_objs as go
import numpy as np
import json


class ObjPlotly(LooqObject):
    """
    Creates an ObjPlotly from a plotly object.

    Attributes:
    --------
        :param dict data: Plotly general values. Can be a dict or a plotly object like Bar, Scatter and etc..
        :param plotly.graph_objs._layout.Layout layout: Layout elements of the plotly, it's a Layout object from
        plotly.graph_objs, if it's not send as a parameter, the function creates it internally.
        :param bool stacked: Define if the element should be stacked.
        :param bool display_mode_bar: Define if the mode bar in the top right of the graphic will appear or not.
        :param str tab_label: Set the name of the tab in the frame.

    Example:
    --------
    >>> trace = go.Scatter(x = list(table.data['Data']), y = list(table.data['Venda']))
    >>> layout = go.Layout(title='title', yaxis=dict(title='Vendas'))
    >>> g = lq.ObjPlotly([trace], layout=layout)

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
        """
    def __init__(self, data, layout=None, stacked=True, display_mode_bar=True, tab_label=None, value=None):
        """
        Creates an ObjPlotly from a plotly object.

        Parameters:
        --------
            :param dict data: Plotly general values. Can be a dict or a plotly object like Bar, Scatter and etc..
            :param plotly.graph_objs._layout.Layout layout: Layout elements of the plotly, it's a Layout object from
            plotly.graph_objs, if it's not send as a parameter, the function creates it internally.
            :param bool stacked: Define if the element should be stacked.
            :param bool display_mode_bar: Define if the mode bar in the top right of the graphic will appear or not.
            :param str tab_label: Set the name of the tab in the frame.

        Example:
        --------
        >>> trace = go.Scatter(x = list(table.data['Data']), y = list(table.data['Venda']))
        >>> layout = go.Layout(title='title', yaxis=dict(title='Vendas'))
        >>> g = lq.ObjPlotly([trace], layout=layout)
        """
        super().__init__()
        self.data = data
        self.layout = layout
        self.stacked = stacked
        self.display_mode_bar = display_mode_bar
        self.tab_label = tab_label
        self.value = value


    @property
    def to_json_structure(self):
        """
        Create the Plotly JSON structure to be read in the FES.
        In this case the function has some peculiarities, for example, if the plotly object has some field of special
        types like ndarray, datetime and etc.. the json's convertion will break because these types objects are not
        serializable. Because of this, before sent the ObjectPlotly to the response frame, the programmer needs to
        transform these fields into normal lists.

        Example:
        --------
        >>> nparray = nparray.tolist()

        :return: A JSON string.
        """
        if self.layout is None:
            self.layout = go.Layout()

        figure = go.Figure(data=self.data, layout=self.layout)

        figure_json = figure.to_plotly_json()

        for figure in figure_json["data"]:
            for data in figure:
                if isinstance(figure[data], dict):
                    for key in figure[data]:
                        if isinstance(figure[data][key], np.ndarray):
                            figure[data][key] = figure[data][key].tolist()
                elif isinstance(figure[data], list):
                    for sub_group in figure[data]:
                        if isinstance(sub_group, list):
                            for value in sub_group:
                                if isinstance(sub_group[value], np.ndarray):
                                    sub_group[value] = sub_group[value].tolist()
                if isinstance(figure[data], np.ndarray):
                    figure[data] = figure[data].tolist()

        json_content = {
            'objectType': 'plotly',
            'data': json.dumps(figure_json['data'], cls=JsonEncoder),
            'layout': json.dumps(figure_json['layout'], cls=JsonEncoder),
            'stacked': self.stacked,
            'displayModeBar': self.display_mode_bar,
            'tabLabel': self.tab_label
            }

        plotly_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return plotly_json
