
from apminsight.logger import agentlogger

agent_instance = None

def get_agent(config={}):
    global agent_instance
    if agent_instance is None:
        try:
            from apminsight.agent import initalize
            agent_instance = initalize(options=config)
            agentlogger.info('agent initialized')
        except Exception:
            agentlogger.exception('agent initialization')
    
    return agent_instance