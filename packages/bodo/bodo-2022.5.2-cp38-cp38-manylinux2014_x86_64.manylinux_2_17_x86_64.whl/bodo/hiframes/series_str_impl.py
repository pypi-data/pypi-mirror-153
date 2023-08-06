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
        tru__rqa = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(tru__rqa)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        feafo__fpn = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, feafo__fpn)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        swuth__enj, = args
        bvbc__elcy = signature.return_type
        orvp__hhb = cgutils.create_struct_proxy(bvbc__elcy)(context, builder)
        orvp__hhb.obj = swuth__enj
        context.nrt.incref(builder, signature.args[0], swuth__enj)
        return orvp__hhb._getvalue()
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
        nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(nqq__okt, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
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
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(nqq__okt, pat
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(nqq__okt, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    wnx__yzt = S_str.stype.data
    if (wnx__yzt != string_array_split_view_type and not is_str_arr_type(
        wnx__yzt)) and not isinstance(wnx__yzt, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(wnx__yzt, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(nqq__okt, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_get_array_impl
    if wnx__yzt == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(nqq__okt)
            hlj__wwocr = 0
            for pvuq__iuim in numba.parfors.parfor.internal_prange(n):
                puaq__pdsy, puaq__pdsy, dcnb__dqpik = get_split_view_index(
                    nqq__okt, pvuq__iuim, i)
                hlj__wwocr += dcnb__dqpik
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, hlj__wwocr)
            for qdsne__duf in numba.parfors.parfor.internal_prange(n):
                udqmy__rnky, dwjp__zoni, dcnb__dqpik = get_split_view_index(
                    nqq__okt, qdsne__duf, i)
                if udqmy__rnky == 0:
                    bodo.libs.array_kernels.setna(out_arr, qdsne__duf)
                    enygr__vfpum = get_split_view_data_ptr(nqq__okt, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        qdsne__duf)
                    enygr__vfpum = get_split_view_data_ptr(nqq__okt, dwjp__zoni
                        )
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    qdsne__duf, enygr__vfpum, dcnb__dqpik)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_get_split_impl
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_get_dict_impl(S_str, i):
            S = S_str._obj
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_get(nqq__okt, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_get_dict_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(nqq__okt)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for qdsne__duf in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(nqq__okt, qdsne__duf) or not len(
                nqq__okt[qdsne__duf]) > i >= -len(nqq__okt[qdsne__duf]):
                out_arr[qdsne__duf] = ''
                bodo.libs.array_kernels.setna(out_arr, qdsne__duf)
            else:
                out_arr[qdsne__duf] = nqq__okt[qdsne__duf][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    wnx__yzt = S_str.stype.data
    if (wnx__yzt != string_array_split_view_type and wnx__yzt !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(wnx__yzt)
        ):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(lys__hjhwy)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for qdsne__duf in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(lys__hjhwy, qdsne__duf):
                out_arr[qdsne__duf] = ''
                bodo.libs.array_kernels.setna(out_arr, qdsne__duf)
            else:
                enfq__ixxal = lys__hjhwy[qdsne__duf]
                out_arr[qdsne__duf] = sep.join(enfq__ixxal)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
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
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(nqq__okt, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            seuz__yed = re.compile(pat, flags)
            pdupx__xwga = len(nqq__okt)
            out_arr = pre_alloc_string_array(pdupx__xwga, -1)
            for qdsne__duf in numba.parfors.parfor.internal_prange(pdupx__xwga
                ):
                if bodo.libs.array_kernels.isna(nqq__okt, qdsne__duf):
                    out_arr[qdsne__duf] = ''
                    bodo.libs.array_kernels.setna(out_arr, qdsne__duf)
                    continue
                out_arr[qdsne__duf] = seuz__yed.sub(repl, nqq__okt[qdsne__duf])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        pdupx__xwga = len(nqq__okt)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(pdupx__xwga, -1)
        for qdsne__duf in numba.parfors.parfor.internal_prange(pdupx__xwga):
            if bodo.libs.array_kernels.isna(nqq__okt, qdsne__duf):
                out_arr[qdsne__duf] = ''
                bodo.libs.array_kernels.setna(out_arr, qdsne__duf)
                continue
            out_arr[qdsne__duf] = nqq__okt[qdsne__duf].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


def is_regex_unsupported(pat):
    ksc__yefb = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(sduw__utjd in pat) for sduw__utjd in ksc__yefb])
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
    lfyf__dkdn = re.IGNORECASE.value
    cqyes__qik = 'def impl(\n'
    cqyes__qik += '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n'
    cqyes__qik += '):\n'
    cqyes__qik += '  S = S_str._obj\n'
    cqyes__qik += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    cqyes__qik += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    cqyes__qik += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    cqyes__qik += '  l = len(arr)\n'
    cqyes__qik += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                cqyes__qik += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                cqyes__qik += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            cqyes__qik += """  get_search_regex(arr, case, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        cqyes__qik += (
            '  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)\n'
            )
    else:
        cqyes__qik += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            cqyes__qik += '  upper_pat = pat.upper()\n'
        cqyes__qik += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        cqyes__qik += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        cqyes__qik += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        cqyes__qik += '      else: \n'
        if is_overload_true(case):
            cqyes__qik += '          out_arr[i] = pat in arr[i]\n'
        else:
            cqyes__qik += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    cqyes__qik += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    xsq__rlwk = {}
    exec(cqyes__qik, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': lfyf__dkdn, 'get_search_regex':
        get_search_regex}, xsq__rlwk)
    impl = xsq__rlwk['impl']
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
    cqyes__qik = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    cqyes__qik += '  S = S_str._obj\n'
    cqyes__qik += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    cqyes__qik += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    cqyes__qik += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    cqyes__qik += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        cqyes__qik += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(ojmj__yslx ==
        bodo.dict_str_arr_type for ojmj__yslx in others.data):
        fuq__tkncq = ', '.join(f'data{i}' for i in range(len(others.columns)))
        cqyes__qik += (
            f'  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {fuq__tkncq}), sep)\n'
            )
    else:
        pqnc__azwo = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] +
            [f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len
            (others.columns))])
        cqyes__qik += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        cqyes__qik += '  numba.parfors.parfor.init_prange()\n'
        cqyes__qik += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        cqyes__qik += f'      if {pqnc__azwo}:\n'
        cqyes__qik += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        cqyes__qik += '          continue\n'
        lewwb__srymj = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range
            (len(others.columns))])
        hunu__stlz = "''" if is_overload_none(sep) else 'sep'
        cqyes__qik += (
            f'      out_arr[i] = {hunu__stlz}.join([{lewwb__srymj}])\n')
    cqyes__qik += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    xsq__rlwk = {}
    exec(cqyes__qik, {'bodo': bodo, 'numba': numba}, xsq__rlwk)
    impl = xsq__rlwk['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        seuz__yed = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        pdupx__xwga = len(lys__hjhwy)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(pdupx__xwga, np.int64)
        for i in numba.parfors.parfor.internal_prange(pdupx__xwga):
            if bodo.libs.array_kernels.isna(lys__hjhwy, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(seuz__yed, lys__hjhwy[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
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
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_find(nqq__okt, sub, start, end
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_find_dict_impl

    def impl(S_str, sub, start=0, end=None):
        S = S_str._obj
        lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pdupx__xwga = len(lys__hjhwy)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(pdupx__xwga, np.int64)
        for i in numba.parfors.parfor.internal_prange(pdupx__xwga):
            if bodo.libs.array_kernels.isna(lys__hjhwy, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = lys__hjhwy[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
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
        lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pdupx__xwga = len(lys__hjhwy)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(pdupx__xwga, np.int64)
        for i in numba.parfors.parfor.internal_prange(pdupx__xwga):
            if bodo.libs.array_kernels.isna(lys__hjhwy, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = lys__hjhwy[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
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
        lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pdupx__xwga = len(lys__hjhwy)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pdupx__xwga, -1)
        for qdsne__duf in numba.parfors.parfor.internal_prange(pdupx__xwga):
            if bodo.libs.array_kernels.isna(lys__hjhwy, qdsne__duf):
                bodo.libs.array_kernels.setna(out_arr, qdsne__duf)
            else:
                if stop is not None:
                    szc__ylzf = lys__hjhwy[qdsne__duf][stop:]
                else:
                    szc__ylzf = ''
                out_arr[qdsne__duf] = lys__hjhwy[qdsne__duf][:start
                    ] + repl + szc__ylzf
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):
        if S_str.stype.data == bodo.dict_str_arr_type:

            def _str_repeat_int_dict_impl(S_str, repeats):
                S = S_str._obj
                nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
                gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
                tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
                out_arr = bodo.libs.dict_arr_ext.str_repeat_int(nqq__okt,
                    repeats)
                return bodo.hiframes.pd_series_ext.init_series(out_arr,
                    gwuy__dmqsz, tru__rqa)
            return _str_repeat_int_dict_impl

        def impl(S_str, repeats):
            S = S_str._obj
            lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            pdupx__xwga = len(lys__hjhwy)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pdupx__xwga,
                -1)
            for qdsne__duf in numba.parfors.parfor.internal_prange(pdupx__xwga
                ):
                if bodo.libs.array_kernels.isna(lys__hjhwy, qdsne__duf):
                    bodo.libs.array_kernels.setna(out_arr, qdsne__duf)
                else:
                    out_arr[qdsne__duf] = lys__hjhwy[qdsne__duf] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return impl
    elif is_overload_constant_list(repeats):
        zigyq__qanav = get_overload_const_list(repeats)
        nywde__kthf = all([isinstance(vmx__hhkmh, int) for vmx__hhkmh in
            zigyq__qanav])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        nywde__kthf = True
    else:
        nywde__kthf = False
    if nywde__kthf:

        def impl(S_str, repeats):
            S = S_str._obj
            lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            nri__pndk = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            pdupx__xwga = len(lys__hjhwy)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pdupx__xwga,
                -1)
            for qdsne__duf in numba.parfors.parfor.internal_prange(pdupx__xwga
                ):
                if bodo.libs.array_kernels.isna(lys__hjhwy, qdsne__duf):
                    bodo.libs.array_kernels.setna(out_arr, qdsne__duf)
                else:
                    out_arr[qdsne__duf] = lys__hjhwy[qdsne__duf] * nri__pndk[
                        qdsne__duf]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return impl
    else:
        raise BodoError(
            'Series.str.repeat(): repeats argument must either be an integer or a sequence of integers'
            )


def create_ljust_rjust_center_overload(func_name):
    cqyes__qik = f"""def dict_impl(S_str, width, fillchar=' '):
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
    xsq__rlwk = {}
    lbig__dwnzq = {'bodo': bodo, 'numba': numba}
    exec(cqyes__qik, lbig__dwnzq, xsq__rlwk)
    impl = xsq__rlwk['impl']
    djw__mjmx = xsq__rlwk['dict_impl']

    def overload_ljust_rjust_center_method(S_str, width, fillchar=' '):
        common_validate_padding(func_name, width, fillchar)
        if S_str.stype.data == bodo.dict_str_arr_type:
            return djw__mjmx
        return impl
    return overload_ljust_rjust_center_method


def _install_ljust_rjust_center():
    for zzpsw__ddb in ['ljust', 'rjust', 'center']:
        impl = create_ljust_rjust_center_overload(zzpsw__ddb)
        overload_method(SeriesStrMethodType, zzpsw__ddb, inline='always',
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
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            if side == 'left':
                out_arr = bodo.libs.dict_arr_ext.str_rjust(nqq__okt, width,
                    fillchar)
            elif side == 'right':
                out_arr = bodo.libs.dict_arr_ext.str_ljust(nqq__okt, width,
                    fillchar)
            elif side == 'both':
                out_arr = bodo.libs.dict_arr_ext.str_center(nqq__okt, width,
                    fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_pad_dict_impl

    def impl(S_str, width, side='left', fillchar=' '):
        S = S_str._obj
        lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pdupx__xwga = len(lys__hjhwy)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pdupx__xwga, -1)
        for qdsne__duf in numba.parfors.parfor.internal_prange(pdupx__xwga):
            if bodo.libs.array_kernels.isna(lys__hjhwy, qdsne__duf):
                out_arr[qdsne__duf] = ''
                bodo.libs.array_kernels.setna(out_arr, qdsne__duf)
            elif side == 'left':
                out_arr[qdsne__duf] = lys__hjhwy[qdsne__duf].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[qdsne__duf] = lys__hjhwy[qdsne__duf].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[qdsne__duf] = lys__hjhwy[qdsne__duf].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_zfill_dict_impl(S_str, width):
            S = S_str._obj
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_zfill(nqq__okt, width)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_zfill_dict_impl

    def impl(S_str, width):
        S = S_str._obj
        lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pdupx__xwga = len(lys__hjhwy)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pdupx__xwga, -1)
        for qdsne__duf in numba.parfors.parfor.internal_prange(pdupx__xwga):
            if bodo.libs.array_kernels.isna(lys__hjhwy, qdsne__duf):
                out_arr[qdsne__duf] = ''
                bodo.libs.array_kernels.setna(out_arr, qdsne__duf)
            else:
                out_arr[qdsne__duf] = lys__hjhwy[qdsne__duf].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
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
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_slice(nqq__okt, start,
                stop, step)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_slice_dict_impl

    def impl(S_str, start=None, stop=None, step=None):
        S = S_str._obj
        lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pdupx__xwga = len(lys__hjhwy)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(pdupx__xwga, -1)
        for qdsne__duf in numba.parfors.parfor.internal_prange(pdupx__xwga):
            if bodo.libs.array_kernels.isna(lys__hjhwy, qdsne__duf):
                out_arr[qdsne__duf] = ''
                bodo.libs.array_kernels.setna(out_arr, qdsne__duf)
            else:
                out_arr[qdsne__duf] = lys__hjhwy[qdsne__duf][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(nqq__okt, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pdupx__xwga = len(lys__hjhwy)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(pdupx__xwga)
        for i in numba.parfors.parfor.internal_prange(pdupx__xwga):
            if bodo.libs.array_kernels.isna(lys__hjhwy, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = lys__hjhwy[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
            gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
            tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(nqq__okt, pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                gwuy__dmqsz, tru__rqa)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        lys__hjhwy = bodo.hiframes.pd_series_ext.get_series_data(S)
        tru__rqa = bodo.hiframes.pd_series_ext.get_series_name(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        pdupx__xwga = len(lys__hjhwy)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(pdupx__xwga)
        for i in numba.parfors.parfor.internal_prange(pdupx__xwga):
            if bodo.libs.array_kernels.isna(lys__hjhwy, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = lys__hjhwy[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr, gwuy__dmqsz,
            tru__rqa)
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
    jley__puz, regex = _get_column_names_from_regex(pat, flags, 'extract')
    mjx__cob = len(jley__puz)
    cqyes__qik = 'def impl(S_str, pat, flags=0, expand=True):\n'
    cqyes__qik += '  regex = re.compile(pat, flags=flags)\n'
    cqyes__qik += '  S = S_str._obj\n'
    cqyes__qik += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    cqyes__qik += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    cqyes__qik += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    cqyes__qik += '  numba.parfors.parfor.init_prange()\n'
    cqyes__qik += '  n = len(str_arr)\n'
    for i in range(mjx__cob):
        cqyes__qik += (
            '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
            .format(i))
    cqyes__qik += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    cqyes__qik += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    for i in range(mjx__cob):
        cqyes__qik += "          out_arr_{}[j] = ''\n".format(i)
        cqyes__qik += (
            '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    cqyes__qik += '      else:\n'
    cqyes__qik += '          m = regex.search(str_arr[j])\n'
    cqyes__qik += '          if m:\n'
    cqyes__qik += '            g = m.groups()\n'
    for i in range(mjx__cob):
        cqyes__qik += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
    cqyes__qik += '          else:\n'
    for i in range(mjx__cob):
        cqyes__qik += "            out_arr_{}[j] = ''\n".format(i)
        cqyes__qik += (
            '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    if is_overload_false(expand) and regex.groups == 1:
        tru__rqa = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        cqyes__qik += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(tru__rqa))
        xsq__rlwk = {}
        exec(cqyes__qik, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, xsq__rlwk)
        impl = xsq__rlwk['impl']
        return impl
    tghs__xywku = ', '.join('out_arr_{}'.format(i) for i in range(mjx__cob))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(cqyes__qik, jley__puz,
        tghs__xywku, 'index', extra_globals={'get_utf8_size': get_utf8_size,
        're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    jley__puz, puaq__pdsy = _get_column_names_from_regex(pat, flags,
        'extractall')
    mjx__cob = len(jley__puz)
    etya__zwrrn = isinstance(S_str.stype.index, StringIndexType)
    cqyes__qik = 'def impl(S_str, pat, flags=0):\n'
    cqyes__qik += '  regex = re.compile(pat, flags=flags)\n'
    cqyes__qik += '  S = S_str._obj\n'
    cqyes__qik += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    cqyes__qik += '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n'
    cqyes__qik += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    cqyes__qik += '  index_arr = bodo.utils.conversion.index_to_array(index)\n'
    cqyes__qik += (
        '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n')
    cqyes__qik += '  numba.parfors.parfor.init_prange()\n'
    cqyes__qik += '  n = len(str_arr)\n'
    cqyes__qik += '  out_n_l = [0]\n'
    for i in range(mjx__cob):
        cqyes__qik += '  num_chars_{} = 0\n'.format(i)
    if etya__zwrrn:
        cqyes__qik += '  index_num_chars = 0\n'
    cqyes__qik += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    if etya__zwrrn:
        cqyes__qik += '      index_num_chars += get_utf8_size(index_arr[i])\n'
    cqyes__qik += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
    cqyes__qik += '          continue\n'
    cqyes__qik += '      m = regex.findall(str_arr[i])\n'
    cqyes__qik += '      out_n_l[0] += len(m)\n'
    for i in range(mjx__cob):
        cqyes__qik += '      l_{} = 0\n'.format(i)
    cqyes__qik += '      for s in m:\n'
    for i in range(mjx__cob):
        cqyes__qik += '        l_{} += get_utf8_size(s{})\n'.format(i, 
            '[{}]'.format(i) if mjx__cob > 1 else '')
    for i in range(mjx__cob):
        cqyes__qik += '      num_chars_{0} += l_{0}\n'.format(i)
    cqyes__qik += (
        '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
        )
    for i in range(mjx__cob):
        cqyes__qik += (
            """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
            .format(i))
    if etya__zwrrn:
        cqyes__qik += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
    else:
        cqyes__qik += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
    cqyes__qik += '  out_match_arr = np.empty(out_n, np.int64)\n'
    cqyes__qik += '  out_ind = 0\n'
    cqyes__qik += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    cqyes__qik += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    cqyes__qik += '          continue\n'
    cqyes__qik += '      m = regex.findall(str_arr[j])\n'
    cqyes__qik += '      for k, s in enumerate(m):\n'
    for i in range(mjx__cob):
        cqyes__qik += (
            '        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})\n'
            .format(i, '[{}]'.format(i) if mjx__cob > 1 else ''))
    cqyes__qik += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
    cqyes__qik += (
        '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
        )
    cqyes__qik += '        out_ind += 1\n'
    cqyes__qik += (
        '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n')
    cqyes__qik += "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n"
    tghs__xywku = ', '.join('out_arr_{}'.format(i) for i in range(mjx__cob))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(cqyes__qik, jley__puz,
        tghs__xywku, 'out_index', extra_globals={'get_utf8_size':
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
    lgf__rnrfx = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    jley__puz = [lgf__rnrfx.get(1 + i, i) for i in range(regex.groups)]
    return jley__puz, regex


def create_str2str_methods_overload(func_name):
    pef__vls = func_name in ['lstrip', 'rstrip', 'strip']
    cqyes__qik = f"""def f({'S_str, to_strip=None' if pef__vls else 'S_str'}):
    S = S_str._obj
    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    str_arr = decode_if_dict_array(str_arr)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    numba.parfors.parfor.init_prange()
    n = len(str_arr)
    num_chars = {'-1' if pef__vls else 'num_total_chars(str_arr)'}
    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)
    for j in numba.parfors.parfor.internal_prange(n):
        if bodo.libs.array_kernels.isna(str_arr, j):
            out_arr[j] = ""
            bodo.libs.array_kernels.setna(out_arr, j)
        else:
            out_arr[j] = str_arr[j].{func_name}({'to_strip' if pef__vls else ''})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    cqyes__qik += f"""def _dict_impl({'S_str, to_strip=None' if pef__vls else 'S_str'}):
    S = S_str._obj
    arr = bodo.hiframes.pd_series_ext.get_series_data(S)
    index = bodo.hiframes.pd_series_ext.get_series_index(S)
    name = bodo.hiframes.pd_series_ext.get_series_name(S)
    out_arr = bodo.libs.dict_arr_ext.str_{func_name}({'arr, to_strip' if pef__vls else 'arr'})
    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)
"""
    xsq__rlwk = {}
    exec(cqyes__qik, {'bodo': bodo, 'numba': numba, 'num_total_chars': bodo
        .libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, xsq__rlwk)
    ouc__xjqy = xsq__rlwk['f']
    jkrn__ytdck = xsq__rlwk['_dict_impl']
    if pef__vls:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            if S_str.stype.data == bodo.dict_str_arr_type:
                return jkrn__ytdck
            return ouc__xjqy
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return jkrn__ytdck
            return ouc__xjqy
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):

    def overload_str2bool_methods(S_str):
        cqyes__qik = 'def f(S_str):\n'
        cqyes__qik += '    S = S_str._obj\n'
        cqyes__qik += (
            '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        cqyes__qik += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        cqyes__qik += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        cqyes__qik += '    numba.parfors.parfor.init_prange()\n'
        cqyes__qik += '    l = len(str_arr)\n'
        cqyes__qik += (
            '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        cqyes__qik += '    for i in numba.parfors.parfor.internal_prange(l):\n'
        cqyes__qik += '        if bodo.libs.array_kernels.isna(str_arr, i):\n'
        cqyes__qik += '            bodo.libs.array_kernels.setna(out_arr, i)\n'
        cqyes__qik += '        else:\n'
        cqyes__qik += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
            .format(func_name))
        cqyes__qik += '    return bodo.hiframes.pd_series_ext.init_series(\n'
        cqyes__qik += '      out_arr,index, name)\n'
        xsq__rlwk = {}
        exec(cqyes__qik, {'bodo': bodo, 'numba': numba, 'np': np}, xsq__rlwk)
        ouc__xjqy = xsq__rlwk['f']
        return ouc__xjqy
    return overload_str2bool_methods


def _install_str2str_methods():
    for elyca__aeama in bodo.hiframes.pd_series_ext.str2str_methods:
        thd__aeu = create_str2str_methods_overload(elyca__aeama)
        overload_method(SeriesStrMethodType, elyca__aeama, inline='always',
            no_unliteral=True)(thd__aeu)


def _install_str2bool_methods():
    for elyca__aeama in bodo.hiframes.pd_series_ext.str2bool_methods:
        thd__aeu = create_str2bool_methods_overload(elyca__aeama)
        overload_method(SeriesStrMethodType, elyca__aeama, inline='always',
            no_unliteral=True)(thd__aeu)


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
        tru__rqa = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(tru__rqa)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        feafo__fpn = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, feafo__fpn)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        swuth__enj, = args
        jxhi__lcdbf = signature.return_type
        cwcvr__icn = cgutils.create_struct_proxy(jxhi__lcdbf)(context, builder)
        cwcvr__icn.obj = swuth__enj
        context.nrt.incref(builder, signature.args[0], swuth__enj)
        return cwcvr__icn._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        nqq__okt = bodo.hiframes.pd_series_ext.get_series_data(S)
        gwuy__dmqsz = bodo.hiframes.pd_series_ext.get_series_index(S)
        tru__rqa = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(nqq__okt),
            gwuy__dmqsz, tru__rqa)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for nhr__aewj in unsupported_cat_attrs:
        tsll__pprd = 'Series.cat.' + nhr__aewj
        overload_attribute(SeriesCatMethodType, nhr__aewj)(
            create_unsupported_overload(tsll__pprd))
    for npx__rfrh in unsupported_cat_methods:
        tsll__pprd = 'Series.cat.' + npx__rfrh
        overload_method(SeriesCatMethodType, npx__rfrh)(
            create_unsupported_overload(tsll__pprd))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for npx__rfrh in unsupported_str_methods:
        tsll__pprd = 'Series.str.' + npx__rfrh
        overload_method(SeriesStrMethodType, npx__rfrh)(
            create_unsupported_overload(tsll__pprd))


_install_strseries_unsupported()
