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
        ede__wqwu = 'SeriesStrMethodType({})'.format(stype)
        super(SeriesStrMethodType, self).__init__(ede__wqwu)


@register_model(SeriesStrMethodType)
class SeriesStrModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yvom__vordl = [('obj', fe_type.stype)]
        super(SeriesStrModel, self).__init__(dmm, fe_type, yvom__vordl)


make_attribute_wrapper(SeriesStrMethodType, 'obj', '_obj')


@intrinsic
def init_series_str_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        dkf__qic, = args
        ejz__krirc = signature.return_type
        josww__hfu = cgutils.create_struct_proxy(ejz__krirc)(context, builder)
        josww__hfu.obj = dkf__qic
        context.nrt.incref(builder, signature.args[0], dkf__qic)
        return josww__hfu._getvalue()
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
        wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.array_kernels.get_arr_lens(wkyaj__lyvul, False)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
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
            wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
            cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.hiframes.split_impl.compute_split_view(wkyaj__lyvul,
                pat)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cnldl__tkvsg, ede__wqwu)
        return _str_split_view_impl

    def _str_split_impl(S_str, pat=None, n=-1, expand=False):
        S = S_str._obj
        wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        out_arr = bodo.libs.str_ext.str_split(wkyaj__lyvul, pat, n)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
    return _str_split_impl


@overload_method(SeriesStrMethodType, 'get', no_unliteral=True)
def overload_str_method_get(S_str, i):
    mru__fac = S_str.stype.data
    if (mru__fac != string_array_split_view_type and not is_str_arr_type(
        mru__fac)) and not isinstance(mru__fac, ArrayItemArrayType):
        raise_bodo_error(
            'Series.str.get(): only supports input type of Series(array(item)) and Series(str)'
            )
    int_arg_check('get', 'i', i)
    if isinstance(mru__fac, ArrayItemArrayType):

        def _str_get_array_impl(S_str, i):
            S = S_str._obj
            wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
            cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.array_kernels.get(wkyaj__lyvul, i)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cnldl__tkvsg, ede__wqwu)
        return _str_get_array_impl
    if mru__fac == string_array_split_view_type:

        def _str_get_split_impl(S_str, i):
            S = S_str._obj
            wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
            cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            n = len(wkyaj__lyvul)
            mvwo__iffxo = 0
            for wox__yrlgi in numba.parfors.parfor.internal_prange(n):
                kls__rtls, kls__rtls, ehtpr__tozyn = get_split_view_index(
                    wkyaj__lyvul, wox__yrlgi, i)
                mvwo__iffxo += ehtpr__tozyn
            numba.parfors.parfor.init_prange()
            out_arr = pre_alloc_string_array(n, mvwo__iffxo)
            for qniuu__chpf in numba.parfors.parfor.internal_prange(n):
                shi__ebnqm, jdd__ifvr, ehtpr__tozyn = get_split_view_index(
                    wkyaj__lyvul, qniuu__chpf, i)
                if shi__ebnqm == 0:
                    bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
                    kgk__gda = get_split_view_data_ptr(wkyaj__lyvul, 0)
                else:
                    bodo.libs.str_arr_ext.str_arr_set_not_na(out_arr,
                        qniuu__chpf)
                    kgk__gda = get_split_view_data_ptr(wkyaj__lyvul, jdd__ifvr)
                bodo.libs.str_arr_ext.setitem_str_arr_ptr(out_arr,
                    qniuu__chpf, kgk__gda, ehtpr__tozyn)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cnldl__tkvsg, ede__wqwu)
        return _str_get_split_impl

    def _str_get_impl(S_str, i):
        S = S_str._obj
        wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        n = len(wkyaj__lyvul)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(n, -1)
        for qniuu__chpf in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(wkyaj__lyvul, qniuu__chpf
                ) or not len(wkyaj__lyvul[qniuu__chpf]) > i >= -len(
                wkyaj__lyvul[qniuu__chpf]):
                out_arr[qniuu__chpf] = ''
                bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
            else:
                out_arr[qniuu__chpf] = wkyaj__lyvul[qniuu__chpf][i]
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
    return _str_get_impl


@overload_method(SeriesStrMethodType, 'join', inline='always', no_unliteral
    =True)
