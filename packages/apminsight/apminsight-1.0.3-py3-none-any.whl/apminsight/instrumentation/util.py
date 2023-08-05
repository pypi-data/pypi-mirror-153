
from apminsight.constants import method_str, component_str, is_db_tracker
from apminsight.metric.tracker import Tracker
from apminsight.logger import agentlogger

def create_tracker_info(module, method_info, parent_tracker=None):
    tracker_info = None
    try:
        tracker_name = module + '.' + method_info[method_str]
        tracker_info = { 'name' : tracker_name }
        if isinstance(parent_tracker, Tracker):
            tracker_info['parent'] = parent_tracker

        if component_str in method_info:
            tracker_info[component_str] = method_info[component_str]

        if is_db_tracker in method_info:
            tracker_info[is_db_tracker] = True
    except Exception:
        agentlogger.exception("while creating tracker info")
    finally:
        return tracker_info