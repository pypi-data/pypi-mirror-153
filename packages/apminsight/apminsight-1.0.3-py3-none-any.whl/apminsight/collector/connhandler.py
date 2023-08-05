

"""
    initate connect request and schedule 1min task
"""

import platform
import requests
import json
import time
from apminsight.agentfactory import get_agent
from apminsight.constants import arh_connect, arh_data
from apminsight.logger import agentlogger
from apminsight.collector.reqhandler import send_req
from apminsight.collector.reshandler import handle_connect_response
from apminsight.collector.datahandler import process_collected_data


task_spawned = False
conn_payload = None

def init_connection():
    global task_spawned
    try:
        if task_spawned is True:
            return
        
        import threading
        t = threading.Thread(target=background_task, args=(), kwargs={})
        t.setDaemon(True)
        t.start()
        task_spawned = True

    except Exception :
        agentlogger.exception('Error while spawing thread')


def background_task():
    conn_success = False
    while(True):
        try:
            if conn_success is False:
                conn_success = send_connect()
            else:
                process_collected_data()
        except Exception:
            agentlogger.exception('apm task error')
        finally:
            #get_agent().get_metric_store().cleanup()
            time.sleep(60)


def send_connect():
    payload = getconn_payload() if conn_payload is None else conn_payload
    res_data = send_req(arh_connect, payload)
    return handle_connect_response(res_data)


def getconn_payload():
    global conn_payload
    config = get_agent().get_config()
    conn_payload = { 
            "agent_info" : { 
            "application.type": 'PYTHON', 
            "agent.version": '1.0.3', 
            "application.name": config.get_app_name(), 
            "port": config.get_app_port(), 
            "host.type": config.get_host_type(),
            "hostname": config.get_host_name(),
        }, "environment" : { 
            #"UserName": process.env.USER, 
            "OSVersion": platform.release(), 
            "MachineName": platform.node(), 
            'AgentInstallPath': config.get_installed_dir(), 
            "Python version": platform.python_version(), 
            "OSArch": platform.machine(), 
            "OS": platform.system(),
            "Python implementation" : platform.python_implementation()
        }
    }
    return conn_payload