def overload_str_method_join(S_str, sep):
    mru__fac = S_str.stype.data
    if (mru__fac != string_array_split_view_type and mru__fac !=
        ArrayItemArrayType(string_array_type) and not is_str_arr_type(mru__fac)
        ):
        raise_bodo_error(
            'Series.str.join(): only supports input type of Series(list(str)) and Series(str)'
            )
    str_arg_check('join', 'sep', sep)

    def impl(S_str, sep):
        S = S_str._obj
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        n = len(lflz__rcgd)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)
        for qniuu__chpf in numba.parfors.parfor.internal_prange(n):
            if bodo.libs.array_kernels.isna(lflz__rcgd, qniuu__chpf):
                out_arr[qniuu__chpf] = ''
                bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
            else:
                becx__bjmiy = lflz__rcgd[qniuu__chpf]
                out_arr[qniuu__chpf] = sep.join(becx__bjmiy)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
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
            wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
            cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_replace(wkyaj__lyvul, pat,
                repl, flags, regex)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cnldl__tkvsg, ede__wqwu)
        return _str_replace_dict_impl
    if is_overload_true(regex):

        def _str_replace_regex_impl(S_str, pat, repl, n=-1, case=None,
            flags=0, regex=True):
            S = S_str._obj
            wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
            cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
            numba.parfors.parfor.init_prange()
            zjiw__ekif = re.compile(pat, flags)
            vyan__xvgfw = len(wkyaj__lyvul)
            out_arr = pre_alloc_string_array(vyan__xvgfw, -1)
            for qniuu__chpf in numba.parfors.parfor.internal_prange(vyan__xvgfw
                ):
                if bodo.libs.array_kernels.isna(wkyaj__lyvul, qniuu__chpf):
                    out_arr[qniuu__chpf] = ''
                    bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
                    continue
                out_arr[qniuu__chpf] = zjiw__ekif.sub(repl, wkyaj__lyvul[
                    qniuu__chpf])
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cnldl__tkvsg, ede__wqwu)
        return _str_replace_regex_impl
    if not is_overload_false(regex):
        raise BodoError('Series.str.replace(): regex argument should be bool')

    def _str_replace_noregex_impl(S_str, pat, repl, n=-1, case=None, flags=
        0, regex=True):
        S = S_str._obj
        wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(wkyaj__lyvul)
        numba.parfors.parfor.init_prange()
        out_arr = pre_alloc_string_array(vyan__xvgfw, -1)
        for qniuu__chpf in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(wkyaj__lyvul, qniuu__chpf):
                out_arr[qniuu__chpf] = ''
                bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
                continue
            out_arr[qniuu__chpf] = wkyaj__lyvul[qniuu__chpf].replace(pat, repl)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
    return _str_replace_noregex_impl


@numba.njit
def series_contains_regex(S, pat, case, flags, na, regex):
    with numba.objmode(out_arr=bodo.boolean_array):
        out_arr = S.array._str_contains(pat, case, flags, na, regex)
    return out_arr


