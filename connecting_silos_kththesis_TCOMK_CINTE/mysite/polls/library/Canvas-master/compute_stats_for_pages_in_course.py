#!/usr/bin/python3
#
# ./compute_stats_for_pages_in_course.py  course_id
# 
# it outputs a CSV file with the name statistics_for_course_xx.csv
# where xx is the course_id
#
# G. Q: Maguire Jr.
#
# 2016.07.12
# updated on 2016.07.15 to use the better way of getting the access token, baseURL, etc. from Rasmus Kaj's code.
#

import csv, requests, time
from pprint import pprint
import optparse
import sys

from lxml import html

import json
from textatistic import Textatistic
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


def compute_stats_for_pages_in_course(course_id):
       list_of_all_pages=[]
       page_stats=[]

       # Use the Canvas API to get the list of pages for this course
       #GET /api/v1/courses/:course_id/pages

       url = baseUrl + '%s/pages' % (course_id)
       if Verbose_Flag:
              print("url: " + url)

       r = requests.get(url, headers = header)
       if Verbose_Flag:
              write_to_log("result of getting pages: " + r.text)
       if r.status_code == requests.codes.ok:
              page_response=r.json()
       else:
              print("No pages for course_id: {}".format(course_id))
              return False


       for p_response in page_response:  
              list_of_all_pages.append(p_response)

       # the following is needed when the reponse has been paginated
       # i.e., when the response is split into pieces - each returning only some of the list of modules
       # see "Handling Pagination" - Discussion created by tyler.clair@usu.edu on Apr 27, 2015, https://community.canvaslms.com/thread/1500
       while r.links['current']['url'] != r.links['last']['url']:  
              r = requests.get(r.links['next']['url'], headers=header)  
              page_response = r.json()  
              for p_response in page_response:  
                     list_of_all_pages.append(p_response)

       for p in list_of_all_pages:
              print("{}".format(p["title"]))
              # Use the Canvas API to GET the page
              #GET /api/v1/courses/:course_id/pages/:url

              url = baseUrl + '%s/pages/%s' % (course_id, p["url"])
              if Verbose_Flag:
                     print(url)
              payload={}
              r = requests.get(url, headers = header, data=payload)
              if r.status_code == requests.codes.ok:
                     page_response = r.json()  
                     if Verbose_Flag:
                            print("body: {}".format(page_response["body"]))

                     document = html.document_fromstring(page_response["body"])
                     raw_text = document.text_content()
                     if Verbose_Flag:
                            print("raw_text: {}".format(raw_text))
              else:
                     print("No pages for course_id: {}".format(course_id))
                     return False

              # see http://www.erinhengel.com/software/textatistic/
              try:
                     fixed_title=page_response["title"].replace(',', '_comma_')
                     fixed_title=fixed_title.replace('"', '_doublequote_')
                     fixed_title=fixed_title.replace("'", '_singlequote_')
                     page_entry={"url": url, "page_name": fixed_title, "Textatistic.statistics": Textatistic(raw_text).dict()}
              except ZeroDivisionError:
                     # if there are zero sentences, then some of the scores cannot be computed
                     if Verbose_Flag:
                            print("no sentences in page {}".format(url))
                     continue
              except ValueError:
                     # if there is code on the page, for example a json structure, then the hyphenation package cannot handle this
                     if Verbose_Flag:
                            print("there is likely code on page {}".format(url))
                     continue

              if page_entry: 
                     page_stats.append(page_entry)

       return page_stats

def list_pages(course_id):
    list_of_all_pages=[]

    # Use the Canvas API to get the list of pages for this course
    #GET /api/v1/courses/:course_id/pages

    url = baseUrl + '%s/pages' % (course_id)
    if Verbose_Flag:
       print("url: " + url)

    r = requests.get(url, headers = header)
    if Verbose_Flag:
           write_to_log("result of getting pages: " + r.text)
    if r.status_code == requests.codes.ok:
       page_response=r.json()

    for p_response in page_response:  
       list_of_all_pages.append(p_response)

    # the following is needed when the reponse has been paginated
    # i.e., when the response is split into pieces - each returning only some of the list of modules
    # see "Handling Pagination" - Discussion created by tyler.clair@usu.edu on Apr 27, 2015, https://community.canvaslms.com/thread/1500
    while r.links['current']['url'] != r.links['last']['url']:  
       r = requests.get(r.links['next']['url'], headers=header)  
       page_response = r.json()  
       for p_response in page_response:  
           list_of_all_pages.append(p_response)

    for p in list_of_all_pages:
       print("{}".format(p["title"]))


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
              output=compute_stats_for_pages_in_course(course_id)
              if (output):
                     if Verbose_Flag:
                            print(output)
                     with open('statistics_for_course_'+course_id+'.csv', "wb") as writer:
                            spreadsheet_headings = ['url', 'page_name', 'sent_count', 'notdalechall_count', 'polysyblword_count', 'word_count', 'char_count', 'sybl_count', 'fleschkincaid_score', 'flesch_score', 'gunningfog_score', 'dalechall_score', 'smog_score']
                            for heading in spreadsheet_headings:
                                   encoded_output  =bytes((heading + ","), 'UTF-8')
                                   writer.write(encoded_output)
                            writer.write(bytes(u'\n', 'UTF-8'))

                            for item in output:
                                   out_row = [item['url'], item['page_name'], item["Textatistic.statistics"]['sent_count'], item["Textatistic.statistics"]['notdalechall_count'], item["Textatistic.statistics"]['polysyblword_count'], item["Textatistic.statistics"]['word_count'], item["Textatistic.statistics"]['char_count'], item["Textatistic.statistics"]['sybl_count'], item["Textatistic.statistics"]['fleschkincaid_score'], item["Textatistic.statistics"]['flesch_score'],  item["Textatistic.statistics"]['gunningfog_score'], item["Textatistic.statistics"]['dalechall_score'], item["Textatistic.statistics"]['smog_score'] ]
                                   for v in out_row:
                                          if type(v) is str:
                                                 encoded_output = bytes((v + ","), 'UTF-8')
                                          else: 
                                                 encoded_output = bytes((str(v) + ","), 'UTF-8')
                                          writer.write(encoded_output)
                                   writer.write(bytes(u'\n', 'UTF-8'))

                     writer.close()

       # add time stamp to log file
       log_time = str(time.asctime(time.localtime(time.time())))
       if Verbose_Flag:
              write_to_log(log_time)   
              write_to_log("\n--DONE--\n\n")

if __name__ == "__main__": main()

