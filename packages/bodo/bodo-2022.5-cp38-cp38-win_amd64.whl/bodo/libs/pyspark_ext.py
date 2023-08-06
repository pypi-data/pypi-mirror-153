"""
Support for PySpark APIs in Bodo JIT functions
"""
from collections import namedtuple
import numba
import numba.cpython.tupleobj
import numpy as np
import pyspark
import pyspark.sql.functions as F
from numba.core import cgutils, ir_utils, types
from numba.core.imputils import lower_constant
from numba.core.typing.templates import AbstractTemplate, AttributeTemplate, infer_global, signature
from numba.extending import NativeValue, box, infer_getattr, intrinsic, lower_builtin, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model, typeof_impl, unbox
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType, check_runtime_cols_unsupported
from bodo.utils.typing import BodoError, check_unsupported_args, dtype_to_array_type, get_overload_const_list, get_overload_const_str, is_overload_constant_list, is_overload_constant_str, is_overload_true
ANON_SENTINEL = 'bodo_field_'


class SparkSessionType(types.Opaque):

    def __init__(self):
        super(SparkSessionType, self).__init__(name='SparkSessionType')


spark_session_type = SparkSessionType()
register_model(SparkSessionType)(models.OpaqueModel)


class SparkSessionBuilderType(types.Opaque):

    def __init__(self):
        super(SparkSessionBuilderType, self).__init__(name=
            'SparkSessionBuilderType')


spark_session_builder_type = SparkSessionBuilderType()
register_model(SparkSessionBuilderType)(models.OpaqueModel)


@intrinsic
def init_session(typingctx=None):

    def codegen(context, builder, signature, args):
        return context.get_constant_null(spark_session_type)
    return spark_session_type(), codegen


@intrinsic
def init_session_builder(typingctx=None):

    def codegen(context, builder, signature, args):
        return context.get_constant_null(spark_session_builder_type)
    return spark_session_builder_type(), codegen


@overload_method(SparkSessionBuilderType, 'appName', no_unliteral=True)
def overload_appName(A, s):
    return lambda A, s: A


@overload_method(SparkSessionBuilderType, 'getOrCreate', inline='always',
    no_unliteral=True)
def overload_getOrCreate(A):
    return lambda A: bodo.libs.pyspark_ext.init_session()


@typeof_impl.register(pyspark.sql.session.SparkSession)
def typeof_session(val, c):
    return spark_session_type


@box(SparkSessionType)
def box_spark_session(typ, val, c):
    yyfnn__jrkb = c.context.insert_const_string(c.builder.module, 'pyspark')
    rnlq__quy = c.pyapi.import_module_noblock(yyfnn__jrkb)
    klh__dyn = c.pyapi.object_getattr_string(rnlq__quy, 'sql')
    fddx__tpaej = c.pyapi.object_getattr_string(klh__dyn, 'SparkSession')
    wog__rbcn = c.pyapi.object_getattr_string(fddx__tpaej, 'builder')
    ysh__phrm = c.pyapi.call_method(wog__rbcn, 'getOrCreate', ())
    c.pyapi.decref(rnlq__quy)
    c.pyapi.decref(klh__dyn)
    c.pyapi.decref(fddx__tpaej)
    c.pyapi.decref(wog__rbcn)
    return ysh__phrm


@unbox(SparkSessionType)
def unbox_spark_session(typ, obj, c):
    return NativeValue(c.context.get_constant_null(spark_session_type))


@lower_constant(SparkSessionType)
def lower_constant_spark_session(context, builder, ty, pyval):
    return context.get_constant_null(spark_session_type)


class RowType(types.BaseNamedTuple):

    def __init__(self, types, fields):
        self.types = tuple(types)
        self.count = len(self.types)
        self.fields = tuple(fields)
        self.instance_class = namedtuple('Row', fields)
        sxq__rqbo = 'Row({})'.format(', '.join(f'{wiq__lmxvy}:{lpeq__gnsv}' for
            wiq__lmxvy, lpeq__gnsv in zip(self.fields, self.types)))
        super(RowType, self).__init__(sxq__rqbo)

    @property
    def key(self):
        return self.fields, self.types

    def __getitem__(self, i):
        return self.types[i]

    def __len__(self):
        return len(self.types)

    def __iter__(self):
        return iter(self.types)


@register_model(RowType)
class RowModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jvq__yjxsn = [(wiq__lmxvy, lpeq__gnsv) for wiq__lmxvy, lpeq__gnsv in
            zip(fe_type.fields, fe_type.types)]
        super(RowModel, self).__init__(dmm, fe_type, jvq__yjxsn)


