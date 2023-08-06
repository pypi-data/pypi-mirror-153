"""
JIT support for Python's logging module
"""
import logging
import numba
from numba.core import types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import bound_function
from numba.core.typing.templates import AttributeTemplate, infer_getattr, signature
from numba.extending import NativeValue, box, models, overload_attribute, overload_method, register_model, typeof_impl, unbox
from bodo.utils.typing import create_unsupported_overload, gen_objmode_attr_overload


class LoggingLoggerType(types.Type):

    def __init__(self, is_root=False):
        self.is_root = is_root
        super(LoggingLoggerType, self).__init__(name=
            f'LoggingLoggerType(is_root={is_root})')


@typeof_impl.register(logging.RootLogger)
@typeof_impl.register(logging.Logger)
def typeof_logging(val, c):
    if isinstance(val, logging.RootLogger):
        return LoggingLoggerType(is_root=True)
    else:
        return LoggingLoggerType(is_root=False)


register_model(LoggingLoggerType)(models.OpaqueModel)


@box(LoggingLoggerType)
def box_logging_logger(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(LoggingLoggerType)
def unbox_logging_logger(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@lower_constant(LoggingLoggerType)
def lower_constant_logger(context, builder, ty, pyval):
    mkqqf__stw = context.get_python_api(builder)
    return mkqqf__stw.unserialize(mkqqf__stw.serialize_object(pyval))


gen_objmode_attr_overload(LoggingLoggerType, 'level', None, types.int64)
gen_objmode_attr_overload(LoggingLoggerType, 'name', None, 'unicode_type')
gen_objmode_attr_overload(LoggingLoggerType, 'propagate', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'disabled', None, types.boolean)
gen_objmode_attr_overload(LoggingLoggerType, 'parent', None,
    LoggingLoggerType())
gen_objmode_attr_overload(LoggingLoggerType, 'root', None,
    LoggingLoggerType(is_root=True))


@infer_getattr
class LoggingLoggerAttribute(AttributeTemplate):
    key = LoggingLoggerType

    def _resolve_helper(self, logger_typ, args, kws):
        kws = dict(kws)
        kag__eqst = ', '.join('e{}'.format(ynjs__wvsns) for ynjs__wvsns in
            range(len(args)))
        if kag__eqst:
            kag__eqst += ', '
        wux__eqk = ', '.join("{} = ''".format(kfkli__mwfh) for kfkli__mwfh in
            kws.keys())
        raog__cbm = f'def format_stub(string, {kag__eqst} {wux__eqk}):\n'
        raog__cbm += '    pass\n'
        bqn__csxl = {}
        exec(raog__cbm, {}, bqn__csxl)
        blz__wpfkk = bqn__csxl['format_stub']
        zkxpn__cgaa = numba.core.utils.pysignature(blz__wpfkk)
        bumyd__srvpn = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, bumyd__srvpn).replace(pysig=zkxpn__cgaa)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for yvw__cwup in ('logging.Logger', 'logging.RootLogger'):
        for iqq__nas in func_names:
            udz__qnfgt = f'@bound_function("{yvw__cwup}.{iqq__nas}")\n'
            udz__qnfgt += (
                f'def resolve_{iqq__nas}(self, logger_typ, args, kws):\n')
            udz__qnfgt += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(udz__qnfgt)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for dxw__zljp in logging_logger_unsupported_attrs:
        yaep__frv = 'logging.Logger.' + dxw__zljp
        overload_attribute(LoggingLoggerType, dxw__zljp)(
            create_unsupported_overload(yaep__frv))
    for grfrz__nprws in logging_logger_unsupported_methods:
        yaep__frv = 'logging.Logger.' + grfrz__nprws
        overload_method(LoggingLoggerType, grfrz__nprws)(
            create_unsupported_overload(yaep__frv))


_install_logging_logger_unsupported_objects()
