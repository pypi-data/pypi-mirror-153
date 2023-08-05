
import os
import requests
import apminsight
import apminsight.constants as constants
from apminsight.logger import agentlogger
from apminsight.util import is_empty_string, is_non_empty_string
import platform

class Configuration:
    __license_key = None
    __app_name = None
    __app_port =  None
    __collector_host = None
    __collector_host = None
    __proxy_server_host = None
    __proxy_server_port = None
    __proxy_username = None
    __proxy_password = None
    __agent_version = None
    __installed_path = None
    __cloud_instance_id = None
    __is_cloud_instance = None
    __cloud_type = None

    def __init__(self, info):
        self.__license_key = get_license_key(info)
        self.__app_name = get_app_name(info)
        self.__app_port = get_app_port(info)
        self.__collector_host = get_collector_host(self.__license_key, info)
        self.__collector_port = get_collector_port(info)
        self.__proxy_server_host = get_proxy_server_host(info)
        self.__proxy_server_port = get_proxy_server_port(info)
        self.__proxy_username = get_proxy_auth_username(info)
        self.__proxy_password = get_proxy_auth_password(info)
        self.__agent_version = apminsight.version
        payload_config = os.getenv(constants.apm_print_payload, '')
        self.print_payload = False if is_empty_string(payload_config) else True
        self.__installed_path = apminsight.installed_path
        self.__is_cloud_instance, self.__cloud_type, self.__cloud_instance_id = get_cloud_details(self)
        
        
    def is_configured_properly(self):
        if is_empty_string(self.__license_key):
            return False
       
        return True

    def update_collector_info(self, collector_info):
        if collector_info is None:
            return

        try:
            self.__collector_host = collector_info.get('host', self.__collector_host)
            self.__collector_port = collector_info.get('port', self.__collector_port)
        except Exception:
            agentlogger.exception('while updating collector info')
            
    def get_license_key(self):
        return self.__license_key

    def get_app_name(self):
        return self.__app_name

    def get_app_port(self):
        return self.__app_port
        
    def get_collector_host(self):
        return self.__collector_host

    def get_collector_port(self):
        return self.__collector_port

    def get_agent_version(self):
        return self.__agent_version

    def get_installed_dir(self):
        return self.__installed_path

    def is_payload_print_enabled(self):
        return self.print_payload
    
    def get_is_cloud_instance(self):
        return self.__is_cloud_instance

    def get_cloud_instance_id(self):
        return self.__cloud_instance_id

    def get_cloud_type(self):
        return self.__cloud_type

    def get_host_name(self):
        if  self.__cloud_instance_id:
            return self.__cloud_instance_id
        return platform.node()
        
    def get_host_type(self):
        if self.__cloud_type:
            return self.__cloud_type
        return platform.system()

    def get_proxy_details(self):
        if not self.__proxy_server_host or not self.__proxy_server_port:
            return False
        if self.__proxy_username and self.__proxy_password :
            proxy_details = { 'http': 'http://' + self.__proxy_username + ':' + self.__proxy_password + '@' + self.__proxy_server_host + ':' + self.__proxy_server_port,
                    'https': 'http://' + self.__proxy_username + ':' + self.__proxy_password + '@' + self.__proxy_server_host + ':' + self.__proxy_server_port
                    }
        else:
            proxy_details = { 'http': 'http://' + self.__proxy_server_host + ':' + self.__proxy_server_port,
                    'https': 'http://' + self.__proxy_server_host + ':' + self.__proxy_server_port
                    }
        return proxy_details
        
def get_collector_host(license_key, info):

    host = os.getenv(constants.apm_collector_host, '')
    if is_non_empty_string(host):
        return host

    if 'apm_collector_host' in info and is_non_empty_string(info['apm_collector_host']):
        return info['apm_collector_host']

    if is_non_empty_string(license_key):
        if license_key.startswith('eu_'):
            return constants.eu_collector_host

        if license_key.startswith('cn_'):
            return constants.cn_collector_host

        if license_key.startswith('in_'):
            return constants.ind_collector_host

        if license_key.startswith('au_'):
            return constants.aus_collector_host 

        return constants.us_collector_host

    return ''


def get_license_key(info):
    license_key = os.getenv(constants.license_key_env)
    if is_non_empty_string(license_key):
        return license_key
    if 'license_key' in info and is_non_empty_string(info['license_key']):
        return info['license_key']

    return ''

def get_app_name(info):

    app_name = os.getenv(constants.apm_app_name)
    if is_non_empty_string(app_name) :
        return app_name
    if 'appname' in info and is_non_empty_string(info['appname']):
        return info['appname']

    return 'Python-Application'


def get_app_port(info):
    app_port = os.getenv(constants.apm_app_port)
    if is_non_empty_string(app_port) :
        return app_port
    if 'app_port' in info and is_non_empty_string(info['app_port']):
        return info['app_port']

    return '80'

def get_collector_port(info):
    collector_port = os.getenv(constants.apm_collector_port)
    if is_non_empty_string(collector_port):
        return collector_port
    if 'apm_collector_port' in info and is_non_empty_string(info['apm_collector_port']):
        return info['apm_collector_port']

    return constants.ssl_port

def get_proxy_server_host(info):
    proxy_server_host = os.getenv('PROXY_SERVER_HOST')
    if is_non_empty_string(proxy_server_host):
        return proxy_server_host
    if 'proxy_server_host' in info and is_non_empty_string(info['proxy_server_host']):
        return info['proxy_server_host']
    return None

def get_proxy_server_port(info):
    proxy_server_port = os.getenv('PROXY_SERVER_PORT')
    if is_non_empty_string(proxy_server_port):
        return proxy_server_port
    if 'proxy_server_port' in info and is_non_empty_string(info['proxy_server_port']):
        return info['proxy_server_port']
    return None

def get_proxy_auth_username(info):
    proxy_auth_username = os.getenv('PROXY_AUTH_USERNAME')
    if is_non_empty_string(proxy_auth_username):
        return proxy_auth_username
    if 'proxy_auth_username' in info and is_non_empty_string(info['proxy_auth_username']):
        return info['proxy_auth_username']
    return None

def get_proxy_auth_password(info):
    proxy_auth_password = os.getenv('PROXY_AUTH_PASSWORD')
    if is_non_empty_string(proxy_auth_password):
        return proxy_auth_password
    if 'proxy_auth_password' in info and is_non_empty_string(info['proxy_auth_password']):
        return info['proxy_auth_password']
    return None

def is_aws(self):
    try: 
        response = requests.get(constants.aws_url, timeout=0.005)
        # rep.encoding = 'utf8'
        if(response.status_code == 200 and  is_non_empty_string(response.text)):
            cloud_instance_id = response.text
            cloud_type = "AWS"
            return (True, cloud_type, cloud_instance_id)
    except Exception:
        agentlogger.info('AWS instance checking Failed')

    return False

def is_azure(self): 
    try:
        headers = {'content-type': 'application/json'}
        response = requests.get(constants.azure_url, headers=headers, timeout=0.005)
        if(response.status_code == 200 and is_non_empty_string(response.json().get('ID'))):
            cloud_instance_id = response.json().get('ID')
            cloud_type = "AZURE"
            return (True, cloud_type, cloud_instance_id)
    except Exception:
        agentlogger.info('Azure instance checking Failed')

    return False

def get_cloud_details(self):
    aws =  is_aws(self)
    azure = is_azure(self)
    if aws:
        return aws 
    elif azure:
        return azure
    return (False, None, None)
