"""Support scikit-learn using object mode of Numba """
import itertools
import numbers
import types as pytypes
import warnings
import numba
import numpy as np
import pandas as pd
import sklearn.cluster
import sklearn.ensemble
import sklearn.feature_extraction
import sklearn.linear_model
import sklearn.metrics
import sklearn.model_selection
import sklearn.naive_bayes
import sklearn.svm
import sklearn.utils
from mpi4py import MPI
from numba.core import cgutils, types
from numba.extending import NativeValue, box, models, overload, overload_attribute, overload_method, register_jitable, register_model, typeof_impl, unbox
from scipy import stats
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.metrics import hinge_loss, log_loss, mean_squared_error
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing._data import _handle_zeros_in_scale as sklearn_handle_zeros_in_scale
from sklearn.utils.extmath import _safe_accumulator_op as sklearn_safe_accumulator_op
from sklearn.utils.validation import _check_sample_weight, column_or_1d
import bodo
from bodo.hiframes.pd_dataframe_ext import DataFrameType
from bodo.hiframes.pd_index_ext import NumericIndexType
from bodo.hiframes.pd_series_ext import SeriesType
from bodo.libs.csr_matrix_ext import CSRMatrixType
from bodo.libs.distributed_api import Reduce_Type, create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks, get_num_nodes
from bodo.utils.typing import BodoError, BodoWarning, check_unsupported_args, get_overload_const, get_overload_const_int, get_overload_const_str, is_overload_constant_number, is_overload_constant_str, is_overload_false, is_overload_none, is_overload_true
_is_sklearn_supported_version = False
_min_sklearn_version = 1, 0, 0
_min_sklearn_ver_str = '.'.join(str(x) for x in _min_sklearn_version)
_max_sklearn_version_exclusive = 1, 1, 0
_max_sklearn_ver_str = '.'.join(str(x) for x in _max_sklearn_version_exclusive)
try:
    import re
    import sklearn
    regex = re.compile('(\\d+)\\.(\\d+)\\..*(\\d+)')
    sklearn_version = sklearn.__version__
    m = regex.match(sklearn_version)
    if m:
        ver = tuple(map(int, m.groups()))
        if (ver >= _min_sklearn_version and ver <
            _max_sklearn_version_exclusive):
            _is_sklearn_supported_version = True
except ImportError as ywajq__bej:
    pass


def check_sklearn_version():
    if not _is_sklearn_supported_version:
        mbsrf__abmmv = f""" Bodo supports scikit-learn version >= {_min_sklearn_ver_str} and < {_max_sklearn_ver_str}.
             Installed version is {sklearn.__version__}.
"""
        raise BodoError(mbsrf__abmmv)


def random_forest_model_fit(m, X, y):
    jbqn__atg = m.n_estimators
    eeotg__xva = MPI.Get_processor_name()
    hbsg__smrqh = get_host_ranks()
    mtpqp__cbydp = len(hbsg__smrqh)
    znpd__not = bodo.get_rank()
    m.n_estimators = bodo.libs.distributed_api.get_node_portion(jbqn__atg,
        mtpqp__cbydp, znpd__not)
    if znpd__not == hbsg__smrqh[eeotg__xva][0]:
        m.n_jobs = len(hbsg__smrqh[eeotg__xva])
        if m.random_state is None:
            m.random_state = np.random.RandomState()
        from sklearn.utils import parallel_backend
        with parallel_backend('threading'):
            m.fit(X, y)
        m.n_jobs = 1
    with numba.objmode(first_rank_node='int32[:]'):
        first_rank_node = get_nodes_first_ranks()
    nurmz__lhiqq = create_subcomm_mpi4py(first_rank_node)
    if nurmz__lhiqq != MPI.COMM_NULL:
        clbrk__pvpki = 10
        jgncj__dcjbc = bodo.libs.distributed_api.get_node_portion(jbqn__atg,
            mtpqp__cbydp, 0)
        awhz__hfe = jgncj__dcjbc // clbrk__pvpki
        if jgncj__dcjbc % clbrk__pvpki != 0:
            awhz__hfe += 1
        lww__oqpf = []
        for rmu__ufq in range(awhz__hfe):
            lsyz__yhah = nurmz__lhiqq.gather(m.estimators_[rmu__ufq *
                clbrk__pvpki:rmu__ufq * clbrk__pvpki + clbrk__pvpki])
            if znpd__not == 0:
                lww__oqpf += list(itertools.chain.from_iterable(lsyz__yhah))
        if znpd__not == 0:
            m.estimators_ = lww__oqpf
    ylh__qmk = MPI.COMM_WORLD
    if znpd__not == 0:
        for rmu__ufq in range(0, jbqn__atg, 10):
            ylh__qmk.bcast(m.estimators_[rmu__ufq:rmu__ufq + 10])
        if isinstance(m, sklearn.ensemble.RandomForestClassifier):
            ylh__qmk.bcast(m.n_classes_)
            ylh__qmk.bcast(m.classes_)
        ylh__qmk.bcast(m.n_outputs_)
    else:
        bpmhh__hsyye = []
        for rmu__ufq in range(0, jbqn__atg, 10):
            bpmhh__hsyye += ylh__qmk.bcast(None)
        if isinstance(m, sklearn.ensemble.RandomForestClassifier):
            m.n_classes_ = ylh__qmk.bcast(None)
            m.classes_ = ylh__qmk.bcast(None)
        m.n_outputs_ = ylh__qmk.bcast(None)
        m.estimators_ = bpmhh__hsyye
    assert len(m.estimators_) == jbqn__atg
    m.n_estimators = jbqn__atg
    m.n_features_in_ = X.shape[1]


class BodoRandomForestClassifierType(types.Opaque):

    def __init__(self):
        super(BodoRandomForestClassifierType, self).__init__(name=
            'BodoRandomForestClassifierType')


random_forest_classifier_type = BodoRandomForestClassifierType()
types.random_forest_classifier_type = random_forest_classifier_type
register_model(BodoRandomForestClassifierType)(models.OpaqueModel)


@typeof_impl.register(sklearn.ensemble.RandomForestClassifier)
def typeof_random_forest_classifier(val, c):
    return random_forest_classifier_type


@box(BodoRandomForestClassifierType)
def box_random_forest_classifier(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoRandomForestClassifierType)
def unbox_random_forest_classifier(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.ensemble.RandomForestClassifier, no_unliteral=True)
def sklearn_ensemble_RandomForestClassifier_overload(n_estimators=100,
    criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf
    =1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=
    None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False,
    n_jobs=None, random_state=None, verbose=0, warm_start=False,
    class_weight=None, ccp_alpha=0.0, max_samples=None):
    check_sklearn_version()

    def _sklearn_ensemble_RandomForestClassifier_impl(n_estimators=100,
        criterion='gini', max_depth=None, min_samples_split=2,
        min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=
        'auto', max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=
        True, oob_score=False, n_jobs=None, random_state=None, verbose=0,
        warm_start=False, class_weight=None, ccp_alpha=0.0, max_samples=None):
        with numba.objmode(m='random_forest_classifier_type'):
            if random_state is not None and get_num_nodes() > 1:
                print(
                    'With multinode, fixed random_state seed values are ignored.\n'
                    )
                random_state = None
            m = sklearn.ensemble.RandomForestClassifier(n_estimators=
                n_estimators, criterion=criterion, max_depth=max_depth,
                min_samples_split=min_samples_split, min_samples_leaf=
                min_samples_leaf, min_weight_fraction_leaf=
                min_weight_fraction_leaf, max_features=max_features,
                max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=
                min_impurity_decrease, bootstrap=bootstrap, oob_score=
                oob_score, n_jobs=1, random_state=random_state, verbose=
                verbose, warm_start=warm_start, class_weight=class_weight,
                ccp_alpha=ccp_alpha, max_samples=max_samples)
        return m
    return _sklearn_ensemble_RandomForestClassifier_impl


def parallel_predict_regression(m, X):
    check_sklearn_version()

    def _model_predict_impl(m, X):
        with numba.objmode(result='float64[:]'):
            m.n_jobs = 1
            if len(X) == 0:
                result = np.empty(0, dtype=np.float64)
            else:
                result = m.predict(X).astype(np.float64).flatten()
        return result
    return _model_predict_impl


def parallel_predict(m, X):
    check_sklearn_version()

    def _model_predict_impl(m, X):
        with numba.objmode(result='int64[:]'):
            m.n_jobs = 1
            if X.shape[0] == 0:
                result = np.empty(0, dtype=np.int64)
            else:
                result = m.predict(X).astype(np.int64).flatten()
        return result
    return _model_predict_impl


def parallel_predict_proba(m, X):
    check_sklearn_version()

    def _model_predict_proba_impl(m, X):
        with numba.objmode(result='float64[:,:]'):
            m.n_jobs = 1
            if X.shape[0] == 0:
                result = np.empty((0, 0), dtype=np.float64)
            else:
                result = m.predict_proba(X).astype(np.float64)
        return result
    return _model_predict_proba_impl


def parallel_predict_log_proba(m, X):
    check_sklearn_version()

    def _model_predict_log_proba_impl(m, X):
        with numba.objmode(result='float64[:,:]'):
            m.n_jobs = 1
            if X.shape[0] == 0:
                result = np.empty((0, 0), dtype=np.float64)
            else:
                result = m.predict_log_proba(X).astype(np.float64)
        return result
    return _model_predict_log_proba_impl


def parallel_score(m, X, y, sample_weight=None, _is_data_distributed=False):
    check_sklearn_version()

    def _model_score_impl(m, X, y, sample_weight=None, _is_data_distributed
        =False):
        with numba.objmode(result='float64[:]'):
            result = m.score(X, y, sample_weight=sample_weight)
            if _is_data_distributed:
                result = np.full(len(y), result)
            else:
                result = np.array([result])
        if _is_data_distributed:
            result = bodo.allgatherv(result)
        return result.mean()
    return _model_score_impl


@overload_method(BodoRandomForestClassifierType, 'predict', no_unliteral=True)
def overload_model_predict(m, X):
    check_sklearn_version()
    """Overload Random Forest Classifier predict. (Data parallelization)"""
    return parallel_predict(m, X)


@overload_method(BodoRandomForestClassifierType, 'predict_proba',
    no_unliteral=True)
def overload_rf_predict_proba(m, X):
    check_sklearn_version()
    """Overload Random Forest Classifier predict_proba. (Data parallelization)"""
    return parallel_predict_proba(m, X)


@overload_method(BodoRandomForestClassifierType, 'predict_log_proba',
    no_unliteral=True)
def overload_rf_predict_log_proba(m, X):
    check_sklearn_version()
    """Overload Random Forest Classifier predict_log_proba. (Data parallelization)"""
    return parallel_predict_log_proba(m, X)


