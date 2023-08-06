import requests
import random
import urllib.parse as urlparse
from urllib.parse import parse_qs
from enum import Enum
from py_rule34 import __version__


__base_url__ = "https://rule34.xxx/"
__useragent__ = f"Mozilla/5.0 (compatible; rule34Py/{__version__})"

__headers__ = {
    "User-Agent": __useragent__
}

class API_URLS(str, Enum):
    SEARCH = f"{__base_url__}index.php?page=dapi&s=post&q=index&limit={{LIMIT}}&tags={{TAGS}}&json=1" # returns: JSON
    COMMENTS = f"{__base_url__}index.php?page=dapi&s=comment&q=index&post_id={{POST_ID}}" # returns: XML
    USER_FAVORITES = f"{__base_url__}index.php?page=favorites&s=view&id={{USR_ID}}" # returns: HTML
    GET_POST = f"{__base_url__}index.php?page=dapi&s=post&q=index&id={{POST_ID}}&json=1" # returns: JSON
    ICAME = f"{__base_url__}icameout.php" # returns: HTML
    RANDOM_POST = f"{__base_url__}index.php?page=post&s=random" #  returns: HTML

class rule34Py(Exception):
    def __init__(self):
        self._init = True

    def search(self, tags: list, page_id: int = None, limit: int = 100) -> dict:
        """Search for posts

        Args:
            tags (list): Search tags
            page_num (int, optional): Page ID
            limit (int, optional): Limit for Posts. Max 100.

        Returns:
            list: Posts result list

        Tags Cheatsheet: https://rule34.xxx/index.php?page=tags&s=list
        """

        # Check if "limit" is in between 1 and 100
        if limit > 100 or limit <= 0:
            raise Exception("invalid value for \"limit\"\n  valid valius: 1-100")
            return

        params = [
            ["TAGS", "+".join(tags)],
            ["LIMIT", str(limit)],
        ]
        # Add "page_id"
        if page_id != None:
            params.append(["PAGE_ID", str(page_id)])

        formatted_url = API_URLS.SEARCH.value.replace + ("&pid={{PAGE_ID}}" if page_id != None else "")
        formatted_url = self._parseUrlParams(formatted_url, params)

        res = req = requests.get(formatted_url, headers=__headers__)

        print("Length:" + str(len(res)))


    def _parseUrlParams(self, url: str, params: list):
        # Usage: _parseUrlParams("domain.com/index.php?v={{VERSION}}", [["VERSION", "1.10"]])
        retURL =  url

        for g in params:
            key = g[0]
            value = g[1]

            retURL = retURL.replace(key, value)

        return retURL
