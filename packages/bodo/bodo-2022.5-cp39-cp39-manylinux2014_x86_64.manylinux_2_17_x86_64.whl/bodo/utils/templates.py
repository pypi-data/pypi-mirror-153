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
            kaocn__sfgr = set()
            ymx__bamu = list(self.context._get_attribute_templates(self.key))
            lut__esuq = ymx__bamu.index(self) + 1
            for ghz__rim in range(lut__esuq, len(ymx__bamu)):
                if isinstance(ymx__bamu[ghz__rim], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    kaocn__sfgr.add(ymx__bamu[ghz__rim]._attr)
            self._attr_set = kaocn__sfgr
        return attr_name in self._attr_set
