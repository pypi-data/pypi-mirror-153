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
        gtrws__ycxqs = self._get_h5_type(lhs, rhs)
        if gtrws__ycxqs is not None:
            hvvb__kxw = str(gtrws__ycxqs.dtype)
            ndqg__njg = 'def _h5_read_impl(dset, index):\n'
            ndqg__njg += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(gtrws__ycxqs.ndim, hvvb__kxw))
            xzyep__flzwa = {}
            exec(ndqg__njg, {}, xzyep__flzwa)
            glrj__nsh = xzyep__flzwa['_h5_read_impl']
            znfn__mfrh = compile_to_numba_ir(glrj__nsh, {'bodo': bodo}
                ).blocks.popitem()[1]
            dzswq__pguu = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(znfn__mfrh, [rhs.value, dzswq__pguu])
            dfh__bvuo = znfn__mfrh.body[:-3]
            dfh__bvuo[-1].target = assign.target
            return dfh__bvuo
        return None

    def _get_h5_type(self, lhs, rhs):
        gtrws__ycxqs = self._get_h5_type_locals(lhs)
        if gtrws__ycxqs is not None:
            return gtrws__ycxqs
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        dzswq__pguu = rhs.index if rhs.op == 'getitem' else rhs.index_var
        fjda__btvpg = guard(find_const, self.func_ir, dzswq__pguu)
        require(not isinstance(fjda__btvpg, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            uac__ikggz = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            edds__fqlat = get_const_value_inner(self.func_ir, uac__ikggz,
                arg_types=self.arg_types)
            obj_name_list.append(edds__fqlat)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        zqvg__rdcgt = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        fglxi__gnb = h5py.File(zqvg__rdcgt, 'r')
        xlhlr__phgeh = fglxi__gnb
        for edds__fqlat in obj_name_list:
            xlhlr__phgeh = xlhlr__phgeh[edds__fqlat]
        require(isinstance(xlhlr__phgeh, h5py.Dataset))
        emzsc__ncwh = len(xlhlr__phgeh.shape)
        cld__xbg = numba.np.numpy_support.from_dtype(xlhlr__phgeh.dtype)
        fglxi__gnb.close()
        return types.Array(cld__xbg, emzsc__ncwh, 'C')

    def _get_h5_type_locals(self, varname):
        uauq__fhxyp = self.locals.pop(varname, None)
        if uauq__fhxyp is None and varname is not None:
            uauq__fhxyp = self.flags.h5_types.get(varname, None)
        return uauq__fhxyp
