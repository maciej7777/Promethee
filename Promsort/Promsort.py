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

from decimal import *
from docopt import docopt
from common import comparisons_to_xmcda, create_messages_file, get_dirs, \
get_error_message, get_input_data, write_xmcda, assignments_to_xmcda, assignments_as_intervals_to_xmcda


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
categories_positive_flows, categories_negative_flows, cut_point):

  first_step_assignments = {}
  assignments = {}
  assigned_list = {}
  classes_flows = {}
  unassigned = []

  #prepare class lists
  assigned_list[profiles_categories[1]["classes"]["lower"]] = []
  classes_flows[profiles_categories[1]["classes"]["lower"]] = 0.0
  for category in profiles_categories:
    assigned_list[profiles_categories[category]["classes"]["upper"]] = []
    classes_flows[profiles_categories[category]["classes"]["upper"]] = 0.0
  
  #print (assigned_list)

  #first step
  for alternative in alternatives:
    marked = False
    for i in range (len(profiles_categories), 0, -1):
      if isPreffered(alternatives_positive_flows[alternative], alternatives_negative_flows[alternative], categories_positive_flows[profiles_categories[i]["id"]], categories_negative_flows[profiles_categories[i]["id"]]) is True:
        assignments[alternative] = profiles_categories[i]["classes"]["upper"]
        first_step_assignments[alternative] = (profiles_categories[i]["classes"]["upper"], profiles_categories[i]["classes"]["upper"])
        assigned_list[profiles_categories[i]["classes"]["upper"]].append(alternative)
        classes_flows[profiles_categories[i]["classes"]["upper"]] += alternatives_positive_flows[alternative] - alternatives_negative_flows[alternative]
        marked = True
        break
      elif isIndifferenced(alternatives_positive_flows[alternative], alternatives_negative_flows[alternative], categories_positive_flows[profiles_categories[i]["id"]], categories_negative_flows[profiles_categories[i]["id"]]) or isIncomparable(alternatives_positive_flows[alternative], alternatives_negative_flows[alternative], categories_positive_flows[profiles_categories[i]["id"]], categories_negative_flows[profiles_categories[i]["id"]]):
        #unassigned.append(alternative)
        first_step_assignments[alternative] = (profiles_categories[i]["classes"]["lower"], profiles_categories[i]["classes"]["upper"])
        marked = True
        unassigned.append(alternative)
        break
    if marked is False:
      assigned_list[profiles_categories[1]["classes"]["lower"]].append(alternative)
      classes_flows[profiles_categories[1]["classes"]["lower"]] += alternatives_positive_flows[alternative] - alternatives_negative_flows[alternative]
      assignments[alternative] = profiles_categories[1]["classes"]["lower"]
      first_step_assignments[alternative] = (profiles_categories[1]["classes"]["lower"], profiles_categories[1]["classes"]["lower"])

  #second step
  if ( len(first_step_assignments) != len(assignments) ):
    #for key, value in classes_flows.items():
      #if len(assigned_list[key]) != 0.0:
        #classes_flows[key] = value / len(assigned_list[key])

    print ('We need second step for:')
    print (unassigned)
    #print (classes_flows)

    for alternative_to_assign in unassigned:
      class_t = first_step_assignments[alternative_to_assign][0]
      class_t1 =  first_step_assignments[alternative_to_assign][1]
      
      len_t = len(assigned_list[class_t]) 
      len_t1 = len(assigned_list[class_t1]) 

      dk_positive = len_t * (alternatives_positive_flows[alternative_to_assign] - alternatives_negative_flows[alternative_to_assign]) - classes_flows[class_t]
      dk_negative = classes_flows[class_t1] - len_t1 * (alternatives_positive_flows[alternative_to_assign] - alternatives_negative_flows[alternative_to_assign])
      
      if (len_t > 0.0):
        dk1 = dk_positive/len_t
      else:
        dk1 = 0.0
      if (len_t1 > 0.0):
        dk2 = dk_negative/len_t1
      else:
        dk2 = 0.0

      dk = dk1 - dk2  

      if dk >= cut_point:
        assignments[alternative_to_assign] = class_t1
      else:
        assignments[alternative_to_assign] = class_t

      #temp_diff = abs(categories_flows[profiles_categories[i]["id"]] - alternatives_flows[alternative])
      #if temp_diff <= best_diff:
      #  assignments[alternative] = profiles_categories[i]["classes"]
  #print (assigned_list)
  print (assignments)
  print (first_step_assignments)
  print ('PROMSORT')
  #print (assignments, first_step_assignments)
  return (assignments, first_step_assignments)


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
      'cut_point'
    ]
    d = get_input_data(input_dir, filenames, params, comparison_with='boundary_profiles')
  
    output = sortPromsort(d.alternatives, d.categories, d.profiles_categories, d.alternatives_positive_flows, d.alternatives_negative_flows, d.categories_positive_flows, d.categories_negative_flows, d.cut_point)
    #print (output)
    #print (output[0])
    assignments = output[0]
    first_step_assignments = output[1]
    xmcda_assign = assignments_to_xmcda(assignments)
    xmcda_first_step_assign = assignments_as_intervals_to_xmcda(first_step_assignments)
    write_xmcda(xmcda_assign, os.path.join(output_dir, 'assignments.xml'))
    write_xmcda(xmcda_first_step_assign, os.path.join(output_dir, 'first_step_assignments.xml'))

  except Exception as err:
    err_msg = get_error_message(err)
    log_msg = traceback.format_exc()
    print(log_msg.strip())
    create_messages_file((err_msg, ), (log_msg, ), output_dir)
    return 1

if __name__ == '__main__':
  sys.exit(main())
