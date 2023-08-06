# Defining super class LooqObject
class LooqObject:

    def __init__(self):
        pass

    def to_json_structure(self):
        pass

    def remove_json_nones(self, json_dict: dict):

        # Get all the keys from empty (None) dict values
        empty_key_vals = [key for key, value in json_dict.items() if value is None]

        # Delete the empty keys
        for key in empty_key_vals:
            del json_dict[key]

        return json_dict
