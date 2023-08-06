from collections import OrderedDict
import json


def save_to_json(output_meta_json, meta_json):
    with open(output_meta_json, "w") as json_file:
        json.dump(meta_json, json_file, indent=3)


def get_json_content(input_meta_json):
    with open(input_meta_json) as json_file:
        return json.load(json_file)


def split_different_workflows(record):
    raw_workflows = record['workflow'].split()
    workflows_no_whitespaces = "".join(raw_workflows)
    return workflows_no_whitespaces.split(',')



def update_booleans(record):
    for key in record.keys():
        if isinstance(record[key], str):
            if record[key].replace(" ", "").lower() == "true":
                record[key] = True
            elif record[key].replace(" ", "").lower() == "false":
                record[key] = False


def get_workflows(unsorted_keys):
    return sorted([key for key in unsorted_keys
                   if not key.startswith('input_')
                   and not key.startswith('output_')
                   and not key.startswith('variant')])


def get_inputs(unsorted_keys):
    return sorted([key for key in unsorted_keys
                   if key.startswith('input_')])


def get_variants(unsorted_keys):
    return sorted([key for key in unsorted_keys
                   if key.startswith('variant')])


def get_outputs(unsorted_keys):
    return sorted([key for key in unsorted_keys
                   if key.startswith('output_')])


def order_by_parameter(meta_json):
    sorted_meta = OrderedDict()
    unsorted_keys = list(meta_json.keys())

    workflows = get_workflows(unsorted_keys)
    inputs = get_inputs(unsorted_keys)
    variants = get_variants(unsorted_keys)
    outputs = get_outputs(unsorted_keys)

    sorted_keys = workflows + inputs + variants + outputs
    new_len = len(sorted_keys)
    old_len = len(unsorted_keys)

    if new_len != old_len:
        raise ValueError(f'Sorted keys number [{new_len}] does not equal unsorted keys number [{old_len}]')

    for key in sorted_keys:
        sorted_meta[key] = meta_json[key]

    return sorted_meta

