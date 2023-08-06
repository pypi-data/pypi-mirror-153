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
        hanuh__lbp = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(hanuh__lbp)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qtmtq__aupv = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, qtmtq__aupv)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        kajc__qirwj, = args
        hch__uxgsw = signature.return_type
        pwtcp__oct = cgutils.create_struct_proxy(hch__uxgsw)(context, builder)
        pwtcp__oct.obj = kajc__qirwj
        context.nrt.incref(builder, signature.args[0], kajc__qirwj)
        return pwtcp__oct._getvalue()
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
        nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(nolta__jxpve, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
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
            nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
            orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
            hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(nolta__jxpve,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                orca__zxhtt, hanuh__lbp)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(nolta__jxpve, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    xkg__psu = S_str.stype.data
    if (xkg__psu != string_array_split_view_type and not is_str_arr_type(
        xkg__psu)) and not isinstance(xkg__psu, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(xkg__psu, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
            orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
            hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(nolta__jxpve, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                orca__zxhtt, hanuh__lbp)
        return _str_get_array_impl
    if xkg__psu == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
            orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
            hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(nolta__jxpve)
            omjjn__halr = 0
            for ztfx__qdcri in numba.parfors.parfor.internal_prange(n):
                jfyn__chapd, jfyn__chapd, poga__vazv = get_split_view_index(
                    nolta__jxpve, ztfx__qdcri, i)
                omjjn__halr += poga__vazv
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, omjjn__halr)
            for gktp__blm in numba.parfors.parfor.internal_prange(n):
                zgl__ygqv, nqcf__zleg, poga__vazv = get_split_view_index(
                    nolta__jxpve, gktp__blm, i)
                if zgl__ygqv == 0:
                    bodo.libs.array_kernels.setna(out_arr, gktp__blm)
                    axwm__wmbxl = get_split_view_data_ptr(nolta__jxpve, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr, gktp__blm
                        )
                    axwm__wmbxl = get_split_view_data_ptr(nolta__jxpve,
                        nqcf__zleg)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    gktp__blm, axwm__wmbxl, poga__vazv)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                orca__zxhtt, hanuh__lbp)
        return _str_get_split_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(nolta__jxpve)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for gktp__blm in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(nolta__jxpve, gktp__blm
                ) or not len(nolta__jxpve[gktp__blm]) > i >= -len(nolta__jxpve
                [gktp__blm]):
                out_arr[gktp__blm] = ''
                bodo.libs.array_kernels.setna(out_arr, gktp__blm)
            else:
                out_arr[gktp__blm] = nolta__jxpve[gktp__blm][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    xkg__psu = S_str.stype.data
    if (xkg__psu != string_array_split_view_type and xkg__psu !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(xkg__psu)
        ):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(ltcpe__gii)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for gktp__blm in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(ltcpe__gii, gktp__blm):
                out_arr[gktp__blm] = ''
                bodo.libs.array_kernels.setna(out_arr, gktp__blm)
            else:
                outl__dins = ltcpe__gii[gktp__blm]
                out_arr[gktp__blm] = sep.join(outl__dins)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
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
            nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
            orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
            hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(nolta__jxpve, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                orca__zxhtt, hanuh__lbp)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
            orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
            hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            sdw__zxx = re.compile(pat, flags)
            ietev__amw = len(nolta__jxpve)
            out_arr = pre_alloc_string_array(ietev__amw, -1)
            for gktp__blm in numba.parfors.parfor.internal_prange(ietev__amw):
                if bodo.libs.array_kernels.isna(nolta__jxpve, gktp__blm):
                    out_arr[gktp__blm] = ''
                    bodo.libs.array_kernels.setna(out_arr, gktp__blm)
                    continue
                out_arr[gktp__blm] = sdw__zxx.sub(repl, nolta__jxpve[gktp__blm]
                    )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                orca__zxhtt, hanuh__lbp)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(nolta__jxpve)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(ietev__amw, -1)
        for gktp__blm in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(nolta__jxpve, gktp__blm):
                out_arr[gktp__blm] = ''
                bodo.libs.array_kernels.setna(out_arr, gktp__blm)
                continue
            out_arr[gktp__blm] = nolta__jxpve[gktp__blm].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


def is_regex_unsupported(pat):
    tjxkl__scpt = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(xgi__uosw in pat) for xgi__uosw in tjxkl__scpt])
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
    dfyo__asrv = re.IGNORECASE.value
    vpw__leys = 'def impl(\n'
    vpw__leys += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    vpw__leys += '):\n'
    vpw__leys += '  S = S_str._obj\n'
    vpw__leys += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    vpw__leys += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    vpw__leys += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    vpw__leys += '  l = len(arr)\n'
    vpw__leys += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                vpw__leys += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                vpw__leys += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            vpw__leys += """  get_search_regex(arr, case, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        vpw__leys += (
            '  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)\n'
            )
    else:
        vpw__leys += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            vpw__leys += '  upper_pat = pat.upper()\n'
        vpw__leys += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        vpw__leys += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        vpw__leys += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        vpw__leys += '      else: \n'
        if is_overload_true(case):
            vpw__leys += '          out_arr[i] = pat in arr[i]\n'
        else:
            vpw__leys += '          out_arr[i] = upper_pat in arr[i].upper()\n'
    vpw__leys += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    ure__fto = {}
    exec(vpw__leys, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': dfyo__asrv, 'get_search_regex':
        get_search_regex}, ure__fto)
    impl = ure__fto['impl']
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
    vpw__leys = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    vpw__leys += '  S = S_str._obj\n'
    vpw__leys += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    vpw__leys += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    vpw__leys += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    vpw__leys += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        vpw__leys += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})\n'
            )
    if S_str.stype.data == bodo.dict_str_arr_type and all(frygq__kfza ==
        bodo.dict_str_arr_type for frygq__kfza in others.data):
        yfbj__mqux = ', '.join(f'data{i}' for i in range(len(others.columns)))
        vpw__leys += (
            f'  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {yfbj__mqux}), sep)\n'
            )
    else:
        gqgje__jautc = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        vpw__leys += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        vpw__leys += '  numba.parfors.parfor.init_prange()\n'
        vpw__leys += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        vpw__leys += f'      if {gqgje__jautc}:\n'
        vpw__leys += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        vpw__leys += '          continue\n'
        afa__qezp = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        sbsm__xrs = "''" if is_overload_none(sep) else 'sep'
        vpw__leys += f'      out_arr[i] = {sbsm__xrs}.join([{afa__qezp}])\n'
    vpw__leys += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    ure__fto = {}
    exec(vpw__leys, {'bodo': bodo, 'numba': numba}, ure__fto)
    impl = ure__fto['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        sdw__zxx = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(ietev__amw, np.int64)
        for i in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(sdw__zxx, ltcpe__gii[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return impl


@overload_method(SeriesStrMethodType, 'find', inline='always', no_unliteral
    =True)
def overload_str_method_find(S_str, sub, start=0, end=None):
    str_arg_check('find', 'sub', sub)
    int_arg_check('find', 'start', start)
    if not is_overload_none(end):
        int_arg_check('find', 'end', end)

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(ietev__amw, np.int64)
        for i in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ltcpe__gii[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
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
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(ietev__amw, np.int64)
        for i in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ltcpe__gii[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return impl


@overload_method(SeriesStrMethodType, 'center', inline='always',
    no_unliteral=True)
def overload_str_method_center(S_str, width, fillchar=' '):
    common_validate_padding('center', width, fillchar)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_center_dict_impl(S_str, width, fillchar=' '):
            S = S_str._obj
            nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
            orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
            hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_center(nolta__jxpve, width,
                fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                orca__zxhtt, hanuh__lbp)
        return _str_center_dict_impl

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(ietev__amw, -1)
        for gktp__blm in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, gktp__blm):
                out_arr[gktp__blm] = ''
                bodo.libs.array_kernels.setna(out_arr, gktp__blm)
            else:
                out_arr[gktp__blm] = ltcpe__gii[gktp__blm].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
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
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(ietev__amw, -1)
        for gktp__blm in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, gktp__blm):
                bodo.libs.array_kernels.setna(out_arr, gktp__blm)
            else:
                if stop is not None:
                    kjp__ukal = ltcpe__gii[gktp__blm][stop:]
                else:
                    kjp__ukal = ''
                out_arr[gktp__blm] = ltcpe__gii[gktp__blm][:start
                    ] + repl + kjp__ukal
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):

        def impl(S_str, repeats):
            S = S_str._obj
            ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
            hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
            orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            ietev__amw = len(ltcpe__gii)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(ietev__amw,
                -1)
            for gktp__blm in numba.parfors.parfor.internal_prange(ietev__amw):
                if bodo.libs.array_kernels.isna(ltcpe__gii, gktp__blm):
                    bodo.libs.array_kernels.setna(out_arr, gktp__blm)
                else:
                    out_arr[gktp__blm] = ltcpe__gii[gktp__blm] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                orca__zxhtt, hanuh__lbp)
        return impl
    elif is_overload_constant_list(repeats):
        rtaui__wdqda = get_overload_const_list(repeats)
        mpv__woc = all([isinstance(zmsu__rgcx, int) for zmsu__rgcx in
            rtaui__wdqda])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        mpv__woc = True
    else:
        mpv__woc = False
    if mpv__woc:

        def impl(S_str, repeats):
            S = S_str._obj
            ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
            hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
            orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
            dvss__bfoy = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            ietev__amw = len(ltcpe__gii)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(ietev__amw,
                -1)
            for gktp__blm in numba.parfors.parfor.internal_prange(ietev__amw):
                if bodo.libs.array_kernels.isna(ltcpe__gii, gktp__blm):
                    bodo.libs.array_kernels.setna(out_arr, gktp__blm)
                else:
                    out_arr[gktp__blm] = ltcpe__gii[gktp__blm] * dvss__bfoy[
                        gktp__blm]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                orca__zxhtt, hanuh__lbp)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


@overload_method(SeriesStrMethodType, 'ljust', inline='always',
    no_unliteral=True)
def overload_str_method_ljust(S_str, width, fillchar=' '):
    common_validate_padding('ljust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(ietev__amw, -1)
        for gktp__blm in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, gktp__blm):
                out_arr[gktp__blm] = ''
                bodo.libs.array_kernels.setna(out_arr, gktp__blm)
            else:
                out_arr[gktp__blm] = ltcpe__gii[gktp__blm].ljust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return impl


@overload_method(SeriesStrMethodType, 'rjust', inline='always',
    no_unliteral=True)
def overload_str_method_rjust(S_str, width, fillchar=' '):
    common_validate_padding('rjust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(ietev__amw, -1)
        for gktp__blm in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, gktp__blm):
                out_arr[gktp__blm] = ''
                bodo.libs.array_kernels.setna(out_arr, gktp__blm)
            else:
                out_arr[gktp__blm] = ltcpe__gii[gktp__blm].rjust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return impl


@overload_method(SeriesStrMethodType, 'pad', no_unliteral=True)
def overload_str_method_pad(S_str, width, side='left', fillchar=' '):
    common_validate_padding('pad', width, fillchar)
    if is_overload_constant_str(side):
        if get_overload_const_str(side) not in ['left', 'right', 'both']:
            raise BodoError('Series.str.pad(): Invalid Side')
    else:
        raise BodoError('Series.str.pad(): Invalid Side')

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(ietev__amw, -1)
        for gktp__blm in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, gktp__blm):
                out_arr[gktp__blm] = ''
                bodo.libs.array_kernels.setna(out_arr, gktp__blm)
            elif side == 'left':
                out_arr[gktp__blm] = ltcpe__gii[gktp__blm].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[gktp__blm] = ltcpe__gii[gktp__blm].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[gktp__blm] = ltcpe__gii[gktp__blm].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)

    def impl(S_str, width):
        S = S_str._obj
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(ietev__amw, -1)
        for gktp__blm in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, gktp__blm):
                out_arr[gktp__blm] = ''
                bodo.libs.array_kernels.setna(out_arr, gktp__blm)
            else:
                out_arr[gktp__blm] = ltcpe__gii[gktp__blm].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return impl


@overload_method(SeriesStrMethodType, 'slice', no_unliteral=True)
def overload_str_method_slice(S_str, start=None, stop=None, step=None):
    if not is_overload_none(start):
        int_arg_check('slice', 'start', start)
    if not is_overload_none(stop):
        int_arg_check('slice', 'stop', stop)
    if not is_overload_none(step):
        int_arg_check('slice', 'step', step)

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(ietev__amw, -1)
        for gktp__blm in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, gktp__blm):
                out_arr[gktp__blm] = ''
                bodo.libs.array_kernels.setna(out_arr, gktp__blm)
            else:
                out_arr[gktp__blm] = ltcpe__gii[gktp__blm][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
            orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
            hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(nolta__jxpve,
                pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                orca__zxhtt, hanuh__lbp)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(ietev__amw)
        for i in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ltcpe__gii[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
            orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
            hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(nolta__jxpve, pat, na
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                orca__zxhtt, hanuh__lbp)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        ltcpe__gii = bodo.hiframes.pd_series_ext.get_series_data(S)
        hanuh__lbp = bodo.hiframes.pd_series_ext.get_series_name(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        ietev__amw = len(ltcpe__gii)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(ietev__amw)
        for i in numba.parfors.parfor.internal_prange(ietev__amw):
            if bodo.libs.array_kernels.isna(ltcpe__gii, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = ltcpe__gii[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, orca__zxhtt,
            hanuh__lbp)
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
    inyg__wqs, regex = _get_column_names_from_regex(pat, flags, 'extract')
    ysel__ribit = len(inyg__wqs)
    vpw__leys = 'def impl(S_str, pat, flags=0, expand=True):\n'
    vpw__leys += '  regex = re.compile(pat, flags=flags)\n'
    vpw__leys += '  S = S_str._obj\n'
    vpw__leys += '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    vpw__leys += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    vpw__leys += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    vpw__leys += '  numba.parfors.parfor.init_prange()\n'
    vpw__leys += '  n = len(str_arr)\n'
    for i in range(ysel__ribit):
        vpw__leys += (
            '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
            .format(i))
    vpw__leys += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    vpw__leys += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    for i in range(ysel__ribit):
        vpw__leys += "          out_arr_{}[j] = ''\n".format(i)
        vpw__leys += (
            '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    vpw__leys += '      else:\n'
    vpw__leys += '          m = regex.search(str_arr[j])\n'
    vpw__leys += '          if m:\n'
    vpw__leys += '            g = m.groups()\n'
    for i in range(ysel__ribit):
        vpw__leys += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
    vpw__leys += '          else:\n'
    for i in range(ysel__ribit):
        vpw__leys += "            out_arr_{}[j] = ''\n".format(i)
        vpw__leys += (
            '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    if is_overload_false(expand) and regex.groups == 1:
        hanuh__lbp = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        vpw__leys += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(hanuh__lbp))
        ure__fto = {}
        exec(vpw__leys, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, ure__fto)
        impl = ure__fto['impl']
        return impl
    ibuli__ydf = ', '.join('out_arr_{}'.format(i) for i in range(ysel__ribit))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(vpw__leys, inyg__wqs,
        ibuli__ydf, 'index', extra_globals={'get_utf8_size': get_utf8_size,
        're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    inyg__wqs, jfyn__chapd = _get_column_names_from_regex(pat, flags,
        'extractall')
    ysel__ribit = len(inyg__wqs)
    hqkc__sps = isinstance(S_str.stype.index, StringIndexType)
    vpw__leys = 'def impl(S_str, pat, flags=0):\n'
    vpw__leys += '  regex = re.compile(pat, flags=flags)\n'
    vpw__leys += '  S = S_str._obj\n'
    vpw__leys += '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    vpw__leys += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    vpw__leys += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    vpw__leys += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    vpw__leys += (
        '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n')
    vpw__leys += '  numba.parfors.parfor.init_prange()\n'
    vpw__leys += '  n = len(str_arr)\n'
    vpw__leys += '  out_n_l = [0]\n'
    for i in range(ysel__ribit):
        vpw__leys += '  num_chars_{} = 0\n'.format(i)
    if hqkc__sps:
        vpw__leys += '  index_num_chars = 0\n'
    vpw__leys += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    if hqkc__sps:
        vpw__leys += '      index_num_chars += get_utf8_size(index_arr[i])\n'
    vpw__leys += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
    vpw__leys += '          continue\n'
    vpw__leys += '      m = regex.findall(str_arr[i])\n'
    vpw__leys += '      out_n_l[0] += len(m)\n'
    for i in range(ysel__ribit):
        vpw__leys += '      l_{} = 0\n'.format(i)
    vpw__leys += '      for s in m:\n'
    for i in range(ysel__ribit):
        vpw__leys += '        l_{} += get_utf8_size(s{})\n'.format(i, 
            '[{}]'.format(i) if ysel__ribit > 1 else '')
    for i in range(ysel__ribit):
        vpw__leys += '      num_chars_{0} += l_{0}\n'.format(i)
    vpw__leys += (
        '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
        )
    for i in range(ysel__ribit):
        vpw__leys += (
            """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
            .format(i))
    if hqkc__sps:
        vpw__leys += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
    else:
        vpw__leys += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
    vpw__leys += '  out_match_arr = np.empty(out_n, np.int64)\n'
    vpw__leys += '  out_ind = 0\n'
    vpw__leys += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    vpw__leys += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    vpw__leys += '          continue\n'
    vpw__leys += '      m = regex.findall(str_arr[j])\n'
    vpw__leys += '      for k, s in enumerate(m):\n'
    for i in range(ysel__ribit):
        vpw__leys += (
            '        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})\n'
            .format(i, '[{}]'.format(i) if ysel__ribit > 1 else ''))
    vpw__leys += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
    vpw__leys += (
        '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
        )
    vpw__leys += '        out_ind += 1\n'
    vpw__leys += (
        '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n')
    vpw__leys += "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n"
    ibuli__ydf = ', '.join('out_arr_{}'.format(i) for i in range(ysel__ribit))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(vpw__leys, inyg__wqs,
        ibuli__ydf, 'out_index', extra_globals={'get_utf8_size':
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
    ggwbp__pboke = dict(zip(regex.groupindex.values(), regex.groupindex.keys())
        )
    inyg__wqs = [ggwbp__pboke.get(1 + i, i) for i in range(regex.groups)]
    return inyg__wqs, regex


def create_str2str_methods_overload(func_name):
    if func_name in ['lstrip', 'rstrip', 'strip']:
        vpw__leys = 'def f(S_str, to_strip=None):\n'
    else:
        vpw__leys = 'def f(S_str):\n'
    vpw__leys += '    S = S_str._obj\n'
    vpw__leys += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    vpw__leys += '    str_arr = decode_if_dict_array(str_arr)\n'
    vpw__leys += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    vpw__leys += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    vpw__leys += '    numba.parfors.parfor.init_prange()\n'
    vpw__leys += '    n = len(str_arr)\n'
    if func_name in ('capitalize', 'lower', 'swapcase', 'title', 'upper'):
        vpw__leys += '    num_chars = num_total_chars(str_arr)\n'
    else:
        vpw__leys += '    num_chars = -1\n'
    vpw__leys += (
        '    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)\n'
        )
    vpw__leys += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    vpw__leys += '        if bodo.libs.array_kernels.isna(str_arr, j):\n'
    vpw__leys += '            out_arr[j] = ""\n'
    vpw__leys += '            bodo.libs.array_kernels.setna(out_arr, j)\n'
    vpw__leys += '        else:\n'
    if func_name in ['lstrip', 'rstrip', 'strip']:
        vpw__leys += ('            out_arr[j] = str_arr[j].{}(to_strip)\n'.
            format(func_name))
    else:
        vpw__leys += '            out_arr[j] = str_arr[j].{}()\n'.format(
            func_name)
    vpw__leys += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    vpw__leys += 'def _dict_impl(S_str):\n'
    vpw__leys += '    S = S_str._obj\n'
    vpw__leys += '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    vpw__leys += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    vpw__leys += '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    vpw__leys += f'    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr)\n'
    vpw__leys += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    ure__fto = {}
    exec(vpw__leys, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo.
        libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, ure__fto)
    zpsl__iwuxf = ure__fto['f']
    xxjx__juxz = ure__fto['_dict_impl']
    if func_name in ['lstrip', 'rstrip', 'strip']:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            return zpsl__iwuxf
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return xxjx__juxz
            return zpsl__iwuxf
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):

    def overload_str2bool_methods(S_str):
        vpw__leys = 'def f(S_str):\n'
        vpw__leys += '    S = S_str._obj\n'
        vpw__leys += (
            '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        vpw__leys += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        vpw__leys += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        vpw__leys += '    numba.parfors.parfor.init_prange()\n'
        vpw__leys += '    l = len(str_arr)\n'
        vpw__leys += (
            '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        vpw__leys += '    for i in numba.parfors.parfor.internal_prange(l):\n'
        vpw__leys += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
        vpw__leys += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        vpw__leys += '        else:\n'
        vpw__leys += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
            .format(func_name))
        vpw__leys += '    return bodo.hiframes.pd_series_ext.init_series(\n'
        vpw__leys += '      out_arr,index, name)\n'
        ure__fto = {}
        exec(vpw__leys, {'bodo': bodo, 'numba': numba, 'np': np}, ure__fto)
        zpsl__iwuxf = ure__fto['f']
        return zpsl__iwuxf
    return overload_str2bool_methods


def _install_str2str_methods():
    for prx__hnj in bodo.hiframes.pd_series_ext.str2str_methods:
        ebm__ihahy = create_str2str_methods_overload(prx__hnj)
        overload_method(SeriesStrMethodType, prx__hnj, inline='always',
            no_unliteral=True)(ebm__ihahy)


def _install_str2bool_methods():
    for prx__hnj in bodo.hiframes.pd_series_ext.str2bool_methods:
        ebm__ihahy = create_str2bool_methods_overload(prx__hnj)
        overload_method(SeriesStrMethodType, prx__hnj, inline='always',
            no_unliteral=True)(ebm__ihahy)


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
        hanuh__lbp = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(hanuh__lbp)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        qtmtq__aupv = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, qtmtq__aupv)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        kajc__qirwj, = args
        azdj__wet = signature.return_type
        ari__klz = cgutils.create_struct_proxy(azdj__wet)(context, builder)
        ari__klz.obj = kajc__qirwj
        context.nrt.incref(builder, signature.args[0], kajc__qirwj)
        return ari__klz._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        nolta__jxpve = bodo.hiframes.pd_series_ext.get_series_data(S)
        orca__zxhtt = bodo.hiframes.pd_series_ext.get_series_index(S)
        hanuh__lbp = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(nolta__jxpve),
            orca__zxhtt, hanuh__lbp)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for uxw__niez in unsupported_cat_attrs:
        lky__xszyb = 'Series.cat.' + uxw__niez
        overload_attribute(SeriesCatMethodType, uxw__niez)(
            create_unsupported_overload(lky__xszyb))
    for myfz__zdd in unsupported_cat_methods:
        lky__xszyb = 'Series.cat.' + myfz__zdd
        overload_method(SeriesCatMethodType, myfz__zdd)(
            create_unsupported_overload(lky__xszyb))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for myfz__zdd in unsupported_str_methods:
        lky__xszyb = 'Series.str.' + myfz__zdd
        overload_method(SeriesStrMethodType, myfz__zdd)(
            create_unsupported_overload(lky__xszyb))


_install_strseries_unsupported()
