
from apminsight import constants
from apminsight.util import is_non_empty_string

def extract_info(tracker, args=(), kwargs={}, return_value=None):
    print(args)
    print(kwargs)
    if isinstance(args, (list, tuple)) and len(args)>1:
        if is_non_empty_string(args[1]):
            tracker.set_info({'opn' : args[1]})
        elif isinstance(args[1], (bytes, bytearray)):
            operation = args[1].decode("utf-8")
            opn = operation.split()[0].upper()
            tracker.set_info({ 'opn' : opn})

        if hasattr(args[0], 'address'):
            address = args[0].address
            if isinstance(address, (list, tuple)) and len(address)==2:
                tracker.set_info({'host' : address[0], 'port' : address[1]})

module_info = {

    'memcache' : [
        {
            constants.class_str : '_Host',
            constants.method_str : 'send_cmd',
            constants.component_str : constants.memcache_comp,
            constants.extract_info : extract_info
        },
        {
            constants.class_str : '_Host',
            constants.method_str : 'send_cmds',
            constants.component_str : constants.memcache_comp,
            constants.extract_info : extract_info
        },   
    ]
}

