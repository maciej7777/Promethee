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
get_error_message, get_input_data, write_xmcda, assignments_to_xmcda


__version__ = '0.0.1'



def sortWithBoundaryProfiles(alternatives, categories, profiles_categories, alternatives_flows, categories_flows):
  
  assignments = {}
  for alternative in alternatives:
    assignments[alternative] = profiles_categories[1]["classes"]["lower"]
    for i in range (1,len(profiles_categories)+1):
      if alternatives_flows[alternative] >= categories_flows[profiles_categories[i]["id"]]:
        assignments[alternative] = profiles_categories[i]["classes"]["upper"]
      else:
        break  
  print (assignments)
  print ('boundary')
  return assignments


def sortWithCentralProfiles(alternatives, categories, profiles_categories, alternatives_flows, categories_flows):

  assignments = {}

  for alternative in alternatives:
    assignments[alternative] = profiles_categories[1]["classes"]
    for i in range (2,len(profiles_categories)+1):
      if alternatives_flows[alternative] > (categories_flows[profiles_categories[i]["id"]] + categories_flows[profiles_categories[i-1]["id"]])/2:
        assignments[alternative] = profiles_categories[i]["classes"]
      else:
        break
  
  print (assignments)
  print ('central')
  return assignments


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
      ('flows.xml', False),
    ]
    params = [
      'alternatives',
      'categories',
      'comparison_with',
      'alternatives_flows',
      'categories_flows',
      'categories_rank',
      'profiles_categories'
    ]
    d = get_input_data(input_dir, filenames, params)
  
    if d.comparison_with == 'boundary_profiles':
      assignments = sortWithBoundaryProfiles(d.alternatives, d.categories, d.profiles_categories, d.alternatives_flows, d.categories_flows)
      xmcda_assign = assignments_to_xmcda(assignments)
    elif d.comparison_with == 'central_profiles':
      assignments = sortWithCentralProfiles(d.alternatives, d.categories, d.profiles_categories, d.alternatives_flows, d.categories_flows)
      xmcda_assign = assignments_to_xmcda(assignments)
    else:
      raise InputDataError("Wrong comparison type ('{}') specified."
                             .format(comparison_with))

    write_xmcda(xmcda_assign, os.path.join(output_dir, 'assignments.xml'))

  except Exception as err:
    err_msg = get_error_message(err)
    log_msg = traceback.format_exc()
    print(log_msg.strip())
    create_messages_file((err_msg, ), (log_msg, ), output_dir)
    return 1

if __name__ == '__main__':
  sys.exit(main())
