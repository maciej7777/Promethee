#!/usr/bin/env python

"""
Usage:
    FlowSortPrometheeISorting.py -i DIR -o DIR

Options:
    -i DIR     Specify input directory. It should contain the following files:
                   alternatives.xml
                   classes.xml
                   classes_profiles.xml
                   flows.xml
                   method_params.xml
    -o DIR     Specify output directory. Files generated as output:

    --version  Show version.
    -h --help  Show this screen.
"""

import os
import sys
import traceback

from docopt import docopt

from common import comparisons_to_xmcda, create_messages_file, get_dirs, \
get_error_message, get_input_data, write_xmcda, Vividict


__version__ = '0.0.1'



def sortWithLimitingProfiles():
  print ('a')


def sortWithCentralProfiles():
  print ('b')


def main():
  #try:
  args = docopt(__doc__, version=__version__)
  output_dir = None
  input_dir, output_dir = get_dirs(args)
  filenames = [
    # every tuple below == (filename, is_optional)
    ('alternatives.xml', False),
    ('classes.xml', False),
    ('method_parameters.xml', False),
    ('classes_profiles.xml', False),
    ('alternatives_values.xml', False),
  ]
  params = [
    'alternatives',
    'categories',
    'comparison_with',
    'categories_profiles',
    'alternatives_values',
  ]
  d = get_input_data(input_dir, filenames, params)
  
  print (d.alternatives_values)
  #except Exception as err:
  #  err_msg = get_error_message(err)
  #  log_msg = traceback.format_exc()
  #  print(log_msg.strip())
  #  create_messages_file((err_msg, ), (log_msg, ), output_dir)
  #  print ('blad')
  #  return 1



if __name__ == '__main__':
  sys.exit(main())
