import os, os, platform, sys
from ctypes.util import find_library
from ._ffi import ffi

class ANNISException(Exception):
    def __init__(self, m : str):
        self.message = m

    def __str__(self):
        return self.message

package_dir = os.path.normpath(os.path.realpath(__file__) + '/..')

lib_file_name = None
system_id = None
# check system is 64 bit
if sys.maxsize > 2**32:
    if platform.system() == "Linux":
        lib_file_name = "libgraphannis.so"
        system_id = "linux-x86-64"

    elif platform.system() == "Darwin":
        lib_file_name = "libgraphannis.dylib"
        system_id = "darwin-x86-64"

    elif platform.system() == "Windows":
        lib_file_name = "graphannis.dll"
        system_id = "win32-x86-64"

else:
    raise ANNISException("graphANNIS only works on 64 bit systems")

search_dirs = [
    package_dir + '/' + system_id + '/' + lib_file_name,
]

shared_obj_file = None
for d in search_dirs:
    d = os.path.normpath(d)
    if os.path.exists(d):
        shared_obj_file = d
        break

if shared_obj_file == None:
    # let the system search for the shared library
    shared_obj_file = find_library('graphannis')

if shared_obj_file == None:
    on_rtd = os.environ.get('READTHEDOCS') == 'True'
    
    # ignore missing shared library when called to create the API documentation
    if on_rtd:
        CAPI = None
    else:
        raise ANNISException("Could not find graphannis library in path (e.g. LD_LIBRARY_PATH)")
else:
    CAPI = ffi.dlopen(shared_obj_file)