@typeof_impl.register(pyspark.sql.types.Row)
def typeof_row(val, c):
    fields = val.__fields__ if hasattr(val, '__fields__') else tuple(
        f'{ANON_SENTINEL}{i}' for i in range(len(val)))
    return RowType(tuple(numba.typeof(bfsl__ugg) for bfsl__ugg in val), fields)


@box(RowType)
def box_row(typ, val, c):
    bsr__gpyth = c.pyapi.unserialize(c.pyapi.serialize_object(pyspark.sql.
        types.Row))
    if all(wiq__lmxvy.startswith(ANON_SENTINEL) for wiq__lmxvy in typ.fields):
        tyj__aqcs = [c.box(lpeq__gnsv, c.builder.extract_value(val, i)) for
            i, lpeq__gnsv in enumerate(typ.types)]
        hdlw__hid = c.pyapi.call_function_objargs(bsr__gpyth, tyj__aqcs)
        for obj in tyj__aqcs:
            c.pyapi.decref(obj)
        c.pyapi.decref(bsr__gpyth)
        return hdlw__hid
    args = c.pyapi.tuple_pack([])
    tyj__aqcs = []
    gbub__aoxj = []
    for i, lpeq__gnsv in enumerate(typ.types):
        acg__rqylx = c.builder.extract_value(val, i)
        obj = c.box(lpeq__gnsv, acg__rqylx)
        gbub__aoxj.append((typ.fields[i], obj))
        tyj__aqcs.append(obj)
    kws = c.pyapi.dict_pack(gbub__aoxj)
    hdlw__hid = c.pyapi.call(bsr__gpyth, args, kws)
    for obj in tyj__aqcs:
        c.pyapi.decref(obj)
    c.pyapi.decref(bsr__gpyth)
    c.pyapi.decref(args)
    c.pyapi.decref(kws)
    return hdlw__hid


@infer_global(pyspark.sql.types.Row)
class RowConstructor(AbstractTemplate):

    def generic(self, args, kws):
        if args and kws:
            raise BodoError(
                'pyspark.sql.types.Row: Cannot use both args and kwargs to create Row'
                )
        mwkd__zsa = ', '.join(f'arg{i}' for i in range(len(args)))
        qujpj__gevfv = ', '.join(f"{phb__ppkew} = ''" for phb__ppkew in kws)
        func_text = f'def row_stub({mwkd__zsa}{qujpj__gevfv}):\n'
        func_text += '    pass\n'
        zksek__pjgw = {}
        exec(func_text, {}, zksek__pjgw)
        snvw__xngc = zksek__pjgw['row_stub']
        rjbc__pfyw = numba.core.utils.pysignature(snvw__xngc)
        if args:
            pnc__tglbd = RowType(args, tuple(f'{ANON_SENTINEL}{i}' for i in
                range(len(args))))
            return signature(pnc__tglbd, *args).replace(pysig=rjbc__pfyw)
        kws = dict(kws)
        pnc__tglbd = RowType(tuple(kws.values()), tuple(kws.keys()))
        return signature(pnc__tglbd, *kws.values()).replace(pysig=rjbc__pfyw)


lower_builtin(pyspark.sql.types.Row, types.VarArg(types.Any))(numba.cpython
    .tupleobj.namedtuple_constructor)


class SparkDataFrameType(types.Type):

    def __init__(self, df):
        self.df = df
        super(SparkDataFrameType, self).__init__(f'SparkDataFrame({df})')

    @property
    def key(self):
        return self.df

    def copy(self):
        return SparkDataFrameType(self.df)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SparkDataFrameType)
class SparkDataFrameModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        jvq__yjxsn = [('df', fe_type.df)]
        super(SparkDataFrameModel, self).__init__(dmm, fe_type, jvq__yjxsn)


make_attribute_wrapper(SparkDataFrameType, 'df', '_df')


@intrinsic
def init_spark_df(typingctx, df_typ=None):

    def codegen(context, builder, sig, args):
        df, = args
        spark_df = cgutils.create_struct_proxy(sig.return_type)(context,
            builder)
        spark_df.df = df
        context.nrt.incref(builder, sig.args[0], df)
        return spark_df._getvalue()
    return SparkDataFrameType(df_typ)(df_typ), codegen


@overload_method(SparkSessionType, 'createDataFrame', inline='always',
    no_unliteral=True)
