from looqbox.objects.looq_object import LooqObject


class TableCell(LooqObject):

    def __init__(self, cell_value=None, cell_format=None, cell_class=None, cell_style=None,
                 cell_tooltip=None, cell_link=None, cell_droplist=None):
        self.cell_value = cell_value
        self.cell_format = cell_format
        self.cell_class = cell_class
        self.cell_style = cell_style
        self.cell_tooltip = cell_tooltip
        self.cell_link = cell_link
        self.cell_droplist = cell_droplist

    @property
    def to_json_structure(self):
        """
        Generate the json that will be add in the ObjectTable body part.

        :return: body_json: Dictionary that will be converted to a JSON inside the looq_table function.

        """
        # Initializing a dict with keys: None
        cell_json = {'value': self.cell_value, 'style': self.cell_style, 'link': self.cell_link,
                     'tooltip': self.cell_tooltip, 'format': self.cell_format, 'class': self.cell_class}

        if self.cell_droplist is not None:
            del cell_json['link']
            cell_json['droplist'] = self.cell_droplist

        cell_json = self.remove_json_nones(cell_json)

        return cell_json

