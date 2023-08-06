import os
import json
from looqbox.integration.looqbox_global import Looqbox
import datetime


class GlobalCalling:

    looq = Looqbox()

    def set_looq_attributes(new_looq):
        GlobalCalling.looq = new_looq
        if GlobalCalling.looq.test_mode:
            set_looqbox_path(GlobalCalling.looq)
            set_configs_path(GlobalCalling.looq)
            set_client_config(GlobalCalling.looq)

    def log_query(result_log: dict) -> None:

        if GlobalCalling.looq.test_mode:
            print(result_log)
        query_list = GlobalCalling.looq.query_list
        query_list.append(
            {
                "connection": result_log.get("connection", ""),
                "query": result_log.get("query", ""),
                "time": result_log.get("time", ""),
                "success": result_log.get("success", "")
            }
        )


def set_looqbox_path(looq):
    # Setting Looqbox Path
    if "LOOQBOX_HOME" in os.environ.keys():
        looq.home = os.environ["LOOQBOX_HOME"]
        print("Using Looqbox path " + looq.home)
    else:
        looq.home = ""
        print("LOOQBOX_HOME is not defined in the environment")

    looq.temp_dir = os.getcwd() + "/tmp"


def set_configs_path(looq):
    config_path = os.path.join(looq.home, "conf", "R")

    if os.path.exists(config_path):
        config_conn_path = config_path

        # Setting globals
        looq.config_path = config_path
        looq.jdbc_path = os.path.join(config_conn_path, "jdbc")
        looq.driver_path = os.path.join(config_conn_path, "jdbc")
    else:
        config_path = os.path.join(looq.home, "R")
        config_conn_path = os.path.join(looq.home, "connectors")

        # Setting globals
        looq.config_path = config_path
        looq.driver_path = config_conn_path
        looq.jdbc_path = config_conn_path

    looq.config_file = os.path.join(config_path, "config.json")
    looq.client_file = os.path.join(config_path, "client_functions.py")
    looq.connection_file = os.path.join(config_conn_path, "connections.json")


def set_client_config(looq):
    if os.path.isfile(looq.connection_file):
        with open(looq.connection_file) as file:
            looq.connection_config = json.load(file)
    else:
        print("Missing connection file: ", looq.connection_file)

    if os.path.isfile(looq.config_file):
        with open(looq.config_file) as file:
            config = json.load(file)
        looq.client_key = config["clientKey"]
        looq.user.login = config["user"]
        looq.client_host = config["clientHost"]
        looq.language = config["language"]
    else:
        looq.client_key = ""
        looq.user.login = ""
        looq.client_host = ""
        looq.language = ""
