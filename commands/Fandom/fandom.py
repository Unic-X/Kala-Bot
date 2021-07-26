from bs4 import BeautifulSoup

import requests

import time

import json

import wikipedia

import html2text


API_URL = "https://{}.fandom.com/api.php"


def timeit(fn):
    def wrapper(*args, **kwargs):
        av_list = []
        for i in range(10):
            start = time.time()
            fn(*args, **kwargs)
            total = time.time()-start
            av_list.append(total)
        print("average time", sum(av_list)/len(av_list))

    return wrapper

def update_fandom(name: str=None):
    global API_URL
    if name != None:
        API_URL = API_URL.format(name.lower())
    else:
        API_URL="http://en.wikipedia.org/w/api.php"


def _fandom_request(params):

    '''Synchronous request(Blocking)'''
    a = requests.get(API_URL, params=params)
    print(a.url)
    return(a.json())


class Page:

    def __init__(self, pageid: int = None, page_name=None):
        '''Assigning the title or the pageid'''
        self.pageid = pageid

        #page_name ie the Query String ie https://hello.fandom.com/api.php
        self.page_name = page_name
    
    def __repr__(self):
        return f"Page(Id:{self.pageid},Title:{self.title})"

    @property
    def all_content(self):
        SEARCH_PARAMS = {
            "action": "parse",
            "format": "json",
            "pageid": self.pageid,
            "contentformat": 'application/json'
        }
        raw_response = _fandom_request(SEARCH_PARAMS)["parse"]["text"]["*"]
        
        '''THE PROBLEM STARTS FROM HERE PARSING IS NOT DONE CORRECTLY HERE MORE EFFICIENT WORK TO DO'''
        '''⛔⛔⛔⛔⛔⛔⛔⛔❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌❌⛔⛔⛔⛔⛔⛔⛔⛔'''
        
        '''content=BeautifulSoup(raw_response,"lxml")
        raw_response="\n".join((i.text for i in content.findAll(name=)))
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_images=True
        text_maker.ignore_emphasis=True
        text_maker.ignore_tables=True



        text = text_maker.handle(raw_response)
        return text'''


        content = BeautifulSoup(raw_response, "lxml")
        paragraphs = content.find_all(
            "p", limit=10,
        )  # returns list of all <p> inside <div> class_=mw-parser-output we only need 1st(and 2nd if the content is less and even 3rd can be added if needed)
        for par in paragraphs:
            for tags in par.find_all("sup"):
                tags.decompose()
        main_content=""
        for para in paragraphs:
            
            para_text=para.text
            if len(para_text) <= 1:
                pass
            else:
                main_content+="\n"+para_text
                #for paragraph in paragraphs[
                #        
                #        1:]:  # O(1) is more better than searching the whole list
                #    if len(text_content) > 2048 or len(text_content +
                #                                    paragraph.text) > 2048:
                #        break  # breaks the loop if more than 1024 char for Embed
                #    else:
                #        text_content += "\n" + paragraph.text
        return main_content
    @property
    def images(self):
       self.PARSED_DATA

class Search:
    def __init__(self):
        self.last_params = None
    def __str__(self):
        return f"Last Parameters were: {self.last_params}"
    def __eq__(self, value):
        return self.last_params==value.last_params
    def show(self):
        print(self.last_params)

    def search(self, query: str, limit=5):
        SEARCH_PARAMS = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srprop": "",
            "srsearch": query,
            "srlimit": limit,
            "srinfo": ""
        }
        PAGE={}
        self.last_params=SEARCH_PARAMS
        list_of_page = _fandom_request(SEARCH_PARAMS)["query"]["search"]
        for i in list_of_page:
            PAGE[i["pageid"]] = i["title"]
        return PAGE
        

    def open_search(self, item: str):
        SEARCH_PARAMS = {
            "action": "opensearch",
            "format": "json",
            "search": item,
        }
        '''Returns Array with index 0 as the search item, index 1 as the search result'''
        fandom_content = _fandom_request(SEARCH_PARAMS)
        result = dict(zip(fandom_content[1], fandom_content[3]))
        return result

class FandomExceptions(Exception):
    pass
# page=Page(pageid=150086)
# print(page.all_content)
if __name__ =="__main__":
    sex=input("Enter Name")
    print(type(sex))
    update_fandom()
    item=Search()
    time1=time.time()
    a=list(item.search(sex).keys())[0]
    page=Page(pageid=a)
    print(page.all_content)
    print(time.time()-time1)


#print(wikipedia.page(pageid=2616).content)


