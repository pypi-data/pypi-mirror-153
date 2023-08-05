
from apminsight.metric.tracker import Tracker
from apminsight.metric.dbmetric import DbMetric
from apminsight.agentfactory import get_agent
from apminsight.util import get_masked_query, is_empty_string
from apminsight.constants import db_opn_regex
import re

class DbTracker(Tracker):

    def __init__(self, tracker_info={}):
        super(DbTracker, self).__init__(tracker_info)

    def is_allowed_in_trace(self):
        return True

    def get_tracker_name(self):
        if 'opn' not in self.info:
            return self.name

        tracker_name = self.component + ' - '+ self.info['opn']
        if 'host' in self.info and 'port' in self.info:
            tracker_name += ' - ' + self.info['host'] +':' + str(self.info['port'])

        if self.is_error():
            """ include exception in tracker name"""
            pass
        
        return tracker_name


    def get_tracker_info(self, trace_info):
        info = self.extract_operartion_info()
        if 'opn' in info and 'obj' in info:
            opninfo = info['opn'] +'/' + info['obj']
            if opninfo not in trace_info['db_opn']:
                trace_info['db_opn'].append(opninfo)


        return super(DbTracker, self).get_tracker_info(trace_info)

    def get_additional_info(self):
        info = {}
        if self.is_error():
            info['stacktrace'] = self.error.get_error_stack_frames()

        if 'query' in self.info and is_empty_string(self.info['query']):
            return info
            
        if get_agent().get_threshold().is_sql_parameterized():
            info['query'] = get_masked_query(self.info['query'])
        else:
            info['query'] = self.info['query']

        return info

    
    def accumulate(self, name, metric):
        match = metric[name] if name in metric else DbMetric()
        match.accumulate(self)
        metric[name] = match


    def extract_operartion_info(self):
        if 'opn' in self.info and 'obj' in self.info:
            return self.info

        if 'query' in self.info:
            query = self.info['query']
            opn_name = query.split(' ')[0]
            if opn_name.lower() in db_opn_regex:
                regex = db_opn_regex[opn_name.lower()]
                matchobj = re.match(regex, query, re.IGNORECASE)
                if matchobj is not None:
                    self.info['opn'] = matchobj.group(1).lower()
                    self.info['obj'] = matchobj.group(2)
                    return self.info


        return {}




