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
get_error_message, get_input_data, write_xmcda, assignments_to_xmcda


__version__ = '0.0.1'


def isPreffered(action1_positive_flow, action1_negative_flow, action2_positive_flow, action2_negative_flow):
  if ((action1_positive_flow > action2_positive_flow and action1_negative_flow < action2_negative_flow) or
  (action1_positive_flow == action2_positive_flow and action1_negative_flow < action2_negative_flow) or 
  (action1_positive_flow > action2_positive_flow and action1_negative_flow == action2_negative_flow)):
    return True
  return False 

def isIndifferenced(action1_positive_flow, action1_negative_flow, action2_positive_flow, action2_negative_flow):
  if action1_positive_flow == action2_positive_flow and action1_negative_flow == action2_negative_flow:
    return True
  return False

def isIncomparable(action1_positive_flow, action1_negative_flow, action2_positive_flow, action2_negative_flow):
  if ((action1_positive_flow > action2_positive_flow and action1_negative_flow > action2_negative_flow) or 
  (action1_positive_flow < action2_positive_flow and action1_negative_flow < action2_negative_flow)):
    return True
  return False
    

def sortPromsort(alternatives, categories, profiles_categories, alternatives_positive_flows, alternatives_negative_flows, 
categories_positive_flows, categories_negative_flows):

  first_step_assignments = {}
  assignments = {}
  assigned = {}

  for alternative in alternatives:
    assigned = False
    for i in range (len(profiles_categories)+1, 1):
      if isPreffered(alternatives_positive_flows[alternative], alternatives_negative_flows[alternative], categories_positive_flows[profiles_categories[i]["id"]], categories_negative_flows[profiles_categories[i]["id"]]):
        assignments[alternative] = profiles_categories[i]["classes"]["upper"]
        first_step_assignments[alternative] = (profiles_categories[i]["classes"]["upper"], profiles_categories[i]["classes"]["upper"])
        assigned[profiles_categories[i]["classes"]["upper"]] = alternative #.append(
        assigned = True
        break
      elif isIndifferenced(alternatives_positive_flows[alternative], alternatives_negative_flows[alternative], categories_positive_flows[profiles_categories[i]["id"]], categories_negative_flows[profiles_categories[i]["id"]]) or isIncomparable(alternatives_positive_flows[alternative], alternatives_negative_flows[alternative], categories_positive_flows[profiles_categories[i]["id"]], categories_negative_flows[profiles_categories[i]["id"]]):
        #unassigned.append(alternative)
        first_step_assignments[alternative] = (profiles_categories[i]["classes"]["lower"], profiles_categories[i]["classes"]["upper"])
        assigned = True
    if assigned is False:
      assignments[alternative] = profiles_categories[1]["classes"]["lower"]
      #calculate second step here!
      #add assignment



      #temp_diff = abs(categories_flows[profiles_categories[i]["id"]] - alternatives_flows[alternative])
      #if temp_diff <= best_diff:
      #  assignments[alternative] = profiles_categories[i]["classes"]
  print (isIncomparable(1,2,2,3))
  print (assignments)
  print(first_step_assignments)
  print ('PROMSORT')
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
      ('positive_flows.xml', False),
      ('negative_flows.xml', False),
    ]
    params = [
      'alternatives',
      'categories',
      'alternatives_positive_flows',
      'alternatives_negative_flows',
      'categories_positive_flows',
      'categories_negative_flows',
      'categories_rank',
      'profiles_categories',
      #'cut_point'
    ]
    d = get_input_data(input_dir, filenames, params, comparison_with='boundary_profiles')
  
    output = sortPromsort(d.alternatives, d.categories, d.profiles_categories, d.alternatives_positive_flows, d.alternatives_negative_flows, d.categories_positive_flows, d.categories_negative_flows)
    #xmcda_assign = assignments_to_xmcda(assignments)
    #xmcda_assign = assignments_as_intervals_to_xmcda(assignments)
    #write_xmcda(xmcda_assign, os.path.join(output_dir, 'assignments.xml'))

  except Exception as err:
    err_msg = get_error_message(err)
    log_msg = traceback.format_exc()
    print(log_msg.strip())
    create_messages_file((err_msg, ), (log_msg, ), output_dir)
    return 1

if __name__ == '__main__':
  sys.exit(main())
