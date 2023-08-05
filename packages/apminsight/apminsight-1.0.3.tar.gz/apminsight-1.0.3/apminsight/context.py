

import threading

thread_local = threading.local()

def set_cur_txn(txn):
    setattr(thread_local, 'apm_cur_txn', txn)


def set_cur_tracker(tracker):
    setattr(thread_local, 'apm_cur_tracker', tracker)

def ser_cur_context(txn, tracker):
    set_cur_txn(txn)
    set_cur_tracker(tracker)

def clear_cur_context():
    ser_cur_context(None, None)

def get_cur_txn():
    return getattr(thread_local, 'apm_cur_txn', None)
    
def get_cur_tracker():
    return getattr(thread_local, 'apm_cur_tracker', None)

def is_txn_active():
    txn = get_cur_txn()
    return txn is not None

def is_no_active_txn():
    txn = get_cur_txn()
    return txn is None

