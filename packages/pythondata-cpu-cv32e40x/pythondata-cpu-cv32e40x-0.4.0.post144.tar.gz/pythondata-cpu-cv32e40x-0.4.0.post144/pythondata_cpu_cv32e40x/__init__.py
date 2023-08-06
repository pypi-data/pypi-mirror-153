import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.4.0.post144"
version_tuple = (0, 4, 0, 144)
try:
    from packaging.version import Version as V
    pversion = V("0.4.0.post144")
except ImportError:
    pass

# Data version info
data_version_str = "0.4.0.post2"
data_version_tuple = (0, 4, 0, 2)
try:
    from packaging.version import Version as V
    pdata_version = V("0.4.0.post2")
except ImportError:
    pass
data_git_hash = "cbb63d0c475bc93ce545e0fc9e74715d80fefaa4"
data_git_describe = "0.4.0-2-gcbb63d0c"
data_git_msg = """\
commit cbb63d0c475bc93ce545e0fc9e74715d80fefaa4
Merge: df030b15 bfa9300b
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Fri Jun 3 10:46:07 2022 +0200

    Merge pull request #565 from silabs-oysteink/silabs-oysteink_rvfi-csr-stateen
    
    Added Smstateen CSRs to RVFI (only supported in cv32e40s)

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