def overload_create_df(sp_session, data, schema=None, samplingRatio=None,
    verifySchema=True):
    check_runtime_cols_unsupported(data, 'spark.createDataFrame()')
    if isinstance(data, DataFrameType):

        def impl_df(sp_session, data, schema=None, samplingRatio=None,
            verifySchema=True):
            data = bodo.scatterv(data, warn_if_dist=False)
            return bodo.libs.pyspark_ext.init_spark_df(data)
        return impl_df
    if not (isinstance(data, types.List) and isinstance(data.dtype, RowType)):
        raise BodoError(
            f"SparkSession.createDataFrame(): 'data' should be a Pandas dataframe or list of Rows, not {data}"
            )
    ame__vkwr = data.dtype.fields
    rvch__yidr = len(data.dtype.types)
    func_text = (
        'def impl(sp_session, data, schema=None, samplingRatio=None, verifySchema=True):\n'
        )
    func_text += f'  n = len(data)\n'
    crvgs__dulo = []
    for i, lpeq__gnsv in enumerate(data.dtype.types):
        wfoc__glib = dtype_to_array_type(lpeq__gnsv)
        func_text += (
            f'  A{i} = bodo.utils.utils.alloc_type(n, arr_typ{i}, (-1,))\n')
        crvgs__dulo.append(wfoc__glib)
    func_text += f'  for i in range(n):\n'
    func_text += f'    r = data[i]\n'
    for i in range(rvch__yidr):
        func_text += (
            f'    A{i}[i] = bodo.utils.conversion.unbox_if_timestamp(r[{i}])\n'
            )
    ucs__xons = '({}{})'.format(', '.join(f'A{i}' for i in range(rvch__yidr
        )), ',' if len(ame__vkwr) == 1 else '')
    func_text += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)\n'
        )
    func_text += f"""  pdf = bodo.hiframes.pd_dataframe_ext.init_dataframe({ucs__xons}, index, {ame__vkwr})
"""
    func_text += f'  pdf = bodo.scatterv(pdf)\n'
    func_text += f'  return bodo.libs.pyspark_ext.init_spark_df(pdf)\n'
    zksek__pjgw = {}
    kyitj__beqqm = {'bodo': bodo}
    for i in range(rvch__yidr):
        kyitj__beqqm[f'arr_typ{i}'] = crvgs__dulo[i]
    exec(func_text, kyitj__beqqm, zksek__pjgw)
    impl = zksek__pjgw['impl']
    return impl


@overload_method(SparkDataFrameType, 'toPandas', inline='always',
    no_unliteral=True)
def overload_to_pandas(spark_df, _is_bodo_dist=False):
    if is_overload_true(_is_bodo_dist):
        return lambda spark_df, _is_bodo_dist=False: spark_df._df

    def impl(spark_df, _is_bodo_dist=False):
        return bodo.gatherv(spark_df._df, warn_if_rep=False)
    return impl


@overload_method(SparkDataFrameType, 'limit', inline='always', no_unliteral
    =True)
def overload_limit(spark_df, num):

    def impl(spark_df, num):
        return bodo.libs.pyspark_ext.init_spark_df(spark_df._df.iloc[:num])
    return impl


def _df_to_rows(df):
    pass


@overload(_df_to_rows)
def overload_df_to_rows(df):
    func_text = 'def impl(df):\n'
    for i in range(len(df.columns)):
        func_text += (
            f'  A{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})\n'
            )
    func_text += '  n = len(df)\n'
    func_text += '  out = []\n'
    func_text += '  for i in range(n):\n'
    ffi__phrvd = ', '.join(f'{c}=A{i}[i]' for i, c in enumerate(df.columns))
    func_text += f'    out.append(Row({ffi__phrvd}))\n'
    func_text += '  return out\n'
    zksek__pjgw = {}
    kyitj__beqqm = {'bodo': bodo, 'Row': pyspark.sql.types.Row}
    exec(func_text, kyitj__beqqm, zksek__pjgw)
    impl = zksek__pjgw['impl']
    return impl


@overload_method(SparkDataFrameType, 'collect', inline='always',
    no_unliteral=True)
def overload_collect(spark_df):

    def impl(spark_df):
        data = bodo.gatherv(spark_df._df, warn_if_rep=False)
        return _df_to_rows(data)
    return impl


@overload_method(SparkDataFrameType, 'take', inline='always', no_unliteral=True
    )
