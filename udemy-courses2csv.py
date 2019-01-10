#!/usr/bin/python
#
# dumps all udemy courses and attributes like title, students enrolled etc to CSV
#
# https://www.udemy.com/developers/affiliate/
#

import requests
import json
import csv
import time
import datetime


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
    
    while True:
        response = requests.get(url, headers=HEADERS, auth=(CLIENT_ID, CLIENT_SECRET), params={'page_size': page_size})

        if response.status_code == requests.codes.ok:
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
                time.sleep(30) 
    return ids



def get_course_details(course_id):

    max_retries = 5
    retries = 0
    url = api_url + course_id
    
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
            time.sleep(30)
    

                            
def write_csv(line):

    header = ['id', 'title', 'url', 'price', 'rating', 'created', 'last_update_date', 'num_reviews', 'num_subscribers', 'earnings', 'content_info']

    datestamp = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = 'udemy_courses_%s.csv' % (datestamp)

    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        print(line)
        writer.writerow(line)


                            
def main():

    for course_id in get_all_course_ids():
        write_csv(get_course_details(course_id))
                            


    
if __name__ == "__main__":
    main()
