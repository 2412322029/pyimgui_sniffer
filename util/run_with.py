import threading

from util.logger import logger


def run_once(func):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return func(*args, **kwargs)

    wrapper.has_run = False
    return wrapper


def flag_controlled(enabled=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if enabled:
                return func(*args, **kwargs)
        return wrapper
    return decorator


def run_in_thread(func):
    def wrapper(*args, **kwargs):
        def target(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as e:
                logger.error(f"An error occurred in thread {threading.current_thread().name}: {str(e)}")
        thread = threading.Thread(target=target, args=args, kwargs=kwargs)
        thread.daemon = True  # 设置线程为守护线程
        thread.start()
    return wrapper
