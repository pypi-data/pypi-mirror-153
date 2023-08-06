import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.3.0.post297"
version_tuple = (0, 3, 0, 297)
try:
    from packaging.version import Version as V
    pversion = V("0.3.0.post297")
except ImportError:
    pass

# Data version info
data_version_str = "0.3.0.post155"
data_version_tuple = (0, 3, 0, 155)
try:
    from packaging.version import Version as V
    pdata_version = V("0.3.0.post155")
except ImportError:
    pass
data_git_hash = "4beb70ada629eddb2ad5f0f959765f847bbbd4a6"
data_git_describe = "0.3.0-155-g4beb70ad"
data_git_msg = """\
commit 4beb70ada629eddb2ad5f0f959765f847bbbd4a6
Merge: dc582f90 be14aef7
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Thu Jun 2 08:07:18 2022 +0200

    Merge pull request #562 from Silabs-ArjanB/ArjanB_instralign
    
    Moved instruction address word alignment to core boundary

"""

# Tool version info
tool_version_str = "0.0.post142"
tool_version_tuple = (0, 0, 142)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post142")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
