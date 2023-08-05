
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
            host= args[0].connection.host
            port= args[0].connection.port
            tracker.set_info({'host':host,'port':port})
        except:
            agentlogger.exception("Extracting host info from MYSQL query")

module_info = {
    'pymysql' : [
        {
            constants.method_str : 'connect',
            constants.component_str : constants.mysql_comp,
        }
    ],
    'pymysql.cursors' : [
        {
            constants.class_str : 'Cursor',
            constants.method_str : 'execute',
            constants.component_str : constants.mysql_comp,
            constants.extract_info : extract_query,
            constants.is_db_tracker : True
        }
    ],
    'MySQLdb.connections' : [
        {
            constants.class_str : 'Connection',
            constants.method_str : 'query',
            constants.component_str : constants.mysql_comp,
            constants.extract_info : extract_query,
            constants.is_db_tracker : True
        }
    ]
}