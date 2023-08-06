import functools
import logging
from django.http import HttpRequest
from django.db.models import Model
from django.db.models.query import QuerySet

def log_model_admin_action(
    action: str, 
    model: Model,
    logger: logging.Logger=None,
    loglevel: int=logging.INFO,
):
    """Decorator for logging which user performed which action on which 
    database object
    
    Args:
        action (str): What action is being performed
        model (Model): The Model in question
        loglevel (int, optional): Level to log action. Defaults to logging.INFO
        logger (logging.Logger, optional): Logger to log action to. If None, 
            gets the target module's logger. Defaults to None.
    """
    def log_model_admin_action_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            my_args = list(args)
            my_kwargs = dict(kwargs)

            if 'request' in my_kwargs:
                request = my_kwargs['request']
            else:
                # Remember for methods "self" is the first argument
                request = my_args[0]
            assert isinstance(request, HttpRequest)

            if 'obj' in my_kwargs:
                obj = my_kwargs['obj']
            else:
                obj = my_args[1]
            # Translate to stringable if queryset
            if isinstance(obj, QuerySet):
                obj = [str(o) for o in obj]

            if logger is None:
                my_logger = logging.getLogger(func.__module__)
            else:
                my_logger = logger

            my_logger.log(loglevel,
                f'{request.user} performing action "{action}" on '
                f'{model.__name__} "{obj}"'
            )
            return func(*args, **kwargs)
        return wrapper
    return log_model_admin_action_wrapper
            