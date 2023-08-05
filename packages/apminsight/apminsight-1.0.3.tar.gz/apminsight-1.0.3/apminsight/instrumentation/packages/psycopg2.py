
from apminsight import constants
from apminsight.instrumentation.dbapi2 import ConnectionProxy

module_info = {
    'psycopg2' : [
        {
            constants.method_str : 'connect',
            constants.component_str : constants.postgres_comp,
            constants.wrapper_str : ConnectionProxy.instrument_conn,
            constants.default_host : constants.localhost,
            constants.default_port : 5432
        }
    ]
}

