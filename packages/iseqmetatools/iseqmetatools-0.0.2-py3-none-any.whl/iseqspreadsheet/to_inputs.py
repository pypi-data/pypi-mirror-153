#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gspread
import argparse
from collections import OrderedDict
from isequtils import spreadsheetutils


__version__ = "0.0.1"


def split_different_workflow_variants(record):
    raw_workflow_variant = record['workflow_variant'].split()
    workflow_variant_no_whitespace = "".join(raw_workflow_variant)
    return workflow_variant_no_whitespace.split(',')


def filter_by_workflow(unfiltered, workflow_name):
    filtered = list()
    for index, record in enumerate(unfiltered):
        workflow_variant_list = split_different_workflow_variants(record)

        for workflow_variant in workflow_variant_list:
            workflow = workflow_variant.split('_')[0]
            if workflow == workflow_name:
                record['workflow_variant'] = workflow_variant
                filtered.append(record)

    return filtered


def get_variant_prefix(subdict):
    workflow_variant = subdict['workflow_variant']
    if '_' in workflow_variant:
        return f"{workflow_variant.split('_')[1]}_"
    return ''


def update_inputs_groups(inputs_groups, meta_json):
    parametrs_to_update = ['name', 'description', 'constraints.minInputs']

    for group in inputs_groups:
        variant_prefix = get_variant_prefix(group)

        groups = meta_json.get(f'{variant_prefix}groupInputs', {})
        groupname = group['readonly_name']
        groups[groupname] = groups.get(groupname, {})

        for parameter in parametrs_to_update:
            if '.' in parameter:
                subgroup = parameter.split('.')[0]
                subparameter = parameter.split('.')[1]
                groups[groupname][subgroup] = groups[groupname].get(subgroup, {})
                groups[groupname][subgroup][subparameter] = group[parameter]
            elif group[parameter]:
                groups[groupname][parameter] = group[parameter]

    return meta_json


def update_inputs(inputs, meta_json):
    parameters = ['name', 'description', 'default', 'advanced', 'groupId']
    for input in inputs:
        variant_prefix = get_variant_prefix(input)
        input['type'] = input.pop('readonly_type')
        name = f"{variant_prefix}input_{input['readonly_name']}"
        for parameter in parameters:
            meta_json[name] = meta_json.get(name, {})
            if input[parameter]:
                meta_json[name][parameter] = input[parameter]
        spreadsheetutils.update_booleans(meta_json[name])
    return meta_json


def update_meta(sheets, meta_json, workflow_name):
    inputs_worksheet = sheets.worksheet('Inputs')
    inputs = inputs_worksheet.get_all_records()

    inputs_groups_worksheet = sheets.worksheet('Inputs groups')
    inputs_groups = inputs_groups_worksheet.get_all_records()

    inputs = filter_by_workflow(inputs, workflow_name)
    inputs_groups = filter_by_workflow(inputs_groups, workflow_name)

    meta_json = update_inputs_groups(inputs_groups, meta_json)
    meta_json = update_inputs(inputs, meta_json)

    return meta_json


def parse(credentials_json, spreadsheet_key, meta_json, workflow_name, output_meta_json):
    gc = gspread.service_account(filename=credentials_json)
    sheets = gc.open_by_key(spreadsheet_key)

    meta_json = spreadsheetutils.get_json_content(meta_json)
    try:
        meta_json = update_meta(sheets, meta_json, workflow_name)
        spreadsheetutils.save_to_json(output_meta_json, meta_json)
    except Exception as ex:
        print(ex)


def main():
    parser = argparse.ArgumentParser(description="""Creates new meta.json with inputs parameters filled from google spreadsheet.
Further explanation can be found here: 
    https://workflows-dev-documentation.readthedocs.io/en/latest/Developer%20tools.html#parsing-google-spreadsheet-to-meta""")
    parser.add_argument('-c', '--credentials', help='Path to credentials file containing data necessary to get access', required=True)
    parser.add_argument('-k', '--spreadsheet_key', help='A key to the google spreadsheet', required=True)
    parser.add_argument('-m', '--meta_json', help='Path to meta json', required=True)
    parser.add_argument('-n', '--workflow_name', help='Workflow name', required=True)
    parser.add_argument('-o', '--output_meta_json', help='Path to an updated output meta json', required=True)
    args = parser.parse_args()

    parse(args.credentials, args.spreadsheet_key, args.meta_json, args.workflow_name, args.output_meta_json)


if __name__ == "__main__":
    main()