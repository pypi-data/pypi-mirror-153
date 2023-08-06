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
    except Exception as hlu__sxex:
        raise ImportError(
            "Bodo Error: please pip install the 'deltalake' package to read parquet from delta lake"
            )
    ebu__hcxh = None
    ecxp__jukm = delta_lake_path.rstrip('/')
    pqgx__ovo = 'AWS_DEFAULT_REGION' in os.environ
    ttvu__zkaq = os.environ.get('AWS_DEFAULT_REGION', '')
    vmf__pygt = False
    if delta_lake_path.startswith('s3://'):
        tkz__llr = get_s3_bucket_region_njit(delta_lake_path, parallel=False)
        if tkz__llr != '':
            os.environ['AWS_DEFAULT_REGION'] = tkz__llr
            vmf__pygt = True
    tujaz__qwf = DeltaTable(delta_lake_path)
    ebu__hcxh = tujaz__qwf.files()
    ebu__hcxh = [(ecxp__jukm + '/' + afww__twmpx) for afww__twmpx in sorted
        (ebu__hcxh)]
    if vmf__pygt:
        if pqgx__ovo:
            os.environ['AWS_DEFAULT_REGION'] = ttvu__zkaq
        else:
            del os.environ['AWS_DEFAULT_REGION']
    return ebu__hcxh


def _make_manifest(path_or_paths, fs, pathsep='/', metadata_nthreads=1,
    open_file_func=None):
    partitions = None
    ykuen__zlpm = None
    mggzz__cirm = None
    if isinstance(path_or_paths, list) and len(path_or_paths) == 1:
        path_or_paths = path_or_paths[0]
    if pq._is_path_like(path_or_paths) and fs.isdir(path_or_paths):
        manifest = ParquetManifest(path_or_paths, filesystem=fs,
            open_file_func=open_file_func, pathsep=getattr(fs, 'pathsep',
            '/'), metadata_nthreads=metadata_nthreads)
        ykuen__zlpm = manifest.common_metadata_path
        mggzz__cirm = manifest.metadata_path
        pieces = manifest.pieces
        partitions = manifest.partitions
    else:
        if not isinstance(path_or_paths, list):
            path_or_paths = [path_or_paths]
        if len(path_or_paths) == 0:
            raise ValueError('Must pass at least one file path')
        pieces = []
        hnywp__rnle = urlparse(path_or_paths[0]).scheme
        for ecxp__jukm in path_or_paths:
            if not hnywp__rnle and not fs.isfile(ecxp__jukm):
                raise OSError(
                    f'Passed non-file path: {ecxp__jukm}, but only files or glob strings (no directories) are supported when passing a list'
                    )
            piece = pq.ParquetDatasetPiece._create(ecxp__jukm,
                open_file_func=open_file_func)
            pieces.append(piece)
    return pieces, partitions, ykuen__zlpm, mggzz__cirm


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
    yknk__axw = dataset.schema.to_arrow_schema()
    if dataset.partitions is not None:
        for vyt__mjr in dataset.partitions.partition_names:
            if yknk__axw.get_field_index(vyt__mjr) != -1:
                vktch__lpkl = yknk__axw.get_field_index(vyt__mjr)
                yknk__axw = yknk__axw.remove(vktch__lpkl)
    return yknk__axw


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
        except Exception as hlu__sxex:
            self.exc = hlu__sxex
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
        hyv__kygup = VisitLevelThread(self)
        hyv__kygup.start()
        hyv__kygup.join()
        for hac__hqk in self.partition_vals.keys():
            self.partition_vals[hac__hqk] = sorted(self.partition_vals[
                hac__hqk])
        for aglmk__fbco in self.partitions.levels:
            aglmk__fbco.keys = sorted(aglmk__fbco.keys)
        for wsk__bjxq in self.pieces:
            if wsk__bjxq.partition_keys is not None:
                wsk__bjxq.partition_keys = [(ona__juyz, self.partition_vals
                    [ona__juyz].index(mugfc__kfvl)) for ona__juyz,
                    mugfc__kfvl in wsk__bjxq.partition_keys]
        self.pieces.sort(key=lambda piece: piece.path)
        if self.common_metadata_path is None:
            self.common_metadata_path = self.metadata_path
        self._thread_pool.shutdown()

    async def _visit_level(self, nxeo__dywtb, base_path, smboo__aovn):
        fs = self.filesystem
        flaur__cpau, acdf__hvz, ktedi__tymb = await self.loop.run_in_executor(
            self._thread_pool, lambda fs, base_bath: next(fs.walk(base_path
            )), fs, base_path)
        if nxeo__dywtb == 0 and '_delta_log' in acdf__hvz:
            self.delta_lake_filter = set(get_parquet_filesnames_from_deltalake
                (base_path))
        ecsr__jbr = []
        for ecxp__jukm in ktedi__tymb:
            if ecxp__jukm == '':
                continue
            zmm__kdjcz = self.pathsep.join((base_path, ecxp__jukm))
            if ecxp__jukm.endswith('_common_metadata'):
                self.common_metadata_path = zmm__kdjcz
            elif ecxp__jukm.endswith('_metadata'):
                self.metadata_path = zmm__kdjcz
            elif self._should_silently_exclude(ecxp__jukm):
                continue
            elif self.delta_lake_filter and zmm__kdjcz not in self.delta_lake_filter:
                continue
            else:
                ecsr__jbr.append(zmm__kdjcz)
        rluim__wex = [self.pathsep.join((base_path, gqisc__weec)) for
            gqisc__weec in acdf__hvz if not pq._is_private_directory(
            gqisc__weec)]
        ecsr__jbr.sort()
        rluim__wex.sort()
        if len(ecsr__jbr) > 0 and len(rluim__wex) > 0:
            raise ValueError('Found files in an intermediate directory: {}'
                .format(base_path))
        elif len(rluim__wex) > 0:
            await self._visit_directories(nxeo__dywtb, rluim__wex, smboo__aovn)
        else:
            self._push_pieces(ecsr__jbr, smboo__aovn)

    async def _visit_directories(self, nxeo__dywtb, acdf__hvz, smboo__aovn):
        eddu__gvn = []
        for ecxp__jukm in acdf__hvz:
            acxh__rhz, fyvd__ytzwd = pq._path_split(ecxp__jukm, self.pathsep)
            ona__juyz, gaspk__fwcsx = pq._parse_hive_partition(fyvd__ytzwd)
            eofmt__wxtj = self.partitions.get_index(nxeo__dywtb, ona__juyz,
                gaspk__fwcsx)
            self.partition_vals[ona__juyz].add(gaspk__fwcsx)
            jaldx__idcxk = smboo__aovn + [(ona__juyz, gaspk__fwcsx)]
            eddu__gvn.append(self._visit_level(nxeo__dywtb + 1, ecxp__jukm,
                jaldx__idcxk))
        await asyncio.wait(eddu__gvn)


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
