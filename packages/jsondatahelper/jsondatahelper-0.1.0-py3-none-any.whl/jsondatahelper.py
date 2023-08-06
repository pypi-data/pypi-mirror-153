import json

KEY_SPLIT_CHAR = "->"
"""

Flattend Dictionary : 
A
    {
        example->flattened->dictionary:"With A Value",
        example->with->index->0->object_name : "name0",
        example->with->index->0->object_id : "id0",
        example->with->index->1->object_name : "name1",
        example->with->index->1->object_id : "id1"
    }

Unflattend (Stanadard) Dictionary : 

B
    {
        "example":{
            "flattened":{
                "dictionary":
                    "With A Value"
                }
            },
            "with":{
                "index":[
                    {
                        "object_name":"name0",
                        "object_id":"id0"
                    },
                    {
                        "object_name":"name1",
                        "object_id":"id1"
                    }
                ]
            }           
        }
    }
"""


def are_all(array, object_type):
    for item in array:
        if not isinstance(item, object_type):
            return False
    return True


def skim_top_levels(dictionary):
    skimmed_dictionary = {}
    for prop_path, prop_value in flatten(dictionary).items():
        skimmed_dictionary[prop_path.split(KEY_SPLIT_CHAR)[-1]] = prop_value
    return skimmed_dictionary


def flatten(dictionary):
    """
    Function that converts stanadard dictionaries to a flattened state for string comparison
    and mapping of dictionaries.

    Example at top of class.

    Indexed Keyless Dict Example:
        "Example": [
            {"This":"dictionary","Is":"Keyless"},
            {"So":"Is","This":"One"}
        ]

        Flattened looks like :

            {
                "Example->0->This":"dictionary",
                "Example->0->Is":"Keyless",
                "Example->1->So":"Is",
                "Example->1->This":"One"
            }
    """

    prop_paths = {}
    try:

        for key, val in dictionary.items():
            if isinstance(val, dict) and val:
                # If the item is a dictionary then recursively call flatten to go further down the path
                deeper = flatten(val).items()
                prop_paths.update(
                    {key + KEY_SPLIT_CHAR + key2: val2 for key2, val2 in deeper}
                )
            elif isinstance(val, list):
                # If the item is a list then recursively call flatten for each item in the list
                for dict_index, list_of_keyless_dicts in enumerate(
                    val
                ):  # Apply indexing to non-keyed dictionaries
                    deeper = flatten({str(dict_index): list_of_keyless_dicts}).items()

                    prop_paths.update(
                        {key + KEY_SPLIT_CHAR + key2: val2 for key2, val2 in deeper}
                    )
            else:
                # If the item is not a dict or list then it is a value we will assign to the key
                prop_paths[key] = val
        return prop_paths
    except AttributeError:
        print("Dictionary could not be flattend!")
        return prop_paths


def split_for_indexed_values(path):
    """
    split_path : this->is->a->path : ["this","is","a","path"]

    found_indexes : [{i0,s0},...,{iN,sN}] where "N" is number of found numeric values in path

        i: location in path e.g 0->1->2->...->N : "value"
        s: String representation of index in path

    """
    split_path = path.split(KEY_SPLIT_CHAR)
    found_indexes = [
        {"location": i, "value": v} for i, v in enumerate(split_path) if v.isdigit()
    ]

    return split_path, found_indexes


def subpath_value(path_dictionary, desired_key):

    split_path = list(path_dictionary.keys())[0].split(KEY_SPLIT_CHAR)
    path_value = list(path_dictionary.values())[0]
    desired_key_idx = split_path.index(desired_key) + 1
    last_idx = len(split_path)

    return unflatten(
        {KEY_SPLIT_CHAR.join(split_path[desired_key_idx:last_idx]): path_value}
    )


def unflatten(dictionary, save_indexed_values_for_later=False):
    """
    Function that takes a flattened nested dictionary and reverts it to its original nested state.

    Turns flattened dictionary back into standard format.

    Example of flattened dictionary at top of class.


    """
    if dictionary:
        unflattend = {}
        for key, value in dictionary.items():
            parts, indexes_in_path = split_for_indexed_values(key)

            d = unflattend
            if isinstance(value, str):
                value = value.rstrip().lstrip()

            # Iterates through all parts up to last element
            for i, part in enumerate(parts[:-1]):
                # If the part is a number then d is a list, not a dict
                if part.isdigit() and isinstance(d, list):
                    part = int(part)
                    while len(d) < part + 1:
                        # Add an empty dict to the list until the size of the list is big enough for the index
                        d.append({})
                    # Set d to the correct item in the list and continue traversing the parts
                    d = d[int(part)]
                elif not isinstance(d, list):
                    # part does not already exist in d, we need to add an empty list or dict
                    if part not in d:
                        if parts[i + 1].isdigit():
                            # If the next part is a digit then this part is actually a list
                            d[part] = list()
                        else:
                            # If the next part is not a digit then this part is a dict
                            d[part] = dict()
                    elif parts[i + 1].isdigit() and not isinstance(d[part], list):
                        # If part already exists in d but the next part is a digit and the d[part] is not currently
                        # a list then overwrite with a new list
                        d[part] = list()
                    # d is a dict, drill down one level and set d to the next part
                    d = d[part]

            # Assign value to the last index of the path
            if isinstance(d, dict):
                d[parts[-1]] = value

        return unflattend


