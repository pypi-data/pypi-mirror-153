from looqbox.integration.user import User
import os
import re
import string
import random


def random_hash(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for pos in range(size))


class Looqbox:

    def __init__(self, home=None, version=None, language=None, looqbox_path=None, response_path=None, jdbc_path=None,
                 config_path=None, temp_dir=None, config_file=None, client_file=None, connection_file=None,
                 connection_config=None, driver_path=None, client_key=None, client_host=None, test_mode=True,
                 publish_test=None, query_list=[], entity_sync_path=None, response_timeout=None):
        self.home = home
        self.version = version
        self.language = language
        self.looqbox_path = looqbox_path
        self.response_path = response_path
        self.entity_sync_path = entity_sync_path
        self.jdbc_path = jdbc_path
        self.driver_path = driver_path
        self.config_path = config_path
        self.client_key = client_key
        self.client_host = client_host
        self.client_file = client_file
        self.config_file = config_file
        self.connection_file = connection_file
        self.connection_config = connection_config
        self.temp_dir = temp_dir
        self.test_mode = test_mode
        self.publish_test = publish_test
        self.user = User()
        self.query_list = query_list
        self.response_timeout = response_timeout if response_timeout is not None else 30  #set a default value if Java fail to pass parameter 

    def response_dir(self, *args):

        if self.response_path is not None:
            resp_path = os.path.dirname(self.response_path)
        else:
            resp_path = os.getcwd()

        return os.path.join(resp_path, *args)

    def temp_file(self, file_name=None, temporary_dir="tmp", add_hash=True):

        if self.temp_dir is not None:
            temporary_dir = self.temp_dir

        if file_name is None:
            file_name = "file__h" + random_hash(15) + "h__.tmp"
        elif add_hash:
            base_name = re.sub('\.(.+)', '', file_name)
            extension_name = re.search('\.(.+)', file_name).group(0)
            file_name = base_name + "__h" + random_hash(15) + "h__" + extension_name

        return temporary_dir + '/' + file_name
