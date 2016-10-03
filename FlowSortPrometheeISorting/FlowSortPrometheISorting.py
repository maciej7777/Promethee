#!/usr/bin/env python

"""
Usage:
    FlowSortPrometheeISorting.py -i DIR -o DIR

Options:
    -i DIR     Specify input directory. It should contain the following files:
                   alternatives.xml
                   classes.xml
                   classes_profiles.xml
                   positive_flows.xml
                   negative_flows.xml
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



def sortWithBoundaryProfiles(alternatives, categories, profiles_categories, alternatives_positive_flows, alternatives_negative_flows, categories_positive_flows, categories_negative_flows):
  
  alternatives_assigns = {}
  for alternative in alternatives:
    assign = {}
    assign["low"] = profiles_categories[1]["classes"]["lower"]
    assign["top"] = profiles_categories[1]["classes"]["lower"]
    for i in range (1,len(profiles_categories)+1):
      if alternatives_positive_flows[alternative] >= categories_positive_flows[profiles_categories[i]["id"]]:
        assign["top"] = profiles_categories[i]["classes"]["upper"]
      else:
        break
    
    for j in range (1,len(profiles_categories)+1):
      if alternatives_negative_flows[alternative] < categories_negative_flows[profiles_categories[j]["id"]]:
        assign["low"] = profiles_categories[j]["classes"]["upper"]
      else:
        break
    alternatives_assigns[alternative] = assign

  print (alternatives_assigns) 

  #print ('boundary')


def sortWithCentralProfiles(alternatives, categories, profiles_categories, alternatives_positive_flows, alternatives_negative_flows, categories_positive_flows, categories_negative_flows):

  alternatives_assigns = {}

  for alternative in alternatives:
    assign = {}
    assign["low"] = profiles_categories[1]["classes"]
    assign["top"] = profiles_categories[1]["classes"]

    for i in range (2,len(profiles_categories)+1):
      if alternatives_positive_flows[alternative] > (categories_positive_flows[profiles_categories[i]["id"]] + categories_positive_flows[profiles_categories[i-1]["id"]])/2:
        assign["top"] = profiles_categories[i]["classes"]
      else:
        break
    
    for j in range (2,len(profiles_categories)+1):
      if alternatives_negative_flows[alternative] <= (categories_negative_flows[profiles_categories[j]["id"]] + categories_negative_flows[profiles_categories[j-1]["id"]])/2:
        assign["low"] = profiles_categories[j]["classes"]
      else:
        break
    alternatives_assigns[alternative] = assign

  print (alternatives_assigns)
  print ('central')


def main():
  try:
    args = docopt(__doc__, version=__version__)
    output_dir = None
    input_dir, output_dir = get_dirs(args)
    filenames = [
      # every tuple below == (filename, is_optional)
      ('alternatives.xml', False),
      ('classes.xml', False),
      ('classes_profiles.xml', False),
      ('method_parameters.xml', False),
      ('positive_flows.xml', False),
      ('negative_flows.xml', False),
    ]
    params = [
      'alternatives',
      'categories',
      'comparison_with',
      'alternatives_positive_flows',
      'alternatives_negative_flows',
      'categories_positive_flows',
      'categories_negative_flows',
      'categories_rank',
      'profiles_categories'
    ]
    d = get_input_data(input_dir, filenames, params)
  
    if d.comparison_with == 'boundary_profiles':
      sortWithBoundaryProfiles(d.alternatives, d.categories, d.profiles_categories, d.alternatives_positive_flows, d.alternatives_negative_flows, d.categories_positive_flows, d.categories_negative_flows)
    elif d.comparison_with == 'central_profiles':
      sortWithCentralProfiles(d.alternatives, d.categories, d.profiles_categories, d.alternatives_positive_flows, d.alternatives_negative_flows, d.categories_positive_flows, d.categories_negative_flows)
    else:
      raise InputDataError("Wrong comparison type ('{}') specified."
                             .format(comparison_with))

  except Exception as err:
    err_msg = get_error_message(err)
    log_msg = traceback.format_exc()
    print(log_msg.strip())
    create_messages_file((err_msg, ), (log_msg, ), output_dir)
    return 1

if __name__ == '__main__':
  sys.exit(main())