@overload_method(BodoRandomForestClassifierType, 'score', no_unliteral=True)
def overload_model_score(m, X, y, sample_weight=None, _is_data_distributed=
    False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


def precision_recall_fscore_support_helper(MCM, average):

    def multilabel_confusion_matrix(y_true, y_pred, *, sample_weight=None,
        labels=None, samplewise=False):
        return MCM
    fbz__hrb = sklearn.metrics._classification.multilabel_confusion_matrix
    result = -1.0
    try:
        sklearn.metrics._classification.multilabel_confusion_matrix = (
            multilabel_confusion_matrix)
        result = (sklearn.metrics._classification.
            precision_recall_fscore_support([], [], average=average))
    finally:
        sklearn.metrics._classification.multilabel_confusion_matrix = fbz__hrb
    return result


@numba.njit
def precision_recall_fscore_parallel(y_true, y_pred, operation, average=
    'binary'):
    labels = bodo.libs.array_kernels.unique(y_true, parallel=True)
    labels = bodo.allgatherv(labels, False)
    labels = bodo.libs.array_kernels.sort(labels, ascending=True, inplace=False
        )
    mdb__dycwh = len(labels)
    mfduf__uzu = np.zeros(mdb__dycwh, np.int64)
    hsf__zwq = np.zeros(mdb__dycwh, np.int64)
    lknr__rkxg = np.zeros(mdb__dycwh, np.int64)
    toqv__vcg = (bodo.hiframes.pd_categorical_ext.
        get_label_dict_from_categories(labels))
    for rmu__ufq in range(len(y_true)):
        hsf__zwq[toqv__vcg[y_true[rmu__ufq]]] += 1
        if y_pred[rmu__ufq] not in toqv__vcg:
            continue
        eppp__npuxj = toqv__vcg[y_pred[rmu__ufq]]
        lknr__rkxg[eppp__npuxj] += 1
        if y_true[rmu__ufq] == y_pred[rmu__ufq]:
            mfduf__uzu[eppp__npuxj] += 1
    mfduf__uzu = bodo.libs.distributed_api.dist_reduce(mfduf__uzu, np.int32
        (Reduce_Type.Sum.value))
    hsf__zwq = bodo.libs.distributed_api.dist_reduce(hsf__zwq, np.int32(
        Reduce_Type.Sum.value))
    lknr__rkxg = bodo.libs.distributed_api.dist_reduce(lknr__rkxg, np.int32
        (Reduce_Type.Sum.value))
    ckj__rrk = lknr__rkxg - mfduf__uzu
    hlc__odji = hsf__zwq - mfduf__uzu
    jxyxh__zph = mfduf__uzu
    ati__ilqfj = y_true.shape[0] - jxyxh__zph - ckj__rrk - hlc__odji
    with numba.objmode(result='float64[:]'):
        MCM = np.array([ati__ilqfj, ckj__rrk, hlc__odji, jxyxh__zph]
            ).T.reshape(-1, 2, 2)
        if operation == 'precision':
            result = precision_recall_fscore_support_helper(MCM, average)[0]
        elif operation == 'recall':
            result = precision_recall_fscore_support_helper(MCM, average)[1]
        elif operation == 'f1':
            result = precision_recall_fscore_support_helper(MCM, average)[2]
        if average is not None:
            result = np.array([result])
    return result


@overload(sklearn.metrics.precision_score, no_unliteral=True)
def overload_precision_score(y_true, y_pred, labels=None, pos_label=1,
    average='binary', sample_weight=None, zero_division='warn',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _precision_score_impl(y_true, y_pred, labels=None,
                pos_label=1, average='binary', sample_weight=None,
                zero_division='warn', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.precision_score(y_true, y_pred,
                        labels=labels, pos_label=pos_label, average=average,
                        sample_weight=sample_weight, zero_division=
                        zero_division)
                return score
            return _precision_score_impl
        else:

            def _precision_score_impl(y_true, y_pred, labels=None,
                pos_label=1, average='binary', sample_weight=None,
                zero_division='warn', _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'precision', average=average)
            return _precision_score_impl
    elif is_overload_false(_is_data_distributed):

        def _precision_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.precision_score(y_true, y_pred,
                    labels=labels, pos_label=pos_label, average=average,
                    sample_weight=sample_weight, zero_division=zero_division)
            return score
        return _precision_score_impl
    else:

        def _precision_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred,
                'precision', average=average)
            return score[0]
        return _precision_score_impl


@overload(sklearn.metrics.recall_score, no_unliteral=True)
def overload_recall_score(y_true, y_pred, labels=None, pos_label=1, average
    ='binary', sample_weight=None, zero_division='warn',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.recall_score(y_true, y_pred,
                        labels=labels, pos_label=pos_label, average=average,
                        sample_weight=sample_weight, zero_division=
                        zero_division)
                return score
            return _recall_score_impl
        else:

            def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'recall', average=average)
            return _recall_score_impl
    elif is_overload_false(_is_data_distributed):

        def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.recall_score(y_true, y_pred, labels
                    =labels, pos_label=pos_label, average=average,
                    sample_weight=sample_weight, zero_division=zero_division)
            return score
        return _recall_score_impl
    else:

        def _recall_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred,
                'recall', average=average)
            return score[0]
        return _recall_score_impl


@overload(sklearn.metrics.f1_score, no_unliteral=True)
def overload_f1_score(y_true, y_pred, labels=None, pos_label=1, average=
    'binary', sample_weight=None, zero_division='warn',
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_none(average):
        if is_overload_false(_is_data_distributed):

            def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    score = sklearn.metrics.f1_score(y_true, y_pred, labels
                        =labels, pos_label=pos_label, average=average,
                        sample_weight=sample_weight, zero_division=
                        zero_division)
                return score
            return _f1_score_impl
        else:

            def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
                average='binary', sample_weight=None, zero_division='warn',
                _is_data_distributed=False):
                return precision_recall_fscore_parallel(y_true, y_pred,
                    'f1', average=average)
            return _f1_score_impl
    elif is_overload_false(_is_data_distributed):

        def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = sklearn.metrics.f1_score(y_true, y_pred, labels=
                    labels, pos_label=pos_label, average=average,
                    sample_weight=sample_weight, zero_division=zero_division)
            return score
        return _f1_score_impl
    else:

        def _f1_score_impl(y_true, y_pred, labels=None, pos_label=1,
            average='binary', sample_weight=None, zero_division='warn',
            _is_data_distributed=False):
            score = precision_recall_fscore_parallel(y_true, y_pred, 'f1',
                average=average)
            return score[0]
        return _f1_score_impl


def mse_mae_dist_helper(y_true, y_pred, sample_weight, multioutput, squared,
    metric):
    if metric == 'mse':
        cuad__oasty = sklearn.metrics.mean_squared_error(y_true, y_pred,
            sample_weight=sample_weight, multioutput='raw_values', squared=True
            )
    elif metric == 'mae':
        cuad__oasty = sklearn.metrics.mean_absolute_error(y_true, y_pred,
            sample_weight=sample_weight, multioutput='raw_values')
    else:
        raise RuntimeError(
            f"Unrecognized metric {metric}. Must be one of 'mae' and 'mse'")
    ylh__qmk = MPI.COMM_WORLD
    cvo__isst = ylh__qmk.Get_size()
    if sample_weight is not None:
        szx__hlc = np.sum(sample_weight)
    else:
        szx__hlc = np.float64(y_true.shape[0])
    ubrk__svl = np.zeros(cvo__isst, dtype=type(szx__hlc))
    ylh__qmk.Allgather(szx__hlc, ubrk__svl)
    guv__zkbpc = np.zeros((cvo__isst, *cuad__oasty.shape), dtype=
        cuad__oasty.dtype)
    ylh__qmk.Allgather(cuad__oasty, guv__zkbpc)
    bqcla__hxhf = np.average(guv__zkbpc, weights=ubrk__svl, axis=0)
    if metric == 'mse' and not squared:
        bqcla__hxhf = np.sqrt(bqcla__hxhf)
    if isinstance(multioutput, str) and multioutput == 'raw_values':
        return bqcla__hxhf
    elif isinstance(multioutput, str) and multioutput == 'uniform_average':
        return np.average(bqcla__hxhf)
    else:
        return np.average(bqcla__hxhf, weights=multioutput)


@overload(sklearn.metrics.mean_squared_error, no_unliteral=True)
def overload_mean_squared_error(y_true, y_pred, sample_weight=None,
    multioutput='uniform_average', squared=True, _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', squared=True, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=squared, metric='mse')
                    else:
                        err = sklearn.metrics.mean_squared_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput, squared=squared)
                return err
            return _mse_impl
        else:

            def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', squared=True, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=squared, metric='mse')
                    else:
                        err = sklearn.metrics.mean_squared_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput, squared=squared)
                return err
            return _mse_impl
    elif is_overload_none(sample_weight):

        def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', squared=True, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        squared, metric='mse')
                else:
                    err = sklearn.metrics.mean_squared_error(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=
                        multioutput, squared=squared)
            return err
        return _mse_impl
    else:

        def _mse_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', squared=True, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        squared, metric='mse')
                else:
                    err = sklearn.metrics.mean_squared_error(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=
                        multioutput, squared=squared)
            return err
        return _mse_impl


@overload(sklearn.metrics.mean_absolute_error, no_unliteral=True)
def overload_mean_absolute_error(y_true, y_pred, sample_weight=None,
    multioutput='uniform_average', _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=True, metric='mae')
                    else:
                        err = sklearn.metrics.mean_absolute_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput)
                return err
            return _mae_impl
        else:

            def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
                'uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(err='float64[:]'):
                    if _is_data_distributed:
                        err = mse_mae_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput, squared=True, metric='mae')
                    else:
                        err = sklearn.metrics.mean_absolute_error(y_true,
                            y_pred, sample_weight=sample_weight,
                            multioutput=multioutput)
                return err
            return _mae_impl
    elif is_overload_none(sample_weight):

        def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        True, metric='mae')
                else:
                    err = sklearn.metrics.mean_absolute_error(y_true,
                        y_pred, sample_weight=sample_weight, multioutput=
                        multioutput)
            return err
        return _mae_impl
    else:

        def _mae_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(err='float64'):
                if _is_data_distributed:
                    err = mse_mae_dist_helper(y_true, y_pred, sample_weight
                        =sample_weight, multioutput=multioutput, squared=
                        True, metric='mae')
                else:
                    err = sklearn.metrics.mean_absolute_error(y_true,
                        y_pred, sample_weight=sample_weight, multioutput=
                        multioutput)
            return err
        return _mae_impl


def accuracy_score_dist_helper(y_true, y_pred, normalize, sample_weight):
    score = sklearn.metrics.accuracy_score(y_true, y_pred, normalize=False,
        sample_weight=sample_weight)
    ylh__qmk = MPI.COMM_WORLD
    score = ylh__qmk.allreduce(score, op=MPI.SUM)
    if normalize:
        nal__imujl = np.sum(sample_weight
            ) if sample_weight is not None else len(y_true)
        nal__imujl = ylh__qmk.allreduce(nal__imujl, op=MPI.SUM)
        score = score / nal__imujl
    return score


