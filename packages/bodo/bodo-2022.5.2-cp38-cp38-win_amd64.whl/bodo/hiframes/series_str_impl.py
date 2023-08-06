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
        aiof__tjy = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(aiof__tjy)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gvf__rtgm = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, gvf__rtgm)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        endn__knbk, = args
        kxz__vbtm = signature.return_type
        wjww__kcy = cgutils.create_struct_proxy(kxz__vbtm)(context, builder)
        wjww__kcy.obj = endn__knbk
        context.nrt.incref(builder, signature.args[0], endn__knbk)
        return wjww__kcy._getvalue()
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
        rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(rlgcs__effxv, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
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
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(rlgcs__effxv,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(rlgcs__effxv, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    tdoa__yit = S_str.stype.data
    if (tdoa__yit != string_array_split_view_type and not is_str_arr_type(
        tdoa__yit)) and not isinstance(tdoa__yit, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(tdoa__yit, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(rlgcs__effxv, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_get_array_impl
    if tdoa__yit == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(rlgcs__effxv)
            fog__uzkht = 0
            for ymn__ypd in numba.parfors.parfor.internal_prange(n):
                ozgcs__yfg, ozgcs__yfg, tbjka__znqrl = get_split_view_index(
                    rlgcs__effxv, ymn__ypd, i)
                fog__uzkht += tbjka__znqrl
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, fog__uzkht)
            for cet__cnitg in numba.parfors.parfor.internal_prange(n):
                lfxa__kkr, zbijq__ljf, tbjka__znqrl = get_split_view_index(
                    rlgcs__effxv, cet__cnitg, i)
                if lfxa__kkr == 0:
                    bodo.libs.array_kernels.setna(out_arr, cet__cnitg)
                    lupdx__jyupp = get_split_view_data_ptr(rlgcs__effxv, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        cet__cnitg)
                    lupdx__jyupp = get_split_view_data_ptr(rlgcs__effxv,
                        zbijq__ljf)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    cet__cnitg, lupdx__jyupp, tbjka__znqrl)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(rlgcs__effxv, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(rlgcs__effxv)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for cet__cnitg in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(rlgcs__effxv, cet__cnitg
                ) or not len(rlgcs__effxv[cet__cnitg]) > i >= -len(rlgcs__effxv
                [cet__cnitg]):
                out_arr[cet__cnitg] = ''
                bodo.libs.array_kernels.setna(out_arr, cet__cnitg)
            else:
                out_arr[cet__cnitg] = rlgcs__effxv[cet__cnitg][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    tdoa__yit = S_str.stype.data
    if (tdoa__yit != string_array_split_view_type and tdoa__yit !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(
        tdoa__yit)):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(xpj__uhc)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for cet__cnitg in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(xpj__uhc, cet__cnitg):
                out_arr[cet__cnitg] = ''
                bodo.libs.array_kernels.setna(out_arr, cet__cnitg)
            else:
                mitij__mevdz = xpj__uhc[cet__cnitg]
                out_arr[cet__cnitg] = sep.join(mitij__mevdz)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
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
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(rlgcs__effxv, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            qjlji__tniw = re.compile(pat, flags)
            utyg__ougvk = len(rlgcs__effxv)
            out_arr = pre_alloc_string_array(utyg__ougvk, -1)
            for cet__cnitg in numba.parfors.parfor.internal_prange(utyg__ougvk
                ):
                if bodo.libs.array_kernels.isna(rlgcs__effxv, cet__cnitg):
                    out_arr[cet__cnitg] = ''
                    bodo.libs.array_kernels.setna(out_arr, cet__cnitg)
                    continue
                out_arr[cet__cnitg] = qjlji__tniw.sub(repl, rlgcs__effxv[
                    cet__cnitg])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        utyg__ougvk = len(rlgcs__effxv)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(utyg__ougvk, -1)
        for cet__cnitg in numba.parfors.parfor.internal_prange(utyg__ougvk):
            if bodo.libs.array_kernels.isna(rlgcs__effxv, cet__cnitg):
                out_arr[cet__cnitg] = ''
                bodo.libs.array_kernels.setna(out_arr, cet__cnitg)
                continue
            out_arr[cet__cnitg] = rlgcs__effxv[cet__cnitg].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


def is_regex_unsupported(pat):
    ddw__zsp = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(ifc__brk in pat) for ifc__brk in ddw__zsp])
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
    muf__oygyu = re.IGNORECASE.value
    moj__obqw = 'def impl(\n'
    moj__obqw += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    moj__obqw += '):\n'
    moj__obqw += '  S = S_str._obj\n'
    moj__obqw += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    moj__obqw += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    moj__obqw += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    moj__obqw += '  l = len(arr)\n'
    moj__obqw += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                moj__obqw += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                moj__obqw += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            moj__obqw += """  get_search_regex(arr, case, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        moj__obqw += (
            '  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)\n'
            )
    else:
        moj__obqw += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            moj__obqw += '  upper_pat = pat.upper()\n'
        moj__obqw += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        moj__obqw += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        moj__obqw += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        moj__obqw += '      else: \n'
        if is_overload_true(case):
            moj__obqw += '          out_arr[i] = pat in arr[i]\n'
        else:
            moj__obqw += '          out_arr[i] = upper_pat in arr[i].upper()\n'
    moj__obqw += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    nowrg__sbjmu = {}
    exec(moj__obqw, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': muf__oygyu, 'get_search_regex':
        get_search_regex}, nowrg__sbjmu)
    impl = nowrg__sbjmu['impl']
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
    moj__obqw = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    moj__obqw += '  S = S_str._obj\n'
    moj__obqw += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    moj__obqw += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    moj__obqw += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    moj__obqw += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        moj__obqw += (
            f'  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})\n'
            )
    if S_str.stype.data == bodo.dict_str_arr_type and all(vwmnf__jkmar ==
        bodo.dict_str_arr_type for vwmnf__jkmar in others.data):
        zdlki__cjddn = ', '.join(f'data{i}' for i in range(len(others.columns))
            )
        moj__obqw += f"""  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {zdlki__cjddn}), sep)
"""
    else:
        yjh__ekag = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        moj__obqw += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        moj__obqw += '  numba.parfors.parfor.init_prange()\n'
        moj__obqw += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        moj__obqw += f'      if {yjh__ekag}:\n'
        moj__obqw += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        moj__obqw += '          continue\n'
        unyg__ikda = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        glzc__uicc = "''" if is_overload_none(sep) else 'sep'
        moj__obqw += f'      out_arr[i] = {glzc__uicc}.join([{unyg__ikda}])\n'
    moj__obqw += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    nowrg__sbjmu = {}
    exec(moj__obqw, {'bodo': bodo, 'numba': numba}, nowrg__sbjmu)
    impl = nowrg__sbjmu['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        qjlji__tniw = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        utyg__ougvk = len(xpj__uhc)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(utyg__ougvk, np.int64)
        for i in numba.parfors.parfor.internal_prange(utyg__ougvk):
            if bodo.libs.array_kernels.isna(xpj__uhc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(qjlji__tniw, xpj__uhc[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
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
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(rlgcs__effxv, sub,
                start, end)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        utyg__ougvk = len(xpj__uhc)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(utyg__ougvk, np.int64)
        for i in numba.parfors.parfor.internal_prange(utyg__ougvk):
            if bodo.libs.array_kernels.isna(xpj__uhc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = xpj__uhc[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
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
        xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        utyg__ougvk = len(xpj__uhc)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(utyg__ougvk, np.int64)
        for i in numba.parfors.parfor.internal_prange(utyg__ougvk):
            if bodo.libs.array_kernels.isna(xpj__uhc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = xpj__uhc[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
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
        xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        utyg__ougvk = len(xpj__uhc)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(utyg__ougvk, -1)
        for cet__cnitg in numba.parfors.parfor.internal_prange(utyg__ougvk):
            if bodo.libs.array_kernels.isna(xpj__uhc, cet__cnitg):
                bodo.libs.array_kernels.setna(out_arr, cet__cnitg)
            else:
                if stop is not None:
                    wratr__llgc = xpj__uhc[cet__cnitg][stop:]
                else:
                    wratr__llgc = ''
                out_arr[cet__cnitg] = xpj__uhc[cet__cnitg][:start
                    ] + repl + wratr__llgc
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
                sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
                aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(rlgcs__effxv,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    sjmc__isays, aiof__tjy)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            utyg__ougvk = len(xpj__uhc)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(utyg__ougvk,
                -1)
            for cet__cnitg in numba.parfors.parfor.internal_prange(utyg__ougvk
                ):
                if bodo.libs.array_kernels.isna(xpj__uhc, cet__cnitg):
                    bodo.libs.array_kernels.setna(out_arr, cet__cnitg)
                else:
                    out_arr[cet__cnitg] = xpj__uhc[cet__cnitg] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return impl
    elif is_overload_constant_list(repeats):
        eavt__bcgu = get_overload_const_list(repeats)
        did__fos = all([isinstance(jxox__nzn, int) for jxox__nzn in eavt__bcgu]
            )
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        did__fos = True
    else:
        did__fos = False
    if did__fos:

        def impl(S_str, repeats):
            S = S_str._obj
            xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            nci__bdu = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            utyg__ougvk = len(xpj__uhc)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(utyg__ougvk,
                -1)
            for cet__cnitg in numba.parfors.parfor.internal_prange(utyg__ougvk
                ):
                if bodo.libs.array_kernels.isna(xpj__uhc, cet__cnitg):
                    bodo.libs.array_kernels.setna(out_arr, cet__cnitg)
                else:
                    out_arr[cet__cnitg] = xpj__uhc[cet__cnitg] * nci__bdu[
                        cet__cnitg]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    moj__obqw = f"""def dict_impl(S_str, width, fillchar=' '):
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
    nowrg__sbjmu = {}
    ndfy__tfjab = {'bodo': bodo, 'numba': numba}
    exec(moj__obqw, ndfy__tfjab, nowrg__sbjmu)
    impl = nowrg__sbjmu['impl']
    mfd__tdq = nowrg__sbjmu['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return mfd__tdq
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for cmh__llqlx in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(cmh__llqlx)
        overload_method(SeriesStrMethodType, cmh__llqlx, inline='always',
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
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(rlgcs__effxv,
                    width, fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(rlgcs__effxv,
                    width, fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(rlgcs__effxv,
                    width, fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        utyg__ougvk = len(xpj__uhc)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(utyg__ougvk, -1)
        for cet__cnitg in numba.parfors.parfor.internal_prange(utyg__ougvk):
            if bodo.libs.array_kernels.isna(xpj__uhc, cet__cnitg):
                out_arr[cet__cnitg] = ''
                bodo.libs.array_kernels.setna(out_arr, cet__cnitg)
            elif side == 'left':
                out_arr[cet__cnitg] = xpj__uhc[cet__cnitg].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[cet__cnitg] = xpj__uhc[cet__cnitg].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[cet__cnitg] = xpj__uhc[cet__cnitg].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(rlgcs__effxv, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        utyg__ougvk = len(xpj__uhc)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(utyg__ougvk, -1)
        for cet__cnitg in numba.parfors.parfor.internal_prange(utyg__ougvk):
            if bodo.libs.array_kernels.isna(xpj__uhc, cet__cnitg):
                out_arr[cet__cnitg] = ''
                bodo.libs.array_kernels.setna(out_arr, cet__cnitg)
            else:
                out_arr[cet__cnitg] = xpj__uhc[cet__cnitg].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
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
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(rlgcs__effxv, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        utyg__ougvk = len(xpj__uhc)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(utyg__ougvk, -1)
        for cet__cnitg in numba.parfors.parfor.internal_prange(utyg__ougvk):
            if bodo.libs.array_kernels.isna(xpj__uhc, cet__cnitg):
                out_arr[cet__cnitg] = ''
                bodo.libs.array_kernels.setna(out_arr, cet__cnitg)
            else:
                out_arr[cet__cnitg] = xpj__uhc[cet__cnitg][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(rlgcs__effxv,
                pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        utyg__ougvk = len(xpj__uhc)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(utyg__ougvk)
        for i in numba.parfors.parfor.internal_prange(utyg__ougvk):
            if bodo.libs.array_kernels.isna(xpj__uhc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = xpj__uhc[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
            sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
            aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(rlgcs__effxv, pat, na
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                sjmc__isays, aiof__tjy)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        xpj__uhc = bodo.hiframes.pd_series_ext.get_series_data(S)
        aiof__tjy = bodo.hiframes.pd_series_ext.get_series_name(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        utyg__ougvk = len(xpj__uhc)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(utyg__ougvk)
        for i in numba.parfors.parfor.internal_prange(utyg__ougvk):
            if bodo.libs.array_kernels.isna(xpj__uhc, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = xpj__uhc[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, sjmc__isays,
            aiof__tjy)
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
    lfo__vbw, regex = _get_column_names_from_regex(pat, flags, 'extract')
    pyhv__fnam = len(lfo__vbw)
    moj__obqw = 'def impl(S_str, pat, flags=0, expand=True):\n'
    moj__obqw += '  regex = re.compile(pat, flags=flags)\n'
    moj__obqw += '  S = S_str._obj\n'
    moj__obqw += '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    moj__obqw += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    moj__obqw += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    moj__obqw += '  numba.parfors.parfor.init_prange()\n'
    moj__obqw += '  n = len(str_arr)\n'
    for i in range(pyhv__fnam):
        moj__obqw += (
            '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
            .format(i))
    moj__obqw += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    moj__obqw += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    for i in range(pyhv__fnam):
        moj__obqw += "          out_arr_{}[j] = ''\n".format(i)
        moj__obqw += (
            '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    moj__obqw += '      else:\n'
    moj__obqw += '          m = regex.search(str_arr[j])\n'
    moj__obqw += '          if m:\n'
    moj__obqw += '            g = m.groups()\n'
    for i in range(pyhv__fnam):
        moj__obqw += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
    moj__obqw += '          else:\n'
    for i in range(pyhv__fnam):
        moj__obqw += "            out_arr_{}[j] = ''\n".format(i)
        moj__obqw += (
            '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    if is_overload_false(expand) and regex.groups == 1:
        aiof__tjy = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        moj__obqw += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(aiof__tjy))
        nowrg__sbjmu = {}
        exec(moj__obqw, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, nowrg__sbjmu)
        impl = nowrg__sbjmu['impl']
        return impl
    sfcd__mdd = ', '.join('out_arr_{}'.format(i) for i in range(pyhv__fnam))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(moj__obqw, lfo__vbw,
        sfcd__mdd, 'index', extra_globals={'get_utf8_size': get_utf8_size,
        're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    lfo__vbw, ozgcs__yfg = _get_column_names_from_regex(pat, flags,
        'extractall')
    pyhv__fnam = len(lfo__vbw)
    npxvy__qpz = isinstance(S_str.stype.index, StringIndexType)
    moj__obqw = 'def impl(S_str, pat, flags=0):\n'
    moj__obqw += '  regex = re.compile(pat, flags=flags)\n'
    moj__obqw += '  S = S_str._obj\n'
    moj__obqw += '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    moj__obqw += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    moj__obqw += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    moj__obqw += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    moj__obqw += (
        '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n')
    moj__obqw += '  numba.parfors.parfor.init_prange()\n'
    moj__obqw += '  n = len(str_arr)\n'
    moj__obqw += '  out_n_l = [0]\n'
    for i in range(pyhv__fnam):
        moj__obqw += '  num_chars_{} = 0\n'.format(i)
    if npxvy__qpz:
        moj__obqw += '  index_num_chars = 0\n'
    moj__obqw += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    if npxvy__qpz:
        moj__obqw += '      index_num_chars += get_utf8_size(index_arr[i])\n'
    moj__obqw += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
    moj__obqw += '          continue\n'
    moj__obqw += '      m = regex.findall(str_arr[i])\n'
    moj__obqw += '      out_n_l[0] += len(m)\n'
    for i in range(pyhv__fnam):
        moj__obqw += '      l_{} = 0\n'.format(i)
    moj__obqw += '      for s in m:\n'
    for i in range(pyhv__fnam):
        moj__obqw += '        l_{} += get_utf8_size(s{})\n'.format(i, 
            '[{}]'.format(i) if pyhv__fnam > 1 else '')
    for i in range(pyhv__fnam):
        moj__obqw += '      num_chars_{0} += l_{0}\n'.format(i)
    moj__obqw += (
        '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
        )
    for i in range(pyhv__fnam):
        moj__obqw += (
            """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
            .format(i))
    if npxvy__qpz:
        moj__obqw += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
    else:
        moj__obqw += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
    moj__obqw += '  out_match_arr = np.empty(out_n, np.int64)\n'
    moj__obqw += '  out_ind = 0\n'
    moj__obqw += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    moj__obqw += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    moj__obqw += '          continue\n'
    moj__obqw += '      m = regex.findall(str_arr[j])\n'
    moj__obqw += '      for k, s in enumerate(m):\n'
    for i in range(pyhv__fnam):
        moj__obqw += (
            '        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})\n'
            .format(i, '[{}]'.format(i) if pyhv__fnam > 1 else ''))
    moj__obqw += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
    moj__obqw += (
        '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
        )
    moj__obqw += '        out_ind += 1\n'
    moj__obqw += (
        '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n')
    moj__obqw += "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n"
    sfcd__mdd = ', '.join('out_arr_{}'.format(i) for i in range(pyhv__fnam))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(moj__obqw, lfo__vbw,
        sfcd__mdd, 'out_index', extra_globals={'get_utf8_size':
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
    flyn__hlgs = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    lfo__vbw = [flyn__hlgs.get(1 + i, i) for i in range(regex.groups)]
    return lfo__vbw, regex


def create_str2str_methods_overload(func_name):
    oog__rqvw = func_name in ['lstrip', 'rstrip', 'strip']
    moj__obqw = f"""def f({'S_str, to_strip=None' if oog__rqvw else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if oog__rqvw else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if oog__rqvw else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    moj__obqw += f"""def _dict_impl({'S_str, to_strip=None' if oog__rqvw else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if oog__rqvw else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    nowrg__sbjmu = {}
    exec(moj__obqw, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo.
        libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, nowrg__sbjmu)
    sjt__bxx = nowrg__sbjmu['f']
    yvqyk__seotl = nowrg__sbjmu['_dict_impl']
    if oog__rqvw:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return yvqyk__seotl
            return sjt__bxx
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return yvqyk__seotl
            return sjt__bxx
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):

    def overload_str2bool_methods(S_str):
        moj__obqw = 'def f(S_str):\n'
        moj__obqw += '    S = S_str._obj\n'
        moj__obqw += (
            '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        moj__obqw += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        moj__obqw += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        moj__obqw += '    numba.parfors.parfor.init_prange()\n'
        moj__obqw += '    l = len(str_arr)\n'
        moj__obqw += (
            '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        moj__obqw += '    for i in numba.parfors.parfor.internal_prange(l):\n'
        moj__obqw += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
        moj__obqw += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        moj__obqw += '        else:\n'
        moj__obqw += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
            .format(func_name))
        moj__obqw += '    return bodo.hiframes.pd_series_ext.init_series(\n'
        moj__obqw += '      out_arr,index, name)\n'
        nowrg__sbjmu = {}
        exec(moj__obqw, {'bodo': bodo, 'numba': numba, 'np': np}, nowrg__sbjmu)
        sjt__bxx = nowrg__sbjmu['f']
        return sjt__bxx
    return overload_str2bool_methods


def _install_str2str_methods():
    for pvhh__aqn in bodo.hiframes.pd_series_ext.str2str_methods:
        tbth__zfczy = create_str2str_methods_overload(pvhh__aqn)
        overload_method(SeriesStrMethodType, pvhh__aqn, inline='always',
            no_unliteral=True)(tbth__zfczy)


def _install_str2bool_methods():
    for pvhh__aqn in bodo.hiframes.pd_series_ext.str2bool_methods:
        tbth__zfczy = create_str2bool_methods_overload(pvhh__aqn)
        overload_method(SeriesStrMethodType, pvhh__aqn, inline='always',
            no_unliteral=True)(tbth__zfczy)


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
        aiof__tjy = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(aiof__tjy)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        gvf__rtgm = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, gvf__rtgm)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        endn__knbk, = args
        islfz__aeeqf = signature.return_type
        ttdkf__vzxm = cgutils.create_struct_proxy(islfz__aeeqf)(context,
            builder)
        ttdkf__vzxm.obj = endn__knbk
        context.nrt.incref(builder, signature.args[0], endn__knbk)
        return ttdkf__vzxm._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        rlgcs__effxv = bodo.hiframes.pd_series_ext.get_series_data(S)
        sjmc__isays = bodo.hiframes.pd_series_ext.get_series_index(S)
        aiof__tjy = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(rlgcs__effxv),
            sjmc__isays, aiof__tjy)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for mkna__hef in unsupported_cat_attrs:
        tcu__fxfqg = 'Series.cat.' + mkna__hef
        overload_attribute(SeriesCatMethodType, mkna__hef)(
            create_unsupported_overload(tcu__fxfqg))
    for regss__pvbr in unsupported_cat_methods:
        tcu__fxfqg = 'Series.cat.' + regss__pvbr
        overload_method(SeriesCatMethodType, regss__pvbr)(
            create_unsupported_overload(tcu__fxfqg))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for regss__pvbr in unsupported_str_methods:
        tcu__fxfqg = 'Series.str.' + regss__pvbr
        overload_method(SeriesStrMethodType, regss__pvbr)(
            create_unsupported_overload(tcu__fxfqg))


_install_strseries_unsupported()
