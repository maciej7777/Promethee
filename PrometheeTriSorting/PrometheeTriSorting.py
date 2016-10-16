#!/usr/bin/env python

"""
Usage:
    PrometheeTriSorting.py -i DIR -o DIR

Options:
    -i DIR     Specify input directory. It should contain the following files:
                   alternatives.xml
                   classes.xml
                   classes_profiles.xml
                   flows.xml
                   method_parameters.xml
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


def sortPrometheeTri(alternatives, categories, profiles_categories, alternatives_flows, categories_flows, assign_to_better_class):

  assignments = {}

  for alternative in alternatives:
    assignments[alternative] = profiles_categories[1]["classes"]
    best_diff = abs(categories_flows[profiles_categories[1]["id"]] - alternatives_flows[alternative])
    for i in range (2,len(profiles_categories)+1):
      temp_diff = abs(categories_flows[profiles_categories[i]["id"]] - alternatives_flows[alternative])
      if (temp_diff <= best_diff and assign_to_better_class is True) or (temp_diff < best_diff and assign_to_better_class is False):
        assignments[alternative] = profiles_categories[i]["classes"]      
  
  print (assignments)
  print ('PrometheeTri')
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
      ('flows.xml', False),
      ('method_parameters.xml', False),
    ]
    params = [
      'alternatives',
      'categories',
      'alternatives_flows',
      'categories_flows',
      'categories_rank',
      'profiles_categories',
      'assign_to_better_class'
    ]
    d = get_input_data(input_dir, filenames, params, comparison_with='central_profiles')
  
    assignments = sortPrometheeTri(d.alternatives, d.categories, d.profiles_categories, d.alternatives_flows, d.categories_flows, d.assign_to_better_class)
    xmcda_assign = assignments_to_xmcda(assignments)
    write_xmcda(xmcda_assign, os.path.join(output_dir, 'assignments.xml'))

  except Exception as err:
    err_msg = get_error_message(err)
    log_msg = traceback.format_exc()
    print(log_msg.strip())
    create_messages_file((err_msg, ), (log_msg, ), output_dir)
    return 1

if __name__ == '__main__':
  sys.exit(main())