@overload(sklearn.metrics.accuracy_score, no_unliteral=True)
def overload_accuracy_score(y_true, y_pred, normalize=True, sample_weight=
    None, _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_false(_is_data_distributed):
        if is_overload_none(sample_weight):

            def _accuracy_score_impl(y_true, y_pred, normalize=True,
                sample_weight=None, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64'):
                    score = sklearn.metrics.accuracy_score(y_true, y_pred,
                        normalize=normalize, sample_weight=sample_weight)
                return score
            return _accuracy_score_impl
        else:

            def _accuracy_score_impl(y_true, y_pred, normalize=True,
                sample_weight=None, _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(score='float64'):
                    score = sklearn.metrics.accuracy_score(y_true, y_pred,
                        normalize=normalize, sample_weight=sample_weight)
                return score
            return _accuracy_score_impl
    elif is_overload_none(sample_weight):

        def _accuracy_score_impl(y_true, y_pred, normalize=True,
            sample_weight=None, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                score = accuracy_score_dist_helper(y_true, y_pred,
                    normalize=normalize, sample_weight=sample_weight)
            return score
        return _accuracy_score_impl
    else:

        def _accuracy_score_impl(y_true, y_pred, normalize=True,
            sample_weight=None, _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(score='float64'):
                score = accuracy_score_dist_helper(y_true, y_pred,
                    normalize=normalize, sample_weight=sample_weight)
            return score
        return _accuracy_score_impl


def check_consistent_length_parallel(*arrays):
    ylh__qmk = MPI.COMM_WORLD
    cot__kjw = True
    rwhd__hmbv = [len(wnpu__yexy) for wnpu__yexy in arrays if wnpu__yexy is not
        None]
    if len(np.unique(rwhd__hmbv)) > 1:
        cot__kjw = False
    cot__kjw = ylh__qmk.allreduce(cot__kjw, op=MPI.LAND)
    return cot__kjw


def r2_score_dist_helper(y_true, y_pred, sample_weight, multioutput):
    ylh__qmk = MPI.COMM_WORLD
    if y_true.ndim == 1:
        y_true = y_true.reshape((-1, 1))
    if y_pred.ndim == 1:
        y_pred = y_pred.reshape((-1, 1))
    if not check_consistent_length_parallel(y_true, y_pred, sample_weight):
        raise ValueError(
            'y_true, y_pred and sample_weight (if not None) have inconsistent number of samples'
            )
    lzsi__ztmp = y_true.shape[0]
    pgw__eyxs = ylh__qmk.allreduce(lzsi__ztmp, op=MPI.SUM)
    if pgw__eyxs < 2:
        warnings.warn(
            'R^2 score is not well-defined with less than two samples.',
            UndefinedMetricWarning)
        return np.array([float('nan')])
    if sample_weight is not None:
        sample_weight = column_or_1d(sample_weight)
        rgxx__vdatq = sample_weight[:, np.newaxis]
    else:
        sample_weight = np.float64(y_true.shape[0])
        rgxx__vdatq = 1.0
    elatp__ijy = (rgxx__vdatq * (y_true - y_pred) ** 2).sum(axis=0, dtype=
        np.float64)
    uael__lmu = np.zeros(elatp__ijy.shape, dtype=elatp__ijy.dtype)
    ylh__qmk.Allreduce(elatp__ijy, uael__lmu, op=MPI.SUM)
    obynv__njdf = np.nansum(y_true * rgxx__vdatq, axis=0, dtype=np.float64)
    ejtpo__homex = np.zeros_like(obynv__njdf)
    ylh__qmk.Allreduce(obynv__njdf, ejtpo__homex, op=MPI.SUM)
    elwb__ecpqn = np.nansum(sample_weight, dtype=np.float64)
    vwij__qzyq = ylh__qmk.allreduce(elwb__ecpqn, op=MPI.SUM)
    niulu__qwx = ejtpo__homex / vwij__qzyq
    rmjky__giw = (rgxx__vdatq * (y_true - niulu__qwx) ** 2).sum(axis=0,
        dtype=np.float64)
    riqgm__neu = np.zeros(rmjky__giw.shape, dtype=rmjky__giw.dtype)
    ylh__qmk.Allreduce(rmjky__giw, riqgm__neu, op=MPI.SUM)
    bes__kpp = riqgm__neu != 0
    grgnd__olusm = uael__lmu != 0
    ugd__cfzf = bes__kpp & grgnd__olusm
    zij__deei = np.ones([y_true.shape[1] if len(y_true.shape) > 1 else 1])
    zij__deei[ugd__cfzf] = 1 - uael__lmu[ugd__cfzf] / riqgm__neu[ugd__cfzf]
    zij__deei[grgnd__olusm & ~bes__kpp] = 0.0
    if isinstance(multioutput, str):
        if multioutput == 'raw_values':
            return zij__deei
        elif multioutput == 'uniform_average':
            lqptf__gznyc = None
        elif multioutput == 'variance_weighted':
            lqptf__gznyc = riqgm__neu
            if not np.any(bes__kpp):
                if not np.any(grgnd__olusm):
                    return np.array([1.0])
                else:
                    return np.array([0.0])
    else:
        lqptf__gznyc = multioutput
    return np.array([np.average(zij__deei, weights=lqptf__gznyc)])


@overload(sklearn.metrics.r2_score, no_unliteral=True)
def overload_r2_score(y_true, y_pred, sample_weight=None, multioutput=
    'uniform_average', _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) not in ['raw_values', 'uniform_average',
        'variance_weighted']:
        raise BodoError(
            f"Unsupported argument {get_overload_const_str(multioutput)} specified for 'multioutput'"
            )
    if is_overload_constant_str(multioutput) and get_overload_const_str(
        multioutput) == 'raw_values':
        if is_overload_none(sample_weight):

            def _r2_score_impl(y_true, y_pred, sample_weight=None,
                multioutput='uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                with numba.objmode(score='float64[:]'):
                    if _is_data_distributed:
                        score = r2_score_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                    else:
                        score = sklearn.metrics.r2_score(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                return score
            return _r2_score_impl
        else:

            def _r2_score_impl(y_true, y_pred, sample_weight=None,
                multioutput='uniform_average', _is_data_distributed=False):
                y_true = bodo.utils.conversion.coerce_to_array(y_true)
                y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
                sample_weight = bodo.utils.conversion.coerce_to_array(
                    sample_weight)
                with numba.objmode(score='float64[:]'):
                    if _is_data_distributed:
                        score = r2_score_dist_helper(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                    else:
                        score = sklearn.metrics.r2_score(y_true, y_pred,
                            sample_weight=sample_weight, multioutput=
                            multioutput)
                return score
            return _r2_score_impl
    elif is_overload_none(sample_weight):

        def _r2_score_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            with numba.objmode(score='float64'):
                if _is_data_distributed:
                    score = r2_score_dist_helper(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
                    score = score[0]
                else:
                    score = sklearn.metrics.r2_score(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
            return score
        return _r2_score_impl
    else:

        def _r2_score_impl(y_true, y_pred, sample_weight=None, multioutput=
            'uniform_average', _is_data_distributed=False):
            y_true = bodo.utils.conversion.coerce_to_array(y_true)
            y_pred = bodo.utils.conversion.coerce_to_array(y_pred)
            sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight
                )
            with numba.objmode(score='float64'):
                if _is_data_distributed:
                    score = r2_score_dist_helper(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
                    score = score[0]
                else:
                    score = sklearn.metrics.r2_score(y_true, y_pred,
                        sample_weight=sample_weight, multioutput=multioutput)
            return score
        return _r2_score_impl


def confusion_matrix_dist_helper(y_true, y_pred, labels=None, sample_weight
    =None, normalize=None):
    if normalize not in ['true', 'pred', 'all', None]:
        raise ValueError(
            "normalize must be one of {'true', 'pred', 'all', None}")
    ylh__qmk = MPI.COMM_WORLD
    try:
        pbh__rgl = sklearn.metrics.confusion_matrix(y_true, y_pred, labels=
            labels, sample_weight=sample_weight, normalize=None)
    except ValueError as wmump__keqoo:
        pbh__rgl = wmump__keqoo
    btg__qzdu = isinstance(pbh__rgl, ValueError
        ) and 'At least one label specified must be in y_true' in pbh__rgl.args[
        0]
    lhpvw__furre = ylh__qmk.allreduce(btg__qzdu, op=MPI.LAND)
    if lhpvw__furre:
        raise pbh__rgl
    elif btg__qzdu:
        dtype = np.int64
        if sample_weight is not None and sample_weight.dtype.kind not in {'i',
            'u', 'b'}:
            dtype = np.float64
        ipnoo__qrnq = np.zeros((labels.size, labels.size), dtype=dtype)
    else:
        ipnoo__qrnq = pbh__rgl
    psluy__bpsou = np.zeros_like(ipnoo__qrnq)
    ylh__qmk.Allreduce(ipnoo__qrnq, psluy__bpsou)
    with np.errstate(all='ignore'):
        if normalize == 'true':
            psluy__bpsou = psluy__bpsou / psluy__bpsou.sum(axis=1, keepdims
                =True)
        elif normalize == 'pred':
            psluy__bpsou = psluy__bpsou / psluy__bpsou.sum(axis=0, keepdims
                =True)
        elif normalize == 'all':
            psluy__bpsou = psluy__bpsou / psluy__bpsou.sum()
        psluy__bpsou = np.nan_to_num(psluy__bpsou)
    return psluy__bpsou


@overload(sklearn.metrics.confusion_matrix, no_unliteral=True)
def overload_confusion_matrix(y_true, y_pred, labels=None, sample_weight=
    None, normalize=None, _is_data_distributed=False):
    check_sklearn_version()
    krgh__mcf = 'def _confusion_matrix_impl(\n'
    krgh__mcf += '    y_true, y_pred, labels=None,\n'
    krgh__mcf += '    sample_weight=None, normalize=None,\n'
    krgh__mcf += '    _is_data_distributed=False,\n'
    krgh__mcf += '):\n'
    krgh__mcf += '    y_true = bodo.utils.conversion.coerce_to_array(y_true)\n'
    krgh__mcf += '    y_pred = bodo.utils.conversion.coerce_to_array(y_pred)\n'
    krgh__mcf += (
        '    y_true = bodo.utils.typing.decode_if_dict_array(y_true)\n')
    krgh__mcf += (
        '    y_pred = bodo.utils.typing.decode_if_dict_array(y_pred)\n')
    rmv__uqlfw = 'int64[:,:]', 'np.int64'
    if not is_overload_none(normalize):
        rmv__uqlfw = 'float64[:,:]', 'np.float64'
    if not is_overload_none(sample_weight):
        krgh__mcf += (
            '    sample_weight = bodo.utils.conversion.coerce_to_array(sample_weight)\n'
            )
        if numba.np.numpy_support.as_dtype(sample_weight.dtype).kind not in {
            'i', 'u', 'b'}:
            rmv__uqlfw = 'float64[:,:]', 'np.float64'
    if not is_overload_none(labels):
        krgh__mcf += (
            '    labels = bodo.utils.conversion.coerce_to_array(labels)\n')
    elif is_overload_true(_is_data_distributed):
        krgh__mcf += (
            '    labels = bodo.libs.array_kernels.concat([y_true, y_pred])\n')
        krgh__mcf += (
            '    labels = bodo.libs.array_kernels.unique(labels, parallel=True)\n'
            )
        krgh__mcf += '    labels = bodo.allgatherv(labels, False)\n'
        krgh__mcf += """    labels = bodo.libs.array_kernels.sort(labels, ascending=True, inplace=False)
"""
    krgh__mcf += f"    with numba.objmode(cm='{rmv__uqlfw[0]}'):\n"
    if is_overload_false(_is_data_distributed):
        krgh__mcf += '      cm = sklearn.metrics.confusion_matrix(\n'
    else:
        krgh__mcf += '      cm = confusion_matrix_dist_helper(\n'
    krgh__mcf += '        y_true, y_pred, labels=labels,\n'
    krgh__mcf += '        sample_weight=sample_weight, normalize=normalize,\n'
    krgh__mcf += f'      ).astype({rmv__uqlfw[1]})\n'
    krgh__mcf += '    return cm\n'
    szwxm__wcnjd = {}
    exec(krgh__mcf, globals(), szwxm__wcnjd)
    efp__ofkz = szwxm__wcnjd['_confusion_matrix_impl']
    return efp__ofkz


class BodoSGDRegressorType(types.Opaque):

    def __init__(self):
        super(BodoSGDRegressorType, self).__init__(name='BodoSGDRegressorType')


sgd_regressor_type = BodoSGDRegressorType()
types.sgd_regressor_type = sgd_regressor_type
register_model(BodoSGDRegressorType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.SGDRegressor)
def typeof_sgd_regressor(val, c):
    return sgd_regressor_type


@box(BodoSGDRegressorType)
def box_sgd_regressor(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoSGDRegressorType)
def unbox_sgd_regressor(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.SGDRegressor, no_unliteral=True)
def sklearn_linear_model_SGDRegressor_overload(loss='squared_error',
    penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter
    =1000, tol=0.001, shuffle=True, verbose=0, epsilon=0.1, random_state=
    None, learning_rate='invscaling', eta0=0.01, power_t=0.25,
    early_stopping=False, validation_fraction=0.1, n_iter_no_change=5,
    warm_start=False, average=False):
    check_sklearn_version()

    def _sklearn_linear_model_SGDRegressor_impl(loss='squared_error',
        penalty='l2', alpha=0.0001, l1_ratio=0.15, fit_intercept=True,
        max_iter=1000, tol=0.001, shuffle=True, verbose=0, epsilon=0.1,
        random_state=None, learning_rate='invscaling', eta0=0.01, power_t=
        0.25, early_stopping=False, validation_fraction=0.1,
        n_iter_no_change=5, warm_start=False, average=False):
        with numba.objmode(m='sgd_regressor_type'):
            m = sklearn.linear_model.SGDRegressor(loss=loss, penalty=
                penalty, alpha=alpha, l1_ratio=l1_ratio, fit_intercept=
                fit_intercept, max_iter=max_iter, tol=tol, shuffle=shuffle,
                verbose=verbose, epsilon=epsilon, random_state=random_state,
                learning_rate=learning_rate, eta0=eta0, power_t=power_t,
                early_stopping=early_stopping, validation_fraction=
                validation_fraction, n_iter_no_change=n_iter_no_change,
                warm_start=warm_start, average=average)
        return m
    return _sklearn_linear_model_SGDRegressor_impl


@overload_method(BodoSGDRegressorType, 'fit', no_unliteral=True)
def overload_sgdr_model_fit(m, X, y, coef_init=None, intercept_init=None,
    sample_weight=None, _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_true(_is_data_distributed):
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.SGDRegressor.fit() : 'sample_weight' is not supported for distributed data."
                )
        if not is_overload_none(coef_init):
            raise BodoError(
                "sklearn.linear_model.SGDRegressor.fit() : 'coef_init' is not supported for distributed data."
                )
        if not is_overload_none(intercept_init):
            raise BodoError(
                "sklearn.linear_model.SGDRegressor.fit() : 'intercept_init' is not supported for distributed data."
                )

        def _model_sgdr_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='sgd_regressor_type'):
                m = fit_sgd(m, X, y, _is_data_distributed)
            bodo.barrier()
            return m
        return _model_sgdr_fit_impl
    else:

        def _model_sgdr_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='sgd_regressor_type'):
                m = m.fit(X, y, coef_init, intercept_init, sample_weight)
            return m
        return _model_sgdr_fit_impl


@overload_method(BodoSGDRegressorType, 'predict', no_unliteral=True)
def overload_sgdr_model_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoSGDRegressorType, 'score', no_unliteral=True)
def overload_sgdr_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


class BodoSGDClassifierType(types.Opaque):

    def __init__(self):
        super(BodoSGDClassifierType, self).__init__(name=
            'BodoSGDClassifierType')


sgd_classifier_type = BodoSGDClassifierType()
types.sgd_classifier_type = sgd_classifier_type
register_model(BodoSGDClassifierType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.SGDClassifier)
def typeof_sgd_classifier(val, c):
    return sgd_classifier_type


@box(BodoSGDClassifierType)
def box_sgd_classifier(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoSGDClassifierType)
def unbox_sgd_classifier(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.SGDClassifier, no_unliteral=True)
def sklearn_linear_model_SGDClassifier_overload(loss='hinge', penalty='l2',
    alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter=1000, tol=
    0.001, shuffle=True, verbose=0, epsilon=0.1, n_jobs=None, random_state=
    None, learning_rate='optimal', eta0=0.0, power_t=0.5, early_stopping=
    False, validation_fraction=0.1, n_iter_no_change=5, class_weight=None,
    warm_start=False, average=False):
    check_sklearn_version()

    def _sklearn_linear_model_SGDClassifier_impl(loss='hinge', penalty='l2',
        alpha=0.0001, l1_ratio=0.15, fit_intercept=True, max_iter=1000, tol
        =0.001, shuffle=True, verbose=0, epsilon=0.1, n_jobs=None,
        random_state=None, learning_rate='optimal', eta0=0.0, power_t=0.5,
        early_stopping=False, validation_fraction=0.1, n_iter_no_change=5,
        class_weight=None, warm_start=False, average=False):
        with numba.objmode(m='sgd_classifier_type'):
            m = sklearn.linear_model.SGDClassifier(loss=loss, penalty=
                penalty, alpha=alpha, l1_ratio=l1_ratio, fit_intercept=
                fit_intercept, max_iter=max_iter, tol=tol, shuffle=shuffle,
                verbose=verbose, epsilon=epsilon, n_jobs=n_jobs,
                random_state=random_state, learning_rate=learning_rate,
                eta0=eta0, power_t=power_t, early_stopping=early_stopping,
                validation_fraction=validation_fraction, n_iter_no_change=
                n_iter_no_change, class_weight=class_weight, warm_start=
                warm_start, average=average)
        return m
    return _sklearn_linear_model_SGDClassifier_impl


def fit_sgd(m, X, y, y_classes=None, _is_data_distributed=False):
    ylh__qmk = MPI.COMM_WORLD
    nznt__jteyl = ylh__qmk.allreduce(len(X), op=MPI.SUM)
    uhuod__lkl = len(X) / nznt__jteyl
    maex__iezm = ylh__qmk.Get_size()
    m.n_jobs = 1
    m.early_stopping = False
    ttlzb__mtvpq = np.inf
    zsphb__lgwz = 0
    if m.loss == 'hinge':
        qnuvg__ywf = hinge_loss
    elif m.loss == 'log':
        qnuvg__ywf = log_loss
    elif m.loss == 'squared_error':
        qnuvg__ywf = mean_squared_error
    else:
        raise ValueError('loss {} not supported'.format(m.loss))
    zzfc__zer = False
    if isinstance(m, sklearn.linear_model.SGDRegressor):
        zzfc__zer = True
    for qwrx__zsiq in range(m.max_iter):
        if zzfc__zer:
            m.partial_fit(X, y)
        else:
            m.partial_fit(X, y, classes=y_classes)
        m.coef_ = m.coef_ * uhuod__lkl
        m.coef_ = ylh__qmk.allreduce(m.coef_, op=MPI.SUM)
        m.intercept_ = m.intercept_ * uhuod__lkl
        m.intercept_ = ylh__qmk.allreduce(m.intercept_, op=MPI.SUM)
        if zzfc__zer:
            y_pred = m.predict(X)
            ejbh__rzc = qnuvg__ywf(y, y_pred)
        else:
            y_pred = m.decision_function(X)
            ejbh__rzc = qnuvg__ywf(y, y_pred, labels=y_classes)
        oiyu__tdozz = ylh__qmk.allreduce(ejbh__rzc, op=MPI.SUM)
        ejbh__rzc = oiyu__tdozz / maex__iezm
        if m.tol > np.NINF and ejbh__rzc > ttlzb__mtvpq - m.tol * nznt__jteyl:
            zsphb__lgwz += 1
        else:
            zsphb__lgwz = 0
        if ejbh__rzc < ttlzb__mtvpq:
            ttlzb__mtvpq = ejbh__rzc
        if zsphb__lgwz >= m.n_iter_no_change:
            break
    return m


@overload_method(BodoSGDClassifierType, 'fit', no_unliteral=True)
def overload_sgdc_model_fit(m, X, y, coef_init=None, intercept_init=None,
    sample_weight=None, _is_data_distributed=False):
    check_sklearn_version()
    """
    Provide implementations for the fit function.
    In case input is replicated, we simply call sklearn,
    else we use partial_fit on each rank then use we re-compute the attributes using MPI operations.
    """
    if is_overload_true(_is_data_distributed):
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.SGDClassifier.fit() : 'sample_weight' is not supported for distributed data."
                )
        if not is_overload_none(coef_init):
            raise BodoError(
                "sklearn.linear_model.SGDClassifier.fit() : 'coef_init' is not supported for distributed data."
                )
        if not is_overload_none(intercept_init):
            raise BodoError(
                "sklearn.linear_model.SGDClassifier.fit() : 'intercept_init' is not supported for distributed data."
                )

        def _model_sgdc_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            y_classes = bodo.libs.array_kernels.unique(y, parallel=True)
            y_classes = bodo.allgatherv(y_classes, False)
            with numba.objmode(m='sgd_classifier_type'):
                m = fit_sgd(m, X, y, y_classes, _is_data_distributed)
            return m
        return _model_sgdc_fit_impl
    else:

        def _model_sgdc_fit_impl(m, X, y, coef_init=None, intercept_init=
            None, sample_weight=None, _is_data_distributed=False):
            with numba.objmode(m='sgd_classifier_type'):
                m = m.fit(X, y, coef_init, intercept_init, sample_weight)
            return m
        return _model_sgdc_fit_impl


@overload_method(BodoSGDClassifierType, 'predict', no_unliteral=True)
def overload_sgdc_model_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoSGDClassifierType, 'predict_proba', no_unliteral=True)
def overload_sgdc_model_predict_proba(m, X):
    return parallel_predict_proba(m, X)


@overload_method(BodoSGDClassifierType, 'predict_log_proba', no_unliteral=True)
def overload_sgdc_model_predict_log_proba(m, X):
    return parallel_predict_log_proba(m, X)


@overload_method(BodoSGDClassifierType, 'score', no_unliteral=True)
def overload_sgdc_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoSGDClassifierType, 'coef_')
def get_sgdc_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:,:]'):
            result = m.coef_
        return result
    return impl


class BodoKMeansClusteringType(types.Opaque):

    def __init__(self):
        super(BodoKMeansClusteringType, self).__init__(name=
            'BodoKMeansClusteringType')


kmeans_clustering_type = BodoKMeansClusteringType()
types.kmeans_clustering_type = kmeans_clustering_type
register_model(BodoKMeansClusteringType)(models.OpaqueModel)


@typeof_impl.register(sklearn.cluster.KMeans)
def typeof_kmeans_clustering(val, c):
    return kmeans_clustering_type


@box(BodoKMeansClusteringType)
def box_kmeans_clustering(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoKMeansClusteringType)
def unbox_kmeans_clustering(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.cluster.KMeans, no_unliteral=True)
def sklearn_cluster_kmeans_overload(n_clusters=8, init='k-means++', n_init=
    10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True,
    algorithm='auto'):
    check_sklearn_version()

    def _sklearn_cluster_kmeans_impl(n_clusters=8, init='k-means++', n_init
        =10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x
        =True, algorithm='auto'):
        with numba.objmode(m='kmeans_clustering_type'):
            m = sklearn.cluster.KMeans(n_clusters=n_clusters, init=init,
                n_init=n_init, max_iter=max_iter, tol=tol, verbose=verbose,
                random_state=random_state, copy_x=copy_x, algorithm=algorithm)
        return m
    return _sklearn_cluster_kmeans_impl


def kmeans_fit_helper(m, len_X, all_X, all_sample_weight, _is_data_distributed
    ):
    ylh__qmk = MPI.COMM_WORLD
    znpd__not = ylh__qmk.Get_rank()
    eeotg__xva = MPI.Get_processor_name()
    hbsg__smrqh = get_host_ranks()
    gluen__bdylg = m.n_jobs if hasattr(m, 'n_jobs') else None
    vyu__vasm = m._n_threads if hasattr(m, '_n_threads') else None
    m._n_threads = len(hbsg__smrqh[eeotg__xva])
    if znpd__not == 0:
        m.fit(X=all_X, y=None, sample_weight=all_sample_weight)
    if znpd__not == 0:
        ylh__qmk.bcast(m.cluster_centers_)
        ylh__qmk.bcast(m.inertia_)
        ylh__qmk.bcast(m.n_iter_)
    else:
        m.cluster_centers_ = ylh__qmk.bcast(None)
        m.inertia_ = ylh__qmk.bcast(None)
        m.n_iter_ = ylh__qmk.bcast(None)
    if _is_data_distributed:
        xov__fcxcb = ylh__qmk.allgather(len_X)
        if znpd__not == 0:
            nbalb__hcwgp = np.empty(len(xov__fcxcb) + 1, dtype=int)
            np.cumsum(xov__fcxcb, out=nbalb__hcwgp[1:])
            nbalb__hcwgp[0] = 0
            fbvw__djlx = [m.labels_[nbalb__hcwgp[tbgun__newg]:nbalb__hcwgp[
                tbgun__newg + 1]] for tbgun__newg in range(len(xov__fcxcb))]
            pdb__trmv = ylh__qmk.scatter(fbvw__djlx)
        else:
            pdb__trmv = ylh__qmk.scatter(None)
        m.labels_ = pdb__trmv
    elif znpd__not == 0:
        ylh__qmk.bcast(m.labels_)
    else:
        m.labels_ = ylh__qmk.bcast(None)
    m._n_threads = vyu__vasm
    return m


@overload_method(BodoKMeansClusteringType, 'fit', no_unliteral=True)
def overload_kmeans_clustering_fit(m, X, y=None, sample_weight=None,
    _is_data_distributed=False):

    def _cluster_kmeans_fit_impl(m, X, y=None, sample_weight=None,
        _is_data_distributed=False):
        if _is_data_distributed:
            all_X = bodo.gatherv(X)
            if sample_weight is not None:
                all_sample_weight = bodo.gatherv(sample_weight)
            else:
                all_sample_weight = None
        else:
            all_X = X
            all_sample_weight = sample_weight
        with numba.objmode(m='kmeans_clustering_type'):
            m = kmeans_fit_helper(m, len(X), all_X, all_sample_weight,
                _is_data_distributed)
        return m
    return _cluster_kmeans_fit_impl


def kmeans_predict_helper(m, X, sample_weight):
    vyu__vasm = m._n_threads if hasattr(m, '_n_threads') else None
    m._n_threads = 1
    if len(X) == 0:
        preds = np.empty(0, dtype=np.int64)
    else:
        preds = m.predict(X, sample_weight).astype(np.int64).flatten()
    m._n_threads = vyu__vasm
    return preds


@overload_method(BodoKMeansClusteringType, 'predict', no_unliteral=True)
def overload_kmeans_clustering_predict(m, X, sample_weight=None):

    def _cluster_kmeans_predict(m, X, sample_weight=None):
        with numba.objmode(preds='int64[:]'):
            preds = kmeans_predict_helper(m, X, sample_weight)
        return preds
    return _cluster_kmeans_predict


@overload_method(BodoKMeansClusteringType, 'score', no_unliteral=True)
def overload_kmeans_clustering_score(m, X, y=None, sample_weight=None,
    _is_data_distributed=False):

    def _cluster_kmeans_score(m, X, y=None, sample_weight=None,
        _is_data_distributed=False):
        with numba.objmode(result='float64'):
            vyu__vasm = m._n_threads if hasattr(m, '_n_threads') else None
            m._n_threads = 1
            if len(X) == 0:
                result = 0
            else:
                result = m.score(X, y=y, sample_weight=sample_weight)
            if _is_data_distributed:
                ylh__qmk = MPI.COMM_WORLD
                result = ylh__qmk.allreduce(result, op=MPI.SUM)
            m._n_threads = vyu__vasm
        return result
    return _cluster_kmeans_score


@overload_method(BodoKMeansClusteringType, 'transform', no_unliteral=True)
def overload_kmeans_clustering_transform(m, X):

    def _cluster_kmeans_transform(m, X):
        with numba.objmode(X_new='float64[:,:]'):
            vyu__vasm = m._n_threads if hasattr(m, '_n_threads') else None
            m._n_threads = 1
            if len(X) == 0:
                X_new = np.empty((0, m.n_clusters), dtype=np.int64)
            else:
                X_new = m.transform(X).astype(np.float64)
            m._n_threads = vyu__vasm
        return X_new
    return _cluster_kmeans_transform


class BodoMultinomialNBType(types.Opaque):

    def __init__(self):
        super(BodoMultinomialNBType, self).__init__(name=
            'BodoMultinomialNBType')


multinomial_nb_type = BodoMultinomialNBType()
types.multinomial_nb_type = multinomial_nb_type
register_model(BodoMultinomialNBType)(models.OpaqueModel)


@typeof_impl.register(sklearn.naive_bayes.MultinomialNB)
def typeof_multinomial_nb(val, c):
    return multinomial_nb_type


@box(BodoMultinomialNBType)
def box_multinomial_nb(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoMultinomialNBType)
def unbox_multinomial_nb(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.naive_bayes.MultinomialNB, no_unliteral=True)
def sklearn_naive_bayes_multinomialnb_overload(alpha=1.0, fit_prior=True,
    class_prior=None):
    check_sklearn_version()

    def _sklearn_naive_bayes_multinomialnb_impl(alpha=1.0, fit_prior=True,
        class_prior=None):
        with numba.objmode(m='multinomial_nb_type'):
            m = sklearn.naive_bayes.MultinomialNB(alpha=alpha, fit_prior=
                fit_prior, class_prior=class_prior)
        return m
    return _sklearn_naive_bayes_multinomialnb_impl


@overload_method(BodoMultinomialNBType, 'fit', no_unliteral=True)
def overload_multinomial_nb_model_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _naive_bayes_multinomial_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _naive_bayes_multinomial_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.naive_bayes.MultinomialNB.fit() : 'sample_weight' not supported."
                )
        krgh__mcf = 'def _model_multinomial_nb_fit_impl(\n'
        krgh__mcf += (
            '    m, X, y, sample_weight=None, _is_data_distributed=False\n')
        krgh__mcf += '):  # pragma: no cover\n'
        krgh__mcf += '    y = bodo.utils.conversion.coerce_to_ndarray(y)\n'
        if isinstance(X, DataFrameType):
            krgh__mcf += '    X = X.to_numpy()\n'
        else:
            krgh__mcf += '    X = bodo.utils.conversion.coerce_to_ndarray(X)\n'
        krgh__mcf += '    my_rank = bodo.get_rank()\n'
        krgh__mcf += '    nranks = bodo.get_size()\n'
        krgh__mcf += '    total_cols = X.shape[1]\n'
        krgh__mcf += '    for i in range(nranks):\n'
        krgh__mcf += (
            '        start = bodo.libs.distributed_api.get_start(total_cols, nranks, i)\n'
            )
        krgh__mcf += (
            '        end = bodo.libs.distributed_api.get_end(total_cols, nranks, i)\n'
            )
        krgh__mcf += '        if i == my_rank:\n'
        krgh__mcf += (
            '            X_train = bodo.gatherv(X[:, start:end:1], root=i)\n')
        krgh__mcf += '        else:\n'
        krgh__mcf += '            bodo.gatherv(X[:, start:end:1], root=i)\n'
        krgh__mcf += '    y_train = bodo.allgatherv(y, False)\n'
        krgh__mcf += '    with numba.objmode(m="multinomial_nb_type"):\n'
        krgh__mcf += '        m = fit_multinomial_nb(\n'
        krgh__mcf += """            m, X_train, y_train, sample_weight, total_cols, _is_data_distributed
"""
        krgh__mcf += '        )\n'
        krgh__mcf += '    bodo.barrier()\n'
        krgh__mcf += '    return m\n'
        szwxm__wcnjd = {}
        exec(krgh__mcf, globals(), szwxm__wcnjd)
        pal__ddo = szwxm__wcnjd['_model_multinomial_nb_fit_impl']
        return pal__ddo


def fit_multinomial_nb(m, X_train, y_train, sample_weight=None, total_cols=
    0, _is_data_distributed=False):
    m._check_X_y(X_train, y_train)
    qwrx__zsiq, n_features = X_train.shape
    m.n_features_in_ = n_features
    mca__tyesk = LabelBinarizer()
    qmrjb__txrio = mca__tyesk.fit_transform(y_train)
    m.classes_ = mca__tyesk.classes_
    if qmrjb__txrio.shape[1] == 1:
        qmrjb__txrio = np.concatenate((1 - qmrjb__txrio, qmrjb__txrio), axis=1)
    if sample_weight is not None:
        qmrjb__txrio = qmrjb__txrio.astype(np.float64, copy=False)
        sample_weight = _check_sample_weight(sample_weight, X_train)
        sample_weight = np.atleast_2d(sample_weight)
        qmrjb__txrio *= sample_weight.T
    class_prior = m.class_prior
    rsrt__extb = qmrjb__txrio.shape[1]
    m._init_counters(rsrt__extb, n_features)
    m._count(X_train.astype('float64'), qmrjb__txrio)
    alpha = m._check_alpha()
    m._update_class_log_prior(class_prior=class_prior)
    ruvqd__reop = m.feature_count_ + alpha
    bdg__zzpj = ruvqd__reop.sum(axis=1)
    ylh__qmk = MPI.COMM_WORLD
    maex__iezm = ylh__qmk.Get_size()
    fovoq__losx = np.zeros(rsrt__extb)
    ylh__qmk.Allreduce(bdg__zzpj, fovoq__losx, op=MPI.SUM)
    drx__seu = np.log(ruvqd__reop) - np.log(fovoq__losx.reshape(-1, 1))
    tay__mxow = drx__seu.T.reshape(n_features * rsrt__extb)
    eum__hll = np.ones(maex__iezm) * (total_cols // maex__iezm)
    eys__lio = total_cols % maex__iezm
    for hvsp__ucxqu in range(eys__lio):
        eum__hll[hvsp__ucxqu] += 1
    eum__hll *= rsrt__extb
    wnbw__ggq = np.zeros(maex__iezm, dtype=np.int32)
    wnbw__ggq[1:] = np.cumsum(eum__hll)[:-1]
    xdpu__sygds = np.zeros((total_cols, rsrt__extb), dtype=np.float64)
    ylh__qmk.Allgatherv(tay__mxow, [xdpu__sygds, eum__hll, wnbw__ggq, MPI.
        DOUBLE_PRECISION])
    m.feature_log_prob_ = xdpu__sygds.T
    m.n_features_in_ = m.feature_log_prob_.shape[1]
    return m


@overload_method(BodoMultinomialNBType, 'predict', no_unliteral=True)
def overload_multinomial_nb_model_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoMultinomialNBType, 'score', no_unliteral=True)
def overload_multinomial_nb_model_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


class BodoLogisticRegressionType(types.Opaque):

    def __init__(self):
        super(BodoLogisticRegressionType, self).__init__(name=
            'BodoLogisticRegressionType')


logistic_regression_type = BodoLogisticRegressionType()
types.logistic_regression_type = logistic_regression_type
register_model(BodoLogisticRegressionType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.LogisticRegression)
def typeof_logistic_regression(val, c):
    return logistic_regression_type


@box(BodoLogisticRegressionType)
def box_logistic_regression(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoLogisticRegressionType)
def unbox_logistic_regression(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.LogisticRegression, no_unliteral=True)
def sklearn_linear_model_logistic_regression_overload(penalty='l2', dual=
    False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1,
    class_weight=None, random_state=None, solver='lbfgs', max_iter=100,
    multi_class='auto', verbose=0, warm_start=False, n_jobs=None, l1_ratio=None
    ):
    check_sklearn_version()

    def _sklearn_linear_model_logistic_regression_impl(penalty='l2', dual=
        False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1,
        class_weight=None, random_state=None, solver='lbfgs', max_iter=100,
        multi_class='auto', verbose=0, warm_start=False, n_jobs=None,
        l1_ratio=None):
        with numba.objmode(m='logistic_regression_type'):
            m = sklearn.linear_model.LogisticRegression(penalty=penalty,
                dual=dual, tol=tol, C=C, fit_intercept=fit_intercept,
                intercept_scaling=intercept_scaling, class_weight=
                class_weight, random_state=random_state, solver=solver,
                max_iter=max_iter, multi_class=multi_class, verbose=verbose,
                warm_start=warm_start, n_jobs=n_jobs, l1_ratio=l1_ratio)
        return m
    return _sklearn_linear_model_logistic_regression_impl


@register_jitable
def _raise_SGD_warning(sgd_name):
    with numba.objmode:
        warnings.warn(
            f'Data is distributed so Bodo will fit model with SGD solver optimization ({sgd_name})'
            , BodoWarning)


@overload_method(BodoLogisticRegressionType, 'fit', no_unliteral=True)
def overload_logistic_regression_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _logistic_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _logistic_regression_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.LogisticRegression.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _sgdc_logistic_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDClassifier')
            with numba.objmode(clf='sgd_classifier_type'):
                if m.l1_ratio is None:
                    l1_ratio = 0.15
                else:
                    l1_ratio = m.l1_ratio
                clf = sklearn.linear_model.SGDClassifier(loss='log',
                    penalty=m.penalty, tol=m.tol, fit_intercept=m.
                    fit_intercept, class_weight=m.class_weight,
                    random_state=m.random_state, max_iter=m.max_iter,
                    verbose=m.verbose, warm_start=m.warm_start, n_jobs=m.
                    n_jobs, l1_ratio=l1_ratio)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
                m.classes_ = clf.classes_
            return m
        return _sgdc_logistic_regression_fit_impl


@overload_method(BodoLogisticRegressionType, 'predict', no_unliteral=True)
def overload_logistic_regression_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoLogisticRegressionType, 'predict_proba', no_unliteral=True
    )
def overload_logistic_regression_predict_proba(m, X):
    return parallel_predict_proba(m, X)


@overload_method(BodoLogisticRegressionType, 'predict_log_proba',
    no_unliteral=True)
def overload_logistic_regression_predict_log_proba(m, X):
    return parallel_predict_log_proba(m, X)


@overload_method(BodoLogisticRegressionType, 'score', no_unliteral=True)
def overload_logistic_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoLogisticRegressionType, 'coef_')
def get_logisticR_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:,:]'):
            result = m.coef_
        return result
    return impl