def is_regex_unsupported(pat):
    ayqa__mwf = ['(?a', '(?i', '(?L', '(?m', '(?s', '(?u', '(?x', '(?#']
    if is_overload_constant_str(pat):
        if isinstance(pat, types.StringLiteral):
            pat = pat.literal_value
        return any([(zmqv__teet in pat) for zmqv__teet in ayqa__mwf])
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
    bxf__sjom = re.IGNORECASE.value
    bkywr__diknm = 'def impl(\n'
    bkywr__diknm += (
        '    S_str, pat, case=True, flags=0, na=np.nan, regex=True\n')
    bkywr__diknm += '):\n'
    bkywr__diknm += '  S = S_str._obj\n'
    bkywr__diknm += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    bkywr__diknm += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    bkywr__diknm += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    bkywr__diknm += '  l = len(arr)\n'
    bkywr__diknm += '  out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n'
    if is_overload_true(regex):
        if is_regex_unsupported(pat) or flags:
            if S_str.stype.data == bodo.dict_str_arr_type:
                bkywr__diknm += """  out_arr = bodo.libs.dict_arr_ext.str_series_contains_regex(arr, pat, case, flags, na, regex)
"""
            else:
                bkywr__diknm += """  out_arr = bodo.hiframes.series_str_impl.series_contains_regex(S, pat, case, flags, na, regex)
"""
        else:
            bkywr__diknm += """  get_search_regex(arr, case, bodo.libs.str_ext.unicode_to_utf8(pat), out_arr)
"""
    elif S_str.stype.data == bodo.dict_str_arr_type:
        bkywr__diknm += """  out_arr = bodo.libs.dict_arr_ext.str_contains_non_regex(arr, pat, case)
"""
    else:
        bkywr__diknm += '  numba.parfors.parfor.init_prange()\n'
        if is_overload_false(case):
            bkywr__diknm += '  upper_pat = pat.upper()\n'
        bkywr__diknm += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        bkywr__diknm += '      if bodo.libs.array_kernels.isna(arr, i):\n'
        bkywr__diknm += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        bkywr__diknm += '      else: \n'
        if is_overload_true(case):
            bkywr__diknm += '          out_arr[i] = pat in arr[i]\n'
        else:
            bkywr__diknm += (
                '          out_arr[i] = upper_pat in arr[i].upper()\n')
    bkywr__diknm += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    golsx__kak = {}
    exec(bkywr__diknm, {'re': re, 'bodo': bodo, 'numba': numba, 'np': np,
        're_ignorecase_value': bxf__sjom, 'get_search_regex':
        get_search_regex}, golsx__kak)
    impl = golsx__kak['impl']
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
    bkywr__diknm = (
        "def impl(S_str, others=None, sep=None, na_rep=None, join='left'):\n")
    bkywr__diknm += '  S = S_str._obj\n'
    bkywr__diknm += '  arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n'
    bkywr__diknm += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    bkywr__diknm += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    bkywr__diknm += '  l = len(arr)\n'
    for i in range(len(others.columns)):
        bkywr__diknm += f"""  data{i} = bodo.hiframes.pd_dataframe_ext.get_dataframe_data(others, {i})
"""
    if S_str.stype.data == bodo.dict_str_arr_type and all(xjqt__nzo == bodo
        .dict_str_arr_type for xjqt__nzo in others.data):
        sbj__qim = ', '.join(f'data{i}' for i in range(len(others.columns)))
        bkywr__diknm += (
            f'  out_arr = bodo.libs.dict_arr_ext.cat_dict_str((arr, {sbj__qim}), sep)\n'
            )
    else:
        yow__wdk = ' or '.join(['bodo.libs.array_kernels.isna(arr, i)'] + [
            f'bodo.libs.array_kernels.isna(data{i}, i)' for i in range(len(
            others.columns))])
        bkywr__diknm += (
            '  out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(l, -1)\n'
            )
        bkywr__diknm += '  numba.parfors.parfor.init_prange()\n'
        bkywr__diknm += '  for i in numba.parfors.parfor.internal_prange(l):\n'
        bkywr__diknm += f'      if {yow__wdk}:\n'
        bkywr__diknm += '          bodo.libs.array_kernels.setna(out_arr, i)\n'
        bkywr__diknm += '          continue\n'
        mkqpq__ifq = ', '.join(['arr[i]'] + [f'data{i}[i]' for i in range(
            len(others.columns))])
        kqak__tvsfq = "''" if is_overload_none(sep) else 'sep'
        bkywr__diknm += (
            f'      out_arr[i] = {kqak__tvsfq}.join([{mkqpq__ifq}])\n')
    bkywr__diknm += (
        '  return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    golsx__kak = {}
    exec(bkywr__diknm, {'bodo': bodo, 'numba': numba}, golsx__kak)
    impl = golsx__kak['impl']
    return impl


@overload_method(SeriesStrMethodType, 'count', inline='always',
    no_unliteral=True)
def overload_str_method_count(S_str, pat, flags=0):
    str_arg_check('count', 'pat', pat)
    int_arg_check('count', 'flags', flags)

    def impl(S_str, pat, flags=0):
        S = S_str._obj
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        zjiw__ekif = re.compile(pat, flags)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(vyan__xvgfw, np.int64)
        for i in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = str_findall_count(zjiw__ekif, lflz__rcgd[i])
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
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
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(vyan__xvgfw, np.int64)
        for i in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = lflz__rcgd[i].find(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
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
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.int_arr_ext.alloc_int_array(vyan__xvgfw, np.int64)
        for i in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = lflz__rcgd[i].rfind(sub, start, end)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
    return impl


@overload_method(SeriesStrMethodType, 'center', inline='always',
    no_unliteral=True)
def overload_str_method_center(S_str, width, fillchar=' '):
    common_validate_padding('center', width, fillchar)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_center_dict_impl(S_str, width, fillchar=' '):
            S = S_str._obj
            wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
            cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_center(wkyaj__lyvul, width,
                fillchar)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cnldl__tkvsg, ede__wqwu)
        return _str_center_dict_impl

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(vyan__xvgfw, -1)
        for qniuu__chpf in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, qniuu__chpf):
                out_arr[qniuu__chpf] = ''
                bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
            else:
                out_arr[qniuu__chpf] = lflz__rcgd[qniuu__chpf].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
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
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(vyan__xvgfw, -1)
        for qniuu__chpf in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, qniuu__chpf):
                bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
            else:
                if stop is not None:
                    mfu__hgnxv = lflz__rcgd[qniuu__chpf][stop:]
                else:
                    mfu__hgnxv = ''
                out_arr[qniuu__chpf] = lflz__rcgd[qniuu__chpf][:start
                    ] + repl + mfu__hgnxv
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
    return impl


