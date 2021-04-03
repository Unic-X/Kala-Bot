from bs4 import BeautifulSoup

import requests

import time

import json

import aiohttp,asyncio

async def fetch(session, url,params=None):
    if params==None:
            async with session.get(url) as response:
                return await response.json()
    else:
        async with session.get(url,params=params) as response:
            return await response.json()

import functools

from discord.ext import commands

API_URL = "https://{}.fandom.com/api.php"

# misc wrapper function for time


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

# required to pass


def update_fandom(name: str):
    global API_URL
    if name != None:
        API_URL = API_URL.format(name)
    else:
        raise FandomExceptions("fandom name must not be empty")

# request maker for other functions
# @functools.lru_cache(maxsize=None,typed=False)
async def async_request(params):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session,
                               API_URL,params=params)
        return response
def _fandom_request(params):
    a = requests.get(API_URL, params=params)
    print(a.url)
    return(a.json())


class Page:

    def __init__(self, title=None, pageid: int = None, page_name=None):
        if title and pageid == None:
            raise Exception("Value must be not none")
        self.pageid = pageid
        self.title = title
        self.page_name = page_name
        self.PARSED_DATA = None

    @property
    def all_content(self):
        SEARCH_PARAMS = {
            "action": "parse",
            "format": "json",
            "pageid": self.pageid,
            "contentformat": 'application/json'
        }
        self.PARSED_DATA = asyncio.run(async_request(SEARCH_PARAMS))["parse"]["text"]["*"]
        content = BeautifulSoup(self.PARSED_DATA, "lxml")
        paragraphs = content.find_all(
            "p", limit=10
        )  # returns list of all <p> inside <div> class_=mw-parser-output we only need 1st(and 2nd if the content is less and even 3rd can be added if needed)

        for par in paragraphs:
            for tags in par.find_all(
                    "sup"
            ):  # deletes all the <sup> and returns a clean code without [] but has a time complexity of O(n^2)
                tags.decompose()

        counter = 0
        while len(
                paragraphs[counter].text
        ) == 1:  # the loop will check until the paragraph is not empty
            counter += 1

        text_content = paragraphs[counter].text

        if len(text_content) > 1024:
            text_content = text_content[:1021] + '..'

        for paragraph in paragraphs[
                counter +
                1:]:  # O(1) is more better than searching the whole list
            if len(text_content) > 1024 or len(text_content +
                                               paragraph.text) > 1024:
                break  # breaks the loop if more than 1024 char for Embed
            else:
                text_content += "\n" + paragraph.text
        return text_content

    #@property
    #def images(self):
    #    self.PARSED_DATA

class Search:
    def __init__(self):
        self.last_params = None

    @functools.lru_cache(maxsize=None, typed=False)
    def search(self, query: str, limit=5):
        SEARCH_PARAMS = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srprop": "",
            "srsearch": query,
            "srlimit": 5,
            "srinfo": ""
        }
        PAGE = {}
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
        

# page=Page(pageid=150086)
# print(page.all_content)


class FandomExceptions(Exception):
    pass


class Fandom(commands.Cog):
    @commands.command(aliases=["f", "fan"])
    @commands.cooldown(2, 3)
    async def fandom(self, ctx, name="darksouls", *, search_key: str):
        update_fandom(name=name)
        search_res = Search()
        first = tuple(search_res.search(search_key).keys())[1]
        page = Page(pageid=first)
        sex = page.all_content
        # await ctx.send(page)

    @fandom.error
    async def fandom_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a term to search for")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("It's so embarassing.. I can't find results")
        else:
            raise error


def setup(bot):
    bot.add_cog(Fandom())

update_fandom("darksouls")
page = Page(pageid=52657)
print(page.all_content)
