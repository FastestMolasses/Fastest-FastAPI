def load_contextvar_class():
    from contextvars import ContextVar
    return ContextVar


ContextVar = load_contextvar_class()
