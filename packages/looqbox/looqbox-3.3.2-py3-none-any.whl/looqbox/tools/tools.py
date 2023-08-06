from collections import OrderedDict
from looqbox.objects.looq_table import ObjTable
from looqbox.objects.looq_list import ObjList
from looqbox.view.response_frame import ResponseFrame
from looqbox.global_calling import GlobalCalling
from looqbox.integration.looqbox_global import Looqbox
import pandas as pd
import re
import os
import shutil

__all__ = ["data_comp", "transpose_data", "find_token", "create_file_link"]

# Calling global variable
if GlobalCalling.looq.home is None:
    GlobalCalling.set_looq_attributes(Looqbox())


def find_token(text, token_head, token_type="string"):
    """
    Find a token from a text using a token_head as base

    :param text: Text where the token is
    :param token_head: Base to be search in the text
    :param token_type: Type of the token, can be a string or a digit
    :return:
    """
    if token_type == "string":
        value_regex = ":? ?(\\S+)"
    elif token_type == "digit":
        value_regex = ":? ?(\\d+)"

    p = re.compile(token_head + value_regex)
    tokens = p.findall(text)

    return tokens


def data_comp(table1, table2, by=None, cols_to_compare=None, null_as="-", absolute_delta=False, suffixes=None):
    """
    Creates a ObjTable with values of comparision between table1 and table2.

    Example:
        table1 = ObjTable(data=pd.DataFrame({'Loja': ['SP', 'RJ'],
                                             'Vendas': [2500, 5300]}))
        table2 = ObjTable(data=pd.DataFrame({'Loja': ['SP', 'RJ'],
                                             'Vendas': [500, 1300]}))

        table = data_comp(table1, table2, by='Loja')

    :param absolute_delta: Add a column with the absolute difference
    :param null_as: Set default value for None
    :param table1: An ObjTable object
    :param table2: An ObjTable object
    :param by: Column(s) of type character shared between the two tables
    :param cols_to_compare: Columns to be compared
    :return: An ObjTable object that inherits the value_format of the table1 as well as the total type
    """
    if suffixes is None:
        suffixes = [" P1", " P2"]

    if isinstance(table1, ResponseFrame):
        table1 = table1.content

    if isinstance(table2, ResponseFrame):
        table2 = table2.content

    if not isinstance(table1, ObjTable):
        raise Exception("First argument is not an ObjTable object")

    if not isinstance(table2, ObjTable):
        raise Exception("Second argument is not an ObjTable object")

    comparative_data = _comp_tables(table1, table2, by, cols_to_compare, absolute_delta, suffixes)

    delta_table = ObjTable(null_as=null_as)
    col_order = comparative_data.keys()
    delta_table.data = pd.DataFrame(comparative_data, columns=col_order)

    if table1.cell_format is not None:
        _add_delta_format(delta_table, table1)

    if table1.total is not None:
        total_table1 = table1.total
        total_table2 = table2.total

        # Trecho comentado para caso quebre comparativo por diferença de colunas, retirar no futuro
        # if not len(total_table1.keys()) == len(table1.data.keys()):
        #     raise Exception("Total size is different from number of cols")
        if not len(total_table1.keys()) == len(total_table2.keys()):
            raise Exception("Tables total size are different from number of cols")

        comparative_total = _comp_totals(total_table1, total_table2, by, cols_to_compare, absolute_delta, suffixes)
        delta_table.total = comparative_total

    delta_table.rows = delta_table.data.shape[0]
    delta_table.cols = delta_table.data.shape[1]

    return delta_table


def _add_delta_format(delta_table, table1):
    #  TODO Make a better delta conversion logic, since we have multiple ways to set a format
    delta_table.col_format = {}
    for col in table1.value_format.keys():
        for delta_col in delta_table.data.keys():

            if "∆%" in delta_col:
                delta_table.col_format[delta_col] = "percent:2"
            elif col in delta_col:
                delta_table.col_format[delta_col] = table1.value_format[col]


def _comp_tables(table1, table2, by=None, cols_to_compare=None, absolute_delta=False, suffixes=None):

    if suffixes is None:
        suffixes = [" P1", " P2"]

    if isinstance(table1, dict):
        table1 = pd.DataFrame(table1)

    if isinstance(table2, dict):
        table2 = pd.DataFrame(table2)

    # If by is None, get first column name
    if by is None:
        by = table1.data.columns[0]

    # If cols_to_compare is None, use all the columns of the table
    if cols_to_compare is None:
        cols_to_compare = table1.data.columns

    table3 = pd.merge(table1.data, table2.data, how="outer", on=by, suffixes=suffixes)

    insert_index = 0
    column_order = []
    for comp_col in cols_to_compare:
        try:
            if comp_col in by:
                column_order.append(comp_col)
                insert_index += 1
                continue

            for column in table3.columns:
                if comp_col in column:
                    column_order.append(column)

            if absolute_delta:
                calculated_col = table3.apply(lambda row: float(row[comp_col + suffixes[1]]) - float(row[comp_col + suffixes[0]]), axis=1)
                table3['∆'+comp_col] = calculated_col
                column_order.append('∆'+comp_col)

            calculated_col = table3.apply(lambda row: (float(row[comp_col + suffixes[1]])/float(row[comp_col + suffixes[0]])) - 1
                                          if row[comp_col + suffixes[0]] != 0 else "-", axis=1)
            table3['∆%' + comp_col] = calculated_col
            column_order.append('∆%' + comp_col)
        except TypeError:
            raise TypeError("Column " + comp_col + " is not a numeric type")
        except:
            raise Exception("Column " + comp_col + " not in both data frames")

    table3 = table3[column_order]
    table3.fillna("-", inplace=True)

    return table3


