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
    except Exception as ahcba__akp:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    kdnlc__txk = None
    psalp__hemk = delta_lake_path.rstrip('/')
    vzowq__khglb = 'AWS_DEFAULT_REGION' in os.environ
    obec__icbk = os.environ.get('AWS_DEFAULT_REGION', '')
    lddt__cegk = False
    if delta_lake_path.startswith('s3://'):
        ppw__zpdsx = get_s3_bucket_region_njit(delta_lake_path, parallel=False)
        if ppw__zpdsx != '':
            os.environ['AWS_DEFAULT_REGION'] = ppw__zpdsx
            lddt__cegk = True
    vuu__epa = DeltaTable(delta_lake_path)
    kdnlc__txk = vuu__epa.files()
    kdnlc__txk = [(psalp__hemk + '/' + oyh__qswu) for oyh__qswu in sorted(
        kdnlc__txk)]
    if lddt__cegk:
        if vzowq__khglb:
            os.environ['AWS_DEFAULT_REGION'] = obec__icbk
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return kdnlc__txk


def _make_manifest(path_or_paths, fs, pathsep='/', metadata_nthreads=1,
    open_file_func=None):
    partitions = None
    yuseu__ubwi = None
    qpkud__ibj = None
    if isinstance(path_or_paths, list) and len(path_or_paths) == 1:
        path_or_paths = path_or_paths[0]
    if pq._is_path_like(path_or_paths) and fs.isdir(path_or_paths):
        manifest = ParquetManifest(path_or_paths, filesystem=fs,
            open_file_func=open_file_func, pathsep=getattr(fs, 'pathsep',
            '/'), metadata_nthreads=metadata_nthreads)
        yuseu__ubwi = manifest.common_metadata_path
        qpkud__ibj = manifest.metadata_path
        pieces = manifest.pieces
        partitions = manifest.partitions
    else:
        if not isinstance(path_or_paths, list):
            path_or_paths = [path_or_paths]
        if len(path_or_paths) == 0:
            raise ValueError('Must pass at least one file path')
        pieces = []
        idh__ehb = urlparse(path_or_paths[0]).scheme
        for psalp__hemk in path_or_paths:
            if not idh__ehb and not fs.isfile(psalp__hemk):
                raise OSError(
                    f'Passed non-file path: {psalp__hemk}, but only files or glob strings (no directories) are supported when passing a list'
                    )
            piece = pq.ParquetDatasetPiece._create(psalp__hemk,
                open_file_func=open_file_func)
            pieces.append(piece)
    return pieces, partitions, yuseu__ubwi, qpkud__ibj


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
    jfnkr__eivyk = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for ttedw__ptzk in dataset.partitions.partition_names:
            if jfnkr__eivyk.get_field_index(ttedw__ptzk) != -1:
                kwtas__lxavd = jfnkr__eivyk.get_field_index(ttedw__ptzk)
                jfnkr__eivyk = jfnkr__eivyk.remove(kwtas__lxavd)
    return jfnkr__eivyk


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
        except Exception as ahcba__akp:
            self.exc = ahcba__akp
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
        vxuik__tudj = VisitLevelThread(self)
        vxuik__tudj.start()
        vxuik__tudj.join()
        for pht__alno in self.partition_vals.keys():
            self.partition_vals[pht__alno] = sorted(self.partition_vals[
                pht__alno])
        for hrs__nfp in self.partitions.levels:
            hrs__nfp.keys = sorted(hrs__nfp.keys)
        for rov__eyc in self.pieces:
            if rov__eyc.partition_keys is not None:
                rov__eyc.partition_keys = [(qov__eseam, self.partition_vals
                    [qov__eseam].index(bzzaf__kmdgz)) for qov__eseam,
                    bzzaf__kmdgz in rov__eyc.partition_keys]
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, ntxt__ugusw, base_path, dzsxf__uneoc):
        fs = self.filesystem
        xhowz__mbo, swzn__huzn, kour__vpsn = await self.loop.run_in_executor(
            self._thread_pool, lambda fs, base_bath: next(fs.walk(base_path
            )), fs, base_path)
        if ntxt__ugusw == 0 and '_delta_log' in swzn__huzn:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        xlf__gfhs = []
        for psalp__hemk in kour__vpsn:
            if psalp__hemk == '':
                continue
            phaq__pogy = self.pathsep.join((base_path, psalp__hemk))
            if psalp__hemk.endswith('_common_metadata'):
                self.common_metadata_path = phaq__pogy
            elif psalp__hemk.endswith('_metadata'):
                self.metadata_path = phaq__pogy
            elif self._should_silently_exclude(psalp__hemk):
                continue
            elif self.delta_lake_filter and phaq__pogy not in self.delta_lake_filter:
                continue
            else:
                xlf__gfhs.append(phaq__pogy)
        gipi__rxc = [self.pathsep.join((base_path, rkd__fust)) for
            rkd__fust in swzn__huzn if not pq._is_private_directory(rkd__fust)]
        xlf__gfhs.sort()
        gipi__rxc.sort()
        if len(xlf__gfhs) > 0 and len(gipi__rxc) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(gipi__rxc) > 0:
            await self._visit_directories(ntxt__ugusw, gipi__rxc, dzsxf__uneoc)
        else:
            self._push_pieces(xlf__gfhs, dzsxf__uneoc)

    async def _visit_directories(self, ntxt__ugusw, swzn__huzn, dzsxf__uneoc):
        fjv__nes = []
        for psalp__hemk in swzn__huzn:
            syo__mwxf, bhm__qmiuq = pq._path_split(psalp__hemk, self.pathsep)
            qov__eseam, tgy__cyzc = pq._parse_hive_partition(bhm__qmiuq)
            epmri__leza = self.partitions.get_index(ntxt__ugusw, qov__eseam,
                tgy__cyzc)
            self.partition_vals[qov__eseam].add(tgy__cyzc)
            vckcv__bkdqe = dzsxf__uneoc + [(qov__eseam, tgy__cyzc)]
            fjv__nes.append(self._visit_level(ntxt__ugusw + 1, psalp__hemk,
                vckcv__bkdqe))
        await asyncio.wait(fjv__nes)


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
