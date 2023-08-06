import logging
import sys
import datetime
import json
import requests
from looqbox.view.response_board import ResponseBoard
from looqbox.view.response_board import ResponseFrame
from looqbox.objects.looq_message import ObjMessage
from looqbox.objects.looq_html import ObjHTML
from looqbox.objects.looq_query import ObjQuery
from looqbox.view.view_functions import frame_to_board
from looqbox.view.view_functions import response_to_frame
from looqbox.global_calling import GlobalCalling
from looqbox.integration.looqbox_global import Looqbox
import warnings

__all__ = ["look_tag", "looq_test_question", "view", "get_sso_attributes", "user_id", "user_group_id", "user_login",
           "question_link", "get_entity", "get_partition"]

# Calling global variable
if GlobalCalling.looq.home is not None:
    GlobalCalling.set_looq_attributes(Looqbox())


def _send_to_dev_link(url, response_board: ResponseBoard, show_json=False):
    """
    Function to test the return from scripts in Looqbox's interface

    :param url: Looqbox's client url
    :param response_board: Board resulting from the script
    :param show_json: Print JSON or not
    :return: A request from an api
    """
    response_json = response_board.to_json_structure

    if show_json is True:
        print(response_json)

    try:
        link_request = requests.post(url, data=response_json)
    except requests.ConnectionError:
        logging.error("Page not found -> {0}".format(url))
        sys.exit(1)

    return link_request


def _new_look_tag(tag, par_json, subtag, default, only_value):
    """
    Function to return the look tag using the new JSON format (Version 2)

    """

    is_entity = "$" in subtag

    if isinstance(subtag, list):
        if any(tag_value for tag_value in subtag if tag_value in par_json[tag].keys()):
            if only_value:
                tags_list = [content['value'] for tag_value in subtag if tag_value in par_json[tag] for content in
                            par_json[tag][tag_value]['content']]
            else:
                tags_list = [content for tag_value in subtag if tag_value in par_json[tag] for content in
                             par_json[tag][tag_value]['content']]
            return tags_list

    elif subtag in par_json[tag].keys():
        if is_entity:
            if only_value:
                tags_list = list()
                for content in par_json[tag][subtag]['content']:
                    tags_list.append(content['value'])

                # Flatten the lists in only one
                tags_list = [value for value_list in tags_list for value in value_list]

                return tags_list
            else:
                return par_json[tag][subtag]['content']
        else:
            return par_json[tag][subtag]
    else:
        if only_value and isinstance(default, list):
            if isinstance(default[0], dict):
                return default[0]["value"]
            else:
                return default
        else:
            return default


def _old_look_tag(tag, par_json, default):
    if isinstance(tag, list):
        tags_list = [content for tag_value in tag for content in par_json[tag_value]]
        return tags_list
    elif tag in par_json.keys():
        return par_json[tag]
    else:
        return default


def look_tag(tag, par_json, default=None, only_value=True):
    """
    Function to search for a specific tag inside the JSON sent by the parser

    :param tag: Name to be found
    :param par_json: JSON from parser
    :param default: Default value to be returned
    :param only_value: If True return only the value of the tag, if the value is False the function will return all
    the JSON structure link to this tag
    :return: A JSON structure or a single value
    """

    warnings.warn("look_tag is deprecated, use get_entity instead", DeprecationWarning, stacklevel=2)
    if "apiVersion" not in par_json.keys():
        tag_value = _old_look_tag(tag, par_json, default)
    elif par_json["apiVersion"] is None:
        tag_value = _old_look_tag(tag, par_json, default)
    elif par_json["apiVersion"] == 1:
        tag_value = _old_look_tag(tag, par_json, default)
    elif par_json["apiVersion"] >= 2:
        if tag == "$comparative":
            tag_value = have_comparative(par_json)
        else:
            tag_value = _new_look_tag(
                tag="entities",
                par_json=par_json,
                subtag=tag,
                default=default,
                only_value=only_value)

    return tag_value


def have_comparative(par_json):
    if "$comparative" in par_json["entities"].keys():
        return True
    else:
        return False