class BodoLinearRegressionType(types.Opaque):

    def __init__(self):
        super(BodoLinearRegressionType, self).__init__(name=
            'BodoLinearRegressionType')


linear_regression_type = BodoLinearRegressionType()
types.linear_regression_type = linear_regression_type
register_model(BodoLinearRegressionType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.LinearRegression)
def typeof_linear_regression(val, c):
    return linear_regression_type


@box(BodoLinearRegressionType)
def box_linear_regression(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoLinearRegressionType)
def unbox_linear_regression(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.LinearRegression, no_unliteral=True)
def sklearn_linear_model_linear_regression_overload(fit_intercept=True,
    copy_X=True, n_jobs=None, positive=False):
    check_sklearn_version()

    def _sklearn_linear_model_linear_regression_impl(fit_intercept=True,
        copy_X=True, n_jobs=None, positive=False):
        with numba.objmode(m='linear_regression_type'):
            m = sklearn.linear_model.LinearRegression(fit_intercept=
                fit_intercept, copy_X=copy_X, n_jobs=n_jobs, positive=positive)
        return m
    return _sklearn_linear_model_linear_regression_impl


@overload_method(BodoLinearRegressionType, 'fit', no_unliteral=True)
def overload_linear_regression_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _linear_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _linear_regression_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.LinearRegression.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _sgdc_linear_regression_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                clf = sklearn.linear_model.SGDRegressor(loss=
                    'squared_error', penalty=None, fit_intercept=m.
                    fit_intercept)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
            return m
        return _sgdc_linear_regression_fit_impl


