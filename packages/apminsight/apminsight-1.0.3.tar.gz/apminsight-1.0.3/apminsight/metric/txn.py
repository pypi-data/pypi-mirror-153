
from apminsight.util import current_milli_time
from apminsight.metric.tracker import Tracker
from apminsight.metric.dbtracker import DbTracker
from apminsight.agentfactory import get_agent
from apminsight.util import is_empty_string
from apminsight.metric.component import Component
from apminsight.constants import webtxn_prefix

class Transaction:

    def __init__(self, wsgi_environ={}, root_tracker_info={}):
        self.url = wsgi_environ.get('PATH_INFO', '')
        self.query = wsgi_environ.get('QUERY_STRING', '')
        self.method = wsgi_environ.get('REQUEST_METHOD', '')
        self.root_trakcer = Tracker(root_tracker_info)
        self.start_time = current_milli_time()
        self.end_time = None
        self.rt = 0
        self.completed = False
        self.status_code = None
        self.exceptions_info = {}
        self.exceptions_count = 0
        self.external_comps = {}
        self.internal_comps = {}
        self.extcall_count = 0
        self.db_calls = []

    def end_txn(self, res=None, err=None):
        agent = get_agent()
        if agent.is_data_collection_allowed() is False:
            return

        self.root_trakcer.end_tracker(err)
        self.handle_end_tracker(self.root_trakcer)
        self.end_time = current_milli_time()
        if res is not None and hasattr(res, 'status_code'):
            self.status_code = res.status_code
        if err is not None:
            self.status_code = 500 
        self.rt = self.end_time-self.start_time
        self.completed = True
        agent.push_to_queue(self)
        #agent.get_metric_store().add_web_txn(self)


    def handle_end_tracker(self, tracker):
        self.aggregate_component(tracker)
        self.check_and_add_db_call(tracker)
        self.check_and_add_error(tracker)


    def aggregate_component(self, tracker):
        if is_empty_string(tracker.get_component()):
            return

        component = Component(tracker)
        if component.is_ext():
            component.aggregate_to_global(self.external_comps)
            self.extcall_count += component.get_count() + component.get_error_count()
        else:
            component.aggregate_to_global(self.internal_comps)
         

    def check_and_add_db_call(self, db_tracker):
        if isinstance(db_tracker, DbTracker):
            self.db_calls.append(db_tracker)


    def check_and_add_error(self, tracker):
        if not tracker.is_error():
            return

        err_name = tracker.get_error_name()
        if is_empty_string(err_name):
            return

        err_count = self.exceptions_info.get(err_name, 0)
        self.exceptions_info[err_name] = err_count+1
        self.exceptions_count += 1 


    @staticmethod
    def comp_details_for_trace(allcompinfo):
        comp_details = {'success' : {}, 'fail' : {}}
        for eachcomp in allcompinfo.keys():
            compinfo = allcompinfo[eachcomp]
            if compinfo.get_name() in comp_details['success'].keys():
                comp_details['success'][compinfo.get_name()] += compinfo.get_count()
                comp_details['fail'][compinfo.get_name()] += compinfo.get_error_count()
            else:
                comp_details['success'][compinfo.get_name()] = compinfo.get_count()
                comp_details['fail'][compinfo.get_name()] = compinfo.get_error_count()


        return comp_details


    def get_trace_info(self):
        trace_info = {}
        trace_info['t_name'] = webtxn_prefix + self.get_url()
        trace_info['http_method_name'] = self.get_method()
        trace_info['s_time'] = self.get_start_time()
        trace_info['r_time'] = self.get_rt()
        trace_info['http_query_str'] = self.get_query_param()
        trace_info['trace_reason'] = 4
        trace_info['db_opn'] = []
        trace_info['loginfo'] = []
        trace_info['method_count'] = 1
        #trace_info['dt_count'] = 0
        trace_info['ext_components'] = Transaction.comp_details_for_trace(self.external_comps)
        trace_info['int_components'] = Transaction.comp_details_for_trace(self.internal_comps)
        if self.get_status_code() is not None:
            trace_info['httpcode'] = self.get_status_code()

        return trace_info
        

    def get_trace_data(self):
        trace_info = self.get_trace_info()
        trace_data = self.root_trakcer.get_tracker_data_for_trace(trace_info)
        return [trace_info, trace_data]


    def get_root_tracker(self):
        return self.root_trakcer

    def get_url(self):
        return self.url

    def get_method(self):
        return self.method

    def get_rt(self):
        return self.rt 

    def get_start_time(self):
        return self.start_time

    def get_query_param(self):
        return self.query

    def get_exceptions_info(self):
        return self.exceptions_info

    def get_exceptions_count(self):
        return self.exceptions_count

    def get_status_code(self):
        return self.status_code

    def clear_dbcalls(self):
        self.db_calls = []

    def get_dbcalls(self):
        return self.db_calls

    def get_internal_comps(self):
        return self.internal_comps

    def get_external_comps(self):
        return self.external_comps

    def get_ext_call_count(self):
        return self.extcall_count

    def is_completed(self):
        return self.completed

    def is_error_txn(self):
        if type(self.status_code) is int:
            if self.status_code >= 400:
                return True
        
        return self.root_trakcer.is_error()


    