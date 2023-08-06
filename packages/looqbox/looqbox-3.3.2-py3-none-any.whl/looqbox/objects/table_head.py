from looqbox.objects.table_json_generator import TableJson
from looqbox.objects.table_json_generator import RowJson
from looqbox.objects.looq_object import LooqObject
from collections import OrderedDict


def is_list(a):
    return isinstance(a, list)


def list_of_lists(list_to_eval):
    return any(isinstance(element, list) for element in list_to_eval)


def same_length(a, b):
    return len(a) == len(b)


class TableHead(LooqObject):
    # TODO add head row attributes
    def __init__(self,
                 table_content=None,
                 # Head cell attributes
                 head_link=None,
                 head_style=None,
                 head_class=None,
                 head_tooltip=None,
                 head_filter=None,
                 head_format=None,
                 # Head group cell attributes
                 head_group=None,
                 head_group_link=None,
                 head_group_style=None,
                 head_group_class=None,
                 head_group_tooltip=None,
                 head_group_format=None,
                 # Head group row attributes
                 head_group_row_link=None,
                 head_group_row_style=None,
                 head_group_row_class=None,
                 head_group_row_tooltip=None,
                 head_group_row_format=None,
                 show_head=None,
                 drill_text=None):

        super().__init__()
        self.table_content = table_content
        self.head_link = head_link
        self.head_style = head_style
        self.head_class = head_class
        self.head_tooltip = head_tooltip
        self.head_filter = head_filter
        self.head_format = head_format
        self.head_group = head_group
        self.head_group_link = head_group_link
        self.head_group_style = head_group_style
        self.head_group_class = head_group_class
        self.head_group_tooltip = head_group_tooltip
        self.head_group_format = head_group_format
        self.head_group_row_link = head_group_row_link
        self.head_group_row_style = head_group_row_style
        self.head_group_row_class = head_group_row_class
        self.head_group_row_tooltip = head_group_row_tooltip
        self.head_group_row_format = head_group_row_format
        self.show_head = show_head
        self.drill_text = drill_text

    def head_element_to_json(self, column):
        element = {"title": column,
                   "dataIndex": column
                   }

        element = self.remove_json_nones(element)
        return element

    def build_head_content_and_config(self, table_data, component):
        head_content = list()
        head_cell_config = dict()

        for column in table_data:
            element = self.head_element_to_json(column)
            head_content.append(element)

            # Head configurations
            head_cell_config = component.cell_config(head_cell_config, column)

        return head_content, head_cell_config

    @staticmethod
    def build_head_group(head_group_list, component):
        head_group_row = []
        for head_group in list(OrderedDict.fromkeys(head_group_list)):  # Get unique values from list, maintaining order
            head_group_attributes = dict()
            head_group_elements = {
                head_group: dict(value=head_group, colspan=head_group_list.count(head_group), rowspan=1)}

            head_group_attributes[head_group] = {
                "class": None,
                "style": None,
                "format": None,
                "tooltip": None,
                "drill": None
            }
            group_config = component.cell_config(head_group_attributes, head_group)
            head_group_elements[head_group]["_lq_cell_config"] = group_config.get(head_group, dict())
            head_group_elements = head_group_elements[head_group]

            head_group_row.append(head_group_elements)
        return dict(cols=head_group_row)

    @property
    def to_json_structure(self):

        table_data = self.table_content
        if table_data is None:
            return None

        if self.show_head is None:
            raise TypeError("show_head must be True or False")

        #  TODO a map with index and values would be more appropriate {0 : [values]}
        #  head_group must be a list of lists (each list represents one head group)
        if not list_of_lists(self.head_group) and same_length(self.head_group, self.table_content.columns):
            table_head_group = [self.head_group]
        else:
            table_head_group = self.head_group

        # Head components
        Head = TableJson(
            data=table_data,
            cell_style=self.head_style,
            cell_class=self.head_class,
            cell_filter=self.head_filter,
            cell_format=self.head_format,
            cell_link=self.head_link,
            cell_tooltip=self.head_tooltip,
            drill_text=self.drill_text)

        HeadGroup = TableJson(
            data=table_data,
            cell_style=self.head_group_style,
            cell_class=self.head_group_class,
            cell_format=self.head_group_format,
            cell_link=self.head_group_link,
            cell_tooltip=self.head_group_tooltip)

        HeadGroupRow = RowJson(
            data=table_data,
            value_style=self.head_group_row_style,
            value_class=self.head_group_row_class,
            value_format=self.head_group_row_format,
            value_link=self.head_group_row_link,
            value_tooltip=self.head_group_row_tooltip
        )

        # Build table head in json format
        head_content, head_cell_config = self.build_head_content_and_config(table_data, Head)

        # Build head group in json format
        head_group_row_idx = 0
        head_group_row_list = list()
        for head_group in table_head_group:

            if not is_list(head_group) or not same_length(head_group, self.table_content.columns):
                raise Exception("Table head group must be a list and have the same number of element as the table")

            else:
                head_group_row = self.build_head_group(head_group, HeadGroup)
                head_group_row["_lq_row_config"] = HeadGroupRow.row_config(head_group_row_idx, HeadGroup)
                head_group_row_list.append(head_group_row)

            head_group_row_idx += 1

        header_json = {
            "visible": self.show_head,
            "_lq_cell_config": head_cell_config,
            "content": head_content,
            "group": {
                "rows": head_group_row_list
            }
        }

        return header_json
