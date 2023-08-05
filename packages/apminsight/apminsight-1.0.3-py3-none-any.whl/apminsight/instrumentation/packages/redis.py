
from apminsight import constants
from apminsight.util import is_non_empty_string
from apminsight.metric.tracker import Tracker
from apminsight.context import get_cur_tracker
from apminsight.logger import agentlogger
def extract_info(tracker, args):
    if not isinstance(tracker, Tracker):
        return

    if tracker.get_component()!=constants.redis_comp:
        return

    if isinstance(args, (list, tuple)) and len(args)>1:
        if is_non_empty_string(args[1]):
            tracker.set_info({'opn' : args[1]})

        if hasattr(args[0], 'host') and hasattr(args[0], 'port'):
            host = getattr(args[0], 'host')
            port = getattr(args[0], 'port')
            tracker.set_info({'host' : host, 'port' : port})
        

def wrap_send_command(actual, module, method_info):
    def redis_wrapper(*args, **kwargs):
        try:
            tracker = get_cur_tracker()
            extract_info(tracker, args)
        except:
            agentlogger.exception("While extracting Redis call info")
        finally:
            return actual(*args, **kwargs)

    return redis_wrapper


module_info = {
    'redis.client' : [
        {
            constants.class_str : 'Redis',
            constants.method_str : 'execute_command',
            constants.component_str : constants.redis_comp
        }
    ],
    'redis.connection' : [
        {
            constants.class_str : 'Connection',
            constants.method_str : 'send_command',
            constants.wrapper_str : wrap_send_command
        }
    ]
}


