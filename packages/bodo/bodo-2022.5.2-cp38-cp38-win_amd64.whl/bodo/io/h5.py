"""
Analysis and transformation for HDF5 support.
"""
import types as pytypes
import numba
from numba.core import ir, types
from numba.core.ir_utils import compile_to_numba_ir, find_callname, find_const, get_definition, guard, replace_arg_nodes, require
import bodo
import bodo.io
from bodo.utils.transform import get_const_value_inner


class H5_IO:

    def __init__(self, func_ir, _locals, flags, arg_types):
        self.func_ir = func_ir
        self.locals = _locals
        self.flags = flags
        self.arg_types = arg_types

    def handle_possible_h5_read(self, assign, lhs, rhs):
        kzatn__gagmi = self._get_h5_type(lhs, rhs)
        if kzatn__gagmi is not None:
            rwdxj__vso = str(kzatn__gagmi.dtype)
            tjjf__rvc = 'def _h5_read_impl(dset, index):\n'
            tjjf__rvc += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(kzatn__gagmi.ndim, rwdxj__vso))
            ypnx__kxelk = {}
            exec(tjjf__rvc, {}, ypnx__kxelk)
            tnbn__dmfix = ypnx__kxelk['_h5_read_impl']
            wrma__xjo = compile_to_numba_ir(tnbn__dmfix, {'bodo': bodo}
                ).blocks.popitem()[1]
            btl__ksq = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(wrma__xjo, [rhs.value, btl__ksq])
            vydcs__gluqd = wrma__xjo.body[:-3]
            vydcs__gluqd[-1].target = assign.target
            return vydcs__gluqd
        return None

    def _get_h5_type(self, lhs, rhs):
        kzatn__gagmi = self._get_h5_type_locals(lhs)
        if kzatn__gagmi is not None:
            return kzatn__gagmi
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        btl__ksq = rhs.index if rhs.op == 'getitem' else rhs.index_var
        uxk__pulg = guard(find_const, self.func_ir, btl__ksq)
        require(not isinstance(uxk__pulg, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            ijnke__uuy = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            maf__hnqj = get_const_value_inner(self.func_ir, ijnke__uuy,
                arg_types=self.arg_types)
            obj_name_list.append(maf__hnqj)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        aizmg__uljn = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        kyog__hkvwr = h5py.File(aizmg__uljn, 'r')
        ipjdg__kkaat = kyog__hkvwr
        for maf__hnqj in obj_name_list:
            ipjdg__kkaat = ipjdg__kkaat[maf__hnqj]
        require(isinstance(ipjdg__kkaat, h5py.Dataset))
        fpeu__wtj = len(ipjdg__kkaat.shape)
        lku__jor = numba.np.numpy_support.from_dtype(ipjdg__kkaat.dtype)
        kyog__hkvwr.close()
        return types.Array(lku__jor, fpeu__wtj, 'C')

    def _get_h5_type_locals(self, varname):
        hbd__husm = self.locals.pop(varname, None)
        if hbd__husm is None and varname is not None:
            hbd__husm = self.flags.h5_types.get(varname, None)
        return hbd__husm
