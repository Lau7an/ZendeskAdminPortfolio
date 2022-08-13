import requests
import pandas as pd
import os

# Set the request parameters
base_url = 'https://YOURZENDESKDOMAIN.zendesk.com/'
articles_url = base_url + 'api/v2/help_center/en-us/articles.json?sort_by=updated_at&sort_order=asc'
sections_url = base_url + 'api/v2/help_center/en-us/sections.json?sort_by=updated_at&sort_order=asc'
cats_url = base_url + '/api/v2/help_center/en-us/categories.json?sort_by=updated_at&sort_order=asc'
info_exte = '.json'
page_exte = 'page='

ARTICLES_FILENAME = 'FAQ_Articles'
SECTIONS_FILENAME = 'FAQ_Sections'
CATS_FILENAME = 'FAQ_Categories'

# MUST BE AN ZENDESK ADMIN EMAIL WITH API ACCESS
user = os.getenv("ZENDESK_USERNAME")

# GET TOKEN FROM ZENDESK - ADMIN - API
pwd = os.getenv("ZENDESK_API_TOKEN")


def getcats(page, headers):
    for cat in page['categories']:
        df = pd.DataFrame.from_dict([cat])
        outputfile = CATS_FILENAME + str('1.csv')
        f = open(outputfile, 'a+')
        if headers:
            df.to_csv(f, mode='a', index=False)
        else:
            df.to_csv(f, mode='a', index=False, header=False)
        f.close()


def getarticles(page, headers):
    for article in page['articles']:
        df = pd.DataFrame.from_dict([article])
        outputfile = ARTICLES_FILENAME + str('1.csv')
        f = open(outputfile, 'a+')
        if headers:
            df.to_csv(f, mode='a', index=False)
        else:
            df.to_csv(f, mode='a', index=False, header=False)
        f.close()


def getsections(page, headers):
    for section in page['sections']:
        df = pd.DataFrame.from_dict([section])
        outputfile = SECTIONS_FILENAME + str('1.csv')
        f = open(outputfile, 'a+')
        if headers:
            df.to_csv(f, mode='a', index=False)
        else:
            df.to_csv(f, mode='a', index=False, header=False)
        f.close()


def getpage(u):
    pageinfo = {}
    page_response = requests.get(u, auth=(user, pwd))
    # Check for HTTP codes other than 200
    if page_response.status_code != 200:
        print('Status:', page_response.status_code, 'Problem with the request. Exiting.')
        # exit()
        return pageinfo, 0, 0
    else:
        page_data = page_response.json()
        next_page = page_data['next_page']
        return page_data, next_page

category_headers = True
while len(cats_url) > 0:
    newpage, cats_url = getpage(u=cats_url)
    getcats(newpage, category_headers)
    category_headers = False

section_headers = True
while len(sections_url) > 0:
    newpage, sections_url = getpage(u=sections_url)
    getsections(newpage, section_headers)
    section_headers = False

article_headers = True
while len(articles_url) > 0:
    newpage, articles_url = getpage(u=articles_url)
    getarticles(newpage, article_headers)
    article_headers = False
    

