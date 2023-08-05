
from apminsight.util import current_milli_time
from apminsight.metric.error import ErrorInfo
from apminsight.constants import max_trackers, max_exc_per_trace
class Tracker:

    def __init__(self, tracker_info={}):
        self.parent = tracker_info.get('parent', None)
        self.name = tracker_info.get('name', 'anonymous')
        self.component = tracker_info.get('component', '')
        self.start_time = current_milli_time()
        self.end_time = 0
        self.time = 0
        self.child_overhead = 0
        self.info = {}
        self.child_trackers = []
        self.error = None
        self.completed = False


    def end_tracker(self, err):
        # consider child overhead time 
        if err is not None:
            self.mark_error(err)
        self.end_time = current_milli_time()
        total_time = self.end_time - self.start_time
        self.time =  total_time - self.child_overhead
        if self.parent is not None:
            self.parent.update_child_overhead(self)
            self.parent.add_child_tracker(self)

        self.completed = True
        #self.print_details()

    def mark_error(self, err):
        if isinstance(err, Exception):
            if not hasattr(err, 'apminsight'):
                self.error = ErrorInfo(err)
                err.apminsight = True


    def update_child_overhead(self, child_trakcer):
        self.child_overhead += child_trakcer.get_rt()

    def add_child_tracker(self, child_trakcer):
        self.child_trackers.append(child_trakcer)

    def get_tracker_name(self):
        if 'opn' not in self.info:
            return self.name

        tracker_name = self.component +' - '+ self.info['opn']
        if 'host' in self.info and 'port' in self.info:
            host_info = self.info['host'] + ':' + str(self.info['port'])
            tracker_name += ' - ' + host_info
       
        return tracker_name

    def get_rt(self):
        return self.time

    def is_completed(self):
        return self.completed is True

    def get_component(self):
        return self.component

    def get_info(self):
        return self.info

    def set_info(self, info):
        self.info.update(info)
        
    def is_error(self):
        if self.error is not None:
            return True
        
        return False

    def get_error_name(self):
        if self.error is not None:
            return self.error.get_type()

        return ''

    def get_exc_info(self):
        return self.error


    def check_and_add_loginfo(self, trace_info={}):
        if 'loginfo' not in trace_info:
            trace_info['loginfo'] = []

        if self.is_error() and len(trace_info['loginfo'])<=max_exc_per_trace:
            log_info = {}
            excinfo = self.get_exc_info()
            log_info['time'] = excinfo.get_time()
            log_info['level'] = excinfo.get_level()
            log_info['str'] = excinfo.get_message()
            log_info['err_clz'] = excinfo.get_type()
            log_info['st'] = excinfo.get_error_stack_frames()
            trace_info['loginfo'].append(log_info)


    def get_tracker_info(self, trace_info={}):
        self.check_and_add_loginfo(trace_info)
        tracker_info = []
        tracker_info.append(self.start_time)
        tracker_info.append(self.get_tracker_name())
        tracker_info.append(self.component)
        tracker_info.append(self.time + self.child_overhead) # total
        tracker_info.append(self.time) # exclusive
        tracker_info.append(self.get_additional_info())
        tracker_info.append([])
        return tracker_info


    def get_additional_info(self):
        info = {}
        if self.is_error():
            info['stacktrace'] = self.error.get_error_stack_frames()

        return info

    def get_tracker_data_for_trace(self, trace_info):
        cur_tracker_info = self.get_tracker_info(trace_info)
        for eachchild in self.child_trackers:
            if trace_info['method_count'] > max_trackers:
                break

            child_tracker_data = eachchild.get_tracker_data_for_trace(trace_info)
            cur_tracker_info[6].append(child_tracker_data)
            trace_info['method_count'] += 1
            
        return cur_tracker_info

        
    def print_details(self):
        print('tracker_name', self.name)
        print('time', self.time)
        print('child_overhead', self.child_overhead)
        print('child_tracker_count', len(self.child_trackers))
        if self.parent is not None:
            print('parent:', self.parent.get_tracker_name())
    