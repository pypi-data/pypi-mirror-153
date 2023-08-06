"""
Support for Series.str methods
"""
import operator
import re
import numba
import numpy as np
from numba.core import cgutils, types
from numba.extending import intrinsic, make_attribute_wrapper, models, overload, overload_attribute, overload_method, register_model
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import StringIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.hiframes.split_impl import get_split_view_data_ptr, get_split_view_index, string_array_split_view_type
from bodo.libs.array import get_search_regex
from bodo.libs.array_item_arr_ext import ArrayItemArrayType
from bodo.libs.str_arr_ext import get_utf8_size, pre_alloc_string_array, string_array_type
from bodo.libs.str_ext import str_findall_count
from bodo.utils.typing import BodoError, create_unsupported_overload, get_overload_const_int, get_overload_const_list, get_overload_const_str, get_overload_const_str_len, is_list_like_index_type, is_overload_constant_bool, is_overload_constant_int, is_overload_constant_list, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true, is_str_arr_type, raise_bodo_error


class SeriesStrMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        hqjg__aapw = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(hqjg__aapw)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lnfdq__egof = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, lnfdq__egof)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        wsfdl__opl, = args
        pnf__xyod = signature.return_type
        ofu__fah = cgutils.create_struct_proxy(pnf__xyod)(context, builder)
        ofu__fah.obj = wsfdl__opl
        context.nrt.incref(builder, signature.args[0], wsfdl__opl)
        return ofu__fah._getvalue()
    return SeriesStrMethodType(obj)(obj), codegen


def str_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.UnicodeType) and not is_overload_constant_str(
        arg):
        raise_bodo_error(
            "Series.str.{}(): parameter '{}' expected a string object, not {}"
            .format(func_name, arg_name, arg))


def int_arg_check(func_name, arg_name, arg):
    if not isinstance(arg, types.Integer) and not is_overload_constant_int(arg
        ):
        raise BodoError(
            "Series.str.{}(): parameter '{}' expected an int object, not {}"
            .format(func_name, arg_name, arg))


def not_supported_arg_check(func_name, arg_name, arg, defval):
    if arg_name == 'na':
        if not isinstance(arg, types.Omitted) and (not isinstance(arg,
            float) or not np.isnan(arg)):
            raise BodoError(
                "Series.str.{}(): parameter '{}' is not supported, default: np.nan"
                .format(func_name, arg_name))
    elif not isinstance(arg, types.Omitted) and arg != defval:
        raise BodoError(
            "Series.str.{}(): parameter '{}' is not supported, default: {}"
            .format(func_name, arg_name, defval))


def common_validate_padding(func_name, width, fillchar):
    if is_overload_constant_str(fillchar):
        if get_overload_const_str_len(fillchar) != 1:
            raise BodoError(
                'Series.str.{}(): fillchar must be a character, not str'.
                format(func_name))
    elif not isinstance(fillchar, types.UnicodeType):
        raise BodoError('Series.str.{}(): fillchar must be a character, not {}'
            .format(func_name, fillchar))
    int_arg_check(func_name, 'width', width)


@overload_attribute(SeriesType, 'str')
def overload_series_str(S):
    if not (is_str_arr_type(S.data) or S.data ==
        string_array_split_view_type or isinstance(S.data, ArrayItemArrayType)
        ):
        raise_bodo_error(
            'Series.str: input should be a series of string or arrays')
    return lambda S: bodo.hiframes.series_str_impl.init_series_str_method(S)


@overload_method(SeriesStrMethodType, 'len', inline='always', no_unliteral=True
    )