def get_entity(entity, par_json, entity_default=None, only_value=False):
    """
    Function to search for a specific entity inside the JSON sent by the parser

    :param entity: entity to be found
    :param par_json: JSON from parser
    :param entity_default: Default value to be returned
    :param only_value: if True will only return the entity value
    :return: A Map structure or a single value
    """

    if par_json is None:
        par_json = {"apiVersion": 1}

    if "apiVersion" not in par_json.keys() or par_json["apiVersion"] is None:
        tag_value = _old_look_tag(entity, par_json, entity_default)

    elif par_json["apiVersion"] == 1:
        tag_value = _old_look_tag(
            tag=entity,
            par_json=par_json,
            default=entity_default
        )
    elif par_json["apiVersion"] >= 2:
        if entity_default is None:
            entity_default = [{'segment': None, 'text': None, 'value': None}]
        tag_value = _new_look_tag("entities", par_json, entity, entity_default, only_value)

    return tag_value


def get_partition(partition, par_json, partition_default=None, only_value=False):
    """
    Function to search for a specific partition inside the JSON sent by the parser

    :param partition: entity to be found
    :param par_json: JSON from parser
    :param partition_default: Default value to be returned
    :param only_value: if True will only return the entity value
    :return: A Map structure or a single value
    """

    if par_json is None:
        par_json = {"apiVersion": 1}

    if "apiVersion" not in par_json.keys() or par_json["apiVersion"] is None:
        tag_value = _old_look_tag(partition, par_json, partition_default)

    elif par_json["apiVersion"] == 1:
        tag_value = _old_look_tag(
            tag=partition,
            par_json=par_json,
            default=partition_default
        )

    elif par_json["apiVersion"] >= 2:
        tag_value = _new_look_tag(
            "partitions",
            par_json,
            partition,
            partition_default,
            only_value)

    return tag_value


def _response_json(parser_json, function_call, second_call=False):
    """
    Function called by the python kernel inside the looqbox server. This function get the return in the main script
    and treat it to return a board to the frontend

    :param parser_json: JSON from parser
    :param function_call: Main function to be called inside the kernel. Default: looq_response
    :return: A ResponseBoard object
    """

    if isinstance(parser_json, str):
        par = json.loads(parser_json)
    else:
        par = parser_json

    if "$query" in par and par["$query"] and not second_call:

        response = _response_query(par, function_call, second_call, simple=False)
    else:
        response = function_call(par)
        is_board = isinstance(response, ResponseBoard)
        is_frame = isinstance(response, ResponseFrame)
        is_list = isinstance(response, list)

        if not is_frame and not is_board and is_list:
            response = frame_to_board(response)
        elif not is_frame and not is_board:
            looq_object = response_to_frame(response)
            response = frame_to_board(looq_object)
        elif is_frame:
            response = frame_to_board(response)

    board_json = response.to_json_structure

    return board_json


def _response_query(par, function_call, second_call, simple=False):
    response_execution_error = False
    # start_time = datetime.datetime.now()
    try:
        response = _response_json(json.dumps(par), function_call, second_call=True)
    except:
        response_execution_error = True
    # total_sql_time = datetime.datetime.now() - start_time

    global_queries = GlobalCalling.looq.query_list
    queries_qt = len(global_queries)

    # If the global hasn't any query save
    if queries_qt == 0:
        message = ObjMessage("Sem query encontrada na response")
        response = ResponseFrame([message])
    else:
        response = ResponseFrame(stacked=True)
        # Reversing the list to change the appearing order in the looqbox frame
        global_queries.reverse()
        # For each query we save an objMessage inside a responseFrame
        total_time = datetime.timedelta()
        for query in global_queries:
            query_time = datetime.datetime.strptime(query.get("time"), "%H:%M:%S.%f").time()
            query_time_delta = datetime.timedelta(
                hours=query_time.hour,
                minutes=query_time.minute,
                seconds=query_time.second,
                microseconds=query_time.microsecond
            )
            total_time += query_time_delta
        response.content.insert(0, ObjQuery(queries=global_queries, total_time=str(total_time)))

        response = ResponseBoard([response])

    return response


def _check_test_parameter(parameters, par_name):
    """
    Function to check if the parameter_name(par_name) is on the parameter's keys

    :param parameters: Parameters send in looq_test_question
    :param par_name: Desire name to be found in key
    :return: The value of the par_name in parameter or None
    """
    par_return = None

    if hasattr(parameters, par_name):
        par_return = parameters[par_name]

    return par_return


