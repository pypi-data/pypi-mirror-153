import pyarrow.fs
import pyarrow._hdfs
from ._hdfs import HadoopFileSystem
pyarrow._hdfs.HadoopFileSystem = HadoopFileSystem
pyarrow.fs.HadoopFileSystem = HadoopFileSystem
