
from apminsight import constants
from .wrapper import default_wrapper
from apminsight.util import is_non_empty_string
from apminsight.agentfactory import get_agent
from apminsight.logger import agentlogger
class CursorProxy():

    def __init__(self, cursor, conn):
        self._apm_wrap_cursor = cursor
        self._apm_wrap_conn = conn
        
    def __getattr__(self, key):
        if key in self.__dict__:
            return getattr(self, key)

        return getattr(self._apm_wrap_cursor, key)

    def __setattr__(self, key, value):
        if( key in ['_apm_wrap_cursor', '_apm_wrap_conn', 'execute', 'executemany']):
            self.__dict__[key] = value
        else:
            return setattr(self._apm_wrap_conn, key, value)

    def execute(self, *args, **kwargs):

        if hasattr(self._apm_wrap_cursor, 'execute'):
            actual = getattr(self._apm_wrap_cursor, 'execute')
            method_info = {
                constants.method_str : 'execute',
                constants.component_str : self._apm_wrap_conn._apm_comp_name,
                constants.extract_info : self._apm_extract_query,
                constants.is_db_tracker : True
            }
            wrapper = default_wrapper(actual, 'Cursor', method_info)
            return wrapper(*args, **kwargs)
        else:
            return self._apm_wrap_cursor.execute(*args, **kwargs)

    def executemany(self, *args, **kwargs):
        
        if hasattr(self._apm_wrap_cursor, 'executemany'):
            actual = getattr(self._apm_wrap_cursor, 'executemany')
            method_info = {
                constants.method_str : 'executemany',
                constants.component_str : self._apm_wrap_conn._apm_comp_name,
                constants.extract_info : self._apm_extract_query,
                constants.is_db_tracker : True
            }
            wrapper = default_wrapper(actual, 'Cursor', method_info)
            return wrapper(*args, **kwargs)
        else:
            return self._apm_wrap_cursor.executemany(*args, **kwargs)

    def _apm_extract_query(self, tracker, args=(), kwargs={}, return_value=None):
        tracker.set_info(self._apm_wrap_conn._apm_host_info)
        threshold = get_agent().get_threshold()
        if threshold.is_sql_capture_enabled() is not True:
            return

        if isinstance(args, (list, tuple)) and len(args)>0:
            if is_non_empty_string(args[0]):
                tracker.set_info({'query' : args[0]})


class ConnectionProxy():

    def __init__(self, conn, comp, host_info):
        self._apm_wrap_conn = conn
        self._apm_comp_name = comp
        self._apm_host_info = host_info

    def cursor(self, *args, **kwargs):
        real_cursor = self._apm_wrap_conn.cursor(*args, **kwargs)
        try:
            cur = CursorProxy(real_cursor, self)
            return cur
        except:
            agentlogger.exception("While creating CursorProxy object")
            return real_cursor

    #Special case for capturing SQLITE calls when executed with Connection object
    def execute(self, *args, **kwargs):

        if hasattr(self._apm_wrap_conn, 'execute'):
            actual = getattr(self._apm_wrap_conn, 'execute')
            method_info = {
                constants.method_str : 'execute',
                constants.component_str : self._apm_comp_name,
                constants.extract_info : self._apm_extract_query,
                constants.is_db_tracker : True
            }
            wrapper = default_wrapper(actual, 'Connection', method_info)
            return wrapper(*args, **kwargs)
        else:
            return self._apm_wrap_conn.execute(*args, **kwargs)


    def executemany(self, *args, **kwargs):

        if hasattr(self._apm_wrap_conn, 'executemany'):
            actual = getattr(self._apm_wrap_conn, 'executemany')
            method_info = {
                constants.method_str : 'executemany',
                constants.component_str : self._apm_comp_name,
                constants.extract_info : self._apm_extract_query,
                constants.is_db_tracker : True
            }
            wrapper = default_wrapper(actual, 'Connection', method_info)
            return wrapper(*args, **kwargs)
        else:
            return self._apm_wrap_conn.executemany(*args, **kwargs)
    
    def _apm_extract_query(self, tracker, args=(), kwargs={}, return_value=None):
        tracker.set_info(self._apm_host_info)
        threshold = get_agent().get_threshold()
        if threshold.is_sql_capture_enabled() is not True:
            return

        if isinstance(args, (list, tuple)) and len(args)>0:
            if is_non_empty_string(args[0]):
                tracker.set_info({'query' : args[0]})

    def __getattr__(self, key):
        if key in self.__dict__:
            return getattr(self, key)

        return getattr(self._apm_wrap_conn, key)

    def __setattr__(self, key, value):
        if( key in ['_apm_wrap_conn', '_apm_comp_name', '_apm_host_info']):
            self.__dict__[key] = value
        else:
            return setattr(self._apm_wrap_conn, key, value)
    
    @staticmethod
    def get_host_info(method_info, conn_kwargs):
        host_info = {}
        try:
            if constants.host in conn_kwargs:
                host_info[constants.host] = conn_kwargs[constants.host]
            elif constants.default_host in method_info:
                host_info[constants.host] = method_info[constants.default_host]

            if constants.port in conn_kwargs:
                host_info[constants.port] = conn_kwargs[constants.port]
            elif constants.default_port in method_info:
                host_info[constants.port] = method_info[constants.default_port]
        except:
            agentlogger.exception("While extracting host_info")
        return host_info

    @staticmethod
    def instrument_conn(original, module, method_info):
        def conn_wrapper(*args, **kwargs):
            conn = original(*args, **kwargs)
            if conn is not None:
                comp = method_info.get(constants.component_str, '')
                host_info = ConnectionProxy.get_host_info(method_info, kwargs)
                new_conn = ConnectionProxy(conn, comp, host_info)
                return new_conn

            return conn

        return conn_wrapper

