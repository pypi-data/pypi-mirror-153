from looqbox.objects.table_footer import TableFooter
from looqbox.objects.looq_object import LooqObject
from looqbox.objects.table_head import TableHead
from looqbox.objects.table_body import TableBody
from looqbox.json_encoder import JsonEncoder
import pandas as pd
import warnings
import json


# TODO implement dataclasses to reduce code and improve readability
class ObjTable(LooqObject):
    """
    Creates a looqbox standard table.

    Attributes:
    --------
        :param pandas.DataFrame data: Table data content.
        :param str name: Table name, used as sheet name when an excel is generated from the table.
        :param str title: Table title.
        :param list head_group: Group the table headers.
        :param dict head_group_tooltip: Add a tooltip to a group of header.
        :param dict head_style: Add style to a table head.
        :param dict head_tooltip: Add a tooltip to a table head.
        :param dict cell_format: Formats table data using the column as reference.
            Formats allowed: number:0, 1, 2..., percent:0, 1, 2, ..., date, dateTime.
        :param dict cell_style: Table style (color, font, and other HTML's attributes) using the column as reference.
        :param dict cell_tooltip: Add a tooltip with the information of the cell using the column as reference.
        :param dict cell_link: Add link to table cell using the column as reference.
        :param list col_range: Limit the columns that the attributes will be displayed.
        :param dict drill_configuration: Use to set drilldown feature using generic mask rather string combination.
            Obs: These feature is recommended for larger tables with multiples drillown options.
        :param dict drill_text: Alias that will be inserted in drill_mask. In case the user wihses to use a name
            belonging in the table, this parameter must be leaved empty.
        :param bool collapsible: Enable collapsed table.
        :param list row_hierarchy: Lists hierarchy level for each row
        :param dict row_style: Table style (color, font, and other HTML's attributes) using the row as reference.
            Obs: If the rowValueStyle has some element that is equal to the valueStyle,
            the function will prioritize the valueStyle element.
        :param dict row_format: Formats table data using the row as reference.
            Formats allowed: number:0, 1, 2..., percent:0, 1, 2, ..., date, dateTime.
        :param dict row_link: Add link to table cell using the row as reference.
        :param dict row_tooltip: Add a tooltip with the information of the cell using the row as reference
        :param list row_range: Limit the rows that the attributes will be displayed.
        :param dict or list total: Add a "total" as last row of the table.
        :param dict total_link: Add link to "total" row cell.
        :param dict total_style: Add style (color, font, and other HTML's attributes) to "total" row cell.
        :param dict total_tooltip: Add tooltip to "total" row cell.
        :param bool show_highlight: Enables or disables highlight on the table.
        :param int pagination_size: Number of rows per page on the table.
        :param bool hide_on_single_page: Hide pagination bar options if table has no data to fulfill one page.
        :param bool searchable: Enables or disables a search box in the top left corner of the table.
        :param str search_string: Initial value inside the search box.
        :param bool show_border: Enables or disables table borders.
        :param bool show_head: Enables or disables table headers.
        :param bool show_option_bar: Enables or disables "chart and excel" option bar.
        :param bool sortable: Enables or disables a search box in the top left corner of the table.
        :param bool striped: Enables or disables colored stripes in rows.
        :param bool framed: Defines if the table will be framed.
        :param str framed_title: Add a title in the top of the table frame.
        :param bool stacked: Defines if the table will be stacked with other elements of the frame.
        :param str tab_label: Set the name of the tab in the frame.
        :param list table_class: Table's class.

    Example:
    --------
        >>> table = ObjTable()
        #
        # Data
        >>> table.data = pandas.DataFrame({"Col1": range(1, 30), "Col2": range(1, 30)})
        #
        # Title
        >>> table.title = "test" # Or
        >>> table.title = ["test", "table"]
        #
        # Value Format
        ## "ColName" = "Format"
        >>> table.cell_format = {"Col1": "number:2", "Col2": "percent:1"} # Or
        >>> table.cell_format['Col1'] = "number:2"
        #
        # Row Format
        ## "RowNumber" = "Format"
        >>> table.total_row_format = {"1": "number:0"} # Or
        >>> table.total_row_format["2"] = "number:1"
        #
        # Value Link
        ## "ColName" = "NextResponseQuestion"
        >>> table.cell_link = {"Col1": "test",
        ...                     "Col2": table.create_droplist({"text": "Head", "link": "Test of value {}"},
        ...                                                   [table.data["Col1"]])}
        # Column Value Link
        >>> table.col_link = {"Col1": "test",
        ...                     "Col2": table.create_droplist({"text": "Head", "link": "Test of value {}"},
        ...                                                   [table.data["Col1"]])}
        #
        # Row Link
        ## "RowNumber" = paste(NextResponseQuestion)
        >>> table.cell_link = {"1": "test", "2": "test2"}
        #
        # Drill_configuration
        >>> table.drill_configuration = {"footer": {
        ...                                          "Name0": [
        ...                                                    {
        ...                                                      "text": "listar lojas",
        ...                                                      "link": "listar lojas"
        ...                                                    }
        ...                                                   ]
        ...                                        },
        ...                              "column": {
        ...                                        "Name0": [
        ...                                                  {
        ...                                                    "text": "ficha loja",
        ...                                                    "link": "ficha loja [{c1}|{c0}]"
        ...                                                  }
        ...                                                 ],
        ...                                        "Number1":[
        ...                                                   {
        ...                                                     "text": "venda da loja",
        ...                                                     "link": "venda da loja [{c1}|{c0}]"
        ...                                                   }
        ...                                                  ]
        ...                                      }
        ...                              }
        #
        #drill_text
        >>> table.drill_text = {
        ...                      "header": {"Name0": "H0", "Number1": "H1"},
        ...                      "footer": {"Name0": "Total", "Number1": "Valor"},
        ...                      "column": {"Name1": list(table.data.iloc[:, 2])}
        ...                    }
        #
        # Value Style
        ## "ColName" = style
        >>> table.cell_style = {"Col1": {"color": "blue", "background": "white"}}
        #
        # Row Style
        ## "RowNumber" = style
        >>> table.cell_style = {"1": {"color": "blue", "background": "white"}}
        #
        # Value Tooltip
        >>> table.cell_format = {"Col1": "tooltip", "Col2": "tooltip"}
        #
        # Row Tooltip
        >>> table.cell_format = {"1": "tooltip", "2": "tooltip"}
        #
        # Total
        >>> table.total = [sum(table.data['Col1']), sum(table.data['Col2'])] # Or
        >>> table.total = {"Col1": sum(table.data['Col1']), "Col2": sum(table.data['Col2'])}
        #
        # Total Link
        >>> table.total_link = {"Col1": table.create_droplist({"text": "Head",
        ...                                                   "link": "Test of value " + str(table.total['Col1'])}),
        ...                     "Col2": "test2"}
        #
        # Total Style
        >>> table.total_style = {"Col1": {"color": "blue", "background": "white"},
        ...                      "Col2": {"color": "blue", "background": "white"}}
        #
        # Total Tooltip
        >>> table.total_style = {"Col1": "tooltip", "Col2": "tooltip"}
        #
        # Head Group
        >>> table.head_group = ["G1", "G1"]
        #
        # Head Group Tooltip
        >>> table.head_group_tooltip = {"G1": "This is the head of group G1"}
        #
        # Head Style
        >>> table.head_style = {"G1": {"color": "blue", "background": "white"}}
        #
        # Head Tooltip
        >>> table.cell_tooltip = {"G1": "tooltip"}
        #
        # Logicals
        >>> table.stacked = True
        >>> table.show_head = False
        >>> table.show_border = True
        >>> table.show_option_bar = False
        >>> table.show_highlight = True
        >>> table.striped = False
        >>> table.sortable = True
        >>> table.searchable = False
        #
        # Search String
        >>> table.search_string = "search this"
        #
        # Atribute Column Range
        >>> table.col_range = [1, 5]
        >>> table.col_range = {"style": [0, 1], "format": [1, 2], "tooltip": [0, 2]}
        #
        # Pagination Size
        >>> table.pagination_size = 15
        >>> table.hide_on_single_page = True
        #
        # collapsible
        >>> table.collapsible = True
        >>> table.row_hierarchy = [1, 1, 1, 2, 3, 4, 2, 2, 1, 1]
        #
        # Tab Label
        >>> table.tab_label = "nome"

    Methods:
    --------
        create_droplist(text, link_values)
            :return: A list of the dicts mapped with the columns

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """

    def __init__(self,
                 data=None,
                 name="objTable",
                 title=None,
                 # Head component attributes
                 head_link=None,
                 head_style=None,
                 head_class=None,
                 head_tooltip=None,
                 head_filter=None,
                 head_format=None,
                 head_group=None,
                 head_group_link=None,
                 head_group_style=None,
                 head_group_class=None,
                 head_group_tooltip=None,
                 head_group_format=None,
                 head_group_row_link=None,
                 head_group_row_style=None,
                 head_group_row_class=None,
                 head_group_row_tooltip=None,
                 head_group_row_format=None,
                 show_head=True,
                 # Body component attributes
                 cell_link=None,
                 cell_style=None,
                 cell_class=None,
                 cell_tooltip=None,
                 cell_format=None,
                 row_link=None,
                 row_style=None,
                 row_class=None,
                 row_tooltip=None,
                 row_format=None,
                 row_range=None,
                 col_link=None,
                 col_style=None,
                 col_class=None,
                 col_tooltip=None,
                 col_format=None,
                 col_range=None,
                 drill_configuration=None,
                 drill_text=None,
                 # Collapse attributes
                 collapseable=False,
                 collapsible=False,
                 row_hierarchy=None,
                 # Total component attributes
                 total=None,
                 total_link=None,
                 total_style=None,
                 total_class=None,
                 total_tooltip=None,
                 total_format=None,
                 total_row_link=None,
                 total_row_style=None,
                 total_row_class=None,
                 total_row_tooltip=None,
                 total_row_format=None,
                 # Subtotal component attributes
                 subtotal=None,
                 subtotal_link=None,
                 subtotal_style=None,
                 subtotal_class=None,
                 subtotal_tooltip=None,
                 subtotal_format=None,
                 subtotal_row_link=None,
                 subtotal_row_style=None,
                 subtotal_row_class=None,
                 subtotal_row_tooltip=None,
                 subtotal_row_format=None,
                 # Table options
                 show_highlight=True,
                 pagination_size=0,
                 hide_on_single_page=True,
                 searchable=False,
                 search_string="",
                 show_border=True,
                 show_option_bar=True,
                 sortable=True,
                 striped=True,
                 framed=False,
                 framed_title=None,
                 stacked=True,
                 vertical_scrollbar=False,
                 horizontal_scrollbar=False,
                 freeze_header=False,
                 freeze_footer=False,
                 freeze_columns=None,
                 max_width=None,
                 max_height=None,
                 scrollable_area_width=None,
                 table_class=None,
                 null_as=None,
                 tab_label=None,
                 value=None,
                 # Depreciated attributes
                 value_link=None,
                 value_style=None,
                 value_class=None,
                 value_tooltip=None,
                 value_format=None):

        super().__init__()

        head_link = head_link or dict()
        head_style = head_style or dict()
        head_class = head_class or dict()
        head_tooltip = head_tooltip or dict()
        head_filter = head_filter or dict()
        head_format = head_format or dict()
        head_group = head_group or list()
        head_group_link = head_group_link or dict()
        head_group_style = head_group_style or dict()
        head_group_class = head_group_class or dict()
        head_group_tooltip = head_group_tooltip or dict()
        head_group_format = head_group_format or dict()
        head_group_row_link = head_group_row_link or dict()
        head_group_row_style = head_group_row_style or dict()
        head_group_row_class = head_group_row_class or dict()
        head_group_row_tooltip = head_group_row_tooltip or dict()
        head_group_row_format = head_group_row_format or dict()

        drill_configuration = drill_configuration or dict()
        drill_text = drill_text or dict()
        cell_link = cell_link or dict()
        cell_style = cell_style or dict()
        cell_class = cell_class or dict()
        cell_tooltip = cell_tooltip or dict()
        cell_format = cell_format or dict()
        row_link = row_link or dict()
        row_style = row_style or dict()
        row_class = row_class or dict()
        row_tooltip = row_tooltip or dict()
        row_format = row_format or dict()
        col_link = col_link or dict()
        col_style = col_style or dict()
        col_class = col_class or dict()
        col_tooltip = col_tooltip or dict()
        col_format = col_format or dict()

        row_hierarchy = row_hierarchy or list()

        total_link = total_link or dict()
        total_style = total_style or dict()
        total_class = total_class or dict()
        total_tooltip = total_tooltip or dict()
        total_format = total_format or dict()
        total_row_link = total_row_link or dict()
        total_row_style = total_row_style or dict()
        total_row_class = total_row_class or dict()
        total_row_tooltip = total_row_tooltip or dict()
        total_row_format = total_row_format or dict()

        subtotal = subtotal or list()
        subtotal_link = subtotal_link or dict()
        subtotal_style = subtotal_style or dict()
        subtotal_class = subtotal_class or dict()
        subtotal_tooltip = subtotal_tooltip or dict()
        subtotal_format = subtotal_format or dict()
        subtotal_row_link = subtotal_row_link or dict()
        subtotal_row_style = subtotal_row_style or dict()
        subtotal_row_class = subtotal_row_class or dict()
        subtotal_row_tooltip = subtotal_row_tooltip or dict()
        subtotal_row_format = subtotal_row_format or dict()

        max_width = max_width or dict()
        max_height = max_height or dict()
        scrollable_area_width = scrollable_area_width or 3000
        null_as = null_as or "-"

        value_link = value_link or dict()
        value_style = value_style or dict()
        value_class = value_class or dict()
        value_tooltip = value_tooltip or dict()
        value_format = value_format or dict()

        framed_title = framed_title or dict()
        table_class = table_class or list()
        # title = title or dict()

        self.data = data
        self.name = name
        self.title = title

        self.head_link = head_link  # dict {column: {text:text, link:link}}
        self.head_style = head_style  # dict {column: {attribute:value}}
        self.head_class = head_class  # dict {column: [class]}
        self.head_tooltip = head_tooltip  # dict {column: {active:boolean, value:text}}
        self.head_filter = head_filter  # dict {column: {text:text, value:value}}
        self.head_format = head_format  # dict {column: {active:boolean, value:text}}
        self.head_group = head_group  # list [head1, head1, head2, head2]
        self.head_group_link = head_group_link  # dict {head_group: {text:text, link:link}}
        self.head_group_style = head_group_style  # dict {head_group: {attribute:value}}
        self.head_group_class = head_group_class  # dict {head_group: {attribute:value}}
        self.head_group_tooltip = head_group_tooltip  # dict {head_group: {active:boolean, value:text}}
        self.head_group_format = head_group_format  # dict {head_group: {active:boolean, value:text}}
        self.head_group_row_link = head_group_row_link  # dict {idx: {text:text, link:link}}
        self.head_group_row_style = head_group_row_style  # dict {idx: {attribute:value}}
        self.head_group_row_class = head_group_row_class  # dict {idx: {attribute:value}}
        self.head_group_row_tooltip = head_group_row_tooltip  # dict {idx: {active:boolean, value:text}}
        self.head_group_row_format = head_group_row_format  # dict {idx: {active:boolean, value:text}}
        self.show_head = show_head  # boolean

        self.cell_link = cell_link  # dict {column: {text:text, link:link}}
        self.cell_style = cell_style  # dict {column: {attribute:value}}
        self.cell_class = cell_class  # dict {column: [class]}
        self.cell_tooltip = cell_tooltip  # dict {column: {active:boolean, value:text}}
        self.cell_format = cell_format  # dict {column: {active:boolean, value:text}}
        self.row_link = row_link  # dict {idx: {text:text, link:link}}
        self.row_style = row_style  # dict {idx: {attribute:value}}
        self.row_class = row_class  # dict {idx: [class]}
        self.row_tooltip = row_tooltip  # dict {idx: {active:boolean, value:text}}
        self.row_format = row_format  # dict {idx: {active:boolean, value:text}}
        self.row_range = row_range  # ?
        self.col_link = col_link  # dict {column: {text:text, link:link}}
        self.col_style = col_style  # dict {column: {attribute:value}}
        self.col_class = col_class  # dict {column: [class]}
        self.col_tooltip = col_tooltip  # dict {column: {active:boolean, value:text}}
        self.col_format = col_format  # dict {column: {active:boolean, value:text}}
        self.col_range = col_range  # ?
        self.drill_configuration = drill_configuration  # dict {"cell":{}, "footer":{"column":{"text":, "link":}}}
        self.drill_text = drill_text

        self.collapseable = collapseable  ## Call or not the collpse format
        self.collapsible = collapsible  # Call or not the collpse format
        self.row_hierarchy = row_hierarchy  # list [row1_level, row2_level, ...]

        self.total = total  # list [total1, total2]
        self.total_link = total_link  # dict {column: {text:text, link:link}}
        self.total_style = total_style  # dict {column: {attribute:value}}
        self.total_class = total_class  # dict {column: [class]}
        self.total_tooltip = total_tooltip  # dict {column: {active:boolean, value:text}}
        self.total_format = total_format  # dict {column: {active:boolean, value:text}}
        self.total_row_link = total_row_link  # dict {text:text, link:link}
        self.total_row_style = total_row_style  # dict {attribute:value}
        self.total_row_class = total_row_class  # list [class]
        self.total_row_tooltip = total_row_tooltip  # dict {active:boolean, value:text}
        self.total_row_format = total_row_format  # str number:0

        self.subtotal = subtotal  # list [[subtotal1, subtotal2]]
        self.subtotal_link = subtotal_link  # dict {column: {text:text, link:link}}
        self.subtotal_style = subtotal_style  # dict {column: {attribute:value}}
        self.subtotal_class = subtotal_class  # dict {column: [class]}
        self.subtotal_tooltip = subtotal_tooltip  # dict {column: {active:boolean, value:text}}
        self.subtotal_format = subtotal_format  # dict {column: {active:boolean, value:text}}
        self.subtotal_row_link = subtotal_row_link  # dict {idx: {text:text, link:link}}
        self.subtotal_row_style = subtotal_row_style  # dict {idx: {attribute:value}}
        self.subtotal_row_class = subtotal_row_class  # dict {idx: [class]}
        self.subtotal_row_tooltip = subtotal_row_tooltip  # dict {idx: {active:boolean, value:text}}
        self.subtotal_row_format = subtotal_row_format  # dict {idx: {active:boolean, value:text}}

        self.stacked = stacked
        self.show_border = show_border
        self.show_head = show_head
        self.show_highlight = show_highlight
        self.show_option_bar = show_option_bar
        self.search_string = search_string
        self.searchable = searchable
        self.pagination_size = pagination_size
        self.hide_on_single_page = hide_on_single_page
        self.sortable = sortable
        self.striped = striped
        self.framed = framed
        self.framed_title = framed_title
        self.vertical_scrollbar = vertical_scrollbar
        self.horizontal_scrollbar = horizontal_scrollbar
        self.freeze_header = freeze_header
        self.freeze_footer = freeze_footer
        self.freeze_columns = freeze_columns
        self.max_width = max_width
        self.max_height = max_height
        self.scrollable_area_width = scrollable_area_width
        self.null_as = null_as
        self.table_class = table_class
        self.tab_label = tab_label
        self.value = value

        self.value_link = value_link
        self.value_style = value_style
        self.value_class = value_class
        self.value_tooltip = value_tooltip
        self.value_format = value_format

    def apply_body_format_to_footer(self):
        if not bool(self.total_format) and bool(self.col_format):
            self.total_format = self.col_format
        elif not bool(self.total_format) and bool(self.cell_format):
            self.total_format = self.cell_format

    def convert_depreciated_attributes(self):  # TODO use DeprecationWarning
        if self.value_link:
            self.cell_link = self.value_link
            warnings.warn("value_link is depreciated, use cell_link instead")

        if self.value_style:
            self.cell_style = self.value_style
            warnings.warn("value_style is depreciated, use cell_style instead")

        if self.value_class:
            self.cell_class = self.value_class
            warnings.warn("value_class is depreciated, use cell_class instead")

        if self.value_tooltip:
            self.cell_tooltip = self.value_tooltip
            warnings.warn("value_tooltip is depreciated, use cell_tooltip instead")

        if self.value_format:
            self.cell_format = self.value_format
            warnings.warn("value_format is depreciated, use cell_format instead")

        if self.collapseable:
            self.collapsible = self.collapseable
            warnings.warn("collapseable is depreciated, use collapsible instead")

    def _set_drill_down(self) -> dict:

        # TODO add two model (raw, just repass and create parameter for cell footer column and pivot)
        drill = {
                 "cell": self.drill_configuration.get("cell", []),
                 "footer": self.drill_configuration.get("footer", []),
                 "column": self.drill_configuration.get("column", []),
                 "pivot": self.drill_configuration.get("pivot", [])
                 }
        return drill

    @staticmethod
    def create_droplist(text, link_values=None):
        # TODO droplist format is not optimized to build table json after 3.x
        """
        Create a droplist from a list of values and a base text.

        The function map all the values of the columns with a format in the text using {} as base.

        Example:
        --------
            x = create_droplist({"text": Header, "link": "Link text {} and text2 {}"}, [df[col1], df[col2]])

            The first {} will use the value from df[col1] and the second {} will use the value from df[col2]

            If the user wants more than one droplist it pass a list of this function
            x = [
                create_droplist({"text": Header, "link": "Link text {} and text2 {}"}, [df[col1], df[col2]])
                create_droplist({"text": Header2, "link": "Link text {} and text2 {}"}, [df[col1], df[col2]])
            ]

        :param text: Is the base text of the droplist, use the default dict {"text": Header, "link": "Link text"}
        Example: {"text": Header, "link": "Link text {} and text2 {}"}

        :param link_values: A list with the columns to map the values in the text

        :return: A list of the dicts mapped with the columns
        """
        link_list = []
        format_values = []
        lists_length = 0

        if link_values is None:
            return text

        if not isinstance(link_values, list):
            link_values = [link_values]

        for i in range(len(link_values)):
            # Transforming all pandas Series types in a common list
            if isinstance(link_values[i], pd.Series):
                link_values[i] = list(link_values[i])
            # If is only a value transform to list
            elif not isinstance(link_values[i], list):
                link_values[i] = [link_values[i]]

            # Get lists length
            if lists_length == 0:
                lists_length = len(link_values[i])
            elif len(link_values[i]) != lists_length:
                raise Exception("List " + str(i) + " in droplist values has different length from others")

        for value_i in range(lists_length):
            for list_i in range(len(link_values)):
                format_values.append(link_values[list_i][value_i])
            text_base = text.copy()
            if pd.isnull(format_values[0]):
                text_base["link"] = None
            else:
                text_base["link"] = text_base["link"].format(*format_values)
            link_list.append(text_base)
            format_values = []

        return link_list

    @staticmethod
    def build_scroll_area(attribute):
        if isinstance(attribute, dict):
            scroll_dict = attribute
        elif isinstance(attribute, int):
            scroll_dict = {"desktop": attribute, "mobile": attribute}
        else:
            try:
                scroll_dict = {"desktop": int(attribute), "mobile": int(attribute)}
            except TypeError:
                scroll_dict = {"desktop": None, "mobile": None}

        return scroll_dict

    @property
    def to_json_structure(self):
        """
        Creates the JSON structure to be read by the FES.

        :return: A JSON string.
        """

        self.convert_depreciated_attributes()
        self.apply_body_format_to_footer()

        # TODO refactor on table objects inheritance would be a better approach
        table_head = TableHead(table_content=self.data,
                               head_link=self.head_link,
                               head_style=self.head_style,
                               head_class=self.head_class,
                               head_tooltip=self.head_tooltip,
                               head_filter=self.head_filter,
                               head_format=self.head_format,
                               head_group=self.head_group,
                               head_group_link=self.head_group_link,
                               head_group_style=self.head_group_style,
                               head_group_class=self.head_group_class,
                               head_group_tooltip=self.head_group_tooltip,
                               head_group_format=self.head_group_format,
                               head_group_row_link=self.head_group_row_link,
                               head_group_row_style=self.head_group_row_style,
                               head_group_row_class=self.head_group_row_class,
                               head_group_row_tooltip=self.head_group_row_tooltip,
                               head_group_row_format=self.head_group_row_format,
                               show_head=self.show_head,
                               drill_text=self.drill_text.get("header"))

        table_body = TableBody(table_content=self.data,
                               value_link=self.cell_link,
                               value_style=self.cell_style,
                               value_class=self.cell_class,
                               value_tooltip=self.cell_tooltip,
                               value_format=self.cell_format,
                               row_link=self.row_link,
                               row_style=self.row_style,
                               row_class=self.row_class,
                               row_tooltip=self.row_tooltip,
                               row_format=self.row_format,
                               row_range=self.row_range,
                               col_link=self.col_link,
                               col_style=self.col_style,
                               col_class=self.col_class,
                               col_tooltip=self.col_tooltip,
                               col_format=self.col_format,
                               col_range=self.col_range,
                               null_as=self.null_as,
                               collapsible=self.collapsible,
                               row_hierarchy=self.row_hierarchy,
                               drill_text=self.drill_text.get("column"))

        table_footer = TableFooter(table_content=self.data,
                                   value_format=self.cell_format,
                                   total=self.total,
                                   total_link=self.total_link,
                                   total_style=self.total_style,
                                   total_tooltip=self.total_tooltip,
                                   total_class=self.total_class,
                                   total_format=self.total_format,
                                   total_row_class=self.total_row_class,
                                   total_row_style=self.total_row_style,
                                   total_row_format=self.total_row_format,
                                   total_row_link=self.total_row_link,
                                   total_row_tooltip=self.total_row_tooltip,
                                   subtotal=self.subtotal,
                                   subtotal_format=self.subtotal_format,
                                   subtotal_style=self.subtotal_style,
                                   subtotal_link=self.subtotal_link,
                                   subtotal_tooltip=self.subtotal_tooltip,
                                   subtotal_class=self.subtotal_class,
                                   subtotal_row_format=self.subtotal_row_format,
                                   subtotal_row_style=self.subtotal_row_style,
                                   subtotal_row_link=self.subtotal_row_link,
                                   subtotal_row_tooltip=self.subtotal_row_tooltip,
                                   subtotal_row_class=self.subtotal_row_class,
                                   null_as=self.null_as,
                                   drill_text=self.drill_text.get("footer"))

        # Convert all table components to json structure
        head_json = table_head.to_json_structure
        footer_json = table_footer.to_json_structure
        body_json = table_body.to_json_structure

        # Title must be a list
        if not isinstance(self.title, list):
            self.title = [self.title]

        # Set max width

        max_width = self.build_scroll_area(self.max_width)
        max_height = self.build_scroll_area(self.max_height)
        scrollable_area_width = self.build_scroll_area(self.scrollable_area_width)

        scroll = {
            "mobile": {
                "horizontal": {
                    "active": self.horizontal_scrollbar,
                    "width": max_width.get("mobile"),
                    "scrollableAreaWidth": scrollable_area_width.get("mobile"),
                    "freezeColumns": self.freeze_columns
                },
                "vertical": {
                    "active": self.vertical_scrollbar,
                    "height": max_height.get("mobile"),
                    "fixedFooter": self.freeze_footer,
                    "fixedHeader": self.freeze_header
                }
            },
            "desktop": {
                "horizontal": {
                    "active": self.horizontal_scrollbar,
                    "width": max_width.get("desktop"),
                    "scrollableAreaWidth": scrollable_area_width.get("desktop"),
                    "freezeColumns": self.freeze_columns
                },
                "vertical": {
                    "active": self.vertical_scrollbar,
                    "height": max_height.get("desktop"),
                    "fixedFooter": self.freeze_footer,
                    "fixedHeader": self.freeze_header
                }
            }
        }

        pagination = {
            'active': True if self.pagination_size else False,
            'config': {
                'defaultPageSize': self.pagination_size,
                "hideOnSinglePage": self.hide_on_single_page,
                "pageSizeOptions": [
                    "10",
                    "20",
                    "25",
                    "50",
                    "100"
                ],
            }
        }

        drill_json = self._set_drill_down()

        json_content = {
            'objectType': "table",
            'title': self.title,
            'header': head_json,
            'body': body_json,
            'footer': footer_json,
            'drill': drill_json,
            'searchable': self.searchable,
            'searchString': self.search_string,
            'pagination': pagination,
            'framed': self.framed,
            'framedTitle': self.framed_title,
            'stacked': self.stacked,
            'showBorder': self.show_border,
            'showOptionBar': self.show_option_bar,
            'showHighlight': self.show_highlight,
            'striped': self.striped,
            'sortable': self.sortable,
            'scroll': scroll,
            'tabLabel': self.tab_label,
            'class': self.table_class
        }

        # Transforming in JSON
        table_json = json.dumps(json_content, indent=1, allow_nan=True, cls=JsonEncoder)

        return table_json


def is_not_empty(map: dict) -> bool:
    return len(map) > 0