def overload_take(spark_df, num):

    def impl(spark_df, num):
        return spark_df.limit(num).collect()
    return impl


@infer_getattr
class SparkDataFrameAttribute(AttributeTemplate):
    key = SparkDataFrameType

    def generic_resolve(self, sdf, attr):
        if attr in sdf.df.columns:
            return ColumnType(ExprType('col', (attr,)))


SparkDataFrameAttribute._no_unliteral = True


@overload_method(SparkDataFrameType, 'select', no_unliteral=True)
def overload_df_select(spark_df, *cols):
    return _gen_df_select(spark_df, cols)


def _gen_df_select(spark_df, cols, avoid_stararg=False):
    df_type = spark_df.df
    if isinstance(cols, tuple) and len(cols) == 1 and isinstance(cols[0], (
        types.StarArgTuple, types.StarArgUniTuple)):
        cols = cols[0]
    if len(cols) == 1 and is_overload_constant_list(cols[0]):
        cols = get_overload_const_list(cols[0])
    func_text = f"def impl(spark_df, {'' if avoid_stararg else '*cols'}):\n"
    func_text += '  df = spark_df._df\n'
    out_col_names = []
    out_data = []
    for col in cols:
        col = get_overload_const_str(col) if is_overload_constant_str(col
            ) else col
        out_col_names.append(_get_col_name(col))
        data, aor__jbfzv = _gen_col_code(col, df_type)
        func_text += aor__jbfzv
        out_data.append(data)
    return _gen_init_spark_df(func_text, out_data, out_col_names)


def _gen_init_spark_df(func_text, out_data, out_col_names):
    ucs__xons = '({}{})'.format(', '.join(out_data), ',' if len(out_data) ==
        1 else '')
    dydnm__gbkm = '0' if not out_data else f'len({out_data[0]})'
    func_text += f'  n = {dydnm__gbkm}\n'
    func_text += (
        '  index = bodo.hiframes.pd_index_ext.init_range_index(0, n, 1, None)\n'
        )
    func_text += f"""  pdf = bodo.hiframes.pd_dataframe_ext.init_dataframe({ucs__xons}, index, {tuple(out_col_names)})
"""
    func_text += f'  return bodo.libs.pyspark_ext.init_spark_df(pdf)\n'
    zksek__pjgw = {}
    kyitj__beqqm = {'bodo': bodo, 'np': np}
    exec(func_text, kyitj__beqqm, zksek__pjgw)
    impl = zksek__pjgw['impl']
    return impl


@overload_method(SparkDataFrameType, 'show', inline='always', no_unliteral=True
    )
def overload_show(spark_df, n=20, truncate=True, vertical=False):
    oird__dvx = dict(truncate=truncate, vertical=vertical)
    teas__hauu = dict(truncate=True, vertical=False)
    check_unsupported_args('SparkDataFrameType.show', oird__dvx, teas__hauu)

    def impl(spark_df, n=20, truncate=True, vertical=False):
        print(spark_df._df.head(n))
    return impl


@overload_method(SparkDataFrameType, 'printSchema', inline='always',
    no_unliteral=True)
def overload_print_schema(spark_df):

    def impl(spark_df):
        print(spark_df._df.dtypes)
    return impl


@overload_method(SparkDataFrameType, 'withColumn', inline='always',
    no_unliteral=True)
def overload_with_column(spark_df, colName, col):
    _check_column(col)
    if not is_overload_constant_str(colName):
        raise BodoError(
            f"SparkDataFrame.withColumn(): 'colName' should be a constant string, not {colName}"
            )
    col_name = get_overload_const_str(colName)
    nopl__kwbl = spark_df.df.columns
    opi__zyhdy = nopl__kwbl if col_name in nopl__kwbl else nopl__kwbl + (
        col_name,)
    ojavf__biokt, immd__lxk = _gen_col_code(col, spark_df.df)
    out_data = [(ojavf__biokt if c == col_name else
        f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {nopl__kwbl.index(c)})'
        ) for c in opi__zyhdy]
    func_text = 'def impl(spark_df, colName, col):\n'
    func_text += '  df = spark_df._df\n'
    func_text += immd__lxk
    return _gen_init_spark_df(func_text, out_data, opi__zyhdy)


@overload_method(SparkDataFrameType, 'withColumnRenamed', inline='always',
    no_unliteral=True)
