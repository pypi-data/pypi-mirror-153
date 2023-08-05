

from django.apps import AppConfig
from django.conf import settings
from apminsight.agentfactory import get_agent
from .wrapper import instrument_middlewares


class ApminsightConfig(AppConfig):
    name = 'apminsight'

    def __init__(self, *args, **kwargs):
        super(ApminsightConfig, self).__init__(*args, **kwargs)
        self.client = get_agent({'appname' : ApminsightConfig.get_app_name()})

    def ready(self):
        instrument_middlewares()

    @staticmethod
    def get_app_name():
        appname = ''
        try:
            wsgi_app = settings.WSGI_APPLICATION
            appname = wsgi_app.split('.')[0]
        except Exception:
            pass 
    
        return appname
