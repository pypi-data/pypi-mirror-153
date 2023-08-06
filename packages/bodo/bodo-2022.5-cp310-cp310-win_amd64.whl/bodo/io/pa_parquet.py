import asyncio
import os
import threading
from collections import defaultdict
from concurrent import futures
from urllib.parse import urlparse
import pyarrow.parquet as pq
from bodo.io.fs_io import get_s3_bucket_region_njit


def get_parquet_filesnames_from_deltalake(delta_lake_path):
    try:
        from deltalake import DeltaTable
    except Exception as bzvqn__otg:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    myvrv__nmt = None
    fgrti__yxqvp = delta_lake_path.rstrip('/')
    aoxh__shq = 'AWS_DEFAULT_REGION' in os.environ
    bsk__rbt = os.environ.get('AWS_DEFAULT_REGION', '')
    dmg__vxba = False
    if delta_lake_path.startswith('s3://'):
        srsdn__eaw = get_s3_bucket_region_njit(delta_lake_path, parallel=False)
        if srsdn__eaw != '':
            os.environ['AWS_DEFAULT_REGION'] = srsdn__eaw
            dmg__vxba = True
    ixet__npv = DeltaTable(delta_lake_path)
    myvrv__nmt = ixet__npv.files()
    myvrv__nmt = [(fgrti__yxqvp + '/' + ghwpn__rvg) for ghwpn__rvg in
        sorted(myvrv__nmt)]
    if dmg__vxba:
        if aoxh__shq:
            os.environ['AWS_DEFAULT_REGION'] = bsk__rbt
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return myvrv__nmt


def _make_manifest(path_or_paths, fs, pathsep='/', metadata_nthreads=1,
    open_file_func=None):
    partitions = None
    fbkm__woy = None
    mgaf__jbk = None
    if isinstance(path_or_paths, list) and len(path_or_paths) == 1:
        path_or_paths = path_or_paths[0]
    if pq._is_path_like(path_or_paths) and fs.isdir(path_or_paths):
        manifest = ParquetManifest(path_or_paths, filesystem=fs,
            open_file_func=open_file_func, pathsep=getattr(fs, 'pathsep',
            '/'), metadata_nthreads=metadata_nthreads)
        fbkm__woy = manifest.common_metadata_path
        mgaf__jbk = manifest.metadata_path
        pieces = manifest.pieces
        partitions = manifest.partitions
    else:
        if not isinstance(path_or_paths, list):
            path_or_paths = [path_or_paths]
        if len(path_or_paths) == 0:
            raise ValueError('Must pass at least one file path')
        pieces = []
        kmdj__xqsj = urlparse(path_or_paths[0]).scheme
        for fgrti__yxqvp in path_or_paths:
            if not kmdj__xqsj and not fs.isfile(fgrti__yxqvp):
                raise OSError(
                    f'Passed non-file path: {fgrti__yxqvp}, but only files or glob strings (no directories) are supported when passing a list'
                    )
            piece = pq.ParquetDatasetPiece._create(fgrti__yxqvp,
                open_file_func=open_file_func)
            pieces.append(piece)
    return pieces, partitions, fbkm__woy, mgaf__jbk


pq._make_manifest = _make_manifest


def get_dataset_schema(dataset):
    if hasattr(dataset, '_bodo_arrow_schema'):
        return dataset._bodo_arrow_schema
    if dataset.metadata is None and dataset.schema is None:
        if dataset.common_metadata is not None:
            dataset.schema = dataset.common_metadata.schema
        else:
            dataset.schema = dataset.pieces[0].get_metadata().schema
    elif dataset.schema is None:
        dataset.schema = dataset.metadata.schema
    xlleh__xldr = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for uxt__lxsrk in dataset.partitions.partition_names:
            if xlleh__xldr.get_field_index(uxt__lxsrk) != -1:
                zonf__fewe = xlleh__xldr.get_field_index(uxt__lxsrk)
                xlleh__xldr = xlleh__xldr.remove(zonf__fewe)
    return xlleh__xldr


class VisitLevelThread(threading.Thread):

    def __init__(self, manifest):
        threading.Thread.__init__(self)
        self.manifest = manifest
        self.exc = None

    def run(self):
        try:
            manifest = self.manifest
            manifest.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(manifest.loop)
            manifest.loop.run_until_complete(manifest._visit_level(0,
                manifest.dirpath, []))
        except Exception as bzvqn__otg:
            self.exc = bzvqn__otg
        finally:
            if hasattr(manifest, 'loop') and not manifest.loop.is_closed():
                manifest.loop.close()

    def join(self):
        super(VisitLevelThread, self).join()
        if self.exc:
            raise self.exc


