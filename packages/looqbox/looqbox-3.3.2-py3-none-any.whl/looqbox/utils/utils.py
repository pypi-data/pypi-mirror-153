import random
import base64
import datetime
import itertools
import types
import string
from monthdelta import monthdelta
from looqbox.global_calling import GlobalCalling
from looqbox.integration.looqbox_global import Looqbox
import os
import importlib.util

__all__ = ["random_hash", "base64_encode", "base64_decode", "paste_if", "format", "format_cnpj", "format_cpf",
           "title_with_date", "map", "drill_if", "current_day", "partition", "library"]

# Calling global variable
if GlobalCalling.looq.home is None:
    GlobalCalling.set_looq_attributes(Looqbox())


def library(file=None):
    """
    Call (import) functions from a file in the Looqbox server. The file must be in the R folder.

    The return of this function must be saved in a variable to be used like a python module.

    :param file: File's name
    :return: A module with all the functions from the file
    """
    home = GlobalCalling.looq.home
    config = os.path.join(home, "R")
    name = file.split(".")[0]

    spec = importlib.util.spec_from_file_location(name, os.path.join(config, file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def random_hash(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for pos in range(size))


def base64_encode(text):
    encoded_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')

    return encoded_text


def base64_decode(text):
    decoded_text = base64.b64decode(text).decode('utf-8')

    return decoded_text


def paste_if(head, args=None, closure="", args_separator="|"):
    """
    Paste only if argument exists, otherwise returns None.

    :param head: Text to be inserted before the argument
    :param args: Value to be inserted after the head, if the value is None, the title will not be shown
    :param closure: Text to be inserted after the argument
    :param args_separator: Character string to separate the results
    :return: a string or None
    """
    if isinstance(args, dict):
        raise Exception("Dictionary not accept in paste_if")
    elif isinstance(args, list):
        args_with_sep = ""

        for arg in args[0:len(args) - 1]:
            args_with_sep = args_with_sep + str(arg) + args_separator

        return head + args_with_sep + str(args[-1]) + closure

    elif isinstance(args, str):
        return head + args + closure

    elif isinstance(args, float) or isinstance(args, int) or isinstance(args, complex):
        return head + str(args) + closure
    else:
        return ""


def format(value, value_format=None, language=GlobalCalling.looq.language):
    """
    Sets a value according to the specified format.

    :param value: Value to be formatted
    :param value_format: Format to be assigned to value. Formats allowed:
    * number:0
    * number:1
    * number:2
    * percent:0
    * percent:1
    * percent:2
    * date
    * datetime
    :return: A string formatted according to the value_format parameter
    """

    date_format = "%d/%m/%Y"
    datetime_format = "%d/%m/%Y %H:%M:%S"

    if language == "en-us":
        date_format = "%m/%d/%Y"
        datetime_format = "%m/%d/%Y %H:%M:%S"

    if value_format is None:
        raise Exception("Format not defined")

    if isinstance(value_format, types.FunctionType):
        return value_format(value)

    if language == "pt-br":
        if value_format == "number:2":
            value = "{0:,.2f}".format(float(value))
            value = value.translate(str.maketrans(",.", ".,"))
        elif value_format == "number:1":
            value = "{0:,.1f}".format(float(value))
            value = value.translate(str.maketrans(",.", ".,"))
        elif value_format == "number:0":
            value = "{0:,.0f}".format(float(value))
            value = value.translate(str.maketrans(",.", ".,"))
        elif value_format == "percent:2":
            value = "{0:.2%}".format(value)
            value = value.translate(str.maketrans(",.", ".,"))
        elif value_format == "percent:1":
            value = "{0:.1%}".format(value)
            value = value.translate(str.maketrans(",.", ".,"))
        elif value_format == "percent:0":
            value = "{0:.0%}".format(value)
            value = value.translate(str.maketrans(",.", ".,"))
        elif value_format == "Date" or value_format == "date":
            if isinstance(value, str):
                value = datetime.datetime.strptime(value, '%Y-%m-%d')
            value = datetime.datetime.strftime(value, date_format)
        elif value_format == "Datetime" or value_format == "datetime":
            if isinstance(value, str):
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            value = datetime.datetime.strftime(value, datetime_format)
    elif language == "en-us":
        if value_format == "number:2":
            value = "{0:,.2f}".format(float(value))
        elif value_format == "number:1":
            value = "{0:,.1f}".format(float(value))
        elif value_format == "number:0":
            value = "{0:,.0f}".format(float(value))
        elif value_format == "percent:2":
            value = "{0:.2%}".format(value)
        elif value_format == "percent:1":
            value = "{0:.1%}".format(value)
        elif value_format == "percent:0":
            value = "{0:.0%}".format(value)
        elif value_format == "Date" or value_format == "date":
            value = datetime.datetime.strftime(value, date_format)
        elif value_format == "Datetime" or value_format == "datetime":
            value = datetime.datetime.strftime(value, datetime_format)

    return value


def format_cnpj(cnpj_string):
    """
    Formats CNPJ to standard format.

    :param cnpj_string: Unformatted CNPJ (string)
    :return: A string in the CNPJ format XX.XXX.XXX/XXXX-XX
    """
    if not isinstance(cnpj_string, str):
        return ""

    if len(cnpj_string) == 13:
        cnpj_string = '0' + cnpj_string
    elif len(cnpj_string) > 14:
        raise Exception('Invalid CNPJ string: More than 14 digits')

    return cnpj_string[:2] + "." + cnpj_string[2:5] + "." + cnpj_string[5:8] + "/" + \
           cnpj_string[8:12] + '-' + cnpj_string[12:]


def format_cpf(cpf_string):
    """
    Formats CPF to standard format.

    :param cpf_string: Unformatted CPF (string)
    :return: A string in the CPF format XXX.XXX.XXX-XX
    """
    return cpf_string[:3] + "." + cpf_string[3:6] + "." + cpf_string[6:9] + '-' + cpf_string[9:]


def week_name(date, language=GlobalCalling.looq.language):
    if language == "pt-br":
        week_rule = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
    elif language == "en-us":
        week_rule = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    elif language == "it":
        week_rule = ["lun", "mar", "mer", "gio", "ven", "sab", "do"]

    date_week_day = date.timetuple()[6]

    return week_rule[date_week_day]


def date_range_name(date_int, language=GlobalCalling.looq.language):
    initial_date = date_int[0]
    finish_date = date_int[1]

    date_range = None

    # Case Day
    if initial_date == finish_date:
        if language == "pt-br":
            date_range = week_name(initial_date, language) + " sem: " + str(initial_date.isocalendar()[1]) + "/" \
                         + str(initial_date.year)
        elif language == "en-us":
            date_range = week_name(initial_date, language) + " week: " + str(initial_date.isocalendar()[1]) + "/" \
                         + str(initial_date.year)
        elif language == "it":
            date_range = week_name(initial_date, language) + " week: " + str(initial_date.isocalendar()[1]) + "/" \
                         + str(initial_date.year)

    # Case Week
    if initial_date.timetuple()[6] == 0 and initial_date + datetime.timedelta(days=6) == finish_date:
        if language == "pt-br":
            date_range = "sem: " + str(initial_date.isocalendar()[1]) + " - " + str(initial_date.year)
        elif language == "en-us":
            date_range = "week: " + str(initial_date.isocalendar()[1]) + " - " + str(initial_date.year)
        elif language == "it":
            date_range = "week: " + str(initial_date.isocalendar()[1]) + " - " + str(initial_date.year)

    # Case Month
    if initial_date.day == 1 and initial_date + monthdelta(1) - datetime.timedelta(days=1) == finish_date:
        if language == "pt-br":
            date_range = "mês: " + str(initial_date.month) + "/" + str(initial_date.year)
        elif language == "en-us":
            date_range = "month: " + str(initial_date.month) + "/" + str(initial_date.year)
        elif language == "it":
            date_range = "mese: " + str(initial_date.month) + "/" + str(initial_date.year)

    # Case MTD
    if initial_date.day == 1 and initial_date.month == finish_date.month and datetime.datetime.now().strftime(
            "%Y-%m-%d") == finish_date:
        if language == "pt-br":
            date_range = "mtd: " + str(initial_date.month) + "/" + str(initial_date.year)
        elif language == "en-us":
            date_range = "mtd: " + str(initial_date.month) + "/" + str(initial_date.year)
        elif language == "it":
            date_range = "mtd: " + str(initial_date.month) + "/" + str(initial_date.year)

    # Case Year
    if initial_date.day == 1 and initial_date.month == 1 \
            and initial_date + monthdelta(12) - datetime.timedelta(1) == finish_date:
        if language == "pt-br":
            date_range = "ano: " + str(initial_date.year)
        elif language == "en-us":
            date_range = "year: " + str(initial_date.year)
        elif language == "it":
            date_range = "ieri: " + str(initial_date.year)

    if date_range is None:
        return ""
    else:
        return " (" + date_range + ")"


def validate_datetime(date_text):

    if isinstance(date_text, datetime.datetime):
        return True
    else:
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False


def title_with_date(header=None, date_int=None, language=GlobalCalling.looq.language):
    """
    Writes a title for the specified date or date range.

    :param header: Text to be placed before the date
    :param date_int: Date(s) interval to be used in the title
    :param language: Title language
    :return: A title string
    """

    if language == "pt-br":
        var_day = " dia "
        var_from = " de "
        var_to = " a "
    elif language == "en-us":
        var_day = " day "
        var_from = " from "
        var_to = " to "
    elif language == "it":
        var_day = " gio "
        var_from = " dal "
        var_to = " al "
    else:
        raise Exception("Language {} is invalid".format(language))

    date_int_aux = date_int.copy()
    is_datetime_0 = validate_datetime(date_int_aux[0])
    is_datetime_1 = validate_datetime(date_int_aux[1])

    if is_datetime_0 and is_datetime_1:
        date_int_aux[0] = datetime.datetime.strptime(date_int[0], '%Y-%m-%d %H:%M:%S').date()
        date_int_aux[1] = datetime.datetime.strptime(date_int[1], '%Y-%m-%d %H:%M:%S').date()
    else:
        date_int_aux[0] = datetime.datetime.strptime(date_int[0], '%Y-%m-%d').date()
        date_int_aux[1] = datetime.datetime.strptime(date_int[1], '%Y-%m-%d').date()

    if isinstance(date_int_aux[0], datetime.date) and isinstance(date_int_aux[1], datetime.date):
        if date_int_aux[0] == date_int_aux[1]:
            date_result = header + var_day + "" + \
                          format(date_int_aux[0], "Date", language) + date_range_name(date_int_aux, language)
        else:
            date_result = header + var_from + "" + format(date_int_aux[0], "Date", language) + var_to \
                          + format(date_int_aux[1], "Date", language) + date_range_name(date_int_aux, language)
    else:
        if date_int_aux[0] == date_int_aux[1]:
            date_result = header + var_day + "" + format(date_int_aux[0], "datetime", language)
        else:
            date_result = header + var_from + "" + format(date_int_aux[0], "datetime", language) + var_to \
                          + format(date_int_aux[1], language)

    return date_result


def map(function_arg, *args):
    """
    Apply function with the arguments defined.

    :param function_arg: Function to apply
    :param args: Function arguments
    :return: The output of the function
    """
    # Verify if it has arguments
    if len(args) == 1 and args[0] is None:
        return function_arg(None)

    # Transforming Nones into str to find the cartesian product
    args_list = list(args)
    for i in range(len(args_list)):
        if args_list[i] is None:
            args_list[i] = ["None"]
    args = tuple(args_list)

    # Finding the cartesian product of my *args
    args_possibilities_list = list(itertools.product(*args))

    # Transform tuple into list
    args_possibilities_list = [list(possibility) for possibility in args_possibilities_list]

    # Turning str None into None type again
    for poss_list in args_possibilities_list:
        for i in range(len(poss_list)):
            if poss_list[i] == "None":
                poss_list[i] = None

    # args_possibilities_list = [args_possibilities_list]

    # Dynamically sending all the possibilities to the function
    result = [function_arg(*arg_product) for arg_product in args_possibilities_list]

    return result


def drill_if(value_link, arg):
    """
    Removes drill in case the correspondent arg is not None.

    :param value_link: value_link of the column of row
    :param arg: Arguments to be evaluated
    """

    if not isinstance(arg, list):
        arg = [arg]

    if len(value_link) == len(list(filter(None, arg))) \
            or (not isinstance(value_link, list) and len(list(filter(None, arg))) == 1):
        value_link = None
    else:
        for i in range(len(arg),0,-1):
            if arg[i-1] is not None:
                value_link.remove(value_link[i-1])


    return value_link


def current_day(format='date'):
    """
    Creates list with current day.

    :param format: Format of the date output (date or datetime)
    :return: A list with two elements of the current day. If an invalid format is specified, then it uses the 'date' format
    """

    if format.lower() == 'date':
        return [datetime.datetime.now().strftime("%Y-%m-%d"), datetime.datetime.now().strftime("%Y-%m-%d")]
    elif format.lower() == 'datetime':
        return [datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M")]
    else:
        return [datetime.datetime.now().strftime("%Y-%m-%d"), datetime.datetime.now().strftime("%Y-%m-%d")]


def partition(values):
    """
    Partitions list into overlapping sublists of length 2.

    :param list ll: List of elements for partition.
    :return: A list of sublists containing 2 elements each.

    Examples:
    --------
    values = ["Monday", 54, True]
    partition(values)
    """
    if not isinstance(values, list):
        values = [values]

    new_list = []

    if len(values) == 1:
        new_list = [values + values]
    else:
        [new_list.append([values[i], values[i + 1]]) for i in range(len(values) - 1)]

    return new_list
