# hr/thread_locals.py
import threading

_thread_locals = threading.local()

def set_current_user_id(user_id):
    _thread_locals.user_id = user_id

def get_current_user_id():
    # return None kalau belum pernah di-set
    return getattr(_thread_locals, "user_id", None)