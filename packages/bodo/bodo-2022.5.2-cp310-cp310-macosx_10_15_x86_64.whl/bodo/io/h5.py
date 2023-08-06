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
        swpmy__mowxd = self._get_h5_type(lhs, rhs)
        if swpmy__mowxd is not None:
            ltvn__fclt = str(swpmy__mowxd.dtype)
            nbs__aoydi = 'def _h5_read_impl(dset, index):\n'
            nbs__aoydi += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(swpmy__mowxd.ndim, ltvn__fclt))
            nujh__lue = {}
            exec(nbs__aoydi, {}, nujh__lue)
            cuzy__foq = nujh__lue['_h5_read_impl']
            dhd__wdfl = compile_to_numba_ir(cuzy__foq, {'bodo': bodo}
                ).blocks.popitem()[1]
            nxlaj__cvw = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(dhd__wdfl, [rhs.value, nxlaj__cvw])
            dbq__ijttw = dhd__wdfl.body[:-3]
            dbq__ijttw[-1].target = assign.target
            return dbq__ijttw
        return None

    def _get_h5_type(self, lhs, rhs):
        swpmy__mowxd = self._get_h5_type_locals(lhs)
        if swpmy__mowxd is not None:
            return swpmy__mowxd
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        nxlaj__cvw = rhs.index if rhs.op == 'getitem' else rhs.index_var
        doq__asba = guard(find_const, self.func_ir, nxlaj__cvw)
        require(not isinstance(doq__asba, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            huxx__xkvw = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            wwppy__lunu = get_const_value_inner(self.func_ir, huxx__xkvw,
                arg_types=self.arg_types)
            obj_name_list.append(wwppy__lunu)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        gvve__eiir = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        vaqyw__enqp = h5py.File(gvve__eiir, 'r')
        jdn__tvy = vaqyw__enqp
        for wwppy__lunu in obj_name_list:
            jdn__tvy = jdn__tvy[wwppy__lunu]
        require(isinstance(jdn__tvy, h5py.Dataset))
        iet__vmts = len(jdn__tvy.shape)
        wri__niwrt = numba.np.numpy_support.from_dtype(jdn__tvy.dtype)
        vaqyw__enqp.close()
        return types.Array(wri__niwrt, iet__vmts, 'C')

    def _get_h5_type_locals(self, varname):
        jogw__oynww = self.locals.pop(varname, None)
        if jogw__oynww is None and varname is not None:
            jogw__oynww = self.flags.h5_types.get(varname, None)
        return jogw__oynww