@overload_method(SeriesStrMethodType, 'repeat', inline='always',
    no_unliteral=True)
def overload_str_method_repeat(S_str, repeats):
    if isinstance(repeats, types.Integer) or is_overload_constant_int(repeats):

        def impl(S_str, repeats):
            S = S_str._obj
            lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
            cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
            numba.parfors.parfor.init_prange()
            vyan__xvgfw = len(lflz__rcgd)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(vyan__xvgfw,
                -1)
            for qniuu__chpf in numba.parfors.parfor.internal_prange(vyan__xvgfw
                ):
                if bodo.libs.array_kernels.isna(lflz__rcgd, qniuu__chpf):
                    bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
                else:
                    out_arr[qniuu__chpf] = lflz__rcgd[qniuu__chpf] * repeats
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cnldl__tkvsg, ede__wqwu)
        return impl
    elif is_overload_constant_list(repeats):
        qussl__hohtr = get_overload_const_list(repeats)
        svnb__uopf = all([isinstance(yuq__acwq, int) for yuq__acwq in
            qussl__hohtr])
    elif is_list_like_index_type(repeats) and isinstance(repeats.dtype,
        types.Integer):
        svnb__uopf = True
    else:
        svnb__uopf = False
    if svnb__uopf:

        def impl(S_str, repeats):
            S = S_str._obj
            lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
            ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
            cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
            zfgo__xvoa = bodo.utils.conversion.coerce_to_array(repeats)
            numba.parfors.parfor.init_prange()
            vyan__xvgfw = len(lflz__rcgd)
            out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(vyan__xvgfw,
                -1)
            for qniuu__chpf in numba.parfors.parfor.internal_prange(vyan__xvgfw
                ):
                if bodo.libs.array_kernels.isna(lflz__rcgd, qniuu__chpf):
                    bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
                else:
                    out_arr[qniuu__chpf] = lflz__rcgd[qniuu__chpf
                        ] * zfgo__xvoa[qniuu__chpf]
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cnldl__tkvsg, ede__wqwu)
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
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(vyan__xvgfw, -1)
        for qniuu__chpf in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, qniuu__chpf):
                out_arr[qniuu__chpf] = ''
                bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
            else:
                out_arr[qniuu__chpf] = lflz__rcgd[qniuu__chpf].ljust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
    return impl


@overload_method(SeriesStrMethodType, 'rjust', inline='always',
    no_unliteral=True)
def overload_str_method_rjust(S_str, width, fillchar=' '):
    common_validate_padding('rjust', width, fillchar)

    def impl(S_str, width, fillchar=' '):
        S = S_str._obj
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(vyan__xvgfw, -1)
        for qniuu__chpf in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, qniuu__chpf):
                out_arr[qniuu__chpf] = ''
                bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
            else:
                out_arr[qniuu__chpf] = lflz__rcgd[qniuu__chpf].rjust(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
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
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(vyan__xvgfw, -1)
        for qniuu__chpf in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, qniuu__chpf):
                out_arr[qniuu__chpf] = ''
                bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
            elif side == 'left':
                out_arr[qniuu__chpf] = lflz__rcgd[qniuu__chpf].rjust(width,
                    fillchar)
            elif side == 'right':
                out_arr[qniuu__chpf] = lflz__rcgd[qniuu__chpf].ljust(width,
                    fillchar)
            elif side == 'both':
                out_arr[qniuu__chpf] = lflz__rcgd[qniuu__chpf].center(width,
                    fillchar)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
    return impl


@overload_method(SeriesStrMethodType, 'zfill', inline='always',
    no_unliteral=True)
def overload_str_method_zfill(S_str, width):
    int_arg_check('zfill', 'width', width)

    def impl(S_str, width):
        S = S_str._obj
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(vyan__xvgfw, -1)
        for qniuu__chpf in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, qniuu__chpf):
                out_arr[qniuu__chpf] = ''
                bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
            else:
                out_arr[qniuu__chpf] = lflz__rcgd[qniuu__chpf].zfill(width)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
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
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(vyan__xvgfw, -1)
        for qniuu__chpf in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, qniuu__chpf):
                out_arr[qniuu__chpf] = ''
                bodo.libs.array_kernels.setna(out_arr, qniuu__chpf)
            else:
                out_arr[qniuu__chpf] = lflz__rcgd[qniuu__chpf][start:stop:step]
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
    return impl


