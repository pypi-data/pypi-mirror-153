import hashlib
import inspect
import warnings
import pandas as pd
pandas_version = tuple(map(int, pd.__version__.split('.')[:2]))
_check_pandas_change = False
if pandas_version < (1, 4):

    def _set_noconvert_columns(self):
        assert self.orig_names is not None
        wfgl__hrvrj = {kqyph__nfit: xrebq__ikmqp for xrebq__ikmqp,
            kqyph__nfit in enumerate(self.orig_names)}
        xvw__edlec = [wfgl__hrvrj[kqyph__nfit] for kqyph__nfit in self.names]
        srji__dkje = self._set_noconvert_dtype_columns(xvw__edlec, self.names)
        for jjjx__sltwc in srji__dkje:
            self._reader.set_noconvert(jjjx__sltwc)
    if _check_pandas_change:
        lines = inspect.getsource(pd.io.parsers.c_parser_wrapper.
            CParserWrapper._set_noconvert_columns)
        if (hashlib.sha256(lines.encode()).hexdigest() !=
            'afc2d738f194e3976cf05d61cb16dc4224b0139451f08a1cf49c578af6f975d3'
            ):
            warnings.warn(
                'pd.io.parsers.c_parser_wrapper.CParserWrapper._set_noconvert_columns has changed'
                )
    (pd.io.parsers.c_parser_wrapper.CParserWrapper._set_noconvert_columns
        ) = _set_noconvert_columns
