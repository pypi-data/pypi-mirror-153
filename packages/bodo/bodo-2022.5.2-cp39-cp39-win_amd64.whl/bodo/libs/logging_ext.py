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
    tgjcc__jfbxa = context.get_python_api(builder)
    return tgjcc__jfbxa.unserialize(tgjcc__jfbxa.serialize_object(pyval))


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
        rtb__adcr = ', '.join('e{}'.format(lvu__rzi) for lvu__rzi in range(
            len(args)))
        if rtb__adcr:
            rtb__adcr += ', '
        ssv__xmw = ', '.join("{} = ''".format(ehdgn__bljz) for ehdgn__bljz in
            kws.keys())
        lsjmg__pxlxc = f'def format_stub(string, {rtb__adcr} {ssv__xmw}):\n'
        lsjmg__pxlxc += '    pass\n'
        zrs__lrq = {}
        exec(lsjmg__pxlxc, {}, zrs__lrq)
        tmzpy__qjjwz = zrs__lrq['format_stub']
        qrw__mtjck = numba.core.utils.pysignature(tmzpy__qjjwz)
        fyg__gkl = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, fyg__gkl).replace(pysig=qrw__mtjck)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for xbhia__kvq in ('logging.Logger', 'logging.RootLogger'):
        for kgcne__hnhmz in func_names:
            blke__ikay = f'@bound_function("{xbhia__kvq}.{kgcne__hnhmz}")\n'
            blke__ikay += (
                f'def resolve_{kgcne__hnhmz}(self, logger_typ, args, kws):\n')
            blke__ikay += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(blke__ikay)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for rvlol__ttv in logging_logger_unsupported_attrs:
        rsif__flqi = 'logging.Logger.' + rvlol__ttv
        overload_attribute(LoggingLoggerType, rvlol__ttv)(
            create_unsupported_overload(rsif__flqi))
    for ifops__auoz in logging_logger_unsupported_methods:
        rsif__flqi = 'logging.Logger.' + ifops__auoz
        overload_method(LoggingLoggerType, ifops__auoz)(
            create_unsupported_overload(rsif__flqi))


_install_logging_logger_unsupported_objects()
