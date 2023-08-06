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
            broqk__qxik = set()
            shm__sstea = list(self.context._get_attribute_templates(self.key))
            sukx__gqtw = shm__sstea.index(self) + 1
            for fyq__gocf in range(sukx__gqtw, len(shm__sstea)):
                if isinstance(shm__sstea[fyq__gocf], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    broqk__qxik.add(shm__sstea[fyq__gocf]._attr)
            self._attr_set = broqk__qxik
        return attr_name in self._attr_set
