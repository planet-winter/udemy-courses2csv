#!/usr/bin/python
#
# dumps all udemy courses and attributes like title, students enrolled etc to CSV
#
# https://www.udemy.com/developers/affiliate/
#

__author__ = 'Daniel Winter'


import requests
import json
import csv
import time
import datetime
import os
import sys

# insert your credentials here see https://www.udemy.com/user/edit-api-clients
CLIENT_ID = ''
CLIENT_SECRET = ''

HEADERS = {'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/45.0.2454.101 Safari/537.36'),
           'referer': 'https://www.udemy.com/'}

api_url = 'https://www.udemy.com/api-2.0/courses/'



def get_all_course_ids():
    
    page_size = 100
    max_retries = 5
    retries = 0
    ids = []
    url = api_url
    page = 1

    print('getting all course ids')
    while True:
        response = requests.get(url, headers=HEADERS, auth=(CLIENT_ID, CLIENT_SECRET), params={'page_size': page_size})

        if response.status_code == requests.codes.ok:
            print('grabbing page %s' % (page))
            page += 1
            response_json = response.json()
            for result in response_json['results']:
                ids.append(str(result['id'])) 
            if response_json['next']:
                next_page = response_json['next']
                url = next_page
            else:
                break
        else:
            if retries <= max_retries:
                retries += 1
                print('sleeping before next retry')
                time.sleep(30)
            else:
                print('ERROR: Failed to fetch course ids after %s retries' % (max_retries))
                sys.exit(1)
    return ids



def get_course_details(course_id):

    max_retries = 5
    retries = 0
    url = api_url + course_id

    while True:
        response = requests.get(url, headers=HEADERS, auth=(CLIENT_ID, CLIENT_SECRET), params={'fields[course]': '@all'})

        if response.status_code == requests.codes.ok:
            response_json = response.json()
            
            title = response_json['title']
            url = response_json['url']
            price = response_json['price']
            rating = str(response_json['rating'])
            created = response_json['created']
            last_update_date = response_json['last_update_date']
            num_reviews = str(response_json['num_reviews'])
            num_subscribers = str(response_json['num_subscribers'])
            earnings = response_json['earnings']
            content_info = response_json['content_info']
            
            return [course_id, title, url, price, rating, created, last_update_date, num_reviews, num_subscribers, earnings, content_info]
        
        else:
            if retries <= max_retries:
                retries += 1
                print('sleeping before next retry')
                time.sleep(30)
            else:
                print('ERROR: Failed to fetch course details after %s retries' % (max_retries))
                sys.exit(1)
                
                            
def write_csv(line):

    csv_header = ['id', 'title', 'url', 'price', 'rating', 'created', 'last_update_date', 'num_reviews', 'num_subscribers', 'earnings', 'content_info']

    datestamp = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = 'udemy_courses_%s.csv' % (datestamp)
    file_exists = os.path.isfile(filename)

    with open(filename, 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='"')
        if not file_exists:
            writer.writerow(csv_header)
        print(line)
        writer.writerow(line)


                            
def main():

    if CLIENT_ID == '' or CLIENT_SECRET == '':
        print('ERROR: You did not provide a CLIENT_ID or CLIENT_SECRET')
        sys.exit(1)
        
    for course_id in get_all_course_ids():
        write_csv(get_course_details(course_id))
                            


    
if __name__ == "__main__":
    main()