@overload_method(BodoLinearRegressionType, 'predict', no_unliteral=True)
def overload_linear_regression_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoLinearRegressionType, 'score', no_unliteral=True)
def overload_linear_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoLinearRegressionType, 'coef_')
def get_lr_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.coef_
        return result
    return impl


class BodoLassoType(types.Opaque):

    def __init__(self):
        super(BodoLassoType, self).__init__(name='BodoLassoType')


lasso_type = BodoLassoType()
types.lasso_type = lasso_type
register_model(BodoLassoType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.Lasso)
def typeof_lasso(val, c):
    return lasso_type


@box(BodoLassoType)
def box_lasso(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoLassoType)
def unbox_lasso(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.Lasso, no_unliteral=True)
def sklearn_linear_model_lasso_overload(alpha=1.0, fit_intercept=True,
    precompute=False, copy_X=True, max_iter=1000, tol=0.0001, warm_start=
    False, positive=False, random_state=None, selection='cyclic'):
    check_sklearn_version()

    def _sklearn_linear_model_lasso_impl(alpha=1.0, fit_intercept=True,
        precompute=False, copy_X=True, max_iter=1000, tol=0.0001,
        warm_start=False, positive=False, random_state=None, selection='cyclic'
        ):
        with numba.objmode(m='lasso_type'):
            m = sklearn.linear_model.Lasso(alpha=alpha, fit_intercept=
                fit_intercept, precompute=precompute, copy_X=copy_X,
                max_iter=max_iter, tol=tol, warm_start=warm_start, positive
                =positive, random_state=random_state, selection=selection)
        return m
    return _sklearn_linear_model_lasso_impl