def _comp_totals(total1, total2, by=None, cols_to_compare=None, absolute_delta=False, suffixes=None):
    if suffixes is None:
        suffixes = [" P1", " P2"]
    d3_total = OrderedDict()

    # If cols_to_compare is None, use all the columns of the table
    if cols_to_compare is None:
        cols_to_compare = total1.keys()
    else:
        cols_to_compare = by + cols_to_compare

    for cols in cols_to_compare:
        try:
            if cols in by:
                d3_total[cols] = total1[cols]
            elif cols in total1.keys() and cols in total2.keys():
                if isinstance(total1[cols], str):
                    try:
                        total1[cols] = float(total1[cols])
                    except:
                        pass

                if isinstance(total2[cols], str):
                    try:
                        total2[cols] = float(total2[cols])
                    except:
                        pass

                d3_total[cols + suffixes[0]] = total1[cols]
                d3_total[cols + suffixes[1]] = total2[cols]
                if absolute_delta:
                    d3_total["∆" + cols] = total2[cols] - total1.get(cols, 0)
                d3_total["∆%" + cols] = (total2[cols] / total1.get(cols, 0)) - 1
        except TypeError:
            raise TypeError("Column " + cols + " is not a numeric type and cannot be converted")
        except:
            raise Exception("Column " + cols + " not in both data frames")

    return d3_total


def _rename_duplicated_values(values_list):
    value_before = None
    counter = 1
    index = 0
    for value in values_list:
        if index != 0:
            if value == value_before:
                values_list[index] = value + "." + str(counter)
                counter += 1
            else:
                counter = 1

        value_before = value
        index += 1


def _get_attributes(transposed_table, table_object):
    row_to_col_dict = {transposed_table.data.loc[row][0]: row for row in transposed_table.data.index}
    col_to_row_in_transpose = None
    if table_object.cell_style is not None:
        for col in table_object.cell_style.keys():
            if transposed_table.total_row_style is None:
                transposed_table.total_row_style = dict()

            col_to_row_in_transpose = row_to_col_dict[col]
            transposed_table.total_row_style[str(col_to_row_in_transpose)] = table_object.cell_style[col]

    if table_object.cell_format is not None:
        for col in table_object.cell_format.keys():
            if transposed_table.total_row_format is None:
                transposed_table.total_row_format = dict()

            col_to_row_in_transpose = row_to_col_dict[col]
            transposed_table.total_row_format[str(col_to_row_in_transpose)] = table_object.cell_format[col]

    if table_object.cell_link is not None:
        for col in table_object.cell_link.keys():
            if col_to_row_in_transpose is None:
                col_to_row_in_transpose = row_to_col_dict[col]

            transposed_table.total_row_link = dict()
            transposed_table.total_row_link[str(col_to_row_in_transpose)] = table_object.cell_link[col]


def transpose_data(table_object, columns_name=None):
    """
    Transpose a data frame and transform it in a ObjTable. The main difference in this function is that the user
    can choose the name of the first row of the transposed table
    :param table_object: Table to be transposed
    :param columns_name: Name of the columns of the transposed table. If the parameter is None the names of the columns
    will be the first row of the data frame.
    :return: A transposed data frame as a ObjTable object
    """

    # converting all to a pandas object
    if isinstance(table_object, ObjTable):
        data = table_object.data
    elif isinstance(table_object, pd.DataFrame):
        data = table_object
    elif isinstance(table_object, dict):
        data = pd.DataFrame(table_object)

    # If the user didn't pass a first_row, get the first columns as name
    if columns_name is None:
        cols_name = data.keys()[0]
        row_values = data.keys()

        # Transposing data frame
        data = data.T

        # Inserting new columns
        data.insert(0, cols_name, list(row_values))

        # Get rows values
        first_row_values = data.loc[cols_name]

        # Changing all the columns to the value of the first line
        data.columns = list(first_row_values)

        # Removing the first line of the data frame
        data = data.drop(data.index[[0]])

        data = data.reset_index()
        del data['index']

    else:
        cols_name = columns_name[0]
        row_values = [columns_name[0]] + list(data.keys())
        data.insert(0, columns_name[0], [columns_name[1]] * len(data.index))

        # Transposing data frame
        data = data.T

        # Inserting new columns
        data.insert(0, cols_name, list(row_values))

        # Get rows values
        first_row_values = list(data.loc[row_values[0]])

        _rename_duplicated_values(first_row_values)

        # Changing all the columns to the value of the first line
        data.columns = list(first_row_values)

        # Removing the first line of the data frame
        data = data.drop(data.index[[0]])

        data = data.reset_index()
        del data['index']

    transposed_table = ObjTable(data)

    _get_attributes(transposed_table, table_object)

    return transposed_table


def create_file_link(file_path):
    """
    Creates a file link for a given file path.

    :param file_path: Chosen file path
    :return: A download link
    """
    if file_path == os.path.basename(file_path):
        template_file = os.path.join(GlobalCalling.looq.response_dir() + "/" + file_path)
        temporary_file = GlobalCalling.looq.temp_file(file_path)
        shutil.copy(template_file, temporary_file)
        source = "looqfile://" + os.path.basename(temporary_file)
    else:
        source = "looqfile://" + os.path.basename(file_path)

    return source
