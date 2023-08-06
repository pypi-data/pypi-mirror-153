#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gspread
import argparse
from collections import OrderedDict
from isequtils import spreadsheetutils


__version__ = "0.0.1"


def split_different_workflows(record):
    raw_workflows = record['workflow'].split()
    workflows_no_whitespaces = "".join(raw_workflows)
    return workflows_no_whitespaces.split(',')


def filter_by_workflow(unfiltered, workflow_name):
    filtered = list()
    for index, record in enumerate(unfiltered):
        workflows_list = split_different_workflows(record)

        for workflow in workflows_list:
            if workflow == workflow_name:
                record['workflow'] = workflow
                filtered.append(record)

    return filtered


def update_outputs_groups(outputs_groups, meta_json):
    groups = meta_json.get('groupOutputs', {})

    for group in outputs_groups:
        groups[group['readonly_name']] = {
            'name': group['name'],
            'description': group['description']
        }
    meta_json['groupsOutputs'] = groups

    return meta_json


def update_outputs(outputs, meta_json):
    parameters = ['type', 'copy', 'name', 'description', 'groupId', 'isForVariantsSelector']
    for output in outputs:
        output['type'] = output.pop('readonly_type')
        name = f"output_{output['readonly_name']}"
        for parameter in parameters:
            meta_json[name] = meta_json.get(name, {})
            if output[parameter]:
                meta_json[name][parameter] = output[parameter]
        spreadsheetutils.update_booleans(meta_json[name])
    return meta_json


def update_meta(sheets, meta_json, workflow_name):
    outputs_worksheet = sheets.worksheet('Outputs')
    outputs = outputs_worksheet.get_all_records()

    outputs_groups_worksheet = sheets.worksheet('Outputs groups')
    outputs_groups = outputs_groups_worksheet.get_all_records()

    outputs = filter_by_workflow(outputs, workflow_name)
    outputs_groups = filter_by_workflow(outputs_groups, workflow_name)

    meta_json = update_outputs_groups(outputs_groups, meta_json)
    meta_json = update_outputs(outputs, meta_json)

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
    parser = argparse.ArgumentParser(description="""Creates new meta.json with input parameters filled from google spreadsheet.
Further explanation can be found here: 
    https://workflows-dev-documentation.readthedocs.io/en/latest/Developer%20tools.html#parsing-google-spreadsheet-to-meta""")
    parser.add_argument('--credentials', help='Path to credentials file containing data necessary to get access', required=True)
    parser.add_argument('--spreadsheet_key', help='A key to the google spreadsheet', required=True)
    parser.add_argument('--meta_json', help='Path to meta json', required=True)
    parser.add_argument('--workflow_name', help='Workflow name', required=True)
    parser.add_argument('--output_meta_json', help='Path to an updated output meta json', required=True)
    args = parser.parse_args()

    parse(args.credentials, args.spreadsheet_key, args.meta_json, args.workflow_name, args.output_meta_json)


if __name__ == "__main__":
    main()