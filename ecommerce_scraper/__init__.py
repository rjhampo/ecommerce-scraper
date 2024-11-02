import json
import logging

scraper_logger = logging.getLogger('__name__')

with open('user_agents.json', 'r') as input:
    USER_AGENTS = json.loads(input.read())