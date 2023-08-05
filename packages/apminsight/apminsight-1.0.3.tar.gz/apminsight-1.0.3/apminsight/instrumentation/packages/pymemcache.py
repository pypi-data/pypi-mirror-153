
from apminsight import constants
from apminsight.util import is_non_empty_string
from apminsight.metric.tracker import Tracker
from apminsight.context import get_cur_tracker

def extract_info(tracker, args=(), kwargs={}, return_value=None):
    if isinstance(args, (list, tuple)) and len(args)>1:
        if is_non_empty_string(args[1]):
            tracker.set_info({'opn' : args[1]})
        elif isinstance(args[1], (bytes, bytearray)):
            opn = args[1].decode("utf-8")
            tracker.set_info({ 'opn' : opn})

        if hasattr(args[0], 'server'):
            server = args[0].server
            if isinstance(server, (list, tuple)) and len(server)==2:
                tracker.set_info({'host' : server[0], 'port' : server[1]})


module_info = {
    'pymemcache.client.base' : [
        {
            constants.class_str : 'Client',
            constants.method_str : '_fetch_cmd',
            constants.component_str : constants.memcache_comp,
            constants.extract_info : extract_info
        },
        {
            constants.class_str : 'Client',
            constants.method_str : '_store_cmd',
            constants.component_str : constants.memcache_comp,
            constants.extract_info : extract_info
        },
        {
            constants.class_str : 'Client',
            constants.method_str : '_misc_cmd',
            constants.component_str : constants.memcache_comp,
            constants.extract_info : extract_info
        }
    ]
}