@overload_method(SeriesStrMethodType, 'startswith', inline='always',
    no_unliteral=True)
def overload_str_method_startswith(S_str, pat, na=np.nan):
    not_supported_arg_check('startswith', 'na', na, np.nan)
    str_arg_check('startswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_startswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
            cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_startswith(wkyaj__lyvul,
                pat, na)
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cnldl__tkvsg, ede__wqwu)
        return _str_startswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(vyan__xvgfw)
        for i in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = lflz__rcgd[i].startswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
    return impl


@overload_method(SeriesStrMethodType, 'endswith', inline='always',
    no_unliteral=True)
def overload_str_method_endswith(S_str, pat, na=np.nan):
    not_supported_arg_check('endswith', 'na', na, np.nan)
    str_arg_check('endswith', 'pat', pat)
    if S_str.stype.data == bodo.dict_str_arr_type:

        def _str_endswith_dict_impl(S_str, pat, na=np.nan):
            S = S_str._obj
            wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
            cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
            ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
            out_arr = bodo.libs.dict_arr_ext.str_endswith(wkyaj__lyvul, pat, na
                )
            return bodo.hiframes.pd_series_ext.init_series(out_arr,
                cnldl__tkvsg, ede__wqwu)
        return _str_endswith_dict_impl

    def impl(S_str, pat, na=np.nan):
        S = S_str._obj
        lflz__rcgd = bodo.hiframes.pd_series_ext.get_series_data(S)
        ede__wqwu = bodo.hiframes.pd_series_ext.get_series_name(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        numba.parfors.parfor.init_prange()
        vyan__xvgfw = len(lflz__rcgd)
        out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(vyan__xvgfw)
        for i in numba.parfors.parfor.internal_prange(vyan__xvgfw):
            if bodo.libs.array_kernels.isna(lflz__rcgd, i):
                bodo.libs.array_kernels.setna(out_arr, i)
            else:
                out_arr[i] = lflz__rcgd[i].endswith(pat)
        return bodo.hiframes.pd_series_ext.init_series(out_arr,
            cnldl__tkvsg, ede__wqwu)
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
    jov__isva, regex = _get_column_names_from_regex(pat, flags, 'extract')
    sgy__bahvj = len(jov__isva)
    bkywr__diknm = 'def impl(S_str, pat, flags=0, expand=True):\n'
    bkywr__diknm += '  regex = re.compile(pat, flags=flags)\n'
    bkywr__diknm += '  S = S_str._obj\n'
    bkywr__diknm += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    bkywr__diknm += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    bkywr__diknm += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    bkywr__diknm += '  numba.parfors.parfor.init_prange()\n'
    bkywr__diknm += '  n = len(str_arr)\n'
    for i in range(sgy__bahvj):
        bkywr__diknm += (
            '  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(n, -1)\n'
            .format(i))
    bkywr__diknm += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    bkywr__diknm += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    for i in range(sgy__bahvj):
        bkywr__diknm += "          out_arr_{}[j] = ''\n".format(i)
        bkywr__diknm += (
            '          bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    bkywr__diknm += '      else:\n'
    bkywr__diknm += '          m = regex.search(str_arr[j])\n'
    bkywr__diknm += '          if m:\n'
    bkywr__diknm += '            g = m.groups()\n'
    for i in range(sgy__bahvj):
        bkywr__diknm += '            out_arr_{0}[j] = g[{0}]\n'.format(i)
    bkywr__diknm += '          else:\n'
    for i in range(sgy__bahvj):
        bkywr__diknm += "            out_arr_{}[j] = ''\n".format(i)
        bkywr__diknm += (
            '            bodo.libs.array_kernels.setna(out_arr_{}, j)\n'.
            format(i))
    if is_overload_false(expand) and regex.groups == 1:
        ede__wqwu = "'{}'".format(list(regex.groupindex.keys()).pop()) if len(
            regex.groupindex.keys()) > 0 else 'name'
        bkywr__diknm += (
            '  return bodo.hiframes.pd_series_ext.init_series(out_arr_0, index, {})\n'
            .format(ede__wqwu))
        golsx__kak = {}
        exec(bkywr__diknm, {'re': re, 'bodo': bodo, 'numba': numba,
            'get_utf8_size': get_utf8_size}, golsx__kak)
        impl = golsx__kak['impl']
        return impl
    owzry__uvnht = ', '.join('out_arr_{}'.format(i) for i in range(sgy__bahvj))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(bkywr__diknm,
        jov__isva, owzry__uvnht, 'index', extra_globals={'get_utf8_size':
        get_utf8_size, 're': re})
    return impl


@overload_method(SeriesStrMethodType, 'extractall', inline='always',
    no_unliteral=True)
def overload_str_method_extractall(S_str, pat, flags=0):
    jov__isva, kls__rtls = _get_column_names_from_regex(pat, flags,
        'extractall')
    sgy__bahvj = len(jov__isva)
    iah__vvrjw = isinstance(S_str.stype.index, StringIndexType)
    bkywr__diknm = 'def impl(S_str, pat, flags=0):\n'
    bkywr__diknm += '  regex = re.compile(pat, flags=flags)\n'
    bkywr__diknm += '  S = S_str._obj\n'
    bkywr__diknm += (
        '  str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    bkywr__diknm += (
        '  index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    bkywr__diknm += '  name = bodo.hiframes.pd_series_ext.get_series_name(S)\n'
    bkywr__diknm += (
        '  index_arr = bodo.utils.conversion.index_to_array(index)\n')
    bkywr__diknm += (
        '  index_name = bodo.hiframes.pd_index_ext.get_index_name(index)\n')
    bkywr__diknm += '  numba.parfors.parfor.init_prange()\n'
    bkywr__diknm += '  n = len(str_arr)\n'
    bkywr__diknm += '  out_n_l = [0]\n'
    for i in range(sgy__bahvj):
        bkywr__diknm += '  num_chars_{} = 0\n'.format(i)
    if iah__vvrjw:
        bkywr__diknm += '  index_num_chars = 0\n'
    bkywr__diknm += '  for i in numba.parfors.parfor.internal_prange(n):\n'
    if iah__vvrjw:
        bkywr__diknm += (
            '      index_num_chars += get_utf8_size(index_arr[i])\n')
    bkywr__diknm += '      if bodo.libs.array_kernels.isna(str_arr, i):\n'
    bkywr__diknm += '          continue\n'
    bkywr__diknm += '      m = regex.findall(str_arr[i])\n'
    bkywr__diknm += '      out_n_l[0] += len(m)\n'
    for i in range(sgy__bahvj):
        bkywr__diknm += '      l_{} = 0\n'.format(i)
    bkywr__diknm += '      for s in m:\n'
    for i in range(sgy__bahvj):
        bkywr__diknm += '        l_{} += get_utf8_size(s{})\n'.format(i, 
            '[{}]'.format(i) if sgy__bahvj > 1 else '')
    for i in range(sgy__bahvj):
        bkywr__diknm += '      num_chars_{0} += l_{0}\n'.format(i)
    bkywr__diknm += (
        '  out_n = bodo.libs.distributed_api.local_alloc_size(out_n_l[0], str_arr)\n'
        )
    for i in range(sgy__bahvj):
        bkywr__diknm += (
            """  out_arr_{0} = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, num_chars_{0})
"""
            .format(i))
    if iah__vvrjw:
        bkywr__diknm += """  out_ind_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(out_n, index_num_chars)
"""
    else:
        bkywr__diknm += '  out_ind_arr = np.empty(out_n, index_arr.dtype)\n'
    bkywr__diknm += '  out_match_arr = np.empty(out_n, np.int64)\n'
    bkywr__diknm += '  out_ind = 0\n'
    bkywr__diknm += '  for j in numba.parfors.parfor.internal_prange(n):\n'
    bkywr__diknm += '      if bodo.libs.array_kernels.isna(str_arr, j):\n'
    bkywr__diknm += '          continue\n'
    bkywr__diknm += '      m = regex.findall(str_arr[j])\n'
    bkywr__diknm += '      for k, s in enumerate(m):\n'
    for i in range(sgy__bahvj):
        bkywr__diknm += (
            """        bodo.libs.distributed_api.set_arr_local(out_arr_{}, out_ind, s{})
"""
            .format(i, '[{}]'.format(i) if sgy__bahvj > 1 else ''))
    bkywr__diknm += """        bodo.libs.distributed_api.set_arr_local(out_ind_arr, out_ind, index_arr[j])
"""
    bkywr__diknm += (
        '        bodo.libs.distributed_api.set_arr_local(out_match_arr, out_ind, k)\n'
        )
    bkywr__diknm += '        out_ind += 1\n'
    bkywr__diknm += (
        '  out_index = bodo.hiframes.pd_multi_index_ext.init_multi_index(\n')
    bkywr__diknm += (
        "    (out_ind_arr, out_match_arr), (index_name, 'match'))\n")
    owzry__uvnht = ', '.join('out_arr_{}'.format(i) for i in range(sgy__bahvj))
    impl = bodo.hiframes.dataframe_impl._gen_init_df(bkywr__diknm,
        jov__isva, owzry__uvnht, 'out_index', extra_globals={
        'get_utf8_size': get_utf8_size, 're': re})
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
    isgy__lzum = dict(zip(regex.groupindex.values(), regex.groupindex.keys()))
    jov__isva = [isgy__lzum.get(1 + i, i) for i in range(regex.groups)]
    return jov__isva, regex


def create_str2str_methods_overload(func_name):
    if func_name in ['lstrip', 'rstrip', 'strip']:
        bkywr__diknm = 'def f(S_str, to_strip=None):\n'
    else:
        bkywr__diknm = 'def f(S_str):\n'
    bkywr__diknm += '    S = S_str._obj\n'
    bkywr__diknm += (
        '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    bkywr__diknm += '    str_arr = decode_if_dict_array(str_arr)\n'
    bkywr__diknm += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    bkywr__diknm += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    bkywr__diknm += '    numba.parfors.parfor.init_prange()\n'
    bkywr__diknm += '    n = len(str_arr)\n'
    if func_name in ('capitalize', 'lower', 'swapcase', 'title', 'upper'):
        bkywr__diknm += '    num_chars = num_total_chars(str_arr)\n'
    else:
        bkywr__diknm += '    num_chars = -1\n'
    bkywr__diknm += (
        '    out_arr = bodo.libs.str_arr_ext.pre_alloc_string_array(n, num_chars)\n'
        )
    bkywr__diknm += '    for j in numba.parfors.parfor.internal_prange(n):\n'
    bkywr__diknm += '        if bodo.libs.array_kernels.isna(str_arr, j):\n'
    bkywr__diknm += '            out_arr[j] = ""\n'
    bkywr__diknm += '            bodo.libs.array_kernels.setna(out_arr, j)\n'
    bkywr__diknm += '        else:\n'
    if func_name in ['lstrip', 'rstrip', 'strip']:
        bkywr__diknm += ('            out_arr[j] = str_arr[j].{}(to_strip)\n'
            .format(func_name))
    else:
        bkywr__diknm += '            out_arr[j] = str_arr[j].{}()\n'.format(
            func_name)
    bkywr__diknm += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    bkywr__diknm += 'def _dict_impl(S_str):\n'
    bkywr__diknm += '    S = S_str._obj\n'
    bkywr__diknm += (
        '    arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
    bkywr__diknm += (
        '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
    bkywr__diknm += (
        '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
    bkywr__diknm += (
        f'    out_arr = bodo.libs.dict_arr_ext.str_{func_name}(arr)\n')
    bkywr__diknm += (
        '    return bodo.hiframes.pd_series_ext.init_series(out_arr, index, name)\n'
        )
    golsx__kak = {}
    exec(bkywr__diknm, {'bodo': bodo, 'numba': numba, 'num_total_chars':
        bodo.libs.str_arr_ext.num_total_chars, 'get_utf8_size': bodo.libs.
        str_arr_ext.get_utf8_size, 'decode_if_dict_array': bodo.utils.
        typing.decode_if_dict_array}, golsx__kak)
    sbbp__eembj = golsx__kak['f']
    ynufd__iyae = golsx__kak['_dict_impl']
    if func_name in ['lstrip', 'rstrip', 'strip']:

        def overload_strip_method(S_str, to_strip=None):
            if not is_overload_none(to_strip):
                str_arg_check(func_name, 'to_strip', to_strip)
            return sbbp__eembj
        return overload_strip_method
    else:

        def overload_str_method_dict_supported(S_str):
            if S_str.stype.data == bodo.dict_str_arr_type:
                return ynufd__iyae
            return sbbp__eembj
        return overload_str_method_dict_supported


def create_str2bool_methods_overload(func_name):

    def overload_str2bool_methods(S_str):
        bkywr__diknm = 'def f(S_str):\n'
        bkywr__diknm += '    S = S_str._obj\n'
        bkywr__diknm += (
            '    str_arr = bodo.hiframes.pd_series_ext.get_series_data(S)\n')
        bkywr__diknm += (
            '    index = bodo.hiframes.pd_series_ext.get_series_index(S)\n')
        bkywr__diknm += (
            '    name = bodo.hiframes.pd_series_ext.get_series_name(S)\n')
        bkywr__diknm += '    numba.parfors.parfor.init_prange()\n'
        bkywr__diknm += '    l = len(str_arr)\n'
        bkywr__diknm += (
            '    out_arr = bodo.libs.bool_arr_ext.alloc_bool_array(l)\n')
        bkywr__diknm += (
            '    for i in numba.parfors.parfor.internal_prange(l):\n')
        bkywr__diknm += (
            '        if bodo.libs.array_kernels.isna(str_arr, i):\n')
        bkywr__diknm += (
            '            bodo.libs.array_kernels.setna(out_arr, i)\n')
        bkywr__diknm += '        else:\n'
        bkywr__diknm += ('            out_arr[i] = np.bool_(str_arr[i].{}())\n'
            .format(func_name))
        bkywr__diknm += '    return bodo.hiframes.pd_series_ext.init_series(\n'
        bkywr__diknm += '      out_arr,index, name)\n'
        golsx__kak = {}
        exec(bkywr__diknm, {'bodo': bodo, 'numba': numba, 'np': np}, golsx__kak
            )
        sbbp__eembj = golsx__kak['f']
        return sbbp__eembj
    return overload_str2bool_methods


def _install_str2str_methods():
    for uofdx__qdz in bodo.hiframes.pd_series_ext.str2str_methods:
        qtb__ysavy = create_str2str_methods_overload(uofdx__qdz)
        overload_method(SeriesStrMethodType, uofdx__qdz, inline='always',
            no_unliteral=True)(qtb__ysavy)


def _install_str2bool_methods():
    for uofdx__qdz in bodo.hiframes.pd_series_ext.str2bool_methods:
        qtb__ysavy = create_str2bool_methods_overload(uofdx__qdz)
        overload_method(SeriesStrMethodType, uofdx__qdz, inline='always',
            no_unliteral=True)(qtb__ysavy)


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
        ede__wqwu = 'SeriesCatMethodType({})'.format(stype)
        super(SeriesCatMethodType, self).__init__(ede__wqwu)

    @property
    def mangling_args(self):
        return self.__class__.__name__, (self._code,)


@register_model(SeriesCatMethodType)
class SeriesCatModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        yvom__vordl = [('obj', fe_type.stype)]
        super(SeriesCatModel, self).__init__(dmm, fe_type, yvom__vordl)


make_attribute_wrapper(SeriesCatMethodType, 'obj', '_obj')


@intrinsic
def init_series_cat_method(typingctx, obj=None):

    def codegen(context, builder, signature, args):
        dkf__qic, = args
        wuctd__ztbp = signature.return_type
        byvxc__qxy = cgutils.create_struct_proxy(wuctd__ztbp)(context, builder)
        byvxc__qxy.obj = dkf__qic
        context.nrt.incref(builder, signature.args[0], dkf__qic)
        return byvxc__qxy._getvalue()
    return SeriesCatMethodType(obj)(obj), codegen


@overload_attribute(SeriesCatMethodType, 'codes')
def series_cat_codes_overload(S_dt):

    def impl(S_dt):
        S = S_dt._obj
        wkyaj__lyvul = bodo.hiframes.pd_series_ext.get_series_data(S)
        cnldl__tkvsg = bodo.hiframes.pd_series_ext.get_series_index(S)
        ede__wqwu = None
        return bodo.hiframes.pd_series_ext.init_series(bodo.hiframes.
            pd_categorical_ext.get_categorical_arr_codes(wkyaj__lyvul),
            cnldl__tkvsg, ede__wqwu)
    return impl


unsupported_cat_attrs = {'categories', 'ordered'}
unsupported_cat_methods = {'rename_categories', 'reorder_categories',
    'add_categories', 'remove_categories', 'remove_unused_categories',
    'set_categories', 'as_ordered', 'as_unordered'}


def _install_catseries_unsupported():
    for tam__wrfip in unsupported_cat_attrs:
        anadm__hgl = 'Series.cat.' + tam__wrfip
        overload_attribute(SeriesCatMethodType, tam__wrfip)(
            create_unsupported_overload(anadm__hgl))
    for isd__zvqk in unsupported_cat_methods:
        anadm__hgl = 'Series.cat.' + isd__zvqk
        overload_method(SeriesCatMethodType, isd__zvqk)(
            create_unsupported_overload(anadm__hgl))


_install_catseries_unsupported()
unsupported_str_methods = {'casefold', 'decode', 'encode', 'findall',
    'fullmatch', 'index', 'match', 'normalize', 'partition', 'rindex',
    'rpartition', 'slice_replace', 'rsplit', 'translate', 'wrap', 'get_dummies'
    }


def _install_strseries_unsupported():
    for isd__zvqk in unsupported_str_methods:
        anadm__hgl = 'Series.str.' + isd__zvqk
        overload_method(SeriesStrMethodType, isd__zvqk)(
            create_unsupported_overload(anadm__hgl))


_install_strseries_unsupported()
