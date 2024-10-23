from random import choice
from scraper import USER_AGENTS

def _get_user_agent():
    user_agent = choice(USER_AGENTS)
    return user_agent
    

def _get_lazada_page_headers(user_agent):
    return {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "dnt": "1",
        "priority": "u=1, i",
        "referer": "https://www.lazada.com.ph/",
        "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": _get_user_agent()
    }