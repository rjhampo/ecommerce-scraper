import json
import logging

logger = logging.getLogger()

with open('user_agents.json', 'r') as input:
    USER_AGENTS = json.loads(input.read())