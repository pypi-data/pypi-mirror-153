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
    vxw__ervfe = context.get_python_api(builder)
    return vxw__ervfe.unserialize(vxw__ervfe.serialize_object(pyval))


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
        mln__tsxzn = ', '.join('e{}'.format(gngz__inlmu) for gngz__inlmu in
            range(len(args)))
        if mln__tsxzn:
            mln__tsxzn += ', '
        har__fqjj = ', '.join("{} = ''".format(xfl__jfjf) for xfl__jfjf in
            kws.keys())
        clya__ksssn = f'def format_stub(string, {mln__tsxzn} {har__fqjj}):\n'
        clya__ksssn += '    pass\n'
        wlbx__vdscz = {}
        exec(clya__ksssn, {}, wlbx__vdscz)
        ycm__blqqu = wlbx__vdscz['format_stub']
        nitqk__mqt = numba.core.utils.pysignature(ycm__blqqu)
        shc__zos = (logger_typ,) + args + tuple(kws.values())
        return signature(logger_typ, shc__zos).replace(pysig=nitqk__mqt)
    func_names = ('debug', 'warning', 'warn', 'info', 'error', 'exception',
        'critical', 'log', 'setLevel')
    for fmspv__fripl in ('logging.Logger', 'logging.RootLogger'):
        for iqgjs__orhd in func_names:
            puil__xdyv = f'@bound_function("{fmspv__fripl}.{iqgjs__orhd}")\n'
            puil__xdyv += (
                f'def resolve_{iqgjs__orhd}(self, logger_typ, args, kws):\n')
            puil__xdyv += (
                '    return self._resolve_helper(logger_typ, args, kws)')
            exec(puil__xdyv)


logging_logger_unsupported_attrs = {'filters', 'handlers', 'manager'}
logging_logger_unsupported_methods = {'addHandler', 'callHandlers', 'fatal',
    'findCaller', 'getChild', 'getEffectiveLevel', 'handle', 'hasHandlers',
    'isEnabledFor', 'makeRecord', 'removeHandler'}


def _install_logging_logger_unsupported_objects():
    for cqm__lez in logging_logger_unsupported_attrs:
        rksy__xnufe = 'logging.Logger.' + cqm__lez
        overload_attribute(LoggingLoggerType, cqm__lez)(
            create_unsupported_overload(rksy__xnufe))
    for qyezl__zptj in logging_logger_unsupported_methods:
        rksy__xnufe = 'logging.Logger.' + qyezl__zptj
        overload_method(LoggingLoggerType, qyezl__zptj)(
            create_unsupported_overload(rksy__xnufe))


_install_logging_logger_unsupported_objects()
