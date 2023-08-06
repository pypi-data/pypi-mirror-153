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
    except Exception as wrbq__xfypc:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    ciu__kkh = None
    ozq__vljla = delta_lake_path.rstrip('/')
    nmeb__tbzta = 'AWS_DEFAULT_REGION' in os.environ
    pxd__eqhxj = os.environ.get('AWS_DEFAULT_REGION', '')
    wumnt__tdaxv = False
    if delta_lake_path.startswith('s3://'):
        ctd__zhx = get_s3_bucket_region_njit(delta_lake_path, parallel=False)
        if ctd__zhx != '':
            os.environ['AWS_DEFAULT_REGION'] = ctd__zhx
            wumnt__tdaxv = True
    zgh__poaq = DeltaTable(delta_lake_path)
    ciu__kkh = zgh__poaq.files()
    ciu__kkh = [(ozq__vljla + '/' + dclvk__jqnds) for dclvk__jqnds in
        sorted(ciu__kkh)]
    if wumnt__tdaxv:
        if nmeb__tbzta:
            os.environ['AWS_DEFAULT_REGION'] = pxd__eqhxj
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return ciu__kkh


def _make_manifest(path_or_paths, fs, pathsep='/', metadata_nthreads=1,
    open_file_func=None):
    partitions = None
    fkp__pxc = None
    qkja__qrop = None
    if isinstance(path_or_paths, list) and len(path_or_paths) == 1:
        path_or_paths = path_or_paths[0]
    if pq._is_path_like(path_or_paths) and fs.isdir(path_or_paths):
        manifest = ParquetManifest(path_or_paths, filesystem=fs,
            open_file_func=open_file_func, pathsep=getattr(fs, 'pathsep',
            '/'), metadata_nthreads=metadata_nthreads)
        fkp__pxc = manifest.common_metadata_path
        qkja__qrop = manifest.metadata_path
        pieces = manifest.pieces
        partitions = manifest.partitions
    else:
        if not isinstance(path_or_paths, list):
            path_or_paths = [path_or_paths]
        if len(path_or_paths) == 0:
            raise ValueError('Must pass at least one file path')
        pieces = []
        ffnel__gdc = urlparse(path_or_paths[0]).scheme
        for ozq__vljla in path_or_paths:
            if not ffnel__gdc and not fs.isfile(ozq__vljla):
                raise OSError(
                    f'Passed non-file path: {ozq__vljla}, but only files or glob strings (no directories) are supported when passing a list'
                    )
            piece = pq.ParquetDatasetPiece._create(ozq__vljla,
                open_file_func=open_file_func)
            pieces.append(piece)
    return pieces, partitions, fkp__pxc, qkja__qrop


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
    rbsps__uvg = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for yex__sezq in dataset.partitions.partition_names:
            if rbsps__uvg.get_field_index(yex__sezq) != -1:
                pcca__zkuv = rbsps__uvg.get_field_index(yex__sezq)
                rbsps__uvg = rbsps__uvg.remove(pcca__zkuv)
    return rbsps__uvg


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
        except Exception as wrbq__xfypc:
            self.exc = wrbq__xfypc
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
        mtqor__tbnr = VisitLevelThread(self)
        mtqor__tbnr.start()
        mtqor__tbnr.join()
        for uow__hyx in self.partition_vals.keys():
            self.partition_vals[uow__hyx] = sorted(self.partition_vals[
                uow__hyx])
        for xlqsy__pdy in self.partitions.levels:
            xlqsy__pdy.keys = sorted(xlqsy__pdy.keys)
        for jcxi__sfkdh in self.pieces:
            if jcxi__sfkdh.partition_keys is not None:
                jcxi__sfkdh.partition_keys = [(xicz__vtrom, self.
                    partition_vals[xicz__vtrom].index(dyh__mtotp)) for 
                    xicz__vtrom, dyh__mtotp in jcxi__sfkdh.partition_keys]
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, xjn__ztp, base_path, vab__aeuiq):
        fs = self.filesystem
        bbugn__syrh, gweqd__hptg, mcwe__tzz = await self.loop.run_in_executor(
            self._thread_pool, lambda fs, base_bath: next(fs.walk(base_path
            )), fs, base_path)
        if xjn__ztp == 0 and '_delta_log' in gweqd__hptg:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        enumw__iqhq = []
        for ozq__vljla in mcwe__tzz:
            if ozq__vljla == '':
                continue
            dtu__orcss = self.pathsep.join((base_path, ozq__vljla))
            if ozq__vljla.endswith('_common_metadata'):
                self.common_metadata_path = dtu__orcss
            elif ozq__vljla.endswith('_metadata'):
                self.metadata_path = dtu__orcss
            elif self._should_silently_exclude(ozq__vljla):
                continue
            elif self.delta_lake_filter and dtu__orcss not in self.delta_lake_filter:
                continue
            else:
                enumw__iqhq.append(dtu__orcss)
        dzmno__owl = [self.pathsep.join((base_path, teqwl__rgeh)) for
            teqwl__rgeh in gweqd__hptg if not pq._is_private_directory(
            teqwl__rgeh)]
        enumw__iqhq.sort()
        dzmno__owl.sort()
        if len(enumw__iqhq) > 0 and len(dzmno__owl) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(dzmno__owl) > 0:
            await self._visit_directories(xjn__ztp, dzmno__owl, vab__aeuiq)
        else:
            self._push_pieces(enumw__iqhq, vab__aeuiq)

    async def _visit_directories(self, xjn__ztp, gweqd__hptg, vab__aeuiq):
        kjoyz__obwyk = []
        for ozq__vljla in gweqd__hptg:
            pcpco__qmhg, buc__oiww = pq._path_split(ozq__vljla, self.pathsep)
            xicz__vtrom, yvhsq__wbwci = pq._parse_hive_partition(buc__oiww)
            jpsf__jdu = self.partitions.get_index(xjn__ztp, xicz__vtrom,
                yvhsq__wbwci)
            self.partition_vals[xicz__vtrom].add(yvhsq__wbwci)
            cpi__rozm = vab__aeuiq + [(xicz__vtrom, yvhsq__wbwci)]
            kjoyz__obwyk.append(self._visit_level(xjn__ztp + 1, ozq__vljla,
                cpi__rozm))
        await asyncio.wait(kjoyz__obwyk)


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
