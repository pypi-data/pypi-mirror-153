import os
import sys
import json
import pprint
import pandas as pd
import pathlib
from lmfa.multifamily_analysis import MultiFamily
from lmfa.multifamily_analysis import MultiFamilyCharts


def run_analysis():
    mf = MultiFamily()
    argv = sys.argv[1:]
    config_filenames = [arg for arg in argv if arg.find('=') < 0]
    if len(config_filenames) == 0:
        config_filenames = ['multifamily_2.yaml', 'multifamily_4.yaml']

    config_outputs = []

    output_folder = os.path.join(
        pathlib.Path(__file__).resolve().parent, 'output')
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    for config_filename in config_filenames:
        config = mf.get_config_data(config_filename=config_filename)
        config = mf.add_missing_inputs(config=config)
        config = mf.get_metrics(config)

        config_outputs.append(config)
        print("=======================================")
        print("For Project A:")
        pprint.pprint(config['projects'][0])

        output_filename = os.path.join(
            pathlib.Path(__file__).resolve().parent, 'output',
            config_filename.split('.')[0] + '_out.yaml')
        with open(output_filename, 'w') as output_file:
            output_file.write(json.dumps(config, indent=4))

    mfc = MultiFamilyCharts()
    mfc.get_common_chart_data(config_outputs)
    mfc.get_all_charts(output_folder)


run_analysis()
'''
TODO 
a/ Increase LP incentive brackets further
b/ Add more breakdown to expenses, renovations, etc.
c/ Automate market research numbers using python tools
d/ Include Class A and B shares if amount is significantly high
e/ Implement sensitivity analysis for financial stress tests
'''