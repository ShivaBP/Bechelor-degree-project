#!/usr/bin/python3
#
# ./list-external-tools-for-course.py  course_id
# 
# outputs a list of external tools for the given course_id
#
# G. Q: Maguire Jr.
#
# 2016.07.17
#

import csv, requests, time
from pprint import pprint
import optparse
import sys

from lxml import html

import json
#############################
###### EDIT THIS STUFF ######
#############################

# styled based upon https://martin-thoma.com/configuration-files-in-python/
with open('config.json') as json_data_file:
       configuration = json.load(json_data_file)
       canvas = configuration['canvas']
       access_token= canvas["access_token"]
       # access_token=configuration["canvas"]["access_token"]
       #baseUrl = 'https://kth.instructure.com/api/v1/courses/' # changed to KTH domain
       baseUrl = 'https://%s/api/v1/courses/' % canvas.get('host', 'kth.instructure.com')
       header = {'Authorization' : 'Bearer ' + access_token}



#modules_csv = 'modules.csv' # name of file storing module names
log_file = 'log.txt' # a log file. it will log things


def write_to_log(message):
       with open(log_file, 'a') as log:
              log.write(message + "\n")
              pprint(message)


def details_of_external_tools_for_course(course_id, external_tool_id):
       # Use the Canvas API to GET the tool's detailed information
       # GET /api/v1/courses/:course_id/external_tools/:external_tool_id
       # GET /api/v1/accounts/:account_id/external_tools/:external_tool_id

       url = baseUrl + '%s/external_tools/%s' % (course_id, external_tool_id)
       if Verbose_Flag:
              print(url)
       payload={}
       r = requests.get(url, headers = header, data=payload)
       if r.status_code == requests.codes.ok:
              tool_response = r.json()  
              pprint(tool_response)
              return tool_response
       else:
              print("No details for tool_id {1} for course_id: {2}".format(external_tool_id, course_id))
              return False

def list_external_tools_for_course(course_id):
       list_of_all_tools=[]
       # Use the Canvas API to get the list of external tools for this course
       # GET /api/v1/courses/:course_id/external_tools
       # GET /api/v1/accounts/:account_id/external_tools
       # GET /api/v1/groups/:group_id/external_tools

       url = baseUrl + '%s/external_tools' % (course_id)
       if Verbose_Flag:
              print("url: " + url)

       r = requests.get(url, headers = header)
       if Verbose_Flag:
              write_to_log("result of getting list of external tools: " + r.text)
       if r.status_code == requests.codes.ok:
              tool_response=r.json()
       else:
              print("No external tools for course_id: {}".format(course_id))
              return False


       for t_response in tool_response:  
              list_of_all_tools.append(t_response)

       # the following is needed when the reponse has been paginated
       # i.e., when the response is split into pieces - each returning only some of the list of modules
       # see "Handling Pagination" - Discussion created by tyler.clair@usu.edu on Apr 27, 2015, https://community.canvaslms.com/thread/1500
       while r.links['current']['url'] != r.links['last']['url']:  
              r = requests.get(r.links['next']['url'], headers=header)  
              tool_response = r.json()  
              for t_response in tool_response:  
                     list_of_all_tools.append(t_response)

       for t in list_of_all_tools:
              print("about to prettyprint tool: {}".format(t['name']))
              pprint(t)


       return list_of_all_tools


def main():
       global Verbose_Flag

       parser = optparse.OptionParser()

       parser.add_option('-v', '--verbose',
                         dest="verbose",
                         default=False,
                         action="store_true",
                         help="Print lots of output to stdout"
       )

       options, remainder = parser.parse_args()

       Verbose_Flag=options.verbose
       if Verbose_Flag:
              print('ARGV      :', sys.argv[1:])
              print('VERBOSE   :', options.verbose)
              print('REMAINING :', remainder)

       # add time stamp to log file
       log_time = str(time.asctime(time.localtime(time.time())))
       if Verbose_Flag:
              write_to_log(log_time)   

       if (len(remainder) < 1):
              print("Inusffient arguments\n must provide course_id\n")
       else:
              course_id=remainder[0]
              output=list_external_tools_for_course(course_id)
              if (output):
                     if Verbose_Flag:
                            pprint(output)

       # add time stamp to log file
       log_time = str(time.asctime(time.localtime(time.time())))
       if Verbose_Flag:
              write_to_log(log_time)   
              write_to_log("\n--DONE--\n\n")

if __name__ == "__main__": main()

