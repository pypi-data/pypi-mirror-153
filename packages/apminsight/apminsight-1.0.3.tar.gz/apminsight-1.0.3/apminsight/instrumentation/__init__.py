
from importlib import import_module
from apminsight.agentfactory import get_agent
from apminsight.logger import agentlogger
from apminsight.constants import class_str, method_str, wrapper_str, wrap_args
from apminsight.metric.txn import Transaction
from apminsight.instrumentation.modules import modules_info
from apminsight.metric.tracker import Tracker
from apminsight.context import is_no_active_txn, get_cur_tracker, set_cur_tracker
from apminsight.constants import component_str, extract_info
from apminsight.util import is_callable
from apminsight.instrumentation.util import create_tracker_info
from apminsight.instrumentation.wrapper import default_wrapper, args_wrapper

"""
act_load = builtins.__import__
cache = {}

def wrapper(*args, **kwargs):
    act_module = act_load(*args, **kwargs)
    check_and_instrument(args[0], act_module)
    return act_module

builtins.__import__ = wrapper"""

def check_and_instrument(module_name, act_module):
    if not module_name:
        return

    if hasattr(act_module, 'apminsight_instrumented'):
        return 

    if module_name in modules_info.keys():
        methods_info = modules_info.get(module_name)
        for each_method_info in methods_info:
            instrument_method(module_name, act_module, each_method_info)

        setattr(act_module, 'apminsight_instrumented', True)
        agentlogger.info(module_name+' instrumented')


def instrument_method(module_name, act_module, method_info):
    parent_ref = act_module
    class_name = ''

    if type(method_info) is not dict:
        return

    if class_str in method_info:
        class_name = method_info.get(class_str)
        if hasattr(act_module, class_name):
            parent_ref = getattr(act_module, class_name)
            module_name = module_name+'.'+class_name


    method_name = method_info.get(method_str, '')
    if hasattr(parent_ref, method_name):
        original = getattr(parent_ref, method_name)
        if not is_callable(original):
            return
        
        # use default wrapper if there is no wrapper attribute
        wrapper_factory = default_wrapper
        if wrap_args in method_info:
            wrapper_factory = args_wrapper
        elif wrapper_str in method_info:
            wrapper_factory = method_info.get(wrapper_str)
        
        wrapper = wrapper_factory(original, module_name, method_info)
        setattr(parent_ref,  method_name, wrapper)


initialized = False

def init_instrumentation():
    global initialized
    for each_mod in modules_info:
        try:
            act_module = import_module(each_mod)
            check_and_instrument(each_mod, act_module)
        except Exception:
            agentlogger.info(each_mod +' is not present')

    initialized = True

