
import os
from .agentfactory import get_agent
import json

name = "apminsight"

version = "1.0.3"

installed_path = os.path.dirname(__file__)

config = {}
current_directory = os.getcwd()
apm_info_file_path = os.path.join(current_directory, 'apminsight_info.json')

if os.path.exists(apm_info_file_path):
    with open(apm_info_file_path,'r') as fh:
        config=json.load(fh)

agent = get_agent(config)