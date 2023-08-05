
import os
import copy
from apminsight.collector.connhandler import init_connection
from apminsight.instrumentation import init_instrumentation
from apminsight.metric.txn import Transaction
from apminsight.metric.tracker import Tracker
from apminsight.metric.dbtracker import DbTracker
from apminsight.metric.metricstore import Metricstore
from apminsight.config.configuration import Configuration
from apminsight.collector.insinfo import Instanceinfo
from apminsight.config.threshold import Threshold
from apminsight import context
from apminsight import constants
from apminsight.logger import agentlogger
from apminsight import util
from apminsight import agentfactory

def initalize(options={}):
    options['agentbasedir'] = util.check_and_create_base_dir()
    agentfactory.agent_instance = Agent(options)
    agent_instance = agentfactory.agent_instance
    if not agent_instance.get_config().is_configured_properly():
        raise RuntimeError('Configure license key in S247_LICENSE_KEY environment')

    init_instrumentation()
    init_connection()
    return agent_instance

class Agent:
    def __init__(self, info):
        self.config = Configuration(info)
        self.insinfo = Instanceinfo(info)
        self.threshold = Threshold()
        self.metricstore = Metricstore()
        self.txn_queue = []

    def push_to_queue(self, txn):
        self.txn_queue.append(txn)

    def get_txn_queue_for_metrics_processing(self):
        txn_list = copy.copy(self.txn_queue)
        self.txn_queue = []
        return txn_list

    def is_data_collection_allowed(self):
        cur_status = self.insinfo.get_status()
        if cur_status is None:
            return True

        if cur_status == constants.manage_agent:
            return True
        
        return False


    def check_and_create_txn(self, wsgi_environ, root_tracker_info):
        try:
            context.clear_cur_context()
            if not self.is_data_collection_allowed():
                agentlogger.info('data collection stopped')
                return

            if type(wsgi_environ) is not dict:
                return

            if type(root_tracker_info) is not dict:
                return

            uri = wsgi_environ.get('PATH_INFO', '')
            if not self.threshold.is_txn_allowed(uri):
                agentlogger.info(uri + ' txn skipped')
                return

            txn = Transaction(wsgi_environ, root_tracker_info)
            context.ser_cur_context(txn, txn.get_root_tracker())
            # handle cross app response
            return txn
        except Exception:
            agentlogger.exception("while creating txn obj")
        return Transaction(wsgi_environ, root_tracker_info)

    def check_and_create_tracker(self, tracker_info):
        track = None
        try:
            if type(tracker_info) is not dict:
                return None

            if context.is_txn_active() is not True:
                return None

            if 'parent' not in tracker_info:
                tracker_info['parent'] = context.get_cur_tracker()

            if constants.is_db_tracker in tracker_info:
                track = DbTracker(tracker_info)
            else:
                track = Tracker(tracker_info)

            context.set_cur_tracker(track)
        except:
            agentlogger.exception("While creating Tracker")
        
        return track

    
    def end_txn(self, txn, res=None, err=None):
        try:
            if txn is None:
                return

            if isinstance(txn, Transaction):
                txn.end_txn(res, err)
        except Exception:
            agentlogger.exception("tracking end txn")


    def end_tracker(self, tracker, err=None):
        if isinstance(tracker, Tracker) is not True:
            return

        txn=context.get_cur_txn()
        if isinstance(txn, Transaction):
            tracker.end_tracker(err)
            cur_txn = context.get_cur_txn()
            cur_txn.handle_end_tracker(tracker)


    def get_config(self):
        return self.config

    def get_threshold(self):
        return self.threshold

    def get_ins_info(self):
        return self.insinfo

    def get_metric_store(self):

        for txn in self.get_txn_queue_for_metrics_processing():
            self.metricstore.add_web_txn(txn)
        return self.metricstore