def overload_str_method_len(S_str):

    def impl(S_str):
        S = S_str._obj
        kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(kmocc__slgd, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return impl


@overload_method(SeriesStrMethodType, 'split', inline='always',
    no_unliteral=True)
def overload_str_method_split(S_str, pat=None, n=-1, expand=False):
    if not is_overload_none(pat):
        str_arg_check('split', 'pat', pat)
    int_arg_check('split', 'n', n)
    not_supported_arg_check('split', 'expand', expand, False)
    if is_overload_constant_str(pat) and len(get_overload_const_str(pat)
        ) == 1 and get_overload_const_str(pat).isascii(
        ) and is_overload_constant_int(n) and get_overload_const_int(n
        ) == -1 and S_str.stype.data == string_array_type:

        def _str_split_view_impl(S_str, pat=None, n=-1, expand=False):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(kmocc__slgd,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(kmocc__slgd, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    vnoj__bcwgx = S_str.stype.data
    if (vnoj__bcwgx != string_array_split_view_type and not is_str_arr_type
        (vnoj__bcwgx)) and not isinstance(vnoj__bcwgx, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(vnoj__bcwgx, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(kmocc__slgd, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_get_array_impl
    if vnoj__bcwgx == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(kmocc__slgd)
            saj__lpiqx = 0
            for yhik__wjr in numba.parfors.parfor.internal_prange(n):
                wpvvn__qnl, wpvvn__qnl, uqqb__eehck = get_split_view_index(
                    kmocc__slgd, yhik__wjr, i)
                saj__lpiqx += uqqb__eehck
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, saj__lpiqx)
            for kbo__qkze in numba.parfors.parfor.internal_prange(n):
                deum__juin, wino__jppa, uqqb__eehck = get_split_view_index(
                    kmocc__slgd, kbo__qkze, i)
                if deum__juin == 0:
                    bodo.libs.array_kernels.setna(out_arr, kbo__qkze)
                    xevej__nvoj = get_split_view_data_ptr(kmocc__slgd, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr, kbo__qkze
                        )
                    xevej__nvoj = get_split_view_data_ptr(kmocc__slgd,
                        wino__jppa)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    kbo__qkze, xevej__nvoj, uqqb__eehck)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(kmocc__slgd, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(kmocc__slgd)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for kbo__qkze in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(kmocc__slgd, kbo__qkze) or not len(
                kmocc__slgd[kbo__qkze]) > i >= -len(kmocc__slgd[kbo__qkze]):
                out_arr[kbo__qkze] = ''
                bodo.libs.array_kernels.setna(out_arr, kbo__qkze)
            else:
                out_arr[kbo__qkze] = kmocc__slgd[kbo__qkze][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    vnoj__bcwgx = S_str.stype.data
    if (vnoj__bcwgx != string_array_split_view_type and vnoj__bcwgx !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        vnoj__bcwgx)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(tfltb__wyra)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for kbo__qkze in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(tfltb__wyra, kbo__qkze):
                out_arr[kbo__qkze] = ''
                bodo.libs.array_kernels.setna(out_arr, kbo__qkze)
            else:
                axob__mtx = tfltb__wyra[kbo__qkze]
                out_arr[kbo__qkze] = sep.join(axob__mtx)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return impl


@overload_method(SeriesStrMethodType, 'replace', inline='always',
    no_unliteral=True)
def overload_str_method_replace(S_str, pat, repl, n=-1, case=None, flags=0,
    regex=True):
    not_supported_arg_check('replace', 'n', n, -1)
    not_supported_arg_check('replace', 'case', case, None)
    str_arg_check('replace', 'pat', pat)
    str_arg_check('replace', 'repl', repl)
    int_arg_check('replace', 'flags', flags)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_replace_dict_impl(S_str, pat, repl, n=-1, case=None, flags
            =0, regex=True):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(kmocc__slgd, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            wbop__qzuf = re.compile(pat, flags)
            gxngq__ebb = len(kmocc__slgd)
            out_arr = pre_alloc_string_array(gxngq__ebb, -1)
            for kbo__qkze in numba.parfors.parfor.internal_prange(gxngq__ebb):
                if bodo.libs.array_kernels.isna(kmocc__slgd, kbo__qkze):
                    out_arr[kbo__qkze] = ''
                    bodo.libs.array_kernels.setna(out_arr, kbo__qkze)
                    continue
                out_arr[kbo__qkze] = wbop__qzuf.sub(repl, kmocc__slgd[
                    kbo__qkze])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        gxngq__ebb = len(kmocc__slgd)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(gxngq__ebb, -1)
        for kbo__qkze in numba.parfors.parfor.internal_prange(gxngq__ebb):
            if bodo.libs.array_kernels.isna(kmocc__slgd, kbo__qkze):
                out_arr[kbo__qkze] = ''
                bodo.libs.array_kernels.setna(out_arr, kbo__qkze)
                continue
            out_arr[kbo__qkze] = kmocc__slgd[kbo__qkze].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


def is_regex_unsupported(pat):
    xwh__eugfo = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(oopia__eee in pat) for oopia__eee in xwh__eugfo])
    else:
        return True


@overload_method(SeriesStrMethodType, 'contains', no_unliteral=True)
def overload_str_method_contains(S_str, pat, case=True, flags=0, na=np.nan,
    regex=True):
    not_supported_arg_check('contains', 'na', na, np.nan)
    str_arg_check('contains', 'pat', pat)
    int_arg_check('contains', 'flags', flags)
    if not is_overload_constant_bool(regex):
        raise BodoError(
            "Series.str.contains(): 'regex' argument should be a constant boolean"
            )
    if not is_overload_constant_bool(case):
        raise BodoError(
            "Series.str.contains(): 'case' argument should be a constant boolean"
            )
    lvrvp__cmcww = re.IGNORECASE.value
    ncu__bfq = 'def impl(\n'
    ncu__bfq += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    ncu__bfq += '):\n'
    ncu__bfq += '  S = S_str._obj\n'
    ncu__bfq += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    ncu__bfq += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    ncu__bfq += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    ncu__bfq += '  l = len(arr)\n'
    ncu__bfq += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                ncu__bfq += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                ncu__bfq += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            ncu__bfq += """  get_search_regex(arr, case, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        ncu__bfq += (
            '  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)\n'
            )
    else:
        ncu__bfq += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            ncu__bfq += '  upper_pat = pat.upper()\n'
        ncu__bfq += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        ncu__bfq += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        ncu__bfq += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        ncu__bfq += '      else: \n'
        if is_overload_true(case):
            ncu__bfq += '          out_arr[i] = pat in arr[i]\n'
        else:
            ncu__bfq += '          out_arr[i] = upper_pat in arr[i].upper()\n'
    ncu__bfq += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    nkwi__izwp = {}
    exec(ncu__bfq, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': lvrvp__cmcww, 'get_search_regex':
        get_search_regex}, nkwi__izwp)
    impl = nkwi__izwp['impl']
    return impl


@overload_method(SeriesStrMethodType, 'cat', no_unliteral=True)
def overload_str_method_cat(S_str, others=None, sep=None, na_rep=None, join
    ='left'):
    if not isinstance(others, DataFrameType):
        raise_bodo_error(
            "Series.str.cat(): 'others' must be a DataFrame currently")
    if not is_overload_none(sep):
        str_arg_check('cat', 'sep', sep)
    if not is_overload_constant_str(join) or get_overload_const_str(join
        ) != 'left':
        raise_bodo_error("Series.str.cat(): 'join' not supported yet")
    ncu__bfq = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    ncu__bfq += '  S = S_str._obj\n'
    ncu__bfq += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    ncu__bfq += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    ncu__bfq += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    ncu__bfq += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        ncu__bfq += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})\n'
            )
    if S_str.stype.data == bodo.dict_str_arr_type and all(bcgjm__bmuuk ==
        bodo.dict_str_arr_type for bcgjm__bmuuk in others.data):
        psih__jbehi = ', '.join(f'data{i}' for i in range(len(others.columns)))
        ncu__bfq += (
            f'  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {psih__jbehi}), sep)\n'
            )
    else:
        yvt__smlqt = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        ncu__bfq += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        ncu__bfq += '  numba.parfors.parfor.init_prange()\n'
        ncu__bfq += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        ncu__bfq += f'      if {yvt__smlqt}:\n'
        ncu__bfq += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        ncu__bfq += '          continue\n'
        uic__yaczi = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        hjdi__qsnp = "''" if is_overload_none(sep) else 'sep'
        ncu__bfq += f'      out_arr[i] = {hjdi__qsnp}.join([{uic__yaczi}])\n'
    ncu__bfq += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    nkwi__izwp = {}
    exec(ncu__bfq, {'bodo': bodo, 'numba': numba}, nkwi__izwp)
    impl = nkwi__izwp['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        wbop__qzuf = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        gxngq__ebb = len(tfltb__wyra)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(gxngq__ebb, np.int64)
        for i in numba.parfors.parfor.internal_prange(gxngq__ebb):
            if bodo.libs.array_kernels.isna(tfltb__wyra, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(wbop__qzuf, tfltb__wyra[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return impl


@overload_method(SeriesStrMethodType, 'find', inline='always', no_unliteral
    =True)
def overload_str_method_find(S_str, sub, start=0, end=None):
    str_arg_check('find', 'sub', sub)
    int_arg_check('find', 'start', start)
    if not is_overload_none(end):
        int_arg_check('find', 'end', end)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_find_dict_impl(S_str, sub, start=0, end=None):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(kmocc__slgd, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gxngq__ebb = len(tfltb__wyra)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(gxngq__ebb, np.int64)
        for i in numba.parfors.parfor.internal_prange(gxngq__ebb):
            if bodo.libs.array_kernels.isna(tfltb__wyra, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = tfltb__wyra[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return impl


@overload_method(SeriesStrMethodType, 'rfind', inline='always',
    no_unliteral=True)
def overload_str_method_rfind(S_str, sub, start=0, end=None):
    str_arg_check('rfind', 'sub', sub)
    if start != 0:
        int_arg_check('rfind', 'start', start)
    if not is_overload_none(end):
        int_arg_check('rfind', 'end', end)

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gxngq__ebb = len(tfltb__wyra)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(gxngq__ebb, np.int64)
        for i in numba.parfors.parfor.internal_prange(gxngq__ebb):
            if bodo.libs.array_kernels.isna(tfltb__wyra, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = tfltb__wyra[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return impl


@overload_method(SeriesStrMethodType, 'slice_replace', inline='always',
    no_unliteral=True)
def overload_str_method_slice_replace(S_str, start=0, stop=None, repl=''):
    int_arg_check('slice_replace', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice_replace', 'stop', stop)
    str_arg_check('slice_replace', 'repl', repl)

    def impl(S_str, start=0, stop=None, repl=''):
        S = S_str._obj
        tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gxngq__ebb = len(tfltb__wyra)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gxngq__ebb, -1)
        for kbo__qkze in numba.parfors.parfor.internal_prange(gxngq__ebb):
            if bodo.libs.array_kernels.isna(tfltb__wyra, kbo__qkze):
                bodo.libs.array_kernels.setna(out_arr, kbo__qkze)
            else:
                if stop is not None:
                    ohp__gnp = tfltb__wyra[kbo__qkze][stop:]
                else:
                    ohp__gnp = ''
                out_arr[kbo__qkze] = tfltb__wyra[kbo__qkze][:start
                    ] + repl + ohp__gnp
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
                ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
                hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(kmocc__slgd,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    ypsia__dio, hqjg__aapw)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            gxngq__ebb = len(tfltb__wyra)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gxngq__ebb,
                -1)
            for kbo__qkze in numba.parfors.parfor.internal_prange(gxngq__ebb):
                if bodo.libs.array_kernels.isna(tfltb__wyra, kbo__qkze):
                    bodo.libs.array_kernels.setna(out_arr, kbo__qkze)
                else:
                    out_arr[kbo__qkze] = tfltb__wyra[kbo__qkze] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return impl
    elif is_overload_constant_list(repeats):
        mirp__gkjnu = get_overload_const_list(repeats)
        mjbx__mjxt = all([isinstance(zon__nwh, int) for zon__nwh in
            mirp__gkjnu])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        mjbx__mjxt = True
    else:
        mjbx__mjxt = False
    if mjbx__mjxt:

        def impl(S_str, repeats):
            S = S_str._obj
            tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            buopp__kktx = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            gxngq__ebb = len(tfltb__wyra)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gxngq__ebb,
                -1)
            for kbo__qkze in numba.parfors.parfor.internal_prange(gxngq__ebb):
                if bodo.libs.array_kernels.isna(tfltb__wyra, kbo__qkze):
                    bodo.libs.array_kernels.setna(out_arr, kbo__qkze)
                else:
                    out_arr[kbo__qkze] = tfltb__wyra[kbo__qkze] * buopp__kktx[
                        kbo__qkze]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    ncu__bfq = f"""def dict_impl(S_str, width, fillchar=' '):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr, width, fillchar)
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
def impl(S_str, width, fillchar=' '):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    numba.parfors.parfor.init_prange()
    l = len(str_arr)
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)
    for j in numba.parfors.parfor.internal_prange(l):
        if bodo.libs.array_kernels.isna(str_arr, j):
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}(width, fillchar)
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    nkwi__izwp = {}
    vgy__ovyt = {'bodo': bodo, 'numba': numba}
    exec(ncu__bfq, vgy__ovyt, nkwi__izwp)
    impl = nkwi__izwp['impl']
    dcplo__szh = nkwi__izwp['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return dcplo__szh
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for bwc__niew in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(bwc__niew)
        overload_method(SeriesStrMethodType, bwc__niew, inline='always',
            no_unliteral=True)(impl)


_install_ljust_rjust_center()


@overload_method(SeriesStrMethodType, 'pad', no_unliteral=True)
def overload_str_method_pad(S_str, width, side='left', fillchar=' '):
    common_validate_padding('pad', width, fillchar)
    if is_overload_constant_str(side):
        if get_overload_const_str(side) not in ['left', 'right', 'both']:
            raise BodoError('Series.str.pad(): Invalid Side')
    else:
        raise BodoError('Series.str.pad(): Invalid Side')
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_pad_dict_impl(S_str, width, side='left', fillchar=' '):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(kmocc__slgd,
                    width, fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(kmocc__slgd,
                    width, fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(kmocc__slgd,
                    width, fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gxngq__ebb = len(tfltb__wyra)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gxngq__ebb, -1)
        for kbo__qkze in numba.parfors.parfor.internal_prange(gxngq__ebb):
            if bodo.libs.array_kernels.isna(tfltb__wyra, kbo__qkze):
                out_arr[kbo__qkze] = ''
                bodo.libs.array_kernels.setna(out_arr, kbo__qkze)
            elif side == 'left':
                out_arr[kbo__qkze] = tfltb__wyra[kbo__qkze].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[kbo__qkze] = tfltb__wyra[kbo__qkze].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[kbo__qkze] = tfltb__wyra[kbo__qkze].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(kmocc__slgd, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gxngq__ebb = len(tfltb__wyra)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gxngq__ebb, -1)
        for kbo__qkze in numba.parfors.parfor.internal_prange(gxngq__ebb):
            if bodo.libs.array_kernels.isna(tfltb__wyra, kbo__qkze):
                out_arr[kbo__qkze] = ''
                bodo.libs.array_kernels.setna(out_arr, kbo__qkze)
            else:
                out_arr[kbo__qkze] = tfltb__wyra[kbo__qkze].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return impl


@overload_method(SeriesStrMethodType, 'slice', no_unliteral=True)
def overload_str_method_slice(S_str, start=None, stop=None, step=None):
    if not is_overload_none(start):
        int_arg_check('slice', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice', 'stop', stop)
    if not is_overload_none(step):
        int_arg_check('slice', 'step', step)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_slice_dict_impl(S_str, start=None, stop=None, step=None):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(kmocc__slgd, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gxngq__ebb = len(tfltb__wyra)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(gxngq__ebb, -1)
        for kbo__qkze in numba.parfors.parfor.internal_prange(gxngq__ebb):
            if bodo.libs.array_kernels.isna(tfltb__wyra, kbo__qkze):
                out_arr[kbo__qkze] = ''
                bodo.libs.array_kernels.setna(out_arr, kbo__qkze)
            else:
                out_arr[kbo__qkze] = tfltb__wyra[kbo__qkze][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(kmocc__slgd,
                pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gxngq__ebb = len(tfltb__wyra)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(gxngq__ebb)
        for i in numba.parfors.parfor.internal_prange(gxngq__ebb):
            if bodo.libs.array_kernels.isna(tfltb__wyra, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = tfltb__wyra[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
            hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(kmocc__slgd, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                ypsia__dio, hqjg__aapw)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        tfltb__wyra = bodo.hiframes.pd_series_ext.get_series_data(S)
        hqjg__aapw = bodo.hiframes.pd_series_ext.get_series_name(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        gxngq__ebb = len(tfltb__wyra)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(gxngq__ebb)
        for i in numba.parfors.parfor.internal_prange(gxngq__ebb):
            if bodo.libs.array_kernels.isna(tfltb__wyra, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = tfltb__wyra[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, ypsia__dio,
            hqjg__aapw)
    return impl


@overload(operator.getitem, no_unliteral=True)
def overload_str_method_getitem(S_str, ind):
    if not isinstance(S_str, SeriesStrMethodType):
        return
    if not isinstance(types.unliteral(ind), (types.SliceType, types.Integer)):
        raise BodoError(
            'index input to Series.str[] should be a slice or an integer')
    if isinstance(ind, types.SliceType):
        return lambda S_str, ind: S_str.slice(ind.start, ind.stop, ind.step)
    if isinstance(types.unliteral(ind), types.Integer):
        return lambda S_str, ind: S_str.get(ind)


@overload_method(SeriesStrMethodType, 'extract', inline='always',
    no_unliteral=True)
def overload_str_method_extract(S_str, pat, flags=0, expand=True):
    if not is_overload_constant_bool(expand):
        raise BodoError(
            "Series.str.extract(): 'expand' argument should be a constant bool"
            )
    pkm__rne, regex = _get_column_names_from_regex(pat, flags, 'extract')
    uvez__thni = len(pkm__rne)
    ncu__bfq = 'def impl(S_str, pat, flags=0, expand=True):\n'
    ncu__bfq += '  regex = re.compile(pat, flags=flags)\n'
    ncu__bfq += '  S = S_str._obj\n'
    ncu__bfq += '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    ncu__bfq += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    ncu__bfq += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    ncu__bfq += '  numba.parfors.parfor.init_prange()\n'
    ncu__bfq += '  n = len(str_arr)\n'
    for i in range(uvez__thni):
        ncu__bfq += (
            '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
            .format(i))
    ncu__bfq += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    ncu__bfq += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    for i in range(uvez__thni):
        ncu__bfq += "          out_arr_{}[j] = ''\n".format(i)
        ncu__bfq += ('          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'
            .format(i))
    ncu__bfq += '      else:\n'
    ncu__bfq += '          m = regex.search(str_arr[j])\n'
    ncu__bfq += '          if m:\n'
    ncu__bfq += '            g = m.groups()\n'
    for i in range(uvez__thni):
        ncu__bfq += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
    ncu__bfq += '          else:\n'
    for i in range(uvez__thni):
        ncu__bfq += "            out_arr_{}[j] = ''\n".format(i)
        ncu__bfq += (
            '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    if is_overload_false(expand) and regex.groups == 1:
        hqjg__aapw = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        ncu__bfq += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(hqjg__aapw))
        nkwi__izwp = {}
        exec(ncu__bfq, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, nkwi__izwp)
        impl = nkwi__izwp['impl']
        return impl
    xtsu__xqugv = ', '.join('out_arr_{}'.format(i) for i in range(uvez__thni))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(ncu__bfq, pkm__rne,
        xtsu__xqugv, 'index', extra_globals={'get_utf8_size': get_utf8_size,
        're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    pkm__rne, wpvvn__qnl = _get_column_names_from_regex(pat, flags,
        'extractall')
    uvez__thni = len(pkm__rne)
    fkjvx__duqp = isinstance(S_str.stype.index, StringIndexType)
    ncu__bfq = 'def impl(S_str, pat, flags=0):\n'
    ncu__bfq += '  regex = re.compile(pat, flags=flags)\n'
    ncu__bfq += '  S = S_str._obj\n'
    ncu__bfq += '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    ncu__bfq += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    ncu__bfq += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    ncu__bfq += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    ncu__bfq += (
        '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n')
    ncu__bfq += '  numba.parfors.parfor.init_prange()\n'
    ncu__bfq += '  n = len(str_arr)\n'
    ncu__bfq += '  out_n_l = [0]\n'
    for i in range(uvez__thni):
        ncu__bfq += '  num_chars_{} = 0\n'.format(i)
    if fkjvx__duqp:
        ncu__bfq += '  index_num_chars = 0\n'
    ncu__bfq += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    if fkjvx__duqp:
        ncu__bfq += '      index_num_chars += get_utf8_size(index_arr[i])\n'
    ncu__bfq += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
    ncu__bfq += '          continue\n'
    ncu__bfq += '      m = regex.findall(str_arr[i])\n'
    ncu__bfq += '      out_n_l[0] += len(m)\n'
    for i in range(uvez__thni):
        ncu__bfq += '      l_{} = 0\n'.format(i)
    ncu__bfq += '      for s in m:\n'
    for i in range(uvez__thni):
        ncu__bfq += '        l_{} += get_utf8_size(s{})\n'.format(i, '[{}]'
            .format(i) if uvez__thni > 1 else '')
    for i in range(uvez__thni):
        ncu__bfq += '      num_chars_{0} += l_{0}\n'.format(i)
    ncu__bfq += (
        '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
        )
    for i in range(uvez__thni):
        ncu__bfq += (
            """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
            .format(i))
    if fkjvx__duqp:
        ncu__bfq += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
    else:
        ncu__bfq += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
    ncu__bfq += '  out_match_arr = np.empty(out_n, np.int64)\n'
    ncu__bfq += '  out_ind = 0\n'
    ncu__bfq += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    ncu__bfq += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    ncu__bfq += '          continue\n'
    ncu__bfq += '      m = regex.findall(str_arr[j])\n'
    ncu__bfq += '      for k, s in enumerate(m):\n'
    for i in range(uvez__thni):
        ncu__bfq += (
            '        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})\n'
            .format(i, '[{}]'.format(i) if uvez__thni > 1 else ''))
    ncu__bfq += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
    ncu__bfq += (
        '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
        )
    ncu__bfq += '        out_ind += 1\n'
    ncu__bfq += (
        '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n')
    ncu__bfq += "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n"
    xtsu__xqugv = ', '.join('out_arr_{}'.format(i) for i in range(uvez__thni))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(ncu__bfq, pkm__rne,
        xtsu__xqugv, 'out_index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


def _get_column_names_from_regex(pat, flags, func_name):
    if not is_overload_constant_str(pat):
        raise BodoError(
            "Series.str.{}(): 'pat' argument should be a constant string".
            format(func_name))
    if not is_overload_constant_int(flags):
        raise BodoError(
            "Series.str.{}(): 'flags' argument should be a constant int".
            format(func_name))
    pat = get_overload_const_str(pat)
    flags = get_overload_const_int(flags)
    regex = re.compile(pat, flags=flags)
    if regex.groups == 0:
        raise BodoError(
            'Series.str.{}(): pattern {} contains no capture groups'.format
            (func_name, pat))
    wzsm__bpu = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    pkm__rne = [wzsm__bpu.get(1 + i, i) for i in range(regex.groups)]
    return pkm__rne, regex


def create_str2str_methods_overload(func_name):
    omm__zxoms = func_name in ['lstrip', 'rstrip', 'strip']
    ncu__bfq = f"""def f({'S_str, to_strip=None' if omm__zxoms else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if omm__zxoms else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if omm__zxoms else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    ncu__bfq += f"""def _dict_impl({'S_str, to_strip=None' if omm__zxoms else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if omm__zxoms else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    nkwi__izwp = {}
    exec(ncu__bfq, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo.
        libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, nkwi__izwp)
    jcc__ugwm = nkwi__izwp['f']
    wcd__ntqrb = nkwi__izwp['_dict_impl']
    if omm__zxoms:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return wcd__ntqrb
            return jcc__ugwm
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return wcd__ntqrb
            return jcc__ugwm
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):

    def overload_str2bool_methods(S_str):
        ncu__bfq = 'def f(S_str):\n'
        ncu__bfq += '    S = S_str._obj\n'
        ncu__bfq += (
            '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        ncu__bfq += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        ncu__bfq += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        ncu__bfq += '    numba.parfors.parfor.init_prange()\n'
        ncu__bfq += '    l = len(str_arr)\n'
        ncu__bfq += (
            '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        ncu__bfq += '    for i in numba.parfors.parfor.internal_prange(l):\n'
        ncu__bfq += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
        ncu__bfq += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        ncu__bfq += '        else:\n'
        ncu__bfq += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
            .format(func_name))
        ncu__bfq += '    return bodo.hiframes.pd_series_ext.init_series(\n'
        ncu__bfq += '      out_arr,index, name)\n'
        nkwi__izwp = {}
        exec(ncu__bfq, {'bodo': bodo, 'numba': numba, 'np': np}, nkwi__izwp)
        jcc__ugwm = nkwi__izwp['f']
        return jcc__ugwm
    return overload_str2bool_methods


def _install_str2str_methods():
    for mrtgg__tan in bodo.hiframes.pd_series_ext.str2str_methods:
        xti__xkqze = create_str2str_methods_overload(mrtgg__tan)
        overload_method(SeriesStrMethodType, mrtgg__tan, inline='always',
            no_unliteral=True)(xti__xkqze)


def _install_str2bool_methods():
    for mrtgg__tan in bodo.hiframes.pd_series_ext.str2bool_methods:
        xti__xkqze = create_str2bool_methods_overload(mrtgg__tan)
        overload_method(SeriesStrMethodType, mrtgg__tan, inline='always',
            no_unliteral=True)(xti__xkqze)


_install_str2str_methods()
_install_str2bool_methods()


@overload_attribute(SeriesType, 'cat')
def overload_series_cat(s):
    if not isinstance(s.dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):
        raise BodoError('Can only use .cat accessor with categorical values.')
    return lambda s: bodo.hiframes.series_str_impl.init_series_cat_method(s)


class SeriesCatMethodType(types.Type):

    def __init__(self, stype):
        self.stype = stype
        hqjg__aapw = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(hqjg__aapw)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        lnfdq__egof = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, lnfdq__egof)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        wsfdl__opl, = args
        led__cjked = signature.return_type
        srbx__zgzb = cgutils.create_struct_proxy(led__cjked)(context, builder)
        srbx__zgzb.obj = wsfdl__opl
        context.nrt.incref(builder, signature.args[0], wsfdl__opl)
        return srbx__zgzb._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        kmocc__slgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ypsia__dio = bodo.hiframes.pd_series_ext.get_series_index(S)
        hqjg__aapw = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(kmocc__slgd),
            ypsia__dio, hqjg__aapw)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for jml__twbdv in unsupported_cat_attrs:
        pth__xje = 'Series.cat.' + jml__twbdv
        overload_attribute(SeriesCatMethodType, jml__twbdv)(
            create_unsupported_overload(pth__xje))
    for gcw__dgrt in unsupported_cat_methods:
        pth__xje = 'Series.cat.' + gcw__dgrt
        overload_method(SeriesCatMethodType, gcw__dgrt)(
            create_unsupported_overload(pth__xje))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for gcw__dgrt in unsupported_str_methods:
        pth__xje = 'Series.str.' + gcw__dgrt
        overload_method(SeriesStrMethodType, gcw__dgrt)(
            create_unsupported_overload(pth__xje))


_install_strseries_unsupported()
