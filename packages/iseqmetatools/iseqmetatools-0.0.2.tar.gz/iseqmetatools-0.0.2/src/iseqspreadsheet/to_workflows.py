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


def update_workflows_parameters(workflow, variant_name, meta_json):
    workflows_parameters = ['name', 'description', 'price', 'tag', 'longDescription', 'beta']

    for parameter in workflows_parameters:
        if workflow[parameter]:
            meta_json[f'{variant_name}{parameter}'] = workflow[parameter]

    # price always must be string type
    meta_json[f'{variant_name}price'] = str(meta_json[f'{variant_name}price'])

    spreadsheetutils.update_booleans(meta_json)


def update_meta_workflows(workflows, meta_json):
    for workflow in workflows:
        workflow_variant = workflow['workflow_variant'].split('_')
        variant_name = ""

        if len(workflow_variant) > 1:
            variant_name = f"{workflow_variant[1]}_"

        update_workflows_parameters(workflow, variant_name, meta_json)
    return meta_json


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


def update_meta(sheets, meta_json, workflow_name):
    workflows_worksheet = sheets.worksheet('Workflows')
    workflows = workflows_worksheet.get_all_records()

    workflows = filter_by_workflow(workflows, workflow_name)
    meta_json = update_meta_workflows(workflows, meta_json)

    return meta_json


def parse(credentials_json, spreadsheet_key, meta_json, workflow_name, output_meta_json):
    gc = gspread.service_account(filename=credentials_json)
    sheets = gc.open_by_key(spreadsheet_key)

    meta_json = spreadsheetutils.get_json_content(meta_json)
    meta_json = update_meta(sheets, meta_json, workflow_name)

    spreadsheetutils.save_to_json(output_meta_json, meta_json)


def main():
    parser = argparse.ArgumentParser(description="""Creates new meta.json with workflows parameters filled from google spreadsheet.
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