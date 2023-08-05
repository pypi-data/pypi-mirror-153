
from apminsight import constants
from apminsight.instrumentation.wrapper import wsgi_wrapper
from apminsight.context import get_cur_txn, is_no_active_txn
from apminsight.logger import agentlogger

def get_status_code(original, module, method_info):
    def wrapper(*args, **kwargs):
        if is_no_active_txn():
            return original(*args, **kwargs)
            
        res = original(*args, **kwargs)
        cur_txn = get_cur_txn()
        try:
            from werkzeug.exceptions import HTTPException
            if isinstance(res, HTTPException):
                cur_txn.status_code = int(res.code)
        except:
            agentlogger.exception('Exception occured while getting Status Code')
        return res
    return wrapper

module_info = {
    'flask' : [
        {
            constants.class_str : 'Flask',
            constants.method_str : 'wsgi_app',
            constants.wrapper_str : wsgi_wrapper,
            constants.component_str : constants.flask_comp
        },
        {
            constants.class_str : 'Flask',
            constants.method_str : 'add_url_rule',
            constants.component_str : constants.flask_comp,
            constants.wrap_args : 3
        },
        {
            constants.class_str : 'Flask',
            constants.method_str : 'handle_user_exception',
            constants.wrapper_str : get_status_code,
            constants.component_str : constants.flask_comp
        },
    ]
}