def overload_with_column_renamed(spark_df, existing, new):
    if not (is_overload_constant_str(existing) and is_overload_constant_str
        (new)):
        raise BodoError(
            f"SparkDataFrame.withColumnRenamed(): 'existing' and 'new' should be a constant strings, not ({existing}, {new})"
            )
    wqmn__uoddv = get_overload_const_str(existing)
    blr__mywk = get_overload_const_str(new)
    nopl__kwbl = spark_df.df.columns
    opi__zyhdy = tuple(blr__mywk if c == wqmn__uoddv else c for c in nopl__kwbl
        )
    out_data = [f'bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {i})'
         for i in range(len(nopl__kwbl))]
    func_text = 'def impl(spark_df, existing, new):\n'
    func_text += '  df = spark_df._df\n'
    return _gen_init_spark_df(func_text, out_data, opi__zyhdy)


@overload_attribute(SparkDataFrameType, 'columns', inline='always')
def overload_dataframe_columns(spark_df):
    jkryf__orvje = list(str(phb__ppkew) for phb__ppkew in spark_df.df.columns)
    func_text = 'def impl(spark_df):\n'
    func_text += f'  return {jkryf__orvje}\n'
    zksek__pjgw = {}
    exec(func_text, {}, zksek__pjgw)
    impl = zksek__pjgw['impl']
    return impl


class ColumnType(types.Type):

    def __init__(self, expr):
        self.expr = expr
        super(ColumnType, self).__init__(f'Column({expr})')

    @property
    def key(self):
        return self.expr

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


register_model(ColumnType)(models.OpaqueModel)


class ExprType(types.Type):

    def __init__(self, op, children):
        self.op = op
        self.children = children
        super(ExprType, self).__init__(f'{op}({children})')

    @property
    def key(self):
        return self.op, self.children

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


register_model(ExprType)(models.OpaqueModel)


@intrinsic
def init_col_from_name(typingctx, col=None):
    assert is_overload_constant_str(col)
    coo__qulqh = get_overload_const_str(col)
    hble__wpfxh = ColumnType(ExprType('col', (coo__qulqh,)))

    def codegen(context, builder, signature, args):
        return context.get_constant_null(hble__wpfxh)
    return hble__wpfxh(col), codegen


@overload(F.col, no_unliteral=True)
@overload(F.column, no_unliteral=True)
def overload_f_col(col):
    if not is_overload_constant_str(col):
        raise BodoError(
            f'pyspark.sql.functions.col(): column name should be a constant string, not {col}'
            )
    return lambda col: init_col_from_name(col)


@intrinsic
def init_f_sum(typingctx, col=None):
    hble__wpfxh = ColumnType(ExprType('sum', (col.expr,)))

    def codegen(context, builder, signature, args):
        return context.get_constant_null(hble__wpfxh)
    return hble__wpfxh(col), codegen


@overload(F.sum, no_unliteral=True)
def overload_f_sum(col):
    if is_overload_constant_str(col):
        return lambda col: init_f_sum(init_col_from_name(col))
    if not isinstance(col, ColumnType):
        raise BodoError(
            f'pyspark.sql.functions.sum(): input should be a Column object or a constant string, not {col}'
            )
    return lambda col: init_f_sum(col)


def _get_col_name(col):
    if isinstance(col, str):
        return col
    _check_column(col)
    return _get_col_name_exr(col.expr)


def _get_col_name_exr(expr):
    if expr.op == 'sum':
        return f'sum({_get_col_name_exr(expr.children[0])})'
    assert expr.op == 'col'
    return expr.children[0]


def _gen_col_code(col, df_type):
    if isinstance(col, str):
        return _gen_col_code_colname(col, df_type)
    _check_column(col)
    return _gen_col_code_expr(col.expr, df_type)


def _gen_col_code_expr(expr, df_type):
    if expr.op == 'col':
        return _gen_col_code_colname(expr.children[0], df_type)
    if expr.op == 'sum':
        brf__tpsg, lntv__azml = _gen_col_code_expr(expr.children[0], df_type)
        i = ir_utils.next_label()
        func_text = f"""  A{i} = np.asarray([bodo.libs.array_ops.array_op_sum({brf__tpsg}, True, 0)])
"""
        return f'A{i}', lntv__azml + func_text


def _gen_col_code_colname(col_name, df_type):
    zbh__znhh = df_type.columns.index(col_name)
    i = ir_utils.next_label()
    func_text = (
        f'  A{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(df, {zbh__znhh})\n'
        )
    return f'A{i}', func_text


def _check_column(col):
    if not isinstance(col, ColumnType):
        raise BodoError('Column object expected')
