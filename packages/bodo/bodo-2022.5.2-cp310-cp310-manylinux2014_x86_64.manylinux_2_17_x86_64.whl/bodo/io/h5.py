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
        abz__hvmac = self._get_h5_type(lhs, rhs)
        if abz__hvmac is not None:
            pby__vgket = str(abz__hvmac.dtype)
            vqkej__nwvm = 'def _h5_read_impl(dset, index):\n'
            vqkej__nwvm += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(abz__hvmac.ndim, pby__vgket))
            gmq__fmf = {}
            exec(vqkej__nwvm, {}, gmq__fmf)
            alg__hvje = gmq__fmf['_h5_read_impl']
            sxqzg__epaiw = compile_to_numba_ir(alg__hvje, {'bodo': bodo}
                ).blocks.popitem()[1]
            apw__nsyqw = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(sxqzg__epaiw, [rhs.value, apw__nsyqw])
            brno__rgpl = sxqzg__epaiw.body[:-3]
            brno__rgpl[-1].target = assign.target
            return brno__rgpl
        return None

    def _get_h5_type(self, lhs, rhs):
        abz__hvmac = self._get_h5_type_locals(lhs)
        if abz__hvmac is not None:
            return abz__hvmac
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        apw__nsyqw = rhs.index if rhs.op == 'getitem' else rhs.index_var
        kib__fvyap = guard(find_const, self.func_ir, apw__nsyqw)
        require(not isinstance(kib__fvyap, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            egth__wembb = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            mcb__dwfqe = get_const_value_inner(self.func_ir, egth__wembb,
                arg_types=self.arg_types)
            obj_name_list.append(mcb__dwfqe)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        ttiu__xdjy = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        rhte__ksi = h5py.File(ttiu__xdjy, 'r')
        wdhp__nrt = rhte__ksi
        for mcb__dwfqe in obj_name_list:
            wdhp__nrt = wdhp__nrt[mcb__dwfqe]
        require(isinstance(wdhp__nrt, h5py.Dataset))
        cqlgq__wzh = len(wdhp__nrt.shape)
        sob__ybpxh = numba.np.numpy_support.from_dtype(wdhp__nrt.dtype)
        rhte__ksi.close()
        return types.Array(sob__ybpxh, cqlgq__wzh, 'C')

    def _get_h5_type_locals(self, varname):
        msrwy__obuua = self.locals.pop(varname, None)
        if msrwy__obuua is None and varname is not None:
            msrwy__obuua = self.flags.h5_types.get(varname, None)
        return msrwy__obuua
