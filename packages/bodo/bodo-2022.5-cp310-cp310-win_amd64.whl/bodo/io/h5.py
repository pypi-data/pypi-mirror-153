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
        jyplp__heho = self._get_h5_type(lhs, rhs)
        if jyplp__heho is not None:
            caw__pduj = str(jyplp__heho.dtype)
            lowzm__cxv = 'def _h5_read_impl(dset, index):\n'
            lowzm__cxv += (
                "  arr = bodo.io.h5_api.h5_read_dummy(dset, {}, '{}', index)\n"
                .format(jyplp__heho.ndim, caw__pduj))
            xbl__tsb = {}
            exec(lowzm__cxv, {}, xbl__tsb)
            jcet__bbs = xbl__tsb['_h5_read_impl']
            suc__exh = compile_to_numba_ir(jcet__bbs, {'bodo': bodo}
                ).blocks.popitem()[1]
            xffr__qxiup = rhs.index if rhs.op == 'getitem' else rhs.index_var
            replace_arg_nodes(suc__exh, [rhs.value, xffr__qxiup])
            vsq__zono = suc__exh.body[:-3]
            vsq__zono[-1].target = assign.target
            return vsq__zono
        return None

    def _get_h5_type(self, lhs, rhs):
        jyplp__heho = self._get_h5_type_locals(lhs)
        if jyplp__heho is not None:
            return jyplp__heho
        return guard(self._infer_h5_typ, rhs)

    def _infer_h5_typ(self, rhs):
        require(rhs.op in ('getitem', 'static_getitem'))
        xffr__qxiup = rhs.index if rhs.op == 'getitem' else rhs.index_var
        ybyqv__jdhon = guard(find_const, self.func_ir, xffr__qxiup)
        require(not isinstance(ybyqv__jdhon, str))
        val_def = rhs
        obj_name_list = []
        while True:
            val_def = get_definition(self.func_ir, val_def.value)
            require(isinstance(val_def, ir.Expr))
            if val_def.op == 'call':
                return self._get_h5_type_file(val_def, obj_name_list)
            require(val_def.op in ('getitem', 'static_getitem'))
            cffl__cyo = (val_def.index if val_def.op == 'getitem' else
                val_def.index_var)
            yszx__lsxe = get_const_value_inner(self.func_ir, cffl__cyo,
                arg_types=self.arg_types)
            obj_name_list.append(yszx__lsxe)

    def _get_h5_type_file(self, val_def, obj_name_list):
        require(len(obj_name_list) > 0)
        require(find_callname(self.func_ir, val_def) == ('File', 'h5py'))
        require(len(val_def.args) > 0)
        othjk__abbun = get_const_value_inner(self.func_ir, val_def.args[0],
            arg_types=self.arg_types)
        obj_name_list.reverse()
        import h5py
        tkrqv__ltoa = h5py.File(othjk__abbun, 'r')
        hmm__rwlj = tkrqv__ltoa
        for yszx__lsxe in obj_name_list:
            hmm__rwlj = hmm__rwlj[yszx__lsxe]
        require(isinstance(hmm__rwlj, h5py.Dataset))
        bdn__bcfzn = len(hmm__rwlj.shape)
        jdty__atwhp = numba.np.numpy_support.from_dtype(hmm__rwlj.dtype)
        tkrqv__ltoa.close()
        return types.Array(jdty__atwhp, bdn__bcfzn, 'C')

    def _get_h5_type_locals(self, varname):
        tfayj__nyyd = self.locals.pop(varname, None)
        if tfayj__nyyd is None and varname is not None:
            tfayj__nyyd = self.flags.h5_types.get(varname, None)
        return tfayj__nyyd
