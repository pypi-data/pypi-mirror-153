
from apminsight import constants
from apminsight.instrumentation.dbapi2 import ConnectionProxy

module_info = {
    'sqlite3' : [
        {
            constants.method_str : 'connect',
            constants.component_str : constants.sqlite_comp,
            constants.wrapper_str : ConnectionProxy.instrument_conn
        }
    ],
    'sqlite3.dbapi2' : [
        {
            constants.method_str : 'connect',
            constants.component_str : constants.sqlite_comp,
            constants.wrapper_str : ConnectionProxy.instrument_conn
        }
    ]
}
