"""
Helper functions and classes to simplify Template Generation
for Bodo classes.
"""
import numba
from numba.core.typing.templates import AttributeTemplate


class OverloadedKeyAttributeTemplate(AttributeTemplate):
    _attr_set = None

    def _is_existing_attr(self, attr_name):
        if self._attr_set is None:
            jfzs__galz = set()
            dhj__cwdmn = list(self.context._get_attribute_templates(self.key))
            zowqb__umk = dhj__cwdmn.index(self) + 1
            for cwpf__zzkv in range(zowqb__umk, len(dhj__cwdmn)):
                if isinstance(dhj__cwdmn[cwpf__zzkv], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    jfzs__galz.add(dhj__cwdmn[cwpf__zzkv]._attr)
            self._attr_set = jfzs__galz
        return attr_name in self._attr_set