@overload_method(BodoLassoType, 'fit', no_unliteral=True)
def overload_lasso_fit(m, X, y, sample_weight=None, check_input=True,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _lasso_fit_impl(m, X, y, sample_weight=None, check_input=True,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight, check_input)
            return m
        return _lasso_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.Lasso.fit() : 'sample_weight' is not supported for distributed data."
                )
        if not is_overload_true(check_input):
            raise BodoError(
                "sklearn.linear_model.Lasso.fit() : 'check_input' is not supported for distributed data."
                )

        def _sgdc_lasso_fit_impl(m, X, y, sample_weight=None, check_input=
            True, _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                clf = sklearn.linear_model.SGDRegressor(loss=
                    'squared_error', penalty='l1', alpha=m.alpha,
                    fit_intercept=m.fit_intercept, max_iter=m.max_iter, tol
                    =m.tol, warm_start=m.warm_start, random_state=m.
                    random_state)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
            return m
        return _sgdc_lasso_fit_impl


@overload_method(BodoLassoType, 'predict', no_unliteral=True)
def overload_lass_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoLassoType, 'score', no_unliteral=True)
def overload_lasso_score(m, X, y, sample_weight=None, _is_data_distributed=
    False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


class BodoRidgeType(types.Opaque):

    def __init__(self):
        super(BodoRidgeType, self).__init__(name='BodoRidgeType')


ridge_type = BodoRidgeType()
types.ridge_type = ridge_type
register_model(BodoRidgeType)(models.OpaqueModel)


@typeof_impl.register(sklearn.linear_model.Ridge)
def typeof_ridge(val, c):
    return ridge_type


@box(BodoRidgeType)
def box_ridge(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoRidgeType)
def unbox_ridge(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.linear_model.Ridge, no_unliteral=True)
def sklearn_linear_model_ridge_overload(alpha=1.0, fit_intercept=True,
    copy_X=True, max_iter=None, tol=0.001, solver='auto', positive=False,
    random_state=None):
    check_sklearn_version()

    def _sklearn_linear_model_ridge_impl(alpha=1.0, fit_intercept=True,
        copy_X=True, max_iter=None, tol=0.001, solver='auto', positive=
        False, random_state=None):
        with numba.objmode(m='ridge_type'):
            m = sklearn.linear_model.Ridge(alpha=alpha, fit_intercept=
                fit_intercept, copy_X=copy_X, max_iter=max_iter, tol=tol,
                solver=solver, positive=positive, random_state=random_state)
        return m
    return _sklearn_linear_model_ridge_impl


@overload_method(BodoRidgeType, 'fit', no_unliteral=True)
def overload_ridge_fit(m, X, y, sample_weight=None, _is_data_distributed=False
    ):
    if is_overload_false(_is_data_distributed):

        def _ridge_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _ridge_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.linear_model.Ridge.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _ridge_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDRegressor')
            with numba.objmode(clf='sgd_regressor_type'):
                if m.max_iter is None:
                    max_iter = 1000
                else:
                    max_iter = m.max_iter
                clf = sklearn.linear_model.SGDRegressor(loss=
                    'squared_error', penalty='l2', alpha=0.001,
                    fit_intercept=m.fit_intercept, max_iter=max_iter, tol=m
                    .tol, random_state=m.random_state)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
            return m
        return _ridge_fit_impl


@overload_method(BodoRidgeType, 'predict', no_unliteral=True)
def overload_linear_regression_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoRidgeType, 'score', no_unliteral=True)
def overload_linear_regression_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_attribute(BodoRidgeType, 'coef_')
def get_ridge_coef(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.coef_
        return result
    return impl


class BodoLinearSVCType(types.Opaque):

    def __init__(self):
        super(BodoLinearSVCType, self).__init__(name='BodoLinearSVCType')


linear_svc_type = BodoLinearSVCType()
types.linear_svc_type = linear_svc_type
register_model(BodoLinearSVCType)(models.OpaqueModel)


@typeof_impl.register(sklearn.svm.LinearSVC)
def typeof_linear_svc(val, c):
    return linear_svc_type


@box(BodoLinearSVCType)
def box_linear_svc(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoLinearSVCType)
def unbox_linear_svc(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.svm.LinearSVC, no_unliteral=True)
def sklearn_svm_linear_svc_overload(penalty='l2', loss='squared_hinge',
    dual=True, tol=0.0001, C=1.0, multi_class='ovr', fit_intercept=True,
    intercept_scaling=1, class_weight=None, verbose=0, random_state=None,
    max_iter=1000):
    check_sklearn_version()

    def _sklearn_svm_linear_svc_impl(penalty='l2', loss='squared_hinge',
        dual=True, tol=0.0001, C=1.0, multi_class='ovr', fit_intercept=True,
        intercept_scaling=1, class_weight=None, verbose=0, random_state=
        None, max_iter=1000):
        with numba.objmode(m='linear_svc_type'):
            m = sklearn.svm.LinearSVC(penalty=penalty, loss=loss, dual=dual,
                tol=tol, C=C, multi_class=multi_class, fit_intercept=
                fit_intercept, intercept_scaling=intercept_scaling,
                class_weight=class_weight, verbose=verbose, random_state=
                random_state, max_iter=max_iter)
        return m
    return _sklearn_svm_linear_svc_impl


@overload_method(BodoLinearSVCType, 'fit', no_unliteral=True)
def overload_linear_svc_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    if is_overload_false(_is_data_distributed):

        def _svm_linear_svc_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            with numba.objmode():
                m.fit(X, y, sample_weight)
            return m
        return _svm_linear_svc_fit_impl
    else:
        if not is_overload_none(sample_weight):
            raise BodoError(
                "sklearn.svm.LinearSVC.fit() : 'sample_weight' is not supported for distributed data."
                )

        def _svm_linear_svc_fit_impl(m, X, y, sample_weight=None,
            _is_data_distributed=False):
            if bodo.get_rank() == 0:
                _raise_SGD_warning('SGDClassifier')
            with numba.objmode(clf='sgd_classifier_type'):
                clf = sklearn.linear_model.SGDClassifier(loss='hinge',
                    penalty=m.penalty, tol=m.tol, fit_intercept=m.
                    fit_intercept, class_weight=m.class_weight,
                    random_state=m.random_state, max_iter=m.max_iter,
                    verbose=m.verbose)
            clf.fit(X, y, _is_data_distributed=True)
            with numba.objmode():
                m.coef_ = clf.coef_
                m.intercept_ = clf.intercept_
                m.n_iter_ = clf.n_iter_
                m.classes_ = clf.classes_
            return m
        return _svm_linear_svc_fit_impl


@overload_method(BodoLinearSVCType, 'predict', no_unliteral=True)
def overload_svm_linear_svc_predict(m, X):
    return parallel_predict(m, X)


@overload_method(BodoLinearSVCType, 'score', no_unliteral=True)
def overload_svm_linear_svc_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


class BodoPreprocessingStandardScalerType(types.Opaque):

    def __init__(self):
        super(BodoPreprocessingStandardScalerType, self).__init__(name=
            'BodoPreprocessingStandardScalerType')


preprocessing_standard_scaler_type = BodoPreprocessingStandardScalerType()
types.preprocessing_standard_scaler_type = preprocessing_standard_scaler_type
register_model(BodoPreprocessingStandardScalerType)(models.OpaqueModel)


@typeof_impl.register(sklearn.preprocessing.StandardScaler)
def typeof_preprocessing_standard_scaler(val, c):
    return preprocessing_standard_scaler_type


@box(BodoPreprocessingStandardScalerType)
def box_preprocessing_standard_scaler(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoPreprocessingStandardScalerType)
def unbox_preprocessing_standard_scaler(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.preprocessing.StandardScaler, no_unliteral=True)
def sklearn_preprocessing_standard_scaler_overload(copy=True, with_mean=
    True, with_std=True):
    check_sklearn_version()

    def _sklearn_preprocessing_standard_scaler_impl(copy=True, with_mean=
        True, with_std=True):
        with numba.objmode(m='preprocessing_standard_scaler_type'):
            m = sklearn.preprocessing.StandardScaler(copy=copy, with_mean=
                with_mean, with_std=with_std)
        return m
    return _sklearn_preprocessing_standard_scaler_impl


def sklearn_preprocessing_standard_scaler_fit_dist_helper(m, X):
    ylh__qmk = MPI.COMM_WORLD
    cvo__isst = ylh__qmk.Get_size()
    axyiv__upw = m.with_std
    zbjn__jjgh = m.with_mean
    m.with_std = False
    if axyiv__upw:
        m.with_mean = True
    m = m.fit(X)
    m.with_std = axyiv__upw
    m.with_mean = zbjn__jjgh
    if not isinstance(m.n_samples_seen_, numbers.Integral):
        cxrx__kcz = False
    else:
        cxrx__kcz = True
        m.n_samples_seen_ = np.repeat(m.n_samples_seen_, X.shape[1]).astype(np
            .int64, copy=False)
    lbec__nyat = np.zeros((cvo__isst, *m.n_samples_seen_.shape), dtype=m.
        n_samples_seen_.dtype)
    ylh__qmk.Allgather(m.n_samples_seen_, lbec__nyat)
    vwjik__xiny = np.sum(lbec__nyat, axis=0)
    m.n_samples_seen_ = vwjik__xiny
    if m.with_mean or m.with_std:
        xopbq__dvxx = np.zeros((cvo__isst, *m.mean_.shape), dtype=m.mean_.dtype
            )
        ylh__qmk.Allgather(m.mean_, xopbq__dvxx)
        xopbq__dvxx[np.isnan(xopbq__dvxx)] = 0
        rcm__adipw = np.average(xopbq__dvxx, axis=0, weights=lbec__nyat)
        m.mean_ = rcm__adipw
    if m.with_std:
        wojro__rei = sklearn_safe_accumulator_op(np.nansum, (X - rcm__adipw
            ) ** 2, axis=0) / vwjik__xiny
        ifkrf__neyp = np.zeros_like(wojro__rei)
        ylh__qmk.Allreduce(wojro__rei, ifkrf__neyp, op=MPI.SUM)
        m.var_ = ifkrf__neyp
        m.scale_ = sklearn_handle_zeros_in_scale(np.sqrt(m.var_))
    cxrx__kcz = ylh__qmk.allreduce(cxrx__kcz, op=MPI.LAND)
    if cxrx__kcz:
        m.n_samples_seen_ = m.n_samples_seen_[0]
    return m


@overload_method(BodoPreprocessingStandardScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_standard_scaler_fit(m, X, y=None, sample_weight=
    None, _is_data_distributed=False):
    if is_overload_true(_is_data_distributed) and not is_overload_none(
        sample_weight):
        raise BodoError(
            "sklearn.preprocessing.StandardScaler.fit() : 'sample_weight' is not supported for distributed data."
            )

    def _preprocessing_standard_scaler_fit_impl(m, X, y=None, sample_weight
        =None, _is_data_distributed=False):
        with numba.objmode(m='preprocessing_standard_scaler_type'):
            if _is_data_distributed:
                m = sklearn_preprocessing_standard_scaler_fit_dist_helper(m, X)
            else:
                m = m.fit(X, y, sample_weight)
        return m
    return _preprocessing_standard_scaler_fit_impl


@overload_method(BodoPreprocessingStandardScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_standard_scaler_transform(m, X, copy=None):

    def _preprocessing_standard_scaler_transform_impl(m, X, copy=None):
        with numba.objmode(transformed_X='float64[:,:]'):
            transformed_X = m.transform(X, copy=copy)
        return transformed_X
    return _preprocessing_standard_scaler_transform_impl


@overload_method(BodoPreprocessingStandardScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_standard_scaler_inverse_transform(m, X, copy=None):

    def _preprocessing_standard_scaler_inverse_transform_impl(m, X, copy=None):
        with numba.objmode(inverse_transformed_X='float64[:,:]'):
            inverse_transformed_X = m.inverse_transform(X, copy=copy)
        return inverse_transformed_X
    return _preprocessing_standard_scaler_inverse_transform_impl


def get_data_slice_parallel(data, labels, len_train):
    szgx__zwbtg = data[:len_train]
    jhiv__izd = data[len_train:]
    szgx__zwbtg = bodo.rebalance(szgx__zwbtg)
    jhiv__izd = bodo.rebalance(jhiv__izd)
    ejsy__gqxh = labels[:len_train]
    bgx__xflaf = labels[len_train:]
    ejsy__gqxh = bodo.rebalance(ejsy__gqxh)
    bgx__xflaf = bodo.rebalance(bgx__xflaf)
    return szgx__zwbtg, jhiv__izd, ejsy__gqxh, bgx__xflaf


@numba.njit
def get_train_test_size(train_size, test_size):
    if train_size is None:
        train_size = -1.0
    if test_size is None:
        test_size = -1.0
    if train_size == -1.0 and test_size == -1.0:
        return 0.75, 0.25
    elif test_size == -1.0:
        return train_size, 1.0 - train_size
    elif train_size == -1.0:
        return 1.0 - test_size, test_size
    elif train_size + test_size > 1:
        raise ValueError(
            'The sum of test_size and train_size, should be in the (0, 1) range. Reduce test_size and/or train_size.'
            )
    else:
        return train_size, test_size


def set_labels_type(labels, label_type):
    return labels


@overload(set_labels_type, no_unliteral=True)
def overload_set_labels_type(labels, label_type):
    if get_overload_const_int(label_type) == 1:

        def _set_labels(labels, label_type):
            return pd.Series(labels)
        return _set_labels
    elif get_overload_const_int(label_type) == 2:

        def _set_labels(labels, label_type):
            return labels.values
        return _set_labels
    else:

        def _set_labels(labels, label_type):
            return labels
        return _set_labels


def reset_labels_type(labels, label_type):
    return labels


@overload(reset_labels_type, no_unliteral=True)
def overload_reset_labels_type(labels, label_type):
    if get_overload_const_int(label_type) == 1:

        def _reset_labels(labels, label_type):
            return labels.values
        return _reset_labels
    elif get_overload_const_int(label_type) == 2:

        def _reset_labels(labels, label_type):
            return pd.Series(labels, index=np.arange(len(labels)))
        return _reset_labels
    else:

        def _reset_labels(labels, label_type):
            return labels
        return _reset_labels


@overload(sklearn.model_selection.train_test_split, no_unliteral=True)
def overload_train_test_split(data, labels=None, train_size=None, test_size
    =None, random_state=None, shuffle=True, stratify=None,
    _is_data_distributed=False):
    check_sklearn_version()
    hcnj__phs = {'stratify': stratify}
    giomz__ajep = {'stratify': None}
    check_unsupported_args('train_test_split', hcnj__phs, giomz__ajep, 'ml')
    if is_overload_false(_is_data_distributed):
        sbjud__odf = f'data_split_type_{numba.core.ir_utils.next_label()}'
        rnql__dnd = f'labels_split_type_{numba.core.ir_utils.next_label()}'
        for lzdz__kyzn, uyyny__crmdx in ((data, sbjud__odf), (labels,
            rnql__dnd)):
            if isinstance(lzdz__kyzn, (DataFrameType, SeriesType)):
                cmga__jjnsi = lzdz__kyzn.copy(index=NumericIndexType(types.
                    int64))
                setattr(types, uyyny__crmdx, cmga__jjnsi)
            else:
                setattr(types, uyyny__crmdx, lzdz__kyzn)
        krgh__mcf = 'def _train_test_split_impl(\n'
        krgh__mcf += '    data,\n'
        krgh__mcf += '    labels=None,\n'
        krgh__mcf += '    train_size=None,\n'
        krgh__mcf += '    test_size=None,\n'
        krgh__mcf += '    random_state=None,\n'
        krgh__mcf += '    shuffle=True,\n'
        krgh__mcf += '    stratify=None,\n'
        krgh__mcf += '    _is_data_distributed=False,\n'
        krgh__mcf += '):  # pragma: no cover\n'
        krgh__mcf += (
            """    with numba.objmode(data_train='{}', data_test='{}', labels_train='{}', labels_test='{}'):
"""
            .format(sbjud__odf, sbjud__odf, rnql__dnd, rnql__dnd))
        krgh__mcf += """        data_train, data_test, labels_train, labels_test = sklearn.model_selection.train_test_split(
"""
        krgh__mcf += '            data,\n'
        krgh__mcf += '            labels,\n'
        krgh__mcf += '            train_size=train_size,\n'
        krgh__mcf += '            test_size=test_size,\n'
        krgh__mcf += '            random_state=random_state,\n'
        krgh__mcf += '            shuffle=shuffle,\n'
        krgh__mcf += '            stratify=stratify,\n'
        krgh__mcf += '        )\n'
        krgh__mcf += (
            '    return data_train, data_test, labels_train, labels_test\n')
        szwxm__wcnjd = {}
        exec(krgh__mcf, globals(), szwxm__wcnjd)
        _train_test_split_impl = szwxm__wcnjd['_train_test_split_impl']
        return _train_test_split_impl
    else:
        global get_data_slice_parallel
        if isinstance(get_data_slice_parallel, pytypes.FunctionType):
            get_data_slice_parallel = bodo.jit(get_data_slice_parallel,
                all_args_distributed_varlength=True,
                all_returns_distributed=True)
        label_type = 0
        if isinstance(data, DataFrameType) and isinstance(labels, types.Array):
            label_type = 1
        elif isinstance(data, types.Array) and isinstance(labels, SeriesType):
            label_type = 2
        if is_overload_none(random_state):
            random_state = 42

        def _train_test_split_impl(data, labels=None, train_size=None,
            test_size=None, random_state=None, shuffle=True, stratify=None,
            _is_data_distributed=False):
            if data.shape[0] != labels.shape[0]:
                raise ValueError(
                    'Found input variables with inconsistent number of samples\n'
                    )
            train_size, test_size = get_train_test_size(train_size, test_size)
            drtb__mhad = bodo.libs.distributed_api.dist_reduce(len(data),
                np.int32(Reduce_Type.Sum.value))
            len_train = int(drtb__mhad * train_size)
            kjdp__gkr = drtb__mhad - len_train
            if shuffle:
                labels = set_labels_type(labels, label_type)
                znpd__not = bodo.get_rank()
                maex__iezm = bodo.get_size()
                wkf__tdov = np.empty(maex__iezm, np.int64)
                bodo.libs.distributed_api.allgather(wkf__tdov, len(data))
                jgbw__cpg = np.cumsum(wkf__tdov[0:znpd__not + 1])
                xwhtt__zpej = np.full(drtb__mhad, True)
                xwhtt__zpej[:kjdp__gkr] = False
                np.random.seed(42)
                np.random.permutation(xwhtt__zpej)
                if znpd__not:
                    esar__gdugh = jgbw__cpg[znpd__not - 1]
                else:
                    esar__gdugh = 0
                drt__yland = jgbw__cpg[znpd__not]
                oxson__ekl = xwhtt__zpej[esar__gdugh:drt__yland]
                szgx__zwbtg = data[oxson__ekl]
                jhiv__izd = data[~oxson__ekl]
                ejsy__gqxh = labels[oxson__ekl]
                bgx__xflaf = labels[~oxson__ekl]
                szgx__zwbtg = bodo.random_shuffle(szgx__zwbtg, seed=
                    random_state, parallel=True)
                jhiv__izd = bodo.random_shuffle(jhiv__izd, seed=
                    random_state, parallel=True)
                ejsy__gqxh = bodo.random_shuffle(ejsy__gqxh, seed=
                    random_state, parallel=True)
                bgx__xflaf = bodo.random_shuffle(bgx__xflaf, seed=
                    random_state, parallel=True)
                ejsy__gqxh = reset_labels_type(ejsy__gqxh, label_type)
                bgx__xflaf = reset_labels_type(bgx__xflaf, label_type)
            else:
                szgx__zwbtg, jhiv__izd, ejsy__gqxh, bgx__xflaf = (
                    get_data_slice_parallel(data, labels, len_train))
            return szgx__zwbtg, jhiv__izd, ejsy__gqxh, bgx__xflaf
        return _train_test_split_impl


class BodoPreprocessingMinMaxScalerType(types.Opaque):

    def __init__(self):
        super(BodoPreprocessingMinMaxScalerType, self).__init__(name=
            'BodoPreprocessingMinMaxScalerType')


preprocessing_minmax_scaler_type = BodoPreprocessingMinMaxScalerType()
types.preprocessing_minmax_scaler_type = preprocessing_minmax_scaler_type
register_model(BodoPreprocessingMinMaxScalerType)(models.OpaqueModel)


@typeof_impl.register(sklearn.preprocessing.MinMaxScaler)
def typeof_preprocessing_minmax_scaler(val, c):
    return preprocessing_minmax_scaler_type


@box(BodoPreprocessingMinMaxScalerType)
def box_preprocessing_minmax_scaler(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoPreprocessingMinMaxScalerType)
def unbox_preprocessing_minmax_scaler(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.preprocessing.MinMaxScaler, no_unliteral=True)
def sklearn_preprocessing_minmax_scaler_overload(feature_range=(0, 1), copy
    =True, clip=False):
    check_sklearn_version()

    def _sklearn_preprocessing_minmax_scaler_impl(feature_range=(0, 1),
        copy=True, clip=False):
        with numba.objmode(m='preprocessing_minmax_scaler_type'):
            m = sklearn.preprocessing.MinMaxScaler(feature_range=
                feature_range, copy=copy, clip=clip)
        return m
    return _sklearn_preprocessing_minmax_scaler_impl


def sklearn_preprocessing_minmax_scaler_fit_dist_helper(m, X):
    ylh__qmk = MPI.COMM_WORLD
    cvo__isst = ylh__qmk.Get_size()
    m = m.fit(X)
    vwjik__xiny = ylh__qmk.allreduce(m.n_samples_seen_, op=MPI.SUM)
    m.n_samples_seen_ = vwjik__xiny
    zyh__zch = np.zeros((cvo__isst, *m.data_min_.shape), dtype=m.data_min_.
        dtype)
    ylh__qmk.Allgather(m.data_min_, zyh__zch)
    cvecm__okndg = np.nanmin(zyh__zch, axis=0)
    ijl__etedc = np.zeros((cvo__isst, *m.data_max_.shape), dtype=m.
        data_max_.dtype)
    ylh__qmk.Allgather(m.data_max_, ijl__etedc)
    vklvm__qcoce = np.nanmax(ijl__etedc, axis=0)
    cjnw__jhh = vklvm__qcoce - cvecm__okndg
    m.scale_ = (m.feature_range[1] - m.feature_range[0]
        ) / sklearn_handle_zeros_in_scale(cjnw__jhh)
    m.min_ = m.feature_range[0] - cvecm__okndg * m.scale_
    m.data_min_ = cvecm__okndg
    m.data_max_ = vklvm__qcoce
    m.data_range_ = cjnw__jhh
    return m


@overload_method(BodoPreprocessingMinMaxScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_minmax_scaler_fit(m, X, y=None,
    _is_data_distributed=False):

    def _preprocessing_minmax_scaler_fit_impl(m, X, y=None,
        _is_data_distributed=False):
        with numba.objmode(m='preprocessing_minmax_scaler_type'):
            if _is_data_distributed:
                m = sklearn_preprocessing_minmax_scaler_fit_dist_helper(m, X)
            else:
                m = m.fit(X, y)
        return m
    return _preprocessing_minmax_scaler_fit_impl


@overload_method(BodoPreprocessingMinMaxScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_minmax_scaler_transform(m, X):

    def _preprocessing_minmax_scaler_transform_impl(m, X):
        with numba.objmode(transformed_X='float64[:,:]'):
            transformed_X = m.transform(X)
        return transformed_X
    return _preprocessing_minmax_scaler_transform_impl


@overload_method(BodoPreprocessingMinMaxScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_minmax_scaler_inverse_transform(m, X):

    def _preprocessing_minmax_scaler_inverse_transform_impl(m, X):
        with numba.objmode(inverse_transformed_X='float64[:,:]'):
            inverse_transformed_X = m.inverse_transform(X)
        return inverse_transformed_X
    return _preprocessing_minmax_scaler_inverse_transform_impl


class BodoPreprocessingRobustScalerType(types.Opaque):

    def __init__(self):
        super(BodoPreprocessingRobustScalerType, self).__init__(name=
            'BodoPreprocessingRobustScalerType')


preprocessing_robust_scaler_type = BodoPreprocessingRobustScalerType()
types.preprocessing_robust_scaler_type = preprocessing_robust_scaler_type


@register_model(BodoPreprocessingRobustScalerType)
class BodoPreprocessingRobustScalerModel(models.StructModel):

    def __init__(self, dmm, fe_type):
        mojiy__aer = [('meminfo', types.MemInfoPointer(
            preprocessing_robust_scaler_type)), ('pyobj', types.pyobject)]
        super().__init__(dmm, fe_type, mojiy__aer)


@typeof_impl.register(sklearn.preprocessing.RobustScaler)
def typeof_preprocessing_robust_scaler(val, c):
    return preprocessing_robust_scaler_type


@box(BodoPreprocessingRobustScalerType)
def box_preprocessing_robust_scaler(typ, val, c):
    tfloe__knqk = cgutils.create_struct_proxy(typ)(c.context, c.builder, val)
    obj = tfloe__knqk.pyobj
    c.pyapi.incref(obj)
    c.context.nrt.decref(c.builder, typ, val)
    return obj


@unbox(BodoPreprocessingRobustScalerType)
def unbox_preprocessing_robust_scaler(typ, obj, c):
    tfloe__knqk = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    tfloe__knqk.meminfo = c.pyapi.nrt_meminfo_new_from_pyobject(c.context.
        get_constant_null(types.voidptr), obj)
    tfloe__knqk.pyobj = obj
    return NativeValue(tfloe__knqk._getvalue())


@overload_attribute(BodoPreprocessingRobustScalerType, 'with_centering')
def get_robust_scaler_with_centering(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.with_centering
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'with_scaling')
def get_robust_scaler_with_scaling(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.with_scaling
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'quantile_range')
def get_robust_scaler_quantile_range(m):
    typ = numba.typeof((25.0, 75.0))

    def impl(m):
        with numba.objmode(result=typ):
            result = m.quantile_range
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'unit_variance')
def get_robust_scaler_unit_variance(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.unit_variance
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'copy')
def get_robust_scaler_copy(m):

    def impl(m):
        with numba.objmode(result='boolean'):
            result = m.copy
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'center_')
def get_robust_scaler_center_(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.center_
        return result
    return impl


@overload_attribute(BodoPreprocessingRobustScalerType, 'scale_')
def get_robust_scaler_scale_(m):

    def impl(m):
        with numba.objmode(result='float64[:]'):
            result = m.scale_
        return result
    return impl


@overload(sklearn.preprocessing.RobustScaler, no_unliteral=True)
def sklearn_preprocessing_robust_scaler_overload(with_centering=True,
    with_scaling=True, quantile_range=(25.0, 75.0), copy=True,
    unit_variance=False):
    check_sklearn_version()

    def _sklearn_preprocessing_robust_scaler_impl(with_centering=True,
        with_scaling=True, quantile_range=(25.0, 75.0), copy=True,
        unit_variance=False):
        with numba.objmode(m='preprocessing_robust_scaler_type'):
            m = sklearn.preprocessing.RobustScaler(with_centering=
                with_centering, with_scaling=with_scaling, quantile_range=
                quantile_range, copy=copy, unit_variance=unit_variance)
        return m
    return _sklearn_preprocessing_robust_scaler_impl


@overload_method(BodoPreprocessingRobustScalerType, 'fit', no_unliteral=True)
def overload_preprocessing_robust_scaler_fit(m, X, y=None,
    _is_data_distributed=False):
    check_sklearn_version()
    if is_overload_true(_is_data_distributed):
        krgh__mcf = f'def preprocessing_robust_scaler_fit_impl(\n'
        krgh__mcf += f'  m, X, y=None, _is_data_distributed=False\n'
        krgh__mcf += f'):\n'
        if isinstance(X, DataFrameType):
            krgh__mcf += f'  X = X.to_numpy()\n'
        krgh__mcf += (
            f"  with numba.objmode(qrange_l='float64', qrange_r='float64'):\n")
        krgh__mcf += f'    (qrange_l, qrange_r) = m.quantile_range\n'
        krgh__mcf += f'  if not 0 <= qrange_l <= qrange_r <= 100:\n'
        krgh__mcf += f'    raise ValueError(\n'
        krgh__mcf += f"""      'Invalid quantile range provided. Ensure that 0 <= quantile_range[0] <= quantile_range[1] <= 100.'
"""
        krgh__mcf += f'    )\n'
        krgh__mcf += (
            f'  qrange_l, qrange_r = qrange_l / 100.0, qrange_r / 100.0\n')
        krgh__mcf += f'  X = bodo.utils.conversion.coerce_to_array(X)\n'
        krgh__mcf += f'  num_features = X.shape[1]\n'
        krgh__mcf += f'  if m.with_scaling:\n'
        krgh__mcf += f'    scales = np.zeros(num_features)\n'
        krgh__mcf += f'  else:\n'
        krgh__mcf += f'    scales = None\n'
        krgh__mcf += f'  if m.with_centering:\n'
        krgh__mcf += f'    centers = np.zeros(num_features)\n'
        krgh__mcf += f'  else:\n'
        krgh__mcf += f'    centers = None\n'
        krgh__mcf += f'  if m.with_scaling or m.with_centering:\n'
        krgh__mcf += f'    numba.parfors.parfor.init_prange()\n'
        krgh__mcf += (
            f'    for feature_idx in numba.parfors.parfor.internal_prange(num_features):\n'
            )
        krgh__mcf += f"""      column_data = bodo.utils.conversion.ensure_contig_if_np(X[:, feature_idx])
"""
        krgh__mcf += f'      if m.with_scaling:\n'
        krgh__mcf += (
            f'        q1 = bodo.libs.array_kernels.quantile_parallel(\n')
        krgh__mcf += f'          column_data, qrange_l, 0\n'
        krgh__mcf += f'        )\n'
        krgh__mcf += (
            f'        q2 = bodo.libs.array_kernels.quantile_parallel(\n')
        krgh__mcf += f'          column_data, qrange_r, 0\n'
        krgh__mcf += f'        )\n'
        krgh__mcf += f'        scales[feature_idx] = q2 - q1\n'
        krgh__mcf += f'      if m.with_centering:\n'
        krgh__mcf += (
            f'        centers[feature_idx] = bodo.libs.array_ops.array_op_median(\n'
            )
        krgh__mcf += f'          column_data, True, True\n'
        krgh__mcf += f'        )\n'
        krgh__mcf += f'  if m.with_scaling:\n'
        krgh__mcf += (
            f'    constant_mask = scales < 10 * np.finfo(scales.dtype).eps\n')
        krgh__mcf += f'    scales[constant_mask] = 1.0\n'
        krgh__mcf += f'    if m.unit_variance:\n'
        krgh__mcf += f"      with numba.objmode(adjust='float64'):\n"
        krgh__mcf += (
            f'        adjust = stats.norm.ppf(qrange_r) - stats.norm.ppf(qrange_l)\n'
            )
        krgh__mcf += f'      scales = scales / adjust\n'
        krgh__mcf += f'  with numba.objmode():\n'
        krgh__mcf += f'    m.center_ = centers\n'
        krgh__mcf += f'    m.scale_ = scales\n'
        krgh__mcf += f'  return m\n'
        szwxm__wcnjd = {}
        exec(krgh__mcf, globals(), szwxm__wcnjd)
        _preprocessing_robust_scaler_fit_impl = szwxm__wcnjd[
            'preprocessing_robust_scaler_fit_impl']
        return _preprocessing_robust_scaler_fit_impl
    else:

        def _preprocessing_robust_scaler_fit_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_robust_scaler_type'):
                m = m.fit(X, y)
            return m
        return _preprocessing_robust_scaler_fit_impl


@overload_method(BodoPreprocessingRobustScalerType, 'transform',
    no_unliteral=True)
def overload_preprocessing_robust_scaler_transform(m, X):
    check_sklearn_version()

    def _preprocessing_robust_scaler_transform_impl(m, X):
        with numba.objmode(transformed_X='float64[:,:]'):
            transformed_X = m.transform(X)
        return transformed_X
    return _preprocessing_robust_scaler_transform_impl


@overload_method(BodoPreprocessingRobustScalerType, 'inverse_transform',
    no_unliteral=True)
def overload_preprocessing_robust_scaler_inverse_transform(m, X):
    check_sklearn_version()

    def _preprocessing_robust_scaler_inverse_transform_impl(m, X):
        with numba.objmode(inverse_transformed_X='float64[:,:]'):
            inverse_transformed_X = m.inverse_transform(X)
        return inverse_transformed_X
    return _preprocessing_robust_scaler_inverse_transform_impl


class BodoPreprocessingLabelEncoderType(types.Opaque):

    def __init__(self):
        super(BodoPreprocessingLabelEncoderType, self).__init__(name=
            'BodoPreprocessingLabelEncoderType')


preprocessing_label_encoder_type = BodoPreprocessingLabelEncoderType()
types.preprocessing_label_encoder_type = preprocessing_label_encoder_type
register_model(BodoPreprocessingLabelEncoderType)(models.OpaqueModel)


@typeof_impl.register(sklearn.preprocessing.LabelEncoder)
def typeof_preprocessing_label_encoder(val, c):
    return preprocessing_label_encoder_type


@box(BodoPreprocessingLabelEncoderType)
def box_preprocessing_label_encoder(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoPreprocessingLabelEncoderType)
def unbox_preprocessing_label_encoder(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.preprocessing.LabelEncoder, no_unliteral=True)
def sklearn_preprocessing_label_encoder_overload():
    check_sklearn_version()

    def _sklearn_preprocessing_label_encoder_impl():
        with numba.objmode(m='preprocessing_label_encoder_type'):
            m = sklearn.preprocessing.LabelEncoder()
        return m
    return _sklearn_preprocessing_label_encoder_impl


@overload_method(BodoPreprocessingLabelEncoderType, 'fit', no_unliteral=True)
def overload_preprocessing_label_encoder_fit(m, y, _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _sklearn_preprocessing_label_encoder_fit_impl(m, y,
            _is_data_distributed=False):
            y = bodo.utils.typing.decode_if_dict_array(y)
            y_classes = bodo.libs.array_kernels.unique(y, parallel=True)
            y_classes = bodo.allgatherv(y_classes, False)
            y_classes = bodo.libs.array_kernels.sort(y_classes, ascending=
                True, inplace=False)
            with numba.objmode:
                m.classes_ = y_classes
            return m
        return _sklearn_preprocessing_label_encoder_fit_impl
    else:

        def _sklearn_preprocessing_label_encoder_fit_impl(m, y,
            _is_data_distributed=False):
            with numba.objmode(m='preprocessing_label_encoder_type'):
                m = m.fit(y)
            return m
        return _sklearn_preprocessing_label_encoder_fit_impl


@overload_method(BodoPreprocessingLabelEncoderType, 'transform',
    no_unliteral=True)
def overload_preprocessing_label_encoder_transform(m, y,
    _is_data_distributed=False):

    def _preprocessing_label_encoder_transform_impl(m, y,
        _is_data_distributed=False):
        with numba.objmode(transformed_y='int64[:]'):
            transformed_y = m.transform(y)
        return transformed_y
    return _preprocessing_label_encoder_transform_impl


@numba.njit
def le_fit_transform(m, y):
    m = m.fit(y, _is_data_distributed=True)
    transformed_y = m.transform(y, _is_data_distributed=True)
    return transformed_y


@overload_method(BodoPreprocessingLabelEncoderType, 'fit_transform',
    no_unliteral=True)
def overload_preprocessing_label_encoder_fit_transform(m, y,
    _is_data_distributed=False):
    if is_overload_true(_is_data_distributed):

        def _preprocessing_label_encoder_fit_transform_impl(m, y,
            _is_data_distributed=False):
            transformed_y = le_fit_transform(m, y)
            return transformed_y
        return _preprocessing_label_encoder_fit_transform_impl
    else:

        def _preprocessing_label_encoder_fit_transform_impl(m, y,
            _is_data_distributed=False):
            with numba.objmode(transformed_y='int64[:]'):
                transformed_y = m.fit_transform(y)
            return transformed_y
        return _preprocessing_label_encoder_fit_transform_impl


class BodoFExtractHashingVectorizerType(types.Opaque):

    def __init__(self):
        super(BodoFExtractHashingVectorizerType, self).__init__(name=
            'BodoFExtractHashingVectorizerType')


f_extract_hashing_vectorizer_type = BodoFExtractHashingVectorizerType()
types.f_extract_hashing_vectorizer_type = f_extract_hashing_vectorizer_type
register_model(BodoFExtractHashingVectorizerType)(models.OpaqueModel)


@typeof_impl.register(sklearn.feature_extraction.text.HashingVectorizer)
def typeof_f_extract_hashing_vectorizer(val, c):
    return f_extract_hashing_vectorizer_type


@box(BodoFExtractHashingVectorizerType)
def box_f_extract_hashing_vectorizer(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoFExtractHashingVectorizerType)
def unbox_f_extract_hashing_vectorizer(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.feature_extraction.text.HashingVectorizer, no_unliteral=True)
def sklearn_hashing_vectorizer_overload(input='content', encoding='utf-8',
    decode_error='strict', strip_accents=None, lowercase=True, preprocessor
    =None, tokenizer=None, stop_words=None, token_pattern=
    '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', n_features=2 **
    20, binary=False, norm='l2', alternate_sign=True, dtype=np.float64):
    check_sklearn_version()

    def _sklearn_hashing_vectorizer_impl(input='content', encoding='utf-8',
        decode_error='strict', strip_accents=None, lowercase=True,
        preprocessor=None, tokenizer=None, stop_words=None, token_pattern=
        '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word',
        n_features=2 ** 20, binary=False, norm='l2', alternate_sign=True,
        dtype=np.float64):
        with numba.objmode(m='f_extract_hashing_vectorizer_type'):
            m = sklearn.feature_extraction.text.HashingVectorizer(input=
                input, encoding=encoding, decode_error=decode_error,
                strip_accents=strip_accents, lowercase=lowercase,
                preprocessor=preprocessor, tokenizer=tokenizer, stop_words=
                stop_words, token_pattern=token_pattern, ngram_range=
                ngram_range, analyzer=analyzer, n_features=n_features,
                binary=binary, norm=norm, alternate_sign=alternate_sign,
                dtype=dtype)
        return m
    return _sklearn_hashing_vectorizer_impl


@overload_method(BodoFExtractHashingVectorizerType, 'fit_transform',
    no_unliteral=True)
def overload_hashing_vectorizer_fit_transform(m, X, y=None,
    _is_data_distributed=False):
    types.csr_matrix_float64_int64 = CSRMatrixType(types.float64, types.int64)

    def _hashing_vectorizer_fit_transform_impl(m, X, y=None,
        _is_data_distributed=False):
        with numba.objmode(transformed_X='csr_matrix_float64_int64'):
            transformed_X = m.fit_transform(X, y)
            transformed_X.indices = transformed_X.indices.astype(np.int64)
            transformed_X.indptr = transformed_X.indptr.astype(np.int64)
        return transformed_X
    return _hashing_vectorizer_fit_transform_impl


class BodoRandomForestRegressorType(types.Opaque):

    def __init__(self):
        super(BodoRandomForestRegressorType, self).__init__(name=
            'BodoRandomForestRegressorType')


random_forest_regressor_type = BodoRandomForestRegressorType()
types.random_forest_regressor_type = random_forest_regressor_type
register_model(BodoRandomForestRegressorType)(models.OpaqueModel)


@typeof_impl.register(sklearn.ensemble.RandomForestRegressor)
def typeof_random_forest_regressor(val, c):
    return random_forest_regressor_type


@box(BodoRandomForestRegressorType)
def box_random_forest_regressor(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoRandomForestRegressorType)
def unbox_random_forest_regressor(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.ensemble.RandomForestRegressor, no_unliteral=True)
def overload_sklearn_rf_regressor(n_estimators=100, criterion=
    'squared_error', max_depth=None, min_samples_split=2, min_samples_leaf=
    1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=
    None, min_impurity_decrease=0.0, bootstrap=True, oob_score=False,
    n_jobs=None, random_state=None, verbose=0, warm_start=False, ccp_alpha=
    0.0, max_samples=None):
    check_sklearn_version()

    def _sklearn_ensemble_RandomForestRegressor_impl(n_estimators=100,
        criterion='squared_error', max_depth=None, min_samples_split=2,
        min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=
        'auto', max_leaf_nodes=None, min_impurity_decrease=0.0, bootstrap=
        True, oob_score=False, n_jobs=None, random_state=None, verbose=0,
        warm_start=False, ccp_alpha=0.0, max_samples=None):
        with numba.objmode(m='random_forest_regressor_type'):
            if random_state is not None and get_num_nodes() > 1:
                print(
                    'With multinode, fixed random_state seed values are ignored.\n'
                    )
                random_state = None
            m = sklearn.ensemble.RandomForestRegressor(n_estimators=
                n_estimators, criterion=criterion, max_depth=max_depth,
                min_samples_split=min_samples_split, min_samples_leaf=
                min_samples_leaf, min_weight_fraction_leaf=
                min_weight_fraction_leaf, max_features=max_features,
                max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=
                min_impurity_decrease, bootstrap=bootstrap, oob_score=
                oob_score, n_jobs=1, random_state=random_state, verbose=
                verbose, warm_start=warm_start, ccp_alpha=ccp_alpha,
                max_samples=max_samples)
        return m
    return _sklearn_ensemble_RandomForestRegressor_impl


@overload_method(BodoRandomForestRegressorType, 'predict', no_unliteral=True)
def overload_rf_regressor_predict(m, X):
    return parallel_predict_regression(m, X)


@overload_method(BodoRandomForestRegressorType, 'score', no_unliteral=True)
def overload_rf_regressor_score(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    return parallel_score(m, X, y, sample_weight, _is_data_distributed)


@overload_method(BodoRandomForestRegressorType, 'fit', no_unliteral=True)
@overload_method(BodoRandomForestClassifierType, 'fit', no_unliteral=True)
def overload_rf_classifier_model_fit(m, X, y, sample_weight=None,
    _is_data_distributed=False):
    gnyz__emhp = 'RandomForestClassifier'
    if isinstance(m, BodoRandomForestRegressorType):
        gnyz__emhp = 'RandomForestRegressor'
    if not is_overload_none(sample_weight):
        raise BodoError(
            f"sklearn.ensemble.{gnyz__emhp}.fit() : 'sample_weight' is not supported for distributed data."
            )

    def _model_fit_impl(m, X, y, sample_weight=None, _is_data_distributed=False
        ):
        with numba.objmode(first_rank_node='int32[:]'):
            first_rank_node = get_nodes_first_ranks()
        if _is_data_distributed:
            mtpqp__cbydp = len(first_rank_node)
            X = bodo.gatherv(X)
            y = bodo.gatherv(y)
            if mtpqp__cbydp > 1:
                X = bodo.libs.distributed_api.bcast_comm(X, comm_ranks=
                    first_rank_node, nranks=mtpqp__cbydp)
                y = bodo.libs.distributed_api.bcast_comm(y, comm_ranks=
                    first_rank_node, nranks=mtpqp__cbydp)
        with numba.objmode:
            random_forest_model_fit(m, X, y)
        bodo.barrier()
        return m
    return _model_fit_impl


class BodoFExtractCountVectorizerType(types.Opaque):

    def __init__(self):
        super(BodoFExtractCountVectorizerType, self).__init__(name=
            'BodoFExtractCountVectorizerType')


f_extract_count_vectorizer_type = BodoFExtractCountVectorizerType()
types.f_extract_count_vectorizer_type = f_extract_count_vectorizer_type
register_model(BodoFExtractCountVectorizerType)(models.OpaqueModel)


@typeof_impl.register(sklearn.feature_extraction.text.CountVectorizer)
def typeof_f_extract_count_vectorizer(val, c):
    return f_extract_count_vectorizer_type


@box(BodoFExtractCountVectorizerType)
def box_f_extract_count_vectorizer(typ, val, c):
    c.pyapi.incref(val)
    return val


@unbox(BodoFExtractCountVectorizerType)
def unbox_f_extract_count_vectorizer(typ, obj, c):
    c.pyapi.incref(obj)
    return NativeValue(obj)


@overload(sklearn.feature_extraction.text.CountVectorizer, no_unliteral=True)
def sklearn_count_vectorizer_overload(input='content', encoding='utf-8',
    decode_error='strict', strip_accents=None, lowercase=True, preprocessor
    =None, tokenizer=None, stop_words=None, token_pattern=
    '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', max_df=1.0,
    min_df=1, max_features=None, vocabulary=None, binary=False, dtype=np.int64
    ):
    check_sklearn_version()
    if not is_overload_constant_number(min_df) or get_overload_const(min_df
        ) != 1:
        raise BodoError(
            """sklearn.feature_extraction.text.CountVectorizer(): 'min_df' is not supported for distributed data.
"""
            )
    if not is_overload_constant_number(max_df) or get_overload_const(min_df
        ) != 1:
        raise BodoError(
            """sklearn.feature_extraction.text.CountVectorizer(): 'max_df' is not supported for distributed data.
"""
            )

    def _sklearn_count_vectorizer_impl(input='content', encoding='utf-8',
        decode_error='strict', strip_accents=None, lowercase=True,
        preprocessor=None, tokenizer=None, stop_words=None, token_pattern=
        '(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), analyzer='word', max_df=
        1.0, min_df=1, max_features=None, vocabulary=None, binary=False,
        dtype=np.int64):
        with numba.objmode(m='f_extract_count_vectorizer_type'):
            m = sklearn.feature_extraction.text.CountVectorizer(input=input,
                encoding=encoding, decode_error=decode_error, strip_accents
                =strip_accents, lowercase=lowercase, preprocessor=
                preprocessor, tokenizer=tokenizer, stop_words=stop_words,
                token_pattern=token_pattern, ngram_range=ngram_range,
                analyzer=analyzer, max_df=max_df, min_df=min_df,
                max_features=max_features, vocabulary=vocabulary, binary=
                binary, dtype=dtype)
        return m
    return _sklearn_count_vectorizer_impl


@overload_attribute(BodoFExtractCountVectorizerType, 'vocabulary_')
def get_cv_vocabulary_(m):
    types.dict_string_int = types.DictType(types.unicode_type, types.int64)

    def impl(m):
        with numba.objmode(result='dict_string_int'):
            result = m.vocabulary_
        return result
    return impl


def _cv_fit_transform_helper(m, X):
    sud__lfiez = False
    local_vocabulary = m.vocabulary
    if m.vocabulary is None:
        m.fit(X)
        local_vocabulary = m.vocabulary_
        sud__lfiez = True
    return sud__lfiez, local_vocabulary


@overload_method(BodoFExtractCountVectorizerType, 'fit_transform',
    no_unliteral=True)
def overload_count_vectorizer_fit_transform(m, X, y=None,
    _is_data_distributed=False):
    check_sklearn_version()
    types.csr_matrix_int64_int64 = CSRMatrixType(types.int64, types.int64)
    if is_overload_true(_is_data_distributed):
        types.dict_str_int = types.DictType(types.unicode_type, types.int64)

        def _count_vectorizer_fit_transform_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(local_vocabulary='dict_str_int', changeVoc=
                'bool_'):
                changeVoc, local_vocabulary = _cv_fit_transform_helper(m, X)
            if changeVoc:
                local_vocabulary = bodo.utils.conversion.coerce_to_array(list
                    (local_vocabulary.keys()))
                eiss__grqv = bodo.libs.array_kernels.unique(local_vocabulary,
                    parallel=True)
                eiss__grqv = bodo.allgatherv(eiss__grqv, False)
                eiss__grqv = bodo.libs.array_kernels.sort(eiss__grqv,
                    ascending=True, inplace=True)
                vkwsq__wjyy = {}
                for rmu__ufq in range(len(eiss__grqv)):
                    vkwsq__wjyy[eiss__grqv[rmu__ufq]] = rmu__ufq
            else:
                vkwsq__wjyy = local_vocabulary
            with numba.objmode(transformed_X='csr_matrix_int64_int64'):
                if changeVoc:
                    m.vocabulary = vkwsq__wjyy
                transformed_X = m.fit_transform(X, y)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
        return _count_vectorizer_fit_transform_impl
    else:

        def _count_vectorizer_fit_transform_impl(m, X, y=None,
            _is_data_distributed=False):
            with numba.objmode(transformed_X='csr_matrix_int64_int64'):
                transformed_X = m.fit_transform(X, y)
                transformed_X.indices = transformed_X.indices.astype(np.int64)
                transformed_X.indptr = transformed_X.indptr.astype(np.int64)
            return transformed_X
        return _count_vectorizer_fit_transform_impl


@overload_method(BodoFExtractCountVectorizerType, 'get_feature_names_out',
    no_unliteral=True)
def overload_count_vectorizer_get_feature_names_out(m):
    check_sklearn_version()

    def impl(m):
        with numba.objmode(result=bodo.string_array_type):
            result = m.get_feature_names_out()
        return result
    return impl
