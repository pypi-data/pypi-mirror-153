"""
File that contains some IO related helpers.
"""
import pyarrow
from mpi4py import MPI
from numba.core import types
from numba.core.imputils import lower_constant
from numba.extending import NativeValue, models, register_model, typeof_impl, unbox
import bodo


class PyArrowTableSchemaType(types.Opaque):

    def __init__(self):
        super(PyArrowTableSchemaType, self).__init__(name=
            'PyArrowTableSchemaType')


pyarrow_table_schema_type = PyArrowTableSchemaType()
types.pyarrow_table_schema_type = pyarrow_table_schema_type
register_model(PyArrowTableSchemaType)(models.OpaqueModel)


@unbox(PyArrowTableSchemaType)
def unbox_pyarrow_table_schema_type(typ, val, c):
    c.pyapi.incref(val)
    return NativeValue(val)


@typeof_impl.register(pyarrow.lib.Schema)
def typeof_pyarrow_table_schema(val, c):
    return pyarrow_table_schema_type


@lower_constant(PyArrowTableSchemaType)
def lower_pyarrow_table_schema(context, builder, ty, pyval):
    ykkho__qmges = context.get_python_api(builder)
    return ykkho__qmges.unserialize(ykkho__qmges.serialize_object(pyval))


def is_nullable(typ):
    return bodo.utils.utils.is_array_typ(typ, False) and (not isinstance(
        typ, types.Array) and not isinstance(typ, bodo.DatetimeArrayType))


def pa_schema_unify_reduction(schema_a, schema_b, unused):
    return pyarrow.unify_schemas([schema_a, schema_b])


pa_schema_unify_mpi_op = MPI.Op.Create(pa_schema_unify_reduction, commute=True)
