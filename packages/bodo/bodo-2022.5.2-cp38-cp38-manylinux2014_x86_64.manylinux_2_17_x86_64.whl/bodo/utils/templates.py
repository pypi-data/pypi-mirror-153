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
            gjkun__rwwj = set()
            udue__fealx = list(self.context._get_attribute_templates(self.key))
            dnf__vefqd = udue__fealx.index(self) + 1
            for yyi__bfjcc in range(dnf__vefqd, len(udue__fealx)):
                if isinstance(udue__fealx[yyi__bfjcc], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    gjkun__rwwj.add(udue__fealx[yyi__bfjcc]._attr)
            self._attr_set = gjkun__rwwj
        return attr_name in self._attr_set
