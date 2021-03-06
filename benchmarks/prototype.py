import inspect
import typing as tp
from types import SimpleNamespace
from static_frame.core.container import ContainerOperand

PREFIX_TIME = 'asv_time_'

# NOTE: could not get setup_cache to work unless implemented explicitly on the derived class; could not populate it here dynamically either
# see https://github.com/airspeed-velocity/asv/issues/880

def apply_prototype(cls_prototype, container: tp.Type[ContainerOperand], group: str):
    def decorator(cls):

        # NOTE: approach to temporarily exercising only one module
        # if cls.__module__ != 'benchmarks.frame_exporter':
        #     return cls

        for name in dir(cls_prototype):
            if name.startswith(PREFIX_TIME):
                name_new = name.replace(PREFIX_TIME, 'time_')

                fixture = cls.FIXTURE.replace('|', '')
                name_pretty = f"{name.replace(PREFIX_TIME, '')}-{fixture}"

                # NOTE: must bind Prototype func name at func def time
                def func_new(self, ns: SimpleNamespace, name_prototype=name):
                    return getattr(cls_prototype, name_prototype)(self, ns)

                func_new.pretty_name = name_pretty
                func_new.pretty_source = inspect.getsource(getattr(cls_prototype, name))

                # replacing module with a normalized group name; function name must start with "time"
                group_label = f'{container.__name__}{group.replace(" ", "")}'
                func_new.benchmark_name = f'{group_label}.{cls.__name__}.{name_new}'

                setattr(cls, name_new, func_new)
        return cls
    return decorator