def looq_test_question(test_function=None, parameters=None, show_json=False, user=None, host=None):
    """
    Function to simulate parser parameters. Using this developers can test their scripts using entities.

    :param parameters: Entities and its values
    :param show_json: Show final json or not
    :param user: User that the result will be sent
    :param host: Host that the result will be sent
    """
    # test when the process of response is correct
    if test_function is None:
        raise Exception("Function to be tested not been informed")

    if user is None:
        user = GlobalCalling.looq.user.login

    if host is None:
        host = GlobalCalling.looq.client_host

    if GlobalCalling.looq.test_mode is False:
        return None

    if isinstance(parameters, str):
        parameters = json.loads(parameters)

    GlobalCalling.looq.user_id = _check_test_parameter(parameters, "user_id")
    GlobalCalling.looq.user_group_id = _check_test_parameter(parameters, "user_group_id")
    GlobalCalling.looq.user_login = _check_test_parameter(parameters, "user_login")

    if "$query" in parameters and parameters["$query"]:
        response = _response_query(parameters, test_function, second_call=False)
    else:
        initial_response_time = datetime.datetime.now()
        response = test_function(parameters)
        total_response_time = datetime.datetime.now() - initial_response_time

    if GlobalCalling.looq.publish_test is None or GlobalCalling.looq.publish_test is True:
        start_post_time = datetime.datetime.now()
        view(response, show_json, user, host)
        if "$query" in parameters and parameters["$query"]:
            print("Query publicada")
        else:
            total_publish_time = datetime.datetime.now() - start_post_time
            print("Response time: " + str(total_response_time))
            print("Publish time: " + str(total_publish_time))
            print("Total time...:" + str(total_publish_time + total_response_time))


def view(looq_object=None, show_json=False, user=GlobalCalling.looq.user.login,
         host=GlobalCalling.looq.client_host):
    if looq_object is None:
        actual_datetime = datetime.datetime.now()

        if looq_object is None:
            looq_object = ObjMessage(text="teste " + str(actual_datetime), type="alert-success")

    is_board = isinstance(looq_object, ResponseBoard)
    is_frame = isinstance(looq_object, ResponseFrame)
    is_list = isinstance(looq_object, list)

    if not is_frame and not is_board and is_list:
        looq_object = frame_to_board(looq_object)
    elif not is_frame and not is_board:
        looq_object = response_to_frame(looq_object)
        looq_object = frame_to_board(looq_object)
    elif is_frame:
        looq_object = frame_to_board(looq_object)
    url = host + "/api/devlink/" + user
    _send_to_dev_link(url, looq_object, show_json)
    print("looq.view: published for user", user, "in", host)


def looq_process_form_json(form_json, session_json, looq_process_form):
    """
    Function that will receive a form sent by the front. This function will read the parameters and execute then
    inside the looq_process_form in the other script.
    """

    form_data = json.loads(form_json)

    session_data = json.loads(session_json)

    response = looq_process_form(form_data, session_data)

    response = json.dumps(response.to_json_structure)

    return response


def get_sso_attributes(par):
    """
    Get the user SSO information from parser

    :return: The JSON of userSsoAttributes in parser return
    """
    sso_attributes = None

    if par is None:
        par = {"apiVersion": 1}

    if "apiVersion" not in par.keys() or par["apiVersion"] is None:
        sso_attributes = par["userSsoAttributes"]

    elif par["apiVersion"] == 1:
        sso_attributes = par["userSsoAttributes"]

    elif par["apiVersion"] >= 2:
        sso_attributes = par["user"]["ssoAttributes"]

    return sso_attributes


def question_link(question, link_text):
    """
    Creates a link to a question.

    :param str question: Question.
    :param str link_text: Text of the link.
    :return: A link string.
    """
    return "<question-link query='" + question + "'>" + link_text + "</question-link>"


def user_id(par: dict = None) -> str:
    """
    Get the user id from options(par is None) or from parser.

    Examples:
    --------
    >>> user_id(par)

    :return: The id string.
    """
    if par is None:
        return GlobalCalling.looq.user.id
    else:
        return par.get('user').get('id')


def user_login(par: dict = None) -> str:
    """
    Get the user login from options(par is None) or from parser.

    Examples:
    --------
    >>> user_login(par)

    :return: The login string.
    """
    if par is None:
        return GlobalCalling.looq.user.login
    else:
        return par.get('user').get('login')


def user_group_id(par: dict = None) -> str:
    """
    Get the user group id from options(par is None) or from parser.

    Examples:
    --------
    >>> user_group_id(par)

    :return: The group id string.
    """
    if par is None:
        return GlobalCalling.looq.user.group
    else:
        return par.get('user').get('groupId')
