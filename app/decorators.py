'''
app.decorators
~~~~~~~~~~~~~~

Decorators of our own.
'''

from threading import Thread

def async_dec(f):
    '''To run a function in another thread.'''
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper