
class_str = 'class'
method_str = 'method'
wrapper_str = 'wrapper'
component_str = 'component'
wrap_args = 'wrap_args'
extract_info = 'extract_info'
host = 'host'
port = 'port'
default_host = 'default_host'
default_port = 'default_port'
is_db_tracker = 'is_db_tracker'
localhost = 'localhost'

arh_connect = '/arh/connect'
arh_data = '/arh/data'
arh_trace = '/arh/trace'
webtxn_prefix = 'transaction/http/'

aws_url = 'http://169.254.169.254/latest/meta-data/instance-id'
azure_url = 'http://169.254.169.254/metadata/v1/InstanceInfo'

instanceinfo = 'instance-info'
responsecode = 'response-code'
instanceid = 'instanceid'
collectorinfo = 'collector-info'

manage_agent = 911
license_expired = 701
license_instance_exceeded = 702
instance_add_failed = 703
delete_agent = 900
invalid_agent = 901
unmanage_agent = 910
agent_license_updated = 915
agent_config_updated = 920
shutdown = 0


info_file_name = 'apminsight.json'
base_dir = 'apminsightdata'
logs_dir = 'logs'
log_name = 'apminsight-agent-log.txt'
agent_logger_name = 'apminsight-agent'
log_format = '%(asctime)s %(levelname)s %(message)s'


license_key_env = 'S247_LICENSE_KEY'
apm_app_name = 'APM_APP_NAME'
apm_app_port = 'APM_APP_PORT'
apm_print_payload = 'APM_PRINT_PAYLOAD'
apm_collector_host = 'APM_COLLECTOR_HOST'
apm_collector_port = 'APM_COLLECTOR_PORT'
apm_proxy = 'APM_PROXY'
apm_logs_dir = 'APM_LOGS_DIR'
ssl_port = '443'

us_collector_host = 'plusinsight.site24x7.com' 
eu_collector_host = 'plusinsight.site24x7.eu' 
cn_collector_host = 'plusinsight.site24x7.cn'
ind_collector_host = 'plusinsight.site24x7.in'
aus_collector_host = 'plusinsight.site24x7.net.au'

custom_config_info = 'custom_config_info'
agent_specific_info = 'agent_specific_info'
log_level = 'apminsight.log.level'
apdexth = 'apdex.threshold'
sql_capture = 'sql.capture.enabled'
sql_parametrize = 'transaction.trace.sql.parametrize'
last_modified_time = 'last.modified.time'
trace_threshold = 'transaction.trace.threshold'
trace_enabled = 'transaction.trace.enabled'
sql_stracktrace = 'transaction.trace.sql.stacktrace.threshold'
web_txn_sampling_factor = 'transaction.tracking.request.interval'
auto_upgrade = 'autoupgrade.enabled'
txn_skip_listening = 'transaction.skip.listening'
txn_tracker_drop_th = 'webtransaction.tracker.drop.threshold'
txn_trace_ext_count_th = 'webtransaction.trace.external.components.count.threshold'


bgtxn_tracking_enabled = 'bgtransaction.tracking.enabled'
bgtxn_trace_enabled = 'bgtransaction.trace.enabled'
bgtxn_traceth = 'bgtransaction.trace.threshold'
bgtxn_sampling_factor = 'bgtransaction.tracking.request.interval'

apdex_metric = 'metricstore.metric.bucket.size'
db_metric = 'metricstore.dbmetric.bucket'
bg_metric = 'metricstore.bgmetric.bucket.size'
trace_size = 'transaction.tracestore.size'

select_query_matcher = r'\s*(select)\s+.*from\s+(\S+)?.*'
insert_query_matcher = r'\s*(insert)\s+into\s+(\S+)?[(]?.*'
update_query_matcher = r'\s*(update)\s+(\S+)?.*'
delete_query_matcher = r'\s*(delete)\s+.*from\s+(\S+)?.*'
create_query_matcher = r'\s*(create)\s+(?:table|procedure|database|keyspace)\s+(?:if not exists\s+)?(\S+)?[(]?.*'
drop_query_matcher = r'\s*(drop)\s+(?:table|procedure|database|keyspace)\s+(?:if exists\s+)?(\S+)?.*'
alter_query_matcher = r'\s*(alter)\s+(?:table|procedure|database|keyspace)\s+(\S+)?.*'
call_sp_matcher = r'\s*(call)\s+([`\w]+)[\s()]*.*'
exec_sp_matcher = r'\s*(exec)\s+([`\w]+)[\s()]*.*'
show_query_matcher = r'\s*(show)\s+(\w+)(\s+)?.*'


db_opn_regex = {
    'select' : select_query_matcher,
    'insert' : insert_query_matcher,
    'update' : update_query_matcher,
    'delete' : delete_query_matcher,
    'create' : create_query_matcher, 
    'drop' : drop_query_matcher, 
    'alter' : alter_query_matcher,
    'show' : show_query_matcher,
    'call' : call_sp_matcher,
    'exec' : exec_sp_matcher
}



max_trackers = 1000
max_exc_per_trace = 20
django_comp = 'DJANGO'
flask_comp = 'FLASK'
sqlite_comp = 'SQLITE'
postgres_comp = 'POSTGRES'
mysql_comp = 'MYSQL'
redis_comp = 'REDIS'
memcache_comp = 'MEMCACHED'
middleware = 'MIDDLEWARE'
template = 'TEMPLATE'
jinja_comp = 'JINJA'
cassandra_comp = 'CASSANDRA'

int_components = [ django_comp, flask_comp, middleware, jinja_comp ]
ext_components = [ mysql_comp, sqlite_comp, redis_comp, memcache_comp, postgres_comp, cassandra_comp ]