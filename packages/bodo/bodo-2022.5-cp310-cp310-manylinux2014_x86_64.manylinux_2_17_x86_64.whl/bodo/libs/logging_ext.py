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
    gtp__stt = context.get_python_api(builder)
    return gtp__stt.unserialize(gtp__stt.serialize_object(pyval))


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
        rbq__glq = ', '.join('e{}'.format(ohl__wwftt) for ohl__wwftt in
            range(len(args)))
        if rbq__glq:
            rbq__glq += ', '
        gbh__ekx = ', '.join("{} = ''".format(wpc__qfa) for wpc__qfa in kws
            .keys())
        ifzft__qosqd = f'def format_stub(string, {rbq__glq} {gbh__ekx}):\n'
        ifzft__qosqd += '    pass\n'
        izvc__bqfq = {}
        exec(ifzft__qosqd, {}, izvc__bqfq)
        zrvh__eoadl = izvc__bqfq['format_stub']
        msp__ijt = numba.core.utils.pysignature(zrvh__eoadl)
        taowd__ztjll = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, taowd__ztjll).replace(pysig=msp__ijt)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for hasc__weuv in ('logging.Logger', 'logging.RootLogger'):
        for rots__fxrg in func_names:
            kmfl__lsj = f'@bound_function("{hasc__weuv}.{rots__fxrg}")\n'
            kmfl__lsj += (
                f'def resolve_{rots__fxrg}(self, logger_typ, args, kws):\n')
            kmfl__lsj += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(kmfl__lsj)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for ugdnd__vgtgv in logging_logger_unsupported_attrs:
        vusu__dmzi = 'logging.Logger.' + ugdnd__vgtgv
        overload_attribute(LoggingLoggerType, ugdnd__vgtgv)(
            create_unsupported_overload(vusu__dmzi))
    for ruf__iahs in logging_logger_unsupported_methods:
        vusu__dmzi = 'logging.Logger.' + ruf__iahs
        overload_method(LoggingLoggerType, ruf__iahs)(
            create_unsupported_overload(vusu__dmzi))


_install_logging_logger_unsupported_objects()
