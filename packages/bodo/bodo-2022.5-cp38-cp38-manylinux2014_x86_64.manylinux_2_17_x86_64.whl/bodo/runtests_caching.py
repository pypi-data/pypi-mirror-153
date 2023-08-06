"""
File used to run caching tests on CI.
"""
import os
import shutil
import subprocess
import sys
num_processes = int(sys.argv[1])
cache_test_dir = sys.argv[2]
pytest_working_dir = os.getcwd()
try:
    os.chdir(cache_test_dir)
    shutil.rmtree('__pycache__', ignore_errors=True)
finally:
    os.chdir(pytest_working_dir)
if 'NUMBA_CACHE_DIR' in os.environ:
    del os.environ['NUMBA_CACHE_DIR']
pytest_cmd_not_cached_flag = ['pytest', '-s', '-v', cache_test_dir]
cmd = ['mpiexec', '-n', str(num_processes)] + pytest_cmd_not_cached_flag
print('Running', ' '.join(cmd))
p = subprocess.Popen(cmd, shell=False)
rc = p.wait()
failed_tests = False
if rc not in (0, 5):
    failed_tests = True
pytest_cmd_yes_cached_flag = ['pytest', '-s', '-v', cache_test_dir,
    '--is_cached']
cmd = ['mpiexec', '-n', str(num_processes)] + pytest_cmd_yes_cached_flag
print('Running', ' '.join(cmd))
p = subprocess.Popen(cmd, shell=False)
rc = p.wait()
if rc not in (0, 5):
    failed_tests = True
if failed_tests:
    exit(1)
