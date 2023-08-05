from apminsight import constants
from apminsight.util import is_non_empty_string
from apminsight.agentfactory import get_agent
from apminsight.logger import agentlogger

def extract_query(tracker, args=(), kwargs={}, return_value=None):
    threshold = get_agent().get_threshold()
    if threshold.is_sql_capture_enabled() is not True:
        return

    if isinstance(args, (list, tuple)) and len(args)>1:

        if is_non_empty_string(args[1]):
            tracker.set_info({ 'query' : args[1]})
        elif isinstance(args[1], (bytes, bytearray)):
            query = args[1].decode("utf-8")
            tracker.set_info({ 'query' : query})  
    try:
        (host,port)=str(return_value.response_future.coordinator_host).split(":")
        port=int(port)
        tracker.set_info({'host':host,'port':port})

    except:
        agentlogger.exception("Extracting the Host for CASSANDRA query")


module_info = {
    'cassandra.cluster' : [
        {   
            constants.class_str : 'Cluster',
            constants.method_str : 'connect',
            constants.component_str : constants.cassandra_comp,
        },

        {   
            constants.class_str : 'Cluster',
            constants.method_str : 'shutdown',
            constants.component_str : constants.cassandra_comp,
        },

        {
            constants.class_str : 'Session',
            constants.method_str : 'execute',
            constants.component_str : constants.cassandra_comp,
            constants.extract_info : extract_query,
            constants.is_db_tracker : True
        },

        ],
    }
