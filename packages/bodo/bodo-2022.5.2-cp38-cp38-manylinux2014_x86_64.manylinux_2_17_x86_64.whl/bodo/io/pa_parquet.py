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
    except Exception as xtd__lnarf:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    jbslv__abz = None
    bscu__jcne = delta_lake_path.rstrip('/')
    gqdk__cpw = 'AWS_DEFAULT_REGION' in os.environ
    vdw__oynbt = os.environ.get('AWS_DEFAULT_REGION', '')
    ccjd__soj = False
    if delta_lake_path.startswith('s3://'):
        yqmjb__bejzj = get_s3_bucket_region_njit(delta_lake_path, parallel=
            False)
        if yqmjb__bejzj != '':
            os.environ['AWS_DEFAULT_REGION'] = yqmjb__bejzj
            ccjd__soj = True
    wrwq__pqhm = DeltaTable(delta_lake_path)
    jbslv__abz = wrwq__pqhm.files()
    jbslv__abz = [(bscu__jcne + '/' + box__jjghb) for box__jjghb in sorted(
        jbslv__abz)]
    if ccjd__soj:
        if gqdk__cpw:
            os.environ['AWS_DEFAULT_REGION'] = vdw__oynbt
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return jbslv__abz


def _make_manifest(path_or_paths, fs, pathsep='/', metadata_nthreads=1,
    open_file_func=None):
    partitions = None
    gusqd__zzrdn = None
    seiqi__laij = None
    if isinstance(path_or_paths, list) and len(path_or_paths) == 1:
        path_or_paths = path_or_paths[0]
    if pq._is_path_like(path_or_paths) and fs.isdir(path_or_paths):
        manifest = ParquetManifest(path_or_paths, filesystem=fs,
            open_file_func=open_file_func, pathsep=getattr(fs, 'pathsep',
            '/'), metadata_nthreads=metadata_nthreads)
        gusqd__zzrdn = manifest.common_metadata_path
        seiqi__laij = manifest.metadata_path
        pieces = manifest.pieces
        partitions = manifest.partitions
    else:
        if not isinstance(path_or_paths, list):
            path_or_paths = [path_or_paths]
        if len(path_or_paths) == 0:
            raise ValueError('Must pass at least one file path')
        pieces = []
        irpe__echt = urlparse(path_or_paths[0]).scheme
        for bscu__jcne in path_or_paths:
            if not irpe__echt and not fs.isfile(bscu__jcne):
                raise OSError(
                    f'Passed non-file path: {bscu__jcne}, but only files or glob strings (no directories) are supported when passing a list'
                    )
            piece = pq.ParquetDatasetPiece._create(bscu__jcne,
                open_file_func=open_file_func)
            pieces.append(piece)
    return pieces, partitions, gusqd__zzrdn, seiqi__laij


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
    ida__gqao = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for qlj__tfypw in dataset.partitions.partition_names:
            if ida__gqao.get_field_index(qlj__tfypw) != -1:
                pum__bxdg = ida__gqao.get_field_index(qlj__tfypw)
                ida__gqao = ida__gqao.remove(pum__bxdg)
    return ida__gqao


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
        except Exception as xtd__lnarf:
            self.exc = xtd__lnarf
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
        vrsg__vwzfp = VisitLevelThread(self)
        vrsg__vwzfp.start()
        vrsg__vwzfp.join()
        for umo__vkc in self.partition_vals.keys():
            self.partition_vals[umo__vkc] = sorted(self.partition_vals[
                umo__vkc])
        for fnidf__yamcb in self.partitions.levels:
            fnidf__yamcb.keys = sorted(fnidf__yamcb.keys)
        for oez__zsd in self.pieces:
            if oez__zsd.partition_keys is not None:
                oez__zsd.partition_keys = [(cmjh__mecjy, self.
                    partition_vals[cmjh__mecjy].index(mobg__sip)) for 
                    cmjh__mecjy, mobg__sip in oez__zsd.partition_keys]
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, ppygw__uemsk, base_path, rjggp__iwxm):
        fs = self.filesystem
        odgg__snjn, ljbd__zefk, kay__zbzi = await self.loop.run_in_executor(
            self._thread_pool, lambda fs, base_bath: next(fs.walk(base_path
            )), fs, base_path)
        if ppygw__uemsk == 0 and '_delta_log' in ljbd__zefk:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        nqy__ujd = []
        for bscu__jcne in kay__zbzi:
            if bscu__jcne == '':
                continue
            ntkm__kfj = self.pathsep.join((base_path, bscu__jcne))
            if bscu__jcne.endswith('_common_metadata'):
                self.common_metadata_path = ntkm__kfj
            elif bscu__jcne.endswith('_metadata'):
                self.metadata_path = ntkm__kfj
            elif self._should_silently_exclude(bscu__jcne):
                continue
            elif self.delta_lake_filter and ntkm__kfj not in self.delta_lake_filter:
                continue
            else:
                nqy__ujd.append(ntkm__kfj)
        fyap__wnxy = [self.pathsep.join((base_path, kzp__nram)) for
            kzp__nram in ljbd__zefk if not pq._is_private_directory(kzp__nram)]
        nqy__ujd.sort()
        fyap__wnxy.sort()
        if len(nqy__ujd) > 0 and len(fyap__wnxy) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(fyap__wnxy) > 0:
            await self._visit_directories(ppygw__uemsk, fyap__wnxy, rjggp__iwxm
                )
        else:
            self._push_pieces(nqy__ujd, rjggp__iwxm)

    async def _visit_directories(self, ppygw__uemsk, ljbd__zefk, rjggp__iwxm):
        nauxz__jrdhe = []
        for bscu__jcne in ljbd__zefk:
            plt__ogiv, effb__axn = pq._path_split(bscu__jcne, self.pathsep)
            cmjh__mecjy, qtks__cwwp = pq._parse_hive_partition(effb__axn)
            wob__pbudj = self.partitions.get_index(ppygw__uemsk,
                cmjh__mecjy, qtks__cwwp)
            self.partition_vals[cmjh__mecjy].add(qtks__cwwp)
            rbjqx__cjl = rjggp__iwxm + [(cmjh__mecjy, qtks__cwwp)]
            nauxz__jrdhe.append(self._visit_level(ppygw__uemsk + 1,
                bscu__jcne, rbjqx__cjl))
        await asyncio.wait(nauxz__jrdhe)


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