class ParquetManifest:

    def __init__(self, dirpath, open_file_func=None, filesystem=None,
        pathsep='/', partition_scheme='hive', metadata_nthreads=1):
        filesystem, dirpath = pq._get_filesystem_and_path(filesystem, dirpath)
        self.filesystem = filesystem
        self.open_file_func = open_file_func
        self.pathsep = pathsep
        self.dirpath = pq._stringify_path(dirpath)
        self.partition_scheme = partition_scheme
        self.partitions = pq.ParquetPartitions()
        self.pieces = []
        self._metadata_nthreads = metadata_nthreads
        self._thread_pool = futures.ThreadPoolExecutor(max_workers=
            metadata_nthreads)
        self.common_metadata_path = None
        self.metadata_path = None
        self.delta_lake_filter = set()
        self.partition_vals = defaultdict(set)
        vvsx__hbg = VisitLevelThread(self)
        vvsx__hbg.start()
        vvsx__hbg.join()
        for igp__pvt in self.partition_vals.keys():
            self.partition_vals[igp__pvt] = sorted(self.partition_vals[
                igp__pvt])
        for rfnq__edwj in self.partitions.levels:
            rfnq__edwj.keys = sorted(rfnq__edwj.keys)
        for mjl__mnyj in self.pieces:
            if mjl__mnyj.partition_keys is not None:
                mjl__mnyj.partition_keys = [(qkq__srtv, self.partition_vals
                    [qkq__srtv].index(kcz__znc)) for qkq__srtv, kcz__znc in
                    mjl__mnyj.partition_keys]
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, zyh__qbxn, base_path, gljc__nnli):
        fs = self.filesystem
        txi__pbzr, edd__mfha, qfs__bdhlt = await self.loop.run_in_executor(self
            ._thread_pool, lambda fs, base_bath: next(fs.walk(base_path)),
            fs, base_path)
        if zyh__qbxn == 0 and '_delta_log' in edd__mfha:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        qygg__zpuu = []
        for fgrti__yxqvp in qfs__bdhlt:
            if fgrti__yxqvp == '':
                continue
            pbl__qnsq = self.pathsep.join((base_path, fgrti__yxqvp))
            if fgrti__yxqvp.endswith('_common_metadata'):
                self.common_metadata_path = pbl__qnsq
            elif fgrti__yxqvp.endswith('_metadata'):
                self.metadata_path = pbl__qnsq
            elif self._should_silently_exclude(fgrti__yxqvp):
                continue
            elif self.delta_lake_filter and pbl__qnsq not in self.delta_lake_filter:
                continue
            else:
                qygg__zpuu.append(pbl__qnsq)
        zcnda__orix = [self.pathsep.join((base_path, dim__ktzt)) for
            dim__ktzt in edd__mfha if not pq._is_private_directory(dim__ktzt)]
        qygg__zpuu.sort()
        zcnda__orix.sort()
        if len(qygg__zpuu) > 0 and len(zcnda__orix) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(zcnda__orix) > 0:
            await self._visit_directories(zyh__qbxn, zcnda__orix, gljc__nnli)
        else:
            self._push_pieces(qygg__zpuu, gljc__nnli)

    async def _visit_directories(self, zyh__qbxn, edd__mfha, gljc__nnli):
        gzs__jmq = []
        for fgrti__yxqvp in edd__mfha:
            mewg__uiwt, mbmo__vezwt = pq._path_split(fgrti__yxqvp, self.pathsep
                )
            qkq__srtv, qvust__vxb = pq._parse_hive_partition(mbmo__vezwt)
            fvrxi__xxta = self.partitions.get_index(zyh__qbxn, qkq__srtv,
                qvust__vxb)
            self.partition_vals[qkq__srtv].add(qvust__vxb)
            bpvpb__ywiz = gljc__nnli + [(qkq__srtv, qvust__vxb)]
            gzs__jmq.append(self._visit_level(zyh__qbxn + 1, fgrti__yxqvp,
                bpvpb__ywiz))
        await asyncio.wait(gzs__jmq)


ParquetManifest._should_silently_exclude = (pq.ParquetManifest.
    _should_silently_exclude)
ParquetManifest._parse_partition = pq.ParquetManifest._parse_partition
ParquetManifest._push_pieces = pq.ParquetManifest._push_pieces
pq.ParquetManifest = ParquetManifest


def pieces(self):
    return self._pieces


pq.ParquetDataset.pieces = property(pieces)


def partitions(self):
    return self._partitions


pq.ParquetDataset.partitions = property(partitions)
