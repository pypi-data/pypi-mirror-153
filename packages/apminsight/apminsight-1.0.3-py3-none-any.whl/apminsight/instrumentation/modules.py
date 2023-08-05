
from apminsight import constants
from apminsight.instrumentation.packages import django
from apminsight.instrumentation.packages import sqlite
from apminsight.instrumentation.packages import mysql
from apminsight.instrumentation.packages import flask
from apminsight.instrumentation.packages import redis
from apminsight.instrumentation.packages import jinja2
from apminsight.instrumentation.packages import pymemcache
from apminsight.instrumentation.packages import psycopg2
from apminsight.instrumentation.packages import cassandra
from apminsight.instrumentation.packages import memcache

modules_info = {}
modules_info.update(django.module_info)
modules_info.update(sqlite.module_info)
modules_info.update(mysql.module_info)
modules_info.update(flask.module_info)
modules_info.update(redis.module_info)
modules_info.update(jinja2.module_info)
modules_info.update(pymemcache.module_info)
modules_info.update(psycopg2.module_info)
modules_info.update(cassandra.module_info)
modules_info.update(memcache.module_info)
