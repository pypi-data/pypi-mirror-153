""" Support for Spark parity functions in objmode """
import math
import zlib
import numpy as np
from bodo.utils.typing import gen_objmode_func_overload
gen_objmode_func_overload(zlib.crc32, 'uint32')
gen_objmode_func_overload(math.factorial, 'int64')
gen_objmode_func_overload(np.math.factorial, 'int64')
try:
    import scipy
    gen_objmode_func_overload(scipy.math.factorial, 'int64')
except:
    pass
