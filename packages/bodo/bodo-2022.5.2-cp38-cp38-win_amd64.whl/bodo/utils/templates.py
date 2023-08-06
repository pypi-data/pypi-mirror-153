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
            ozwm__stg = set()
            vabha__sfig = list(self.context._get_attribute_templates(self.key))
            tzic__gxeoc = vabha__sfig.index(self) + 1
            for hdk__zqwvp in range(tzic__gxeoc, len(vabha__sfig)):
                if isinstance(vabha__sfig[hdk__zqwvp], numba.core.typing.
                    templates._OverloadAttributeTemplate):
                    ozwm__stg.add(vabha__sfig[hdk__zqwvp]._attr)
            self._attr_set = ozwm__stg
        return attr_name in self._attr_set