def find_value(value_to_find, nested_dictionary):
    flattened_dict = flatten(nested_dictionary)
    if value_to_find in flattened_dict:
        return flattened_dict[value_to_find]
    else:
        matching_dict = dict(
            filter(
                lambda item: item[0].startswith(value_to_find), flattened_dict.items()
            )
        )
        if len(matching_dict) > 0:
            result = dict()
            for key_name, prop_value in matching_dict.items():
                result[key_name.split(value_to_find)[1]] = prop_value
            return result
        else:
            for key_name, prop_value in flattened_dict.items():
                prop_name = key_name.split(KEY_SPLIT_CHAR)[
                    -1
                ]  # Leaf node of nested dictionary
                if str(value_to_find).lower() == prop_name.lower():
                    return prop_value
    return None


def find_and_return_all_values(values_to_find=[], nested_dictionary={}):
    found_values = {}

    for key_name, prop_value in flatten(nested_dictionary).items():
        prop_name = key_name.split(KEY_SPLIT_CHAR)[-1]  # Leaf node of nested dictionary
        for value_to_find in values_to_find:
            if str(value_to_find).lower() == prop_name.lower():
                found_values[value_to_find] = prop_value

    return found_values


def find_all(value_to_find, nested_dictionary):
    found_items = []
    for key_name, prop_value in flatten(nested_dictionary).items():
        prop_name = key_name.split(KEY_SPLIT_CHAR)[-1]  # Leaf node of nested dictionary
        if value_to_find == prop_name:
            found_items.append(prop_value)
    return found_items


def format_dict(dictionary, indent=2):
    try:
        return json.dumps(dictionary, sort_keys=True, indent=indent)
    except TypeError:
        return dictionary


def slice_dict(dictionary, ending_idx, starting_index=0):
    new_dict = {}
    keys = list(dictionary.keys())[starting_index:ending_idx]
    values = list(dictionary.values())[starting_index:ending_idx]

    for i, key in enumerate(keys):
        new_dict[key] = values[i]
    return new_dict


def search_with_default(value_to_find, nested_dictionary, default_return_value):
    found_value = find_value(value_to_find, nested_dictionary)
    if found_value:
        return found_value
    return default_return_value


def purge_empty_dict(dictionary):
    try:
        flattened = flatten(dictionary)
        purged_dict = {}
        for key, val in flattened.items():
            if val and not val == "None":
                purged_dict[key] = val
            if not val and isinstance(val, dict):
                purged_dict[key] = {}
        return unflatten(purged_dict)
    except AttributeError:
        print("Could not purge dictionary!")
        return dictionary


def clean_for_storage(dictionary, remove_empty_values=False):
    """
    Makes all Values in {Key:Value} pairs a string,
    so there are no conversion or formatting issues
    when json file is written to.

    E.g. [Datetime -> String] To prevent json serialization errors.
    """
    flattend_standardized = {}
    for key, val in flatten(dictionary).items():
        # if isinstance(val, datetime.datetime):
        #     flattend_standardized[key] = val.isoformat(sep='T', timespec='milliseconds')
        if isinstance(val, bytes):
            flattend_standardized[key] = "b'" + val.hex()
        else:
            flattend_standardized[key] = str(val)

    clean_dictionary = unflatten(flattend_standardized)

    if remove_empty_values:
        clean_dictionary = purge_empty_dict(clean_dictionary)

    return clean_dictionary


def write_json_file(file_path, data):
    with open(file_path, "w+", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=True,
            indent=4,
        )


def read_json_file(file_path):
    try:
        with open(file_path, "r+") as file_contents:
            return convert_bytes(json.load(file_contents))
    except FileNotFoundError:
        return None


def convert_bytes(loaded_json):
    for key, val in loaded_json.items():
        if isinstance(val, dict):
            loaded_json[key] = convert_bytes(val)
        elif isinstance(val, list):
            for index, item in enumerate(val):
                if isinstance(item, dict):
                    loaded_json[key][index] = convert_bytes(item)
                elif isinstance(item, str) and item.startswith("b'"):
                    loaded_json[key][index] = bytes.fromhex(item.split("b'")[1])
        elif isinstance(val, str) and val.startswith("b'"):
            loaded_json[key] = bytes.fromhex(val.split("b'")[1])

    return loaded_json